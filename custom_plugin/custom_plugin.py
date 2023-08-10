import importlib
import json
import os.path as ospath
import shutil
import tempfile
import re
from collections import OrderedDict
from os import makedirs, path, environ, walk, getcwd
from pathlib import Path

from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin, Config
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from yaml import safe_load

from constants import JS_SCROLL_STR, OS_PICK_BTN, OS_PICK_STR, JS_OS_NEUTRAL

"""
See https://www.mkdocs.org/user-guide/plugins/#developing-plugins for some more information
"""

def gen_content_from_macros():
    """
    For each file/script provided in specific directory, this method runs
    the function named the same name as the script and store its returned value
    to dictionary. These values are injected under the same name as variables
    in the final built documentation.
    :return: Dictionary of returned values from provided scripts.
    """
    scripts = "scripts"
    scripts_dir = ospath.join("computational_macros", scripts)

    outputs = {}
    for rt, _, fns in walk(scripts_dir):
        if rt != scripts_dir:
            continue
        for fn in fns:
            if fn == '__init__.py' or not fn.endswith('.py'):
                continue
            stem = Path(fn).stem
            mod_name = f"{scripts}.{stem}"
            mod = importlib.import_module(mod_name)
            fun = getattr(mod, stem)

            # set global variable name used in docs as the filename without the .py extension
            variable_name = path.splitext(fn)[0]

            outputs[variable_name] = fun()
    return outputs


def log(*args):
    import pprint
    with open('/tmp/output', 'a') as fh:
        for arg in args:
            pprint.pprint(arg, stream=fh)


