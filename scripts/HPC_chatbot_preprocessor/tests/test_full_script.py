import pytest
import os
import shutil
from chatbot_parser import main


@pytest.mark.parametrize("input_directory,actual_output_directory,expected_output_directory, options", [
    ("tests/test_files/ftps", "tests/test_files/ftps/actual",
     "tests/test_files/ftps/output",
     {"SOURCE_DIRECTORY": "tests/test_files/ftps",
      "DESTINATION_DIRECTORY": "tests/test_files/ftps/actual",
      "SPLIT_ON_TITLES": False,
      "SPLIT_ON_PARAGRAPHS": True,
      "MIN_PARAGRAPH_LENGTH": 160,
      "MAX_TITLE_DEPTH": 4,
      "INCLUDE_LINKS_IN_PLAINTEXT": False,
      "DEEP_DIRECTORIES": False,
      "VERBOSE": False}
     ),
    ("tests/test_files/ftts", "tests/test_files/ftts/actual",
     "tests/test_files/ftts/output",
     {"SOURCE_DIRECTORY": "tests/test_files/ftts",
      "DESTINATION_DIRECTORY": "tests/test_files/ftts/actual",
      "SPLIT_ON_TITLES": True,
      "SPLIT_ON_PARAGRAPHS": False,
      "MIN_PARAGRAPH_LENGTH": 160,
      "MAX_TITLE_DEPTH": 4,
      "INCLUDE_LINKS_IN_PLAINTEXT": False,
      "DEEP_DIRECTORIES": True,
      "VERBOSE": False}
     )
])
def test_full_script_generated_directories(input_directory, actual_output_directory, expected_output_directory, options):
    # run the script
    main(options)

    # Compare directories and files
    for dirpath, dirnames, filenames in os.walk(expected_output_directory):
        relative_path = os.path.relpath(dirpath, expected_output_directory)
        actual_dir = os.path.join(actual_output_directory, relative_path)

        # Check if the directory exists
        assert os.path.isdir(actual_dir), f"Directory '{actual_dir}' is missing."

        # Check for files
        for filename in filenames:
            ref_file = os.path.join(dirpath, filename)
            gen_file = os.path.join(actual_dir, filename)

            # Check if the file exists
            assert os.path.isfile(gen_file), f"File '{gen_file}' is missing."

            # Check file content
            with open(ref_file, 'r') as ref_f, open(gen_file, 'r') as gen_f:
                ref_content = ref_f.read().strip()
                gen_content = gen_f.read().strip()
                assert ref_content == gen_content, f"Content of file '{gen_file}' does not match."

    # check that not too many directories have been generated
    for dirpath, dirnames, filenames in os.walk(actual_output_directory):
        relative_path = os.path.relpath(dirpath, actual_output_directory)
        expected_dir = os.path.join(expected_output_directory, relative_path)

        # Check if the directory exists
        assert os.path.isdir(expected_dir), f"Directory '{relative_path}' was made, but shouldn't have been."

    # remove directory
    shutil.rmtree(actual_output_directory, ignore_errors=True)
