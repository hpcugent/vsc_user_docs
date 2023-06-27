import argparse
import glob
import gzip
import os.path
import os
import shutil
import subprocess
import tempfile
from shutil import rmtree

from jinja2 import Template
from yaml import safe_load
from multiprocessing import Pool
import xml.etree.ElementTree as ET

import pathlib

REPO_DIR = pathlib.Path(__file__).parent.resolve()

MKDOCS_BASE = 'mkdocs'
CONFIG_BASE = 'config'
CONFIG_OTHERS = f"{CONFIG_BASE}/others"
CONFIG_TEMPLATE = f"{CONFIG_BASE}/templates"

BUILD_YAML = "config/build.yml"

OS_PICK_SUBDIR = 'choose_os'

args = None

class BuildException(Exception):
    """General build exception."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"""\nSubprocess stderr:\n{self.message}\nBuild process failed. -> Cleaning up and exiting.\nTo ignore
        errors and finish all partial builds, use option '--ignore-errors'.\n """

def make_mkdocs_yml():
    """
    Make all yml files
    - copy verbatim from config/others
    - template from config/templates
    - dest dir mkdocs/
    """
    _, config = load_config()

    for yml in glob.glob(f"{MKDOCS_BASE}/*.yml"):
        os.remove(yml)

    # return 3 lists to be processed in parallel
    #   each list is the yml filename and the destdir
    pre = []
    docs = []
    post = []

    # copy inputs from config (TODO: really needed?)
    for oth in config['others']:
        fn = f"{MKDOCS_BASE}/{oth}.yml"
        if oth in ('landing_page',):
            pre.append([fn, None])
        else:
            docs.append([fn, oth])
        shutil.copy2(f"{CONFIG_OTHERS}/{oth}.yml", fn)

    # hpc over sites and OS
    with open(f"{CONFIG_TEMPLATE}/hpc.template") as fh:
        hpc_templ = Template(fh.read())
    for site in config['sites']:
        lsite = site.lower()
        for ymlos in config['os']:
            lymlos = ymlos.lower()
            fn = f"{MKDOCS_BASE}/hpc_{site}_{ymlos}.yml"
            docs.append([fn, f'{site}/{ymlos}'])
            with open(fn, 'w') as fh:
                fh.write(hpc_templ.render(os=ymlos, los=lymlos, site=site, lsite=lsite))

    # os_pick over sites
    with open(f"{CONFIG_TEMPLATE}/os_pick.template") as fh:
        hpc_templ = Template(fh.read())
    for site in config['sites']:
        lsite = site.lower()
        fn = f"{MKDOCS_BASE}/os_pick_{site}.yml"
        post.append([fn, OS_PICK_SUBDIR])
        with open(fn, 'w') as fh:
            fh.write(hpc_templ.render(site=site, lsite=lsite))

    return pre, docs, post

def load_config(yml=None):

    with open(BUILD_YAML, "r") as file:
        config = safe_load(file)

    if yml is None:
        return None, config

    with open(yml, "r") as file:
        extra = safe_load(file).get("extra")

    build_dir = extra.get("build_dir")
    if build_dir is None:
        build_dir = "build/HPC"

    os.makedirs(build_dir, exist_ok=True)

    # return absolute build dirs
    return f"{REPO_DIR}/{build_dir}", config

def build_cmd(cmd):
    print(f">> {cmd}")
    # combine stdout and stderr, so no capture_output; and yse text=True to avoid a bytestream
    process = subprocess.run(cmd, shell=True, text=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    if ' --verbose ' in cmd or process.returncode != 0:
        print(f"{cmd} {process.stdout}")
    if process.returncode != 0:
        raise BuildException(f"{cmd} {process.stdout}")

def build_pool(ops):
    cmds = []
    verb = '--verbose' if args.verbose else ''
    strict = '' if args.notstrict else '--strict'
    for fn, subdir in ops:
        build_dir, _ = load_config(yml=fn)
        dirs = [build_dir]
        if subdir is not None:
            dirs.append(subdir)
        cmds.append(f"mkdocs {verb} build {strict} {verb} --config-file {fn} --site-dir {os.path.join(*dirs)}")

    # Actual build
    try:
        procs = len(os.sched_getaffinity(0))
    except:
        procs = 4

    with Pool(procs) as pool:
        res = pool.map(build_cmd, cmds, 1)


def os_pick_post(ops):
    for fn, subdir in ops:
        if not 'os_pick' in fn:
            continue
        with open(fn, "r") as file:
            config = safe_load(file)
        build_dir = config["extra"]["build_dir"]

        # so how does this work
        #    os_pick generates a subsite in build_dir/OS_PICK_SUBDIR
        #        the subsite is always wiped, that's why build_dir itself can't be used
        #            as it would wipe build_dir/<OS>
        #        the ugent plugin generates fake .md that are converted into html in build_dir
        #   so we need to move the content of build_dir/OS_PICK_SUBDIR (eg the sitemap and any redirects)
        #       to build_dir manually here
        os_pick_dir = f"{build_dir}/{OS_PICK_SUBDIR}"

        for item in os.listdir(os_pick_dir):
            shutil.move(os.path.join(os_pick_dir, item) , os.path.join(build_dir, item))

        def parse_sitemap(fn):
            tree = ET.parse(fn)
            root = tree.getroot()

            if not root.tag.endswith('}urlset'):
                raise Exception(f"Unsupported sitemap.xml no urlset root {fn}")
            if not all([x.tag.endswith('}url') for x in root]):
                raise Exception(f"Unsupported sitemap.xml other than url elements {fn}")

            return tree, root

        # look for sitemap.xml in build_dir
        mainsitemap = f'{build_dir}/sitemap.xml'
        maintree, mainroot = parse_sitemap(mainsitemap)

        # loop over all OSes and merge it in the main sitemap
        oses = []
        for plug in config['plugins']:
            if 'ugent' in plug:
                oses = plug['ugent']['oses']
        for oss in oses:
            _, rt = parse_sitemap(f'{build_dir}/{oss}/sitemap.xml')
            for url in rt:
                mainroot.append(url)

        # write out updated sitemap
        maintree.write(mainsitemap)
        # create gzipped sitemap
        with open(mainsitemap, 'rb') as f_in, gzip.open(f'{mainsitemap}.gz', 'wb') as f_out:
            f_out.writelines(f_in)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get args.")
    parser.add_argument("--verbose", "-v", action="store_true", dest="verbose", help="Enable verbose logging.")
    parser.add_argument("--nostrict", "-n", action="store_true", dest="notstrict", help="Disable strict mkdocs build.")
    parser.add_argument("--nocleanup", "-b", action="store_true", dest="nocleanup", help="Keep build on failure.")

    args = parser.parse_args()

    pre, docs, post = make_mkdocs_yml()

    landing_page_yml = [x for x in pre if 'landing_page' in x[0]][0][0]
    build_dir, config = load_config(landing_page_yml)

    rmtree(build_dir, ignore_errors=True)
    ospick_tmp_dir = tempfile.mkdtemp(prefix='build_os_pick_')
    os.environ['CUSTOM_PLUGIN_OS_PICK_TMPDIR'] = ospick_tmp_dir

    try:
        build_pool(pre)
        build_pool(docs)
        build_pool(post)

        # Fix styling for OS picking pages.
        assets = os.path.normpath(os.path.join(build_dir, "assets"))
        if os.path.isdir(assets):
            # Save old assets.
            assets_old = os.path.join(os.path.dirname(assets), "assets_old")
            shutil.copytree(assets, assets_old)

            # Remove 'javascript' sub-folder as it is not necessary for OS picking files.
            shutil.rmtree(os.path.join(assets, "javascripts"))

            # Copy assets to all OS picking sub-dirs.
            for r, d, f in os.walk(build_dir):
                for directory in d:
                    if (
                        "assets" not in r
                        and "assets" not in directory
                        and not os.path.isdir(os.path.join(r, directory, "assets"))
                    ):
                        shutil.copytree(
                            assets,
                            os.path.normpath(os.path.join(r, directory, "assets")),
                        )
            # Restore original assets.
            shutil.rmtree(assets)
            shutil.move(assets_old, assets)

        # move os_pick build files to site build_dir and merge os_pick site_maps
        os_pick_post(post)

    except BuildException as exc:
        if args.nocleanup:
            print(f"Not cleaning up build_dir {build_dir} and ospick_tmp_dir {ospick_tmp_dir}")
        else:
            rmtree(build_dir, ignore_errors=True)
            rmtree(ospick_tmp_dir, ignore_errors=True)

        raise exc

    # always clean up on success
    rmtree(ospick_tmp_dir, ignore_errors=True)