class UgentPlugin(BasePlugin):
    config_scheme = (
        ("os_pick", Type(bool, default=False)),
        ("osneutrallinks", Type(bool, default=False)),
        ("oses", Type(list, default=[])),
        ("os", Type(str, default=None)),
        ("site", Type(str, default=None)),
    )

    def __init__(self, *args, **kwargs):
        super(UgentPlugin, self).__init__(*args, **kwargs)
        self.os_pick = None
        self.oses = None
        self.osneutrallinks = None
        self.os = None
        self.site = None
        self.macro_extras = gen_content_from_macros()
        self.tmp_dir = tempfile.mkdtemp(prefix='custom_plugin_')

    def generate_os_pick_files(self, files, build_dir):

        # gather all .md files from each os of self.site
        mds = OrderedDict()
        mds_oses = {}

        has_os_reg = re.compile(f"/({'|'.join(self.oses)})/")

        for os in self.oses:
            with open(self.get_json_filename(os), 'r') as fh:
                for md in json.load(fh):
                    # do we need to check if the abs_dest_path md[2] contains one of the OSes?
                    link_has_os = has_os_reg.search(md[2]) is not None
                    if not link_has_os:
                        raise Exception(f"No OS found in abs_dest_path {md}")

                    # only keep the html dest path
                    mds[md[0]] = md[1]

                    # add list of all oses the md is found
                    md_oses = mds_oses.setdefault(md[0], [])
                    md_oses.append(os)

        # loop over all mds, generate os_pick index files for the structure
        #   this might break the original site-overriding behaviour
        for md, md_html in mds.items():
            # use md[1] i.e. the html dest_path
            relpath = md_html.split('/')

            # the html is generated with use_directory_urls=True (the default)
            #    meaning a md file a/b/c.md is generated as a/b/c/index.html
            htmlfn = relpath.pop(-1)
            if htmlfn != 'index.html':
                raise Exception(f"Found unexpected md {md} {md_html} with filename {fn}")

            # relpath, with md included (make a copy)
            relpathmd = relpath[:]

            # name, without extension
            if relpath:
                md_name = relpath.pop(-1)
            else:
                # and is probably / must be index.md
                md_name = 'index'
                if md != f'{md_name}.md':
                    raise Exception(f"Unexpected empty relpath for md {md} md_html {md_html}")

            # add index in osneutral path, populate one button per os
            md_txt = OS_PICK_STR

            # all found oses for the md files
            oses = mds_oses[md]

            for os in oses:
                # here, you must use the relpathmd to determine the correct links
                #    add additional empty string to get url with traling / to avoid 301 server redirect
                os_link = [".."] * len(relpathmd) + [os] + relpathmd + ['']
                md_txt += OS_PICK_BTN.format(link_has_os, os, "/".join(os_link))

            #log(f"last oslink {os_link} relpath {relpath}")

            # write the content to filestructure in tmpdir
            abs_md_src_dir = path.normpath(path.join(self.tmp_dir, *relpath))
            if not path.exists(abs_md_src_dir):
                makedirs(abs_md_src_dir)

            md_fn = path.join(*relpath, f"{md_name}.md")

            new_file = File(md_fn, self.tmp_dir, path.abspath(build_dir), True)
            with open(new_file.abs_src_path, "w") as file:
                file.write(md_txt)

            log(f"destdir {path.abspath(build_dir)} build_dir {build_dir} {md_fn}", vars(new_file), md_txt)

            files.append(new_file)

        #log("generated os_pick", [vars(x) for x in files._files if x.src_path.endswith('.md')])

    def on_config(self, config: Config):
        """
        Called when loading config. Extracting some variables as object
        properties and injecting Python macro outputs as variables.
        :param config: Original config object.
        :return: Edited Config object.
        """
        self.os_pick = self.config["os_pick"]
        self.oses = self.config["oses"]
        self.osneutrallinks = self.config["osneutrallinks"]
        self.os = self.config["os"]
        self.site = self.config["site"]
        extras = config.get("extra")
        extras = {**extras, **self.macro_extras}
        config["extra"] = extras
        return config

    def get_json_filename(self, os=None):
        if os is None:
            os = self.os
        envvar = 'CUSTOM_PLUGIN_OS_PICK_TMPDIR'
        tmpdir = environ.get(envvar, None)
        if tmpdir and ospath.isdir(tmpdir):
            # implies HPC files
            fn = f"{tmpdir}/mdfiles_{self.site}_{os}.json"
            return fn
        raise Exception(f"No tmpdir {tmpdir} found for envvar {envvar}")

    def on_files(self, files: Files, config: Config):
        """
        Manipulate files
          - handle only/<site>
          - for osneutrallinks, record all .md files in a json
          - for os_pick, generate the indices for the the recorded osneutrallinks
        :param files: Original Files object.
        :param config: Original Config object.
        :return: Edited Files object.
        """

        # rewrite only/<site>
        reg = re.compile(f"^only/{self.site}/", re.I)
        remove = []
        for idx, fil in enumerate(files):
            if fil.src_path.startswith('only/'):
                if reg.search(fil.src_path):
                    # Cannot make a new File instance, don't know the dest_dir or other original args
                    dest_dir = fil.abs_dest_path[:-len(fil.dest_path)]
                    fil.dest_path = reg.sub('', fil.dest_path)
                    fil.abs_dest_path = dest_dir + fil.dest_path
                    fil.url = reg.sub('', fil.url)
                else:
                    remove.append(idx)
        # reverse index removal
        for idx in remove[::-1]:
            files._files.pop(idx)

        if self.os_pick:
            self.generate_os_pick_files(files, config["extra"]["build_dir"])

        if self.osneutrallinks:
            # track all md files in json
            mds = []
            for fil in files:
                if fil.src_path.endswith('.md'):
                    # store source and dest_path (to deal with only/ rewrites)
                    mds.append([fil.src_path, fil.dest_path, fil.abs_dest_path])
            with open(self.get_json_filename(), 'w') as fh:
                json.dump(mds, fh)

        #log("POST on_files", self.os_pick, [vars(x) for x in files._files if x.src_path.endswith('.md')])
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
        if self.osneutrallinks:
            output += JS_OS_NEUTRAL
        return output

    def on_post_build(self, config: Config):
        """
        Remove temporary directory used for generating OS picking files.
        :param config: Config object.
        """
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
