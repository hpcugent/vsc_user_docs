import pytest
from chatbot_parser import insert_links

options_include = {"INCLUDE_LINKS_IN_PLAINTEXT": True}
options_leave_out = {"INCLUDE_LINKS_IN_PLAINTEXT": False}
links_input = {"0": "https://first_link.com", "1": "https://second_link.be", "2": "https://docs.hpc.ugent.be/account#welcome-e-mail", "3": "https://final-link.org"}


@pytest.mark.parametrize("text_input, options_input, text_output, new_links", [
    # Text without links
    # don't include links
    ("Text without links\nand with two lines.", options_leave_out, "Text without links\nand with two lines.", {}),
    # include links
    ("Text without links\nand with two lines.", options_include, "Text without links\nand with two lines.", {}),
    # Text with all links
    # don't include links
    ("Text with all the links\nand with multiple lines.\n§link§link§0§link§link§\n§link§link§1§link§link§\n§link§link§2§link§link§\n§link§link§3§link§link§", options_leave_out,
     "Text with all the links\nand with multiple lines.\n\n\n\n", links_input),
    # include links
    ("Text with all the links\nand with multiple lines.\n§link§link§0§link§link§\n§link§link§1§link§link§\n§link§link§2§link§link§\n§link§link§3§link§link§", options_include,
     "Text with all the links\nand with multiple lines.\n https://first_link.com \n https://second_link.be \n https://docs.hpc.ugent.be/account#welcome-e-mail \n https://final-link.org ", links_input),
    # Text with some links
    # don't include links
    ("Text with all the links\nand with multiple lines.\n§link§link§1§link§link§\n§link§link§3§link§link§", options_leave_out,
     "Text with all the links\nand with multiple lines.\n\n", {"0": "https://second_link.be", "1": "https://final-link.org"}),
    # include links
    ("Text with all the links\nand with multiple lines.\n§link§link§0§link§link§\n§link§link§2§link§link§", options_include,
     "Text with all the links\nand with multiple lines.\n https://first_link.com \n https://docs.hpc.ugent.be/account#welcome-e-mail ", {"0": "https://first_link.com", "1": "https://docs.hpc.ugent.be/account#welcome-e-mail"})
])
def test_insert_links(text_input, options_input, text_output, new_links):
    assert insert_links(text_input, links_input, options_input) == (text_output, new_links)
