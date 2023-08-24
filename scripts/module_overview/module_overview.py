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

import json
import numpy as np
import os
import subprocess
from mdutils.mdutils import MdUtils
from typing import Union, Tuple


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
    return filter_fn(np.array(proc.stderr.split()))


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


# --------------------------------------------------------------------------------------------------------
# Fetch data
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
    Filter function for the output of all software modules (excl. `cluster` and `env` modules).
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
        data[cluster] = module_avail(filter_fn=filter_fn_gent_modules)
        print(f"found {len(data[cluster])} modules!")

    print("All data collected!\n")
    return data


# --------------------------------------------------------------------------------------------------------
# Util functions
# --------------------------------------------------------------------------------------------------------

def mod_name_to_software_name(mod: str) -> str:
    return mod.split("/", 1)[0]


def mod_names_to_software_names(mod_list: np.ndarray) -> np.ndarray:
    """
    Convert a list of module names to a list of the software names.

    @param mod_list: List of the module names
    @return: List of the corresponding software names
    """
    return np.unique([mod_name_to_software_name(mod) for mod in mod_list])


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


# --------------------------------------------------------------------------------------------------------
# Generate markdown
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
    cluster_names = [x.split('/')[1] for x in avail_mods.keys()]
    final = np.append(final, cluster_names)

    for package in all_modules:
        final = np.append(final, package)

        for cluster in avail_mods:
            final = np.append(final, "X" if package in avail_mods[cluster] else " ")

    return final, len(cluster_names) + 1, len(all_modules) + 1


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

def generate_json_overview_data(modules: dict) -> dict:
    """
    Generate the data for the json overview.

    @param modules: Dict with all the modules per cluster. Keys are the cluster names.
    @return: Dictionary with the required JSON structure.
    """
    json_data = {"clusters": list(modules.keys()), "modules": {}}
    avail_software = get_unique_software_names(modules)
    all_software = get_unique_software_names(np.concatenate(list(avail_software.values())))

    # creates a list of booleans for each software that indicates
    # if the software is available for the corresponding cluster.
    for soft in all_software:
        available = []
        for cluster in json_data["clusters"]:
            available.append(int(soft in avail_software[cluster]))
        json_data["modules"][soft] = available
    return json_data


def generate_json_overview(modules: dict) -> None:
    """
    Generate the overview in a JSON format.
    """

    # get data
    json_data = generate_json_overview_data(modules)

    # write it to a file
    with open("json_data.json", 'w') as outfile:
        json.dump(json_data, outfile)


# {
#     "clusters": ['gallade', 'joltik']
#     "software": {
#         "TensorFlow":
#             "clusters": ['gallade', 'joltik'],
#             "versions":{
#                 "2.3.1": ['gallade', 'joltik'],
#                 }
#             "homepage": ""
#             "description": ""
#             "extensions": ['numpy', '']
#     }
# }

def generate_json_detailed_data(modules: dict) -> dict:
    all_clusters = [cluster.split("/", 1)[1] for cluster in modules]
    json_data = {
        "clusters": all_clusters,
        "software": {}
    }

    for cluster in modules:
        cluster_name = cluster.split("/", 1)[1]
        for mod in modules[cluster]:
            software = mod_name_to_software_name(mod)

            if software not in json_data["software"]:
                json_data["software"][software] = {
                    "clusters": [],
                    "versions": {},
                    "homepage": "",
                    "description": ""
                }

            if mod not in json_data["software"][software]["versions"]:
                json_data["software"][software]["versions"][mod] = []

            if cluster_name not in json_data["software"][software]["clusters"]:
                json_data["software"][software]["clusters"].append(cluster_name)

            if cluster_name not in json_data["software"][software]["versions"][mod]:
                json_data["software"][software]["versions"][mod].append(cluster_name)

    return json_data


def generate_json_detailed(modules: dict) -> None:
    json_data = generate_json_detailed_data(modules)
    with open("json_data_detail.json", 'w') as outfile:
        json.dump(json_data, outfile)


# --------------------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------------------

def main():
    # Generate the overviews
    modules = modules_ugent()
    generate_markdown_overview(modules)
    generate_json_overview(modules)


if __name__ == '__main__':
    main()
