import importlib
import os.path
import shutil
import tempfile
from os import makedirs, path
from pathlib import Path

from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin, Config
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from yaml import safe_load

from constants import JS_SCROLL_STR, OS_PICK_BTN, OS_PICK_STR, JS_OS_NEUTRAL

tmp_dir = tempfile.TemporaryDirectory().name


def gen_content_from_macros():
    """
    For each file/script provided in specific directory, this method runs
    the function named the same name as the script and store its returned value
    to dictionary. These values are injected under the same name as variables
    in the final built documentation.
    :return: Dictionary of returned values from provided scripts.
    """
    scripts = "scripts"
    scripts_dir = os.path.join("computational_macros", scripts)

    outputs = {}
    for r, d, f in os.walk(scripts_dir):
        if r != scripts_dir:
            continue
        f = filter(lambda x: not x.__contains__("__init__.py"), f)
        for file in f:
            file = Path(file).stem
            mod_name = f"{scripts}.{file}"
            mod = importlib.import_module(mod_name)
            fun = getattr(mod, file)
            outputs[file] = fun()
    return outputs


class UgentPlugin(BasePlugin):
    config_scheme = (
        ("os_pick", Type(bool, default=False)),
        ("yamls", Type(list, default=[])),
    )

    def __init__(self, *args, **kwargs):
        super(UgentPlugin, self).__init__(*args, **kwargs)
        self.os_pick = None
        self.yamls = None
        self.macro_extras = gen_content_from_macros()

    def generate_os_pick_files(self, extras, files):
        docs_with_os = self.get_docs()
        flatten_docs = dict()
        # The final documentation files structure processing.
        for el in docs_with_os:
            os_name, docs = el  # os_name, docs = (OS, <nav structure of documents>)
            for doc in docs:
                key, value = list(doc.items())[0]
                if type(value) is list:
                    for val in value:
                        flatten_docs = self.to_flat(flatten_docs, os_name, (key,), val)
                else:
                    flatten_docs[(key,)] = {
                        **flatten_docs.get((key,), dict({})),
                        **{os_name: value},
                    }
        # For each documentation file, generate OS picking files.
        for name_chain, links_with_os in list(flatten_docs.items()):
            # It maybe seems weird, that it iterates twice over the same list,
            # but it is necessary to generate correct OS picking files. In case
            # there is no custom documentation .md file, then the inner cycle
            # generates "n" times the same file (although actually written just
            # once), but when some custom documentation .md file exists, then
            # we need generate also "custom" OS picking file.
            for _, link in list(links_with_os.items()):
                os_pick_with_urls_general = OS_PICK_STR
                file_src_dir, file_name = path.split(link)

                for os_name, _ in list(links_with_os.items()):
                    if "index.md" in file_name:
                        base = (len(path.splitext(link)[0].split("/")) - 1) * "../"
                        link_str = (
                            base
                            + f"{os_name}/"
                            + path.dirname(links_with_os[f"{os_name}"])
                        )
                    else:
                        base = len(path.splitext(link)[0].split("/")) * "../"
                        link_str = (
                            base
                            + f"{os_name}/"
                            + path.splitext(links_with_os[f"{os_name}"])[0]
                        )
                    general_link = link_str if links_with_os.get(f"{os_name}") else None
                    os_pick_with_urls_general += OS_PICK_BTN.format(
                        general_link is not None, os_name, general_link
                    )

                # Write the content into file, when such file not already exists.
                os_pick_dir_path = path.normpath(path.join(tmp_dir, file_src_dir))
                os_pick_file_path = path.join(os_pick_dir_path, file_name)
                if not path.exists(os_pick_dir_path):
                    makedirs(os_pick_dir_path)
                with open(os_pick_file_path, "w") as file:
                    file.write(os_pick_with_urls_general)
                dest_dir = path.join(
                    path.abspath(extras.get("build_dir")), file_src_dir
                )
                new_file = File(
                    file_name,
                    path.abspath(os_pick_dir_path),
                    dest_dir,
                    use_directory_urls=True,
                )
                files.append(new_file)

    def get_docs(self):
        """
        Internal method. Parse 'nav' data from defined yamls into temporary
        internal format.
        :return: structure like this:
        [(OS name, [{ page name: document files}, {...}, ...]), ...]
        """
        uris = []
        for yml in self.yamls:
            with open(yml, "r") as file:
                config = safe_load(file)
            opsys = config.get("extra").get("OS")
            uris.append((opsys, config.get("nav")))
        return uris

    def to_flat(self, docs, os_name, par_key, par_values):
        """
        Recursive internal method. Flat a nested structure of nav documents.
        Tuple of the document titles is used as key for target documentation
        file (value).
        :param docs: Nested structure of documents and their titles.
        :param os_name: OS name
        :param par_key: Parent key, used for concatenation with other nested
        keys.
        :param par_values: Parent values can be string (final document) or
        another nested structure.
        :return: Dict of flatten structure.
        """
        if type(par_values) is dict:
            key, value = list(par_values.items())[0]
            if type(value) is list:
                docs = self.to_flat(docs, os_name, (par_key + (key,)), value)
            else:
                docs[par_key + (key,)] = {
                    **docs.get((par_key + (key,)), dict({})),
                    **{os_name: value},
                }
        elif type(par_values) is list:
            for parvalue in par_values:
                docs = self.to_flat(docs, os_name, par_key, parvalue)
        return docs

    def on_config(self, config: Config):
        """
        Called when loading config. Extracting some variables as object
        properties and injecting Python macro outputs as variables.
        :param config: Original config object.
        :return: Edited Config object.
        """
        self.os_pick = self.config["os_pick"]
        self.yamls = self.config["yamls"]
        extras = config.get("extra")
        extras = {**extras, **self.macro_extras}
        config["extra"] = extras
        return config

    def on_files(self, files: Files, config: Config):
        """
        If the OS picking feature is set to True in the yaml config, then
        appropriate files are dynamically generated and added to other
        documentation files.
        :param files: Original Files object.
        :param config: Original Config object.
        :return: Edited Files object.
        """
        extras = config.get("extra")
        if self.os_pick:
            self.generate_os_pick_files(extras, files)
        return files

    def on_post_page(self, output: str, page: Page, config: Config):
        """
        If building OS picking files, then add JavaScript code into every such file to enable scrolling
        to the previously selected section on some page.
        :param output: Generated HTML string of some documentation file.
        :param page: Page object.
        :param config: Config object.
        :return: Edited HTML string.
        """
        if self.os_pick:
            output += JS_SCROLL_STR
        else:
            output += JS_OS_NEUTRAL
        return output

    def on_post_build(self, config: Config):
        """
        Remove temporary directory used for generating OS picking files.
        :param config: Config object.
        """
        shutil.rmtree(tmp_dir, ignore_errors=True)
