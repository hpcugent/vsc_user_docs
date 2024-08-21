import pytest
import shutil
from chatbot_parser import make_valid_title


@pytest.mark.parametrize("input_string,expected", [
    ("", ""),
    ("A-good-filename-with-dashes", "A-good-filename-with-dashes"),
    (" A very good filename beginning and ending in a space ", "A very good filename beginning and ending in a space"),
    ("-A-very-good-filename-beginning-and-ending-in-a-dash-", "A-very-good-filename-beginning-and-ending-in-a-dash"),
    ("A filename containing bad characters <>:\"/\\|?*\0", "A filename containing bad characters"),
    ("A filename ending with {some jinja garbage}", "A filename ending with")
])
def test_make_valid_title(input_string, expected):
    assert make_valid_title(input_string) == expected
