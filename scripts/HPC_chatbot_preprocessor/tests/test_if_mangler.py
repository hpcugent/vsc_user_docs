import pytest
import os
import shutil
from chatbot_parser import mangle_ifs


@pytest.mark.parametrize("input_file,output_file", [
    ("if_mangler_1_input.md", "if_mangler_1_output.md"),
    ("if_mangler_2_input.md", "if_mangler_2_output.md"),
    ("if_mangler_3_input.md", "if_mangler_3_output.md"),
    ("if_mangler_4_input.md", "if_mangler_4_output.md"),
    ("if_mangler_5_input.md", "if_mangler_5_output.md"),
    ("if_mangler_6_input.md", "if_mangler_6_output.md"),
    ("if_mangler_7_input.md", "if_mangler_7_output.md")
])
def test_if_mangler(input_file, output_file):
    # make directory
    os.makedirs(os.path.join("if_mangled_files"), exist_ok=True)

    # make filepaths
    input_file_path = os.path.join("tests", "test_files", "if_mangler_test_files", input_file)
    expected_output_file_path = os.path.join("tests", "test_files", "if_mangler_test_files", output_file)
    actual_output_file_path = os.path.join("if_mangled_files", input_file)
    mangle_ifs(input_file_path, input_file, {"DESTINATION_DIRECTORY": '.'})

    # check every line
    with open(expected_output_file_path, "r") as expected_read_file:
        with open(actual_output_file_path, "r") as actual_read_file:
            assert all([expected_line == actual_line for expected_line, actual_line in zip(expected_read_file, actual_read_file)])

    # remove directory
    shutil.rmtree("if_mangled_files", ignore_errors=True)
