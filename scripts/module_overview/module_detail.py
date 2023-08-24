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
Python script to generate a detail page for the avalable modules across different clusters, in MarkDown format.
It generates 1 markdown for each module.

@author: Michiel Lachaert (Ghent University)
"""

import json
from mdutils import MdUtils
from natsort import natsorted
import os


def dict_sort(dictionary: dict) -> dict:
    """
    Sort a dictionary by key

    @param dictionary: A dictionary
    @return: Sorted dictionary
    """
    return dict(natsorted(dictionary.items()))


def generate_software_table_data(software_data: dict, clusters: list) -> list:
    """
    Construct the data for the detailed software table.

    @param software_data: Software specific data.
    @param clusters: List with all the cluster names
    @return: 1D list with all the data for the table
    """
    table_data = [" "] + clusters

    for k, v in software_data.items():
        row = [k]

        for cluster in clusters:
            row += ("x" if cluster in v else "-")
        table_data += row

    return table_data


def generate_software_detail_page(software_name: str, software_data: dict, clusters: list, path: str) -> None:
    """
    Generate one software specific detail page.

    @param software_name: Name of the software
    @param software_data: Additional information about the software (version, etc...)
    @param clusters: List with all the cluster names
    @param path: Path of the directory where the detailed page will be created.
    """
    filename = f"{path}/{software_name}_detail.md"
    md_file = MdUtils(file_name=filename, title=f"detailed overview of {software_name}")

    sorted_versions = dict_sort(software_data["versions"])
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


def generate_detail_pages() -> None:
    """
    Generate all the detailed pages for all the software that is available.
    """

    with open("json_data_detail.json") as json_data:
        data = json.load(json_data)

    path = "/home/milachae/Documents/HPC_Vakantiejob_2023/vsc_user_docs/mkdocs/docs/HPC/detail"
    os.makedirs(path, exist_ok=True)
    all_clusters = data["clusters"]
    for software, content in data["software"].items():
        generate_software_detail_page(software, content, all_clusters, path)


if __name__ == '__main__':
    generate_detail_pages()
