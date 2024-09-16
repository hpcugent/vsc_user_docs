#
# Copyright 2023-2023 Ghent University
#
# This file is part of vsc_user_docs,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# the Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/hpcugent/vsc_user_docs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Python script to generate an overview of available modules across different clusters, in MarkDown format.

@author: Michiel Lachaert (Ghent University)
"""
import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Union, Tuple
import numpy as np
from mdutils.mdutils import MdUtils
from natsort import natsorted


# --------------------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------------------

def main():
    # EESSI command
    parser = argparse.ArgumentParser()
    parser.add_argument("--eessi", help="eessi mode",
                        action="store_true")
    args = parser.parse_args()

    current_dir = Path(__file__).resolve()
    project_name = 'vsc_user_docs'
    root_dirs = [
        p for p in current_dir.parents if p.parts[-1] == project_name
    ]

    assert len(root_dirs) > 0, f"This script must be called from a child directory of '{project_name}'"

    root_dir = root_dirs[0]
    path_data_dir = os.path.join(root_dir, "mkdocs/docs/HPC/only/gent/available_software/data")

    # Generate the JSON overviews and detail markdown pages.
    if args.eessi:
        modules = modules_eesi()
    else:
        modules = modules_ugent()

    print(modules)
    print("Generate JSON overview... ", end="", flush=True)
    generate_json_overview(modules, path_data_dir)
    print("Done!")
    print("Generate JSON detailed... ", end="", flush=True)
    json_path = generate_json_detailed(modules, path_data_dir)
    print("Done!")
    print("Generate detailed pages... ", end="", flush=True)
    detail_folder = os.path.join(root_dir, "mkdocs/docs/HPC/only/gent/available_software/detail")
    custom_text_folder = os.path.join(root_dir, "mkdocs/docs/HPC/module_custom_text")
    generated_time_yml = os.path.join(root_dir, "mkdocs/extra/gent.yml")  # yml containing time the data was generated
    generate_detail_pages(json_path, detail_folder, custom_text_folder, generated_time_yml)
    print("Done!")


# --------------------------------------------------------------------------------------------------------
# Functions to run bash commands
# --------------------------------------------------------------------------------------------------------

def bash_command(cmd: str) -> np.ndarray:
    proc = subprocess.run(
        ['/bin/bash', '-c', cmd],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return np.array(proc.stdout.split())


# --------------------------------------------------------------------------------------------------------
# Functions to run "module" commands
# --------------------------------------------------------------------------------------------------------

def module(*args, filter_fn=lambda x: x) -> np.ndarray:
    """
    Function to run "module" commands.

    @param args: Extra arguments for the module command.
    @param filter_fn: Filter function on the ouput.
    @return: Array with the output of the module command.
    """
    lmod = os.getenv('LMOD_CMD')
    proc = subprocess.run(
        [lmod, "python", "--terse"] + list(args),
        encoding="utf-8",
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    exec(proc.stdout)
    return filter_fn(np.array(proc.stderr.strip().split("\n")))


def module_avail(name: str = "", filter_fn=lambda x: x) -> np.ndarray:
    """
    Function to run "module avail" commands.

    @param name: Module name, or empty string to return all available modules.
    @param filter_fn: Filter on the output.
    @return: List of all available modules of name, or all if name is not given.
    """
    return module("avail", name, filter_fn=filter_fn)


def module_swap(name: str) -> None:
    """
    Function to run "module swap" commands.

    @param name: Name of module you want to swap to.
    """
    module("swap", name)


def module_use(path: str) -> None:
    """
    Function to run "module use" commands.

    @param path: Path to the directory with all the modules you want to use.
    """
    module("use", path)


def module_unuse(path: str) -> None:
    """
    Function to run "module unuse" commands.

    @param path: Path to the directory with all the modules you want to unuse.
    """
    module("unuse", path)


def module_whatis(name: str) -> dict:
    """
    Function to run "module whatis" commands.

    @param name: Name of module you want the whatis info for.
    """
    whatis = {}
    data = module("show", name)
    for line in data[np.char.startswith(data, "whatis")]:
        content = re.sub(pattern=r'whatis\((.*)\)', repl='\\1', string=line).strip('"')
        key, value = tuple(content.split(":", maxsplit=1))
        whatis[key.strip()] = value.strip()
    return whatis


# --------------------------------------------------------------------------------------------------------
# Fetch data EESSI
# --------------------------------------------------------------------------------------------------------

def filter_fn_eessi_modules(data: np.ndarray) -> np.ndarray:
    """
    Filter function for the output of all software modules for EESSI (excl. `cluster` and `env` modules).
    @param data: Output
    @return: Filtered output
    """
    return data[~np.char.endswith(data, ":")]


def clusters_eessi() -> np.ndarray:
    """
    Returns all the cluster names of EESSI.
    @return: cluster names
    """
    commands = [
        "find /cvmfs/pilot.eessi-hpc.org/versions/2023.06/software/linux/*/* -maxdepth 0 \\( ! -name 'intel' -a ! "
        "-name 'amd' \\) -type d",
        'find /cvmfs/pilot.eessi-hpc.org/versions/2023.06/software/linux/*/{amd,intel}/* -maxdepth 0  -type d'
    ]
    clusters = np.array([])

    for command in commands:
        clusters = np.concatenate([clusters, bash_command(command)])

    return clusters


def modules_eesi() -> dict:
    """
    Returns names of all software module that are installed on EESSI.
    They are grouped by cluster.
    @return: Dictionary with all the modules per cluster
    """
    print("Start collecting modules:")
    data = {}
    module_unuse(os.getenv('MODULEPATH'))
    for cluster in clusters_eessi():
        print(f"\t Collecting available modules for {cluster}... ", end="", flush=True)
        module_use(cluster + "/modules/all/")
        data[cluster] = module_avail(filter_fn=filter_fn_eessi_modules)
        print(f"found {len(data[cluster])} modules!")
        module_unuse(os.getenv('MODULEPATH'))

    print("All data collected!\n")
    return data


# --------------------------------------------------------------------------------------------------------
# Fetch data UGent
# --------------------------------------------------------------------------------------------------------

def filter_fn_gent_cluster(data: np.ndarray) -> np.ndarray:
    """
    Filter function for output of "module avail" commands on HPC-UGent infrastructure.

    Filters out lines ending with ':' (which are paths to module files),
    and lines starting with 'env/' or 'cluster/default', which are not actually software modules
    @param data: Output
    @return: Filtered output
    """
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/") &
                ~np.char.startswith(data, "cluster/default")
                ]


def filter_fn_gent_modules(data: np.ndarray) -> np.ndarray:
    """
    Filter function for the output of all software modules for UGent (excl. `cluster` and `env` modules).
    @param data: Output
    @return: Filtered output
    """
    return data[~np.char.endswith(data, ":") &
                ~np.char.startswith(data, "env/") &
                ~np.char.startswith(data, "cluster/")
                ]


def clusters_ugent() -> np.ndarray:
    """
    Returns all the cluster names of the HPC at UGent.
    @return: cluster names
    """

    return module_avail(name="cluster/", filter_fn=filter_fn_gent_cluster)


def modules_ugent() -> dict:
    """
    Returns names of all software module that are installed on the HPC on UGent.
    They are grouped by cluster.
    @return: Dictionary with all the modules per cluster
    """
    print("Start collecting modules:")
    data = {}
    for cluster in clusters_ugent():
        print(f"\t Collecting available modules for {cluster}... ", end="", flush=True)
        module_swap(cluster)
        cluster_name = cluster.split("/", maxsplit=1)[1]
        data[cluster_name] = module_avail(filter_fn=filter_fn_gent_modules)
        print(f"found {len(data[cluster_name])} modules!")

    print("All data collected!\n")
    return data


# --------------------------------------------------------------------------------------------------------
# Util functions
# --------------------------------------------------------------------------------------------------------

def analyze_module(mod: str) -> Tuple:
    return (
        mod.split("/", 1)[0],
        mod.split("/", 1)[1] if "/" in mod else ""
    )


def mod_names_to_software_names(mod_list: np.ndarray) -> np.ndarray:
    """
    Convert a list of module names to a list of the software names.

    @param mod_list: List of the module names
    @return: List of the corresponding software names
    """
    return np.unique([analyze_module(mod)[0] for mod in mod_list])


def get_unique_software_names(data: Union[dict, list, np.ndarray]) -> Union[dict, list, np.ndarray]:
    """
    Simplify list of modules by removing versions and duplicates.

    @param data: List of modules
    @return: List of software names.
    """

    if isinstance(data, dict):
        simplified_data = {cluster: mod_names_to_software_names(data[cluster]) for cluster in data}
    else:
        simplified_data = mod_names_to_software_names(data)

    return simplified_data


def dict_sort(dictionary: dict) -> dict:
    """
    Sort a dictionary by key.

    @param dictionary: A dictionary
    @return: Sorted dictionary
    """
    return dict(natsorted(dictionary.items()))


# --------------------------------------------------------------------------------------------------------
# Generate detailed markdown
# --------------------------------------------------------------------------------------------------------

def generate_software_table_data(software_data: dict, clusters: list) -> list:
    """
    Construct the data for the detailed software table.

    @param software_data: Software specific data.
    @param clusters: List with all the cluster names
    @return: 1D list with all the data for the table
    """
    table_data = [" "] + clusters

    for module_name, available in list(software_data.items())[::-1]:
        row = [module_name]

        for cluster in clusters:
            row += ("x" if cluster in available else "-")
        table_data += row

    return table_data


def generate_software_detail_page(
        software_name: str,
        software_data: dict,
        clusters: list,
        custom_text_folder: str,
        path: str
) -> None:
    """
    Generate one software specific detail page.

    @param software_name: Name of the software
    @param software_data: Additional information about the software (version, etc...)
    @param clusters: List with all the cluster names
    @param custom_text_folder: Path to the folder with custom text for the software
    @param path: Path of the directory where the detailed page will be created.
    """
    sorted_versions = dict_sort(software_data["versions"])
    newest_version = list(sorted_versions.keys())[-1]

    filename = f"{path}/{software_name}.md"
    md_file = MdUtils(file_name=filename, title=f"{software_name}")

    md_file.write(get_custom_markdown_text(software_name, custom_text_folder))

    md_file.new_header(level=1, title="Available modules")

    md_file.new_paragraph(f"The overview below shows which {software_name} installations are available per HPC-UGent "
                          f"Tier-2 cluster, ordered based on software version (new to old).")
    md_file.new_paragraph(f"To start using {software_name}, load one of these modules using a `module load` command "
                          f"like:")
    md_file.insert_code(f"module load {newest_version}", language="shell")
    md_file.new_paragraph("(This data was automatically generated on {{modules_last_updated}})", bold_italics_code="i")
    md_file.new_line()

    md_file.new_table(
        columns=len(clusters) + 1,
        rows=len(sorted_versions) + 1,
        text=generate_software_table_data(sorted_versions, clusters)
    )

    md_file.create_md_file()

    # Remove the TOC
    with open(filename) as f:
        read_data = f.read()
    with open(filename, 'w') as f:
        f.write("---\nhide:\n  - toc\n---\n" + read_data)


def get_custom_markdown_text(module_name: str, custom_text_folder: str) -> str:
    """
    Get the custom Markdown text that will be added to the detailed Markdown pages.

    @return: Custom Markdown text
    """
    custom_markdown_path = os.path.join(custom_text_folder, module_name + ".md")

    if not os.path.exists(custom_markdown_path):
        return ""

    print(f"Adding custom text for {module_name} located at {custom_markdown_path}")

    with open(custom_markdown_path, 'r') as f:
        return f.read()


def generate_detail_pages(json_path, dest_path, custom_text_folder, generated_time_yml) -> None:
    """
    Generate all the detailed pages for all the software that is available.
    """

    with open(json_path) as json_data:
        data = json.load(json_data)

    # update the time the data was generated
    update_generated_time_yml(generated_time_yml, data["time_generated"])

    all_clusters = data["clusters"]
    for software, content in data["software"].items():
        generate_software_detail_page(software, content, all_clusters, custom_text_folder, dest_path)


def update_generated_time_yml(generated_time_yml, generated_time) -> None:
    """
    Update the time the data was generated in the YAML file.
    This is done by updating the field 'modules_last_updated'.

    @param generated_time_yml: Path to the YAML file containing the field 'modules_last_updated'
    @param generated_time: Time the data was generated
    """
    key = "modules_last_updated"

    # Read the file and replace the specific line
    with open(generated_time_yml, 'r') as file:
        lines = file.readlines()

    replaced = False
    with open(generated_time_yml, 'w') as file:
        for line in lines:
            if line.startswith(key):
                comment = "# This line is automatically updated by scripts/available_modules/available_modules.py"
                line = f"{key}: {generated_time} {comment}\n"
                replaced = True
            file.write(line)

    if not replaced:
        print(f"WARNING: Could not find the key '{key}' in the YAML file '{generated_time_yml}'")


# --------------------------------------------------------------------------------------------------------
# Generate overview markdown
# --------------------------------------------------------------------------------------------------------

def generate_table_data(avail_mods: dict) -> Tuple[np.ndarray, int, int]:
    """
    Generate data that can be used to construct a MarkDown table.

    @param avail_mods: Available modules
    @return: Returns tuple (Table data, #col, #row)
    """
    avail_mods = get_unique_software_names(avail_mods)
    all_modules = get_unique_software_names(np.concatenate(list(avail_mods.values())))

    final = np.array([" "])
    final = np.append(final, list(avail_mods.keys()))

    for package in all_modules:
        final = np.append(final, package)

        for cluster in avail_mods:
            final = np.append(final, "X" if package in avail_mods[cluster] else " ")

    return final, len(avail_mods.keys()) + 1, len(all_modules) + 1


def generate_module_table(data: dict, md_file: MdUtils) -> None:
    """
    Generate the general table of the overview.

    @param data: Dict with all the data. Keys are the cluster names.
    @param md_file: MdUtils object.
    """
    print("Generating markdown table... ", end="", flush=True)
    structured, col, row = generate_table_data(data)
    md_file.new_table(columns=col, rows=row, text=list(structured), text_align='center')
    print("Done!")


def generate_markdown_overview(modules: dict) -> None:
    """
    Generate the general overview in a markdown file.
    It generates a list of all the available software and indicates on which cluster it is available.
    """
    md_fn = 'module_overview.md'
    md_file = MdUtils(file_name=md_fn, title='Overview of available modules per cluster')
    generate_module_table(modules, md_file)
    md_file.create_md_file()
    print(f"Module overview created at {md_fn}")


# --------------------------------------------------------------------------------------------------------
# Generate JSON
# --------------------------------------------------------------------------------------------------------
# -----------
# OVERVIEW
# -----------

# FORMAT OVERVIEW JSON
# {
#     "clusters": ["cluster/dialga", "cluster/pikachu"],
#     "modules": {
#         "Markov": [1, 0],
#         "cfd": [1, 1],
#         "llm": [0, 1],
#         "science": [1, 1]
#     }
# }
def generate_json_overview_data(modules: dict) -> dict:
    """
    Generate the data for the json overview in the above format.

    @param modules: Dictionary with all the modules per cluster. Keys are the cluster names.
    @return: Dictionary with the required JSON structure.

    """
    json_data = {
        "clusters": list(modules.keys()),
        "modules": {},
        "time_generated": time.strftime("%a, %d %b %Y at %H:%M:%S %Z")
    }
    avail_software = get_unique_software_names(modules)
    all_software = get_unique_software_names(np.concatenate(list(modules.values())))

    # creates a list of booleans for each software that indicates
    # if the software is available for the corresponding cluster.
    for soft in all_software:
        available = []
        for cluster in json_data["clusters"]:
            available.append(int(soft in avail_software[cluster]))
        json_data["modules"][soft] = available
    return json_data


def generate_json_overview(modules: dict, path_data_dir: str) -> str:
    """
    Generate the overview in a JSON format.

    @param modules: Dictionary with all the modules per cluster. Keys are the cluster names.
    @param path_data_dir: Path to the directory where the JSON will be placed.
    @return: Absolute path to the json file.
    """

    # get data
    json_data = generate_json_overview_data(modules)

    filepath = os.path.join(path_data_dir, "json_data.json")
    # write it to a file
    with open(filepath, 'w') as outfile:
        json.dump(json_data, outfile)

    return filepath


# -----------
# DETAILED
# -----------

# FORMAT DETAILED JSON:
#
# {
#     "clusters": ["dialga", "pikachu"],
#     "software": {
#         "cfd": {
#             "clusters": ["dialga", "pikachu"],
#             "versions": {
#                 "2.3.1": ["dialga"],
#                 "2.3.2": ["dialga", "pikachu"]
#             }
#         }
#     }
# }

def generate_json_detailed_data(modules: dict) -> dict:
    """
    Generate the data for the detailed JSON in the above format.

    @param modules: Dictionary with all the modules per cluster. Keys are the cluster names.
    @return: Dictionary with the required JSON structure.
    """
    json_data = {
        "clusters": list(modules.keys()),
        "software": {},
        "time_generated": time.strftime("%a, %d %b %Y at %H:%M:%S %Z")
    }

    # Loop over every module in every cluster
    for cluster in modules:
        for mod in modules[cluster]:
            software, version = analyze_module(mod)

            # Exclude modules with no version
            if version != "":
                # If the software is not yet present, add it.
                if software not in json_data["software"]:
                    json_data["software"][software] = {
                        "clusters": [],
                        "versions": {}
                    }

                # If the version is not yet present, add it.
                if mod not in json_data["software"][software]["versions"]:
                    json_data["software"][software]["versions"][mod] = []

                # If the cluster is not yet present, add it.
                if cluster not in json_data["software"][software]["clusters"]:
                    json_data["software"][software]["clusters"].append(cluster)

                # If the cluster is not yet present, add it.
                if cluster not in json_data["software"][software]["versions"][mod]:
                    json_data["software"][software]["versions"][mod].append(cluster)

    return json_data


def generate_json_detailed(modules: dict, path_data_dir: str) -> str:
    """
    Generate the detailed JSON.

    @param modules: Dictionary with all the modules per cluster. Keys are the cluster names.
    @param path_data_dir: Path to the directory where the JSON will be placed.
    @return: Absolute path to the json file.
    """
    json_data = generate_json_detailed_data(modules)
    filepath = os.path.join(path_data_dir, "json_data_detail.json")
    with open(filepath, 'w') as outfile:
        json.dump(json_data, outfile)

    return filepath


if __name__ == '__main__':
    main()
