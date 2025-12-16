import os
import pytest
from urllib import request
from chatbot_parser import main
import json

#################################################### IMPORTANT: This test still fails because there are some invalid links in the documentation ####################################################

whitelist = ["mailto:hpc@ugent.be"]
slow_list = ["https://login.hpc.ugent.be", "https://www.edx.org/course/introduction-linux-linuxfoundationx-lfs101x-0"]

options_general = {"SOURCE_DIRECTORY": "../../mkdocs/docs/HPC",
                   "DESTINATION_DIRECTORY": ".",
                   "SPLIT_ON_TITLES": False,
                   "SPLIT_ON_PARAGRAPHS": True,
                   "MIN_PARAGRAPH_LENGTH": 683,
                   "MAX_TITLE_DEPTH": 4,
                   "INCLUDE_LINKS_IN_PLAINTEXT": False,
                   "DEEP_DIRECTORIES": False,
                   "VERBOSE": False}
options_os_specific = {"SOURCE_DIRECTORY": "../../mkdocs/docs/HPC/linux-tutorial",
                       "DESTINATION_DIRECTORY": "./linux-tutorial",
                       "SPLIT_ON_TITLES": False,
                       "SPLIT_ON_PARAGRAPHS": True,
                       "MIN_PARAGRAPH_LENGTH": 683,
                       "MAX_TITLE_DEPTH": 4,
                       "INCLUDE_LINKS_IN_PLAINTEXT": False,
                       "DEEP_DIRECTORIES": False,
                       "VERBOSE": False}


@pytest.mark.parametrize("options", [options_general, options_os_specific])
def test_all_links(options):
    all_links = {}
    main(options)
    broken_links = {}
    empty_links = {}

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(options['DESTINATION_DIRECTORY'], 'parsed_mds')):
        for filename in filenames:
            all_links[filename] = []
            if filename.endswith('metadata.json'):
                data = json.load(open(os.path.join(dirpath, filename)))
                if 'links' in data.keys():
                    for key in data['links'].keys():
                        all_links[filename].append(data['links'][key])
                all_links[filename].append(data['reference_link'].split("#")[0])

    for filename in all_links.keys():
        all_links[filename] = list(set(all_links[filename]))
        for link in all_links[filename]:
            if len(link) != 0:
                try:
                    if link not in whitelist and link not in slow_list:
                        with request.urlopen(link) as res:
                            if res.status == 200:
                                pass
                except:
                    print("Broken link in " + filename + ": " + link)
                    if filename in broken_links.keys():
                        broken_links[filename].append(link)
                    else:
                        broken_links[filename] = [link]
            else:
                print("Empty link in " + filename)
                if filename in empty_links.keys():
                    empty_links[filename].append(link)
                else:
                    empty_links[filename] = [link]
    assert len(empty_links.keys()) == 0
    assert len(broken_links.keys()) == 0
