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
import os


def generate_software_table(software_name, software_data, clusters):
    table_data = [" "] + clusters
    offset = 0

    for k, v in software_data.items():
        if k != ".default":
            row = [f"{software_name}/{k}"]

            for cluster in clusters:
                row += ("x" if cluster in v else "-")
            table_data += row
        else:
            offset += 1
    return table_data


def generate_software_detail_page(software_name, software_data, clusters):
    path = "/mkdocs/docs/HPC/.detail"
    filename = f"{path}/{software_name}_detail.md"
    md_file = MdUtils(file_name=filename, title=f"detailed overview of {software_name}")

    md_file.new_table(
        columns=len(clusters) + 1,
        rows=len(software_data),
        text=generate_software_table(software_name, software_data, clusters)
    )

    md_file.create_md_file()

    # Remove the TOC
    with open(filename) as f:
        read_data = f.read()
    with open(filename, 'w') as f:
        f.write("---\nhide:\n  - toc\n---\n" + read_data)


def generate_detail_pages():
    with open("modulemap.json") as json_data:
        data = json.load(json_data)

    os.makedirs("detail/", exist_ok=True)
    all_clusters = list(k for k, v in data["clusters"].items() if "." not in v)
    for software, versions in data["software"].items():
        generate_software_detail_page(software, versions, all_clusters)


if __name__ == '__main__':
    generate_detail_pages()
