import pytest
from chatbot_parser import split_on_paragraphs


@pytest.mark.parametrize("file, main_title, options, is_linux_tutorial, expected_text", [
    ("./tests/test_files/list_file/list_test.md",
     "list_test.md",
     {
         "SOURCE_DIRECTORY": "./test_files/list_file",
         "DESTINATION_DIRECTORY": "./test_files/list_file",
         "SPLIT_ON_TITLES": False,
         "SPLIT_ON_PARAGRAPHS": True,
         "MIN_PARAGRAPH_LENGTH": 100,
         "MAX_TITLE_DEPTH": 4,
         "INCLUDE_LINKS_IN_PLAINTEXT": False,
         "DEEP_DIRECTORIES": False,
         "VERBOSE": False
     },
     False,
     {'list_test.md_paragraph_001': 'Title\n'
                                    'Some explanation about the following list that '
                                    'is quite long. This could be problematic since '
                                    'this could mean that the explanation of the '
                                    'content of the list would be part of a '
                                    'different paragraph than the list.\n'
                                    '1. First entry that is very verbose since we '
                                    'want to hit the character limit for a '
                                    "paragraph to make sure a list can't be split "
                                    'in the middle. If this entry is long enough, '
                                    'the character limit should make it so that any '
                                    'of the following newlines can be the start of '
                                    "a new section if the splitter doesn't know it "
                                    'is in a list.\n'
                                    '2. Second entry\n'
                                    '3. Third entry\n'
                                    '4. Fourth entry that is very verbose, so we '
                                    'hit the character limit for a section split, '
                                    "even though it shouldn't be necessary since "
                                    'the explanation of the list is already well '
                                    'above the character limit.\n',
      'list_test.md_paragraph_002': 'And now the text continues like normal in a '
                                    'new section.'}
     )
])
def test_links(file, main_title, options, is_linux_tutorial, expected_text):
    assert split_on_paragraphs(file, main_title, options, is_linux_tutorial)[1] == expected_text
