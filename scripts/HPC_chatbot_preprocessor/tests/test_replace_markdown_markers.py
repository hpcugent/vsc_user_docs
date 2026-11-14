import pytest
from chatbot_parser import replace_markdown_markers


@pytest.mark.parametrize("input_line, input_linklist, in_code_block, main_title, expected_line, expected_linklist", [
    # baseline test
    ("A normal line with nothing special", [], False, "", "A normal line with nothing special", []),
    # image 1
    ("![image](a-nice-image.png)", [], False, "", "", []),
    # image 2
    ("![](img/Look-at-this-photograph.png)", [], False, "", "", []),
    # link 1 (outside docs)
    ("A line with a [link](https://a-nice-link.com)", ["https://another-link.be"], False, "",
     "A line with a link§link§link§1§link§link§", ["https://another-link.be", "https://a-nice-link.com"]),
    # link 2 (another document within the docs)
    ("A line with a [link to the docs](account.md#welcome-e-mail)", ["https://another-link.be"], False, "",
     "A line with a link to the docs§link§link§1§link§link§", ["https://another-link.be", "https://docs.hpc.ugent.be/account/#welcome-e-mail"]),
    # link 3 (the same document)
    ("A line with a [link to the same doc](#welcome-e-mail)", ["https://another-link.be"], False, "account.md",
     "A line with a link to the same doc§link§link§1§link§link§", ["https://another-link.be", "https://docs.hpc.ugent.be/account/#welcome-e-mail"]),
    # codeblock
    ("```shell", [], True, "", "", []),
    # html syntax 1 (normal syntax)
    ("A line with something in <b>Bold</b>", [], False, "", "A line with something in Bold", []),
    # html syntax 2 (link)
    ("A line with another link<a href=website.com>", ["other-website.com"], False, "",
     "A line with another link§link§link§1§link§link§", ["other-website.com", "website.com"]),
    # html syntax 3 (style)
    ("<p style='text-align: center'>A line with style</p>", [], False, "", "A line with style", []),
    # Bot comment
    ("<!--INPUT_FOR_BOT: Something about the following table-->", [], False, "", "Something about the following table", []),
    # non-Bot comment
    ("<!--Something else about the following table-->", [], False, "", "", []),
    # something else with <>
    ("A line with an example where you should put <your own input>", [], False, "", "A line with an example where you should put <your own input>", []),
    # info/tips/warnings
    ("!!! warning", [], False, "", " warning", []),
    # collapsable admonitions
    ("??? note", [], False, "", " note", []),
    # Markdown syntax 1 (not in code block)
    ("`Line` **with** ++a++ _lot_ *of* _++markdown++_ `syntax`", [], False, "", "Line with a lot of markdown syntax", []),
    # Markdown syntax 2 (in code block)
    ("`Line` **with** ++slightly++ _less_ *markdown* _++syntax++_", [], True, "", "`Line` **with** ++slightly++ _less_ *markdown* _++syntax++_", [])
])
def test_replace_markdown_markers(input_line, input_linklist, in_code_block, main_title, expected_line, expected_linklist):
    assert replace_markdown_markers(input_line, input_linklist, in_code_block, main_title, False) == (expected_line, expected_linklist)
