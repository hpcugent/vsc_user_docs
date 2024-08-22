import pytest
import os
from chatbot_parser import write_metadata


@pytest.mark.parametrize("main_title,subtitle,links,title_level,directory,output", [
    ("", "", [], 1, "", {"main_title": "", "subtitle": "", "title_depth": 1, "directory": "", "parent_title": ""}),
    ("A_very_good_main_title", "An_extremely_good_subtitle", ["the_first.link", "the_second.link"], 2,
     os.path.join("A_very_good_main_title", "An_awesome_parent_file", "An_extremely_good_subtitle"),
     {"main_title": "A_very_good_main_title", "subtitle": "An_extremely_good_subtitle", "title_depth": 2,
      "directory": os.path.join("A_very_good_main_title", "An_awesome_parent_file", "An_extremely_good_subtitle"),
      "parent_title": "An_awesome_parent_file", "links": {"0": "the_first.link", "1": "the_second.link"}})
])
def test_write_metadata(main_title, subtitle, links, title_level, directory, output):
    assert write_metadata(main_title, subtitle, links, title_level, directory) == output
