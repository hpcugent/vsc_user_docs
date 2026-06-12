import pytest
import os
from chatbot_parser import write_metadata
from pathlib import Path


@pytest.mark.parametrize("main_title,subtitle,links,title_level,directory,source_file,output", [
    ("", "", [], 1, "", "", {"source_file": "", "main_title": "", "subtitle": "", "title_depth": 1, "directory": ".", "parent_title": ""}),
    ("A_very_good_main_title", "An_extremely_good_subtitle", ["the_first.link", "the_second.link"], 2,
     Path(os.path.join("A_very_good_main_title", "An_awesome_parent_file", "An_extremely_good_subtitle")).as_posix(), "source",
     {"source_file": "source", "main_title": "A_very_good_main_title", "subtitle": "An_extremely_good_subtitle", "title_depth": 2,
      "directory": Path(os.path.join("A_very_good_main_title", "An_awesome_parent_file", "An_extremely_good_subtitle")).as_posix(),
      "parent_title": "An_awesome_parent_file", "links": {"0": "the_first.link", "1": "the_second.link"}})
])
def test_write_metadata(main_title, subtitle, links, title_level, directory, source_file, output):
    assert write_metadata(main_title, subtitle, links, title_level, directory, source_file) == output
