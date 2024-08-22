import copy
import json
import os
import re
import shutil
import yaml
from itertools import chain
from pathlib import Path
from jinja2 import FileSystemLoader, Environment, ChoiceLoader, FunctionLoader, Template

#################### define macro's ####################
# customizable macros
MIN_PARAGRAPH_LENGTH = 160
MAX_TITLE_DEPTH = 4
INCLUDE_LINKS_IN_PLAINTEXT = False
SPLIT_ON_TITLES = True
SPLIT_ON_PARAGRAPHS = not SPLIT_ON_TITLES
DEEP_DIRECTORIES = True and SPLIT_ON_TITLES  # Should always be False if SPLIT_ON_TITLES is False

# directories
PARSED_MDS = "parsed_mds"
COPIES = "copies"
IF_MANGLED_FILES = "if_mangled_files"
LINUX_TUTORIAL = "linux-tutorial"
RETURN_DIR = ".."
MKDOCS_DIR = "mkdocs"
DOCS_DIR = "docs"
HPC_DIR = "HPC"
EXTRA_DIR = "extra"
GENERIC_DIR = "generic"
OS_SPECIFIC_DIR = "os_specific"
MACROS = "macros"

# OSes
LINUX = "linux"
WINDOWS = "windows"
MACOS = "macos"
GENERIC = "generic"

# urls
REPO_URL = 'https://github.com/hpcugent/vsc_user_docs'
DOCS_URL = "https://docs.hpc.ugent.be"

# OS-related if-states
ACTIVE = "active"
INACTIVE = "inactive"

# if mangler states
NON_OS_IF = 0
NON_OS_IF_IN_OS_IF = 1
OS_IF = 2
OS_IF_IN_OS_IF = 3

# if mangler macros
IF_MANGLED_PART = "-if-"

# actions
DONE = "done"
WRITE_TEXT = "write_text"
CHECK_EXTRA_MESSAGE = "check_extra_message"
WRITE_TEXT_AND_CHECK_EXTRA_MESSAGE = "write_text_and_check_extra_message"

# Metadata attributes
MAIN_TITLE = "main_title"
SUBTITLE = "subtitle"
TITLE_DEPTH = "title_depth"
DIRECTORY = "directory"
LINKS = "links"
PARENT_TITLE = "parent_title"
PREVIOUS_SUBTITLE = "previous_title"
NEXT_SUBTITLE = "next_title"
METADATA_OS = "OS"
REFERENCE_LINK = "reference_link"

# if-structure components
IF = "if"
ELSE = "else"
ENDIF = "endif"

# link indicators
LINK_MARKER = r'§link§link§'

# regex patterns
IF_MANGLED_PATTERNS = {
        IF: r'({' + IF_MANGLED_PART + r'%[-\s]*if\s+OS\s*[!=]=\s*.+?[-\s]*%' + IF_MANGLED_PART + '})',
        ELSE: r'({' + IF_MANGLED_PART + r'%\s*-?\s*else\s*-?\s*%' + IF_MANGLED_PART + '})',
        ENDIF: r'({' + IF_MANGLED_PART + r'%\s*-?\s*endif\s*-?\s*%' + IF_MANGLED_PART + '})'
    }


################### define functions ###################

def check_for_title(line, in_code_block, curr_dirs):
    """
    function that checks for titles in the current line. Used by split_text to split the text among the subtitles

    :param line: the current line to be checked for a title
    :param in_code_block: boolean indicating whether the current line is part of a codeblock to be sure comments aren't counted as titles
    :param curr_dirs: the current working directories for each level of subtitle, to be updated when a new title is found
    :return title_length: The amount of hashtags in front of the title on the current line
    """
    # detect titles
    match = re.match(r'^#+ ', line)
    if match and len(match.group(0)) <= 5 and not in_code_block:
        title_length = len(match.group(0)) - 1
        if DEEP_DIRECTORIES:
            curr_dirs[title_length] = os.path.join(curr_dirs[title_length - 1], make_valid_title(line[title_length + 1:-1].replace(' ', '-')))

            # update the higher order current directories
            for i in range(title_length + 1, MAX_TITLE_DEPTH + 1):
                curr_dirs[i] = curr_dirs[title_length]

        return title_length
    else:
        return 0


def replace_markdown_markers(curr_line, linklist, in_code_block, main_title):
    """
    function that replaces certain markdown structures with the equivalent used on the website

    :param curr_line: the current line on which markdown structures need to be replaced
    :param linklist: the list used to store links that need to be printed at the end of the file
    :param in_code_block: boolean indicating whether the current line is part of a code block
    :param main_title: the main title of the file that is being processed
    :return curr_line: the adapted current line
    :return linklist: the updated linklist
    """

    # replace images with an empty line
    if re.search(r'(?i)!\[image]\(.*?\)', curr_line) or re.search(r'!\[]\(img/.*?.png\)', curr_line):
        curr_line = ""

    # replace links with a reference
    matches = re.findall(r'\[(.*?)]\((.*?)\)', curr_line)
    if matches:
        for match in matches:
            curr_line = curr_line.replace(f"[{match[0]}]({match[1]})", match[0] + LINK_MARKER + str(len(linklist)) + LINK_MARKER)
            if ".md" not in match[1]:
                if "#" not in match[1]:
                    linklist.append(match[1])
                else:
                    linklist.append(DOCS_URL + "/" + main_title + "/" + match[1])
            else:
                linklist.append(DOCS_URL + "/" + match[1].replace(".md", "/").replace("index", "").rstrip("/"))

    # codeblock (with ``` -> always stands on a separate line, so line can be dropped)
    if '```' in curr_line:
        curr_line = ""

    # structures within <>
    match = re.findall(r'<(.*?)>', curr_line)
    if match:
        for i, content in enumerate(match):
            syntax_words = ["pre", "b", "code", "sub", "br", "center", "p", "div", "u", "p", "i", "tt", "a", "t", "span"]  # make sure these are always lowercase
            syntax_words_variations = list(chain.from_iterable([[element, element + "/", "/" + element] for element in syntax_words]))
            syntax_words_style = [element + " style=.*" for element in syntax_words]

            # add references for every link of format <a href=...>
            if re.search(r'a href=.*', content):
                link = content[8:-1]
                curr_line = re.sub(f'<{content}>', "[" + str(len(linklist) + 1) + "]", curr_line)
                linklist.append(link)

            # drop the syntax words
            elif content.lower() in syntax_words_variations:
                curr_line = re.sub(f'<{content}>', "", curr_line)

            # drop the version of the syntax_words followed by " style="
            elif any(re.match(pattern, content) for pattern in syntax_words_style):
                curr_line = re.sub(r'<.*?>', "", curr_line)

            # drop markdown comments
            elif re.fullmatch(r'!--.*?--', content):
                curr_line = re.sub(r'<.*?>', "", curr_line)

            # special case (ugly fix)
            elif ' files</b' in content:
                curr_line = re.sub(r'</b>', "", curr_line)

            # keep the rest
            else:
                pass

    # structures with !!! (info, tips, warnings)
    if '!!!' in curr_line:
        curr_line = re.sub(r'!!!', "", curr_line)

    # structures with ??? (collapsable admonitions)
    if '???' in curr_line:
        curr_line = re.sub(r'\?\?\?', "", curr_line)

    # get rid of other markdown indicators (`, *, +, _)
    if not in_code_block:

        backquotes = re.findall(r'`(.*?)`', curr_line)
        if backquotes:
            for i, content in enumerate(backquotes):
                curr_line = curr_line.replace(f"`{content}`", content)

        asterisks = re.findall(r'(?<!\\)(\*+)(.+?)\1', curr_line)
        if asterisks:
            for i, content in enumerate(asterisks):
                curr_line = re.sub(r"(\*+)" + content[1] + r"\1", content[1], curr_line)

        pluses = re.findall(r'\+\+(.+?)\+\+', curr_line)
        if pluses:
            for i, content in enumerate(pluses):
                curr_line = re.sub(r"\+\+" + content + r"\+\+", content, curr_line)

        underscores = re.findall(r' (_+)(.+?)\1 ', curr_line)
        if underscores:
            for i, content in enumerate(underscores):
                curr_line = re.sub(r"(_+)" + content[1] + r"\1", content[1], curr_line)

    return curr_line, linklist


def split_text(file, main_title):
    """
    Function that splits the text into smaller sections and makes them into two dictionaries containing text and metadata

    :param file: the filepath of the file to be split
    :param main_title: the main title of the file
    :return paragraphs_text: dictionary containing the split sections of text
    :return paragraphs_metadata: dictionary containing the metadata of each split section of text
    :return subtitle_order: list containing all encountered subtitles in order of appearance
    """

    if SPLIT_ON_TITLES:
        return split_on_titles(file, main_title)
    elif SPLIT_ON_PARAGRAPHS:
        return split_on_paragraphs(file, main_title)


def split_on_titles(file, main_title):
    """
    Function that splits the text into smaller sections based on the subtitle structure and makes them into two dictionaries containing text and metadata

    :param file: the filepath of the file to be split
    :param main_title: the main title of the file
    :return paragraphs_text: dictionary containing the split sections of text
    :return paragraphs_metadata: dictionary containing the metadata of each split section of text
    :return subtitle_order: list containing all encountered subtitles in order of appearance
    """
    # start of assuming we haven't encountered a title
    after_first_title = False

    # start of assuming we are not in a code_block
    in_code_block = False

    # define initial dictionaries
    paragraphs_os_free_text = {}
    paragraphs_os_text = {}
    paragraphs_metadata = {}

    # variable to keep track of the current paragraph
    current_paragraph = ""

    # list to keep track of links in the text
    link_list = []

    # list to keep track of the order of the subtitles
    subtitle_order = []

    # variable to keep track of the title level
    title_level = 0

    # variable to allow for if statements to "continue" over multiple paragraphs
    open_ifs = ""

    # variable to keep track of how many if-statements deep the current line is
    in_if_statement = 0

    # variable to indicate that previous section was one with if-statements
    previous_contained_if = False

    # list to keep track of most recent directories on each title level
    if LINUX_TUTORIAL not in file:
        curr_dirs = [main_title for _ in range(MAX_TITLE_DEPTH + 1)]
    else:
        curr_dirs = [os.path.join(LINUX_TUTORIAL, main_title) for _ in range(MAX_TITLE_DEPTH + 1)]

    with open(file, 'r') as readfile:

        for line in readfile:

            # detect if-statements starting or ending on the current line
            in_if_statement += len(re.findall(IF_MANGLED_PATTERNS[IF], line)) - len(re.findall(IF_MANGLED_PATTERNS[ENDIF], line))

            # only split up if current line is in a fully non-os-specific section
            if in_if_statement == 0:

                title_level = check_for_title(line, in_code_block, curr_dirs)

                # detect codeblocks to make sure titles aren't detected in them
                if '```' in line or (('<pre><code>' in line) ^ ('</code></pre>' in line)):
                    in_code_block = not in_code_block

                # line is a title with a maximum depth of 4
                if title_level > 0:
                    if after_first_title:

                        # write text of previous file
                        if previous_contained_if:
                            paragraphs_os_text[title] = current_paragraph
                        else:
                            paragraphs_os_free_text[title] = current_paragraph

                        # write metadata of previous file
                        paragraphs_metadata[title] = write_metadata(main_title, title, link_list, last_title_level, last_dir)

                    # make a new title
                    title = make_valid_title(line[title_level + 1:-1])

                    # create an entry for the file in the paragraphs text dictionary
                    current_paragraph = open_ifs

                    after_first_title = True
                    subtitle_order.append(title)

                    # reset link_list
                    link_list = []

                    previous_contained_if = False

                # line is not a title
                elif after_first_title:
                    line, link_list = replace_markdown_markers(line, link_list, in_code_block, main_title)
                    if line != "\n":
                        current_paragraph += line

                # keep track of title level and directory to write to metadata upon discovering a new subtitle
                if title_level > 0:
                    last_title_level = title_level
                    last_dir = curr_dirs[last_title_level]
            else:
                previous_contained_if = True
                line, link_list = replace_markdown_markers(line, link_list, in_code_block, main_title)
                if line != "\n":
                    current_paragraph += line

    # write dictionaries for the last file
    if previous_contained_if:
        paragraphs_os_text[title] = current_paragraph
    else:
        paragraphs_os_free_text[title] = current_paragraph
    paragraphs_metadata[title] = write_metadata(main_title, title, link_list, last_title_level, curr_dirs[last_title_level])

    return paragraphs_os_text, paragraphs_os_free_text, paragraphs_metadata, subtitle_order


def split_on_paragraphs(file, main_title):
    """
    Function that splits the text into smaller sections based on the paragraph structure and makes them into two dictionaries containing text and metadata

    :param file: the filepath of the file to be split
    :param main_title: the main title of the file
    :return paragraphs_text: dictionary containing the split sections of text
    :return paragraphs_metadata: dictionary containing the metadata of each split section of text
    :return subtitle_order: list containing all encountered subtitles in order of appearance
    """
    # start of assuming we haven't encountered a title and the first paragraph hasn't appeared yet
    after_first_title = False

    # first paragraph number
    paragraph_number = 1

    # start of assuming we are not in a code_block
    in_code_block = False

    # define initial dictionaries
    paragraphs_text = {}
    paragraphs_metadata = {}

    # list to keep track of links in the text
    link_list = []

    # list to keep track of the order of the subtitles
    subtitle_order = []

    # variable to keep track of the title level
    title_level = 0

    # initialise the first paragraph
    title = main_title + "_paragraph_" + str(paragraph_number)
    paragraphs_text[title] = ""
    subtitle_order.append(title)

    # list to keep track of most recent directories on each title level
    if LINUX_TUTORIAL not in file:
        curr_dirs = [main_title for _ in range(MAX_TITLE_DEPTH + 1)]
    else:
        curr_dirs = [os.path.join(LINUX_TUTORIAL, main_title) for _ in range(MAX_TITLE_DEPTH + 1)]

    with open(file, 'r') as readfile:

        for line in readfile:

            # keep track of title level and directory to write to metadata upon discovering a new subtitle
            if title_level > 0:
                last_title_level = title_level
                last_dir = curr_dirs[last_title_level]

            title_level = check_for_title(line, in_code_block, curr_dirs)

            # detect codeblocks to make sure titles and beginnings of paragraphs aren't detected in them
            if '```' in line or (('<pre><code>' in line) ^ ('</code></pre>' in line)):
                in_code_block = not in_code_block

            # line is a title with a maximum depth of 4
            if title_level > 0:
                paragraphs_text[title] += line[title_level + 1:]

            elif line == "\n" and len(re.sub(r'\{' + IF_MANGLED_PART + '%.*?%' + IF_MANGLED_PART + '}', "", paragraphs_text[title])) >= MIN_PARAGRAPH_LENGTH:
                # finish the previous file
                paragraphs_text[title], open_ifs = close_ifs(paragraphs_text[title])
                paragraphs_metadata[title] = write_metadata(main_title, title, link_list, last_title_level, last_dir)

                # start a new file
                paragraph_number += 1
                title = make_valid_title(main_title + "_paragraph_" + str(paragraph_number))
                subtitle_order.append(title)

                # create an entry for the next file in the paragraphs text dictionary
                paragraphs_text[title] = open_ifs

                # reset link_list
                link_list = []

            # line is not a title or the ending of a sufficiently large paragraph
            else:
                line, link_list = replace_markdown_markers(line, link_list, in_code_block, main_title)
                if title in paragraphs_text.keys() and line != "\n":
                    paragraphs_text[title] += line
                elif line != "\n":
                    paragraphs_text[title] = line

    # write metadata for the last file
    paragraphs_metadata[title] = write_metadata(main_title, title, link_list, title_level, curr_dirs[last_title_level])

    return paragraphs_text, paragraphs_metadata, subtitle_order


def write_metadata(main_title, subtitle, links, title_level, directory):
    """
    Function that writes metadata about a text section to a dictionary

    :param main_title: The main title of the file containing the section
    :param subtitle: the title of the section
    :param links: a list of links contained within the section
    :param title_level: the depth of the title of the section
    :param directory: the directory where the section will eventually be written (can either be generic or os-specific)
    :return paragraph_metadata: dictionary containing the metadata about the section
    """

    paragraph_metadata = {MAIN_TITLE: main_title, SUBTITLE: subtitle, TITLE_DEPTH: title_level, DIRECTORY: directory}

    if len(links) > 0:
        paragraph_metadata[LINKS] = {}
        for i, link in enumerate(links):
            paragraph_metadata[LINKS][str(i)] = link

    paragraph_metadata[PARENT_TITLE] = Path(directory).parent.name

    return paragraph_metadata


def close_ifs(text):
    """
    Function to check whether all if-statements in a section are closed properly. If that is not the case, the function
    closes all if-statements at the end of the section and returns a prefix for the next section containing all if-statements
    of the section it is processing. This needs to be done because the start of the next section would also be contained within the
    last unclosed if-statement of its previous section.

    :param text: the text of the section it checks
    :return text: the adapted text where all if-statements are closed
    :return prefix: the prefix for the next section
    """

    if_count = len(re.findall(IF_MANGLED_PATTERNS[IF], text.replace("\n", "")))
    endif_count = len(re.findall(IF_MANGLED_PATTERNS[ENDIF], text.replace("\n", "")))
    if IF_MANGLED_PART not in text or if_count == endif_count:
        return text, ""
    else:

        # Find all matches for each pattern
        matches = []
        for key, pattern in IF_MANGLED_PATTERNS.items():
            for match in re.finditer(pattern, text):
                matches.append(match)

        # sort the matches according to their start index
        matches.sort(key=lambda x: x.start())

        # extract the strings from the matches
        open_ifs = []
        for match in matches:
            open_ifs.append(match.group(0))

        # only include the non-closed if-statements
        changed = True
        while changed:
            changed = False
            last_if = -1
            last_else = -1
            for i, if_part in enumerate(open_ifs):
                if re.search(IF_MANGLED_PATTERNS[IF], if_part):
                    last_if = i
                elif re.search(IF_MANGLED_PATTERNS[ELSE], if_part):
                    last_else = i
                elif re.search(IF_MANGLED_PATTERNS[ENDIF], if_part):
                    changed = True
                    del open_ifs[i]
                    if last_else > last_if:
                        del open_ifs[last_else]
                    del open_ifs[last_if]
                    break

        # Concatenate all matches into a single string
        open_ifs = ''.join(open_ifs)

        return text + (r'{' + IF_MANGLED_PART + '% endif %' + IF_MANGLED_PART + '}')*(if_count - endif_count), open_ifs


def jinja_parser(filename, copy_location):
    """
    function that let's jinja do its thing to format the files except for the os-related if-statements

    :param filename: the name of the file that needs to be formatted using jinja
    :param copy_location: the location of the file that needs to be formatted using jinja
    :return:
    """
    # YAML file location
    yml_file_path = os.path.join(RETURN_DIR, RETURN_DIR, MKDOCS_DIR, EXTRA_DIR, 'gent.yml')

    # Read the YAML file
    with open(yml_file_path, 'r') as yml_file:
        words_dict = yaml.safe_load(yml_file)

    # ugly fix for index.md error that occurs because of the macro "config.repo_url" in mkdocs/docs/HPC/index.md
    additional_context = {
        'config': {
            'repo_url': REPO_URL
        }
    }
    combined_context = {**words_dict, **additional_context}

    # Mangle the OS-related if-statements
    mangle_ifs(copy_location, filename)

    # Use Jinja2 to replace the macros
    template_loader = ChoiceLoader([FileSystemLoader(searchpath=[IF_MANGLED_FILES, os.path.join(RETURN_DIR, RETURN_DIR, MKDOCS_DIR, DOCS_DIR, HPC_DIR)]), FunctionLoader(load_macros)])
    templateEnv = Environment(loader=template_loader)
    template = templateEnv.get_template(filename)
    rendered_content = template.render(combined_context)

    # Save the rendered content to a new file
    with open(copy_location, 'w', encoding='utf-8', errors='ignore') as output_file:
        output_file.write(rendered_content)


def load_macros(name):
    """
    function used by the jinja FunctionLoader to retrieve templates from the macros folder since the normal FileSystemLoader can't locate them properly

    :param name: name of the package
    :return:
    """

    macros_location = os.path.join(RETURN_DIR, RETURN_DIR, MKDOCS_DIR, DOCS_DIR, MACROS)

    if "../" + MACROS + "/" in name:
        package_name = name.split("../" + MACROS + "/")[1]
        file_location = os.path.join(macros_location, package_name)

        with open(file_location, 'r') as readfile:
            return readfile.read()


def mangle_os_ifs(line, is_os):
    """
    function that mangles the os-related if-statements. This is needed because we want to keep these if-statements intact after jinja-parsing to build the directory structure.
    We don't want to mangle all if-related statements (such as else and endif) so we need to keep track of the context of the last few if-statements.

    :param line: the current line to check for os-related if-statements
    :param is_os: variable keep track of the current os-state of the if-statements. Can be NON_OS_IF, NON_OS_IF_IN_OS_IF, OS_IF or OS_IF_IN_OS_IF
        NON_OS_IF: not in an os-if
        NON_OS_IF_IN_OS_IF: in a non-os-if nested in an os-if
        OS_IF: in an os-if
        OS_IF_IN_OS_IF: in an os-if nested in an os-if
    :return line: the modified line with  mangled os-related if-statements
    """

    match = re.search(r'\{%(.*?)%}(.*)', line)

    start_index = 0
    added_length = 0

    while match:

        constr_match = re.search(r'\{%.*?%}', match.string)
        if_match = re.search(r'if ', match.group(1))
        if_os_match = re.search(r'if OS ', match.group(1))
        endif_match = re.search(r'endif', match.group(1))
        else_match = re.search(r'else', match.group(1))

        # mangle positions
        pos_first_mangle = constr_match.start() + start_index + added_length + 1
        pos_second_mangle = constr_match.end() + start_index + added_length - 1

        # different parts of the original string
        part_before_mangling = line[:pos_first_mangle]
        part_between_mangling = line[pos_first_mangle:pos_second_mangle]
        part_after_mangling = line[pos_second_mangle:]

        # this logic isn't flawless, there are number of nested if-constructions that are technically possible that would break this logic, but these don't appear in the documentation as it doesn't make sense to have these
        if endif_match:
            if is_os in (OS_IF, OS_IF_IN_OS_IF):
                line = part_before_mangling + IF_MANGLED_PART + part_between_mangling + IF_MANGLED_PART + part_after_mangling
                added_length += 2 * len(IF_MANGLED_PART)
                if is_os == OS_IF:
                    is_os = NON_OS_IF
                elif is_os == OS_IF_IN_OS_IF:
                    is_os = OS_IF
            elif is_os == NON_OS_IF_IN_OS_IF:
                is_os = OS_IF

        elif if_match:
            if if_os_match:
                line = part_before_mangling + IF_MANGLED_PART + part_between_mangling + IF_MANGLED_PART + part_after_mangling
                added_length += 2 * len(IF_MANGLED_PART)
                if is_os == OS_IF:
                    is_os = OS_IF_IN_OS_IF
                else:
                    is_os = OS_IF
            else:
                if is_os == OS_IF:
                    is_os = NON_OS_IF_IN_OS_IF
                else:
                    is_os = NON_OS_IF

        elif else_match:
            if is_os in (OS_IF, OS_IF_IN_OS_IF):
                line = part_before_mangling + IF_MANGLED_PART + part_between_mangling + IF_MANGLED_PART + part_after_mangling
                added_length += 2 * len(IF_MANGLED_PART)

        start_index += constr_match.end()
        match = re.search(r'\{%(.*?)%}(.*)', match.group(2))
    return line, is_os


def mangle_ifs(directory, filename):
    """
    function that writes the if-mangled version of a file to a location where the jinja parser will use it

    :param directory: the directory of the file to be if mangled
    :param filename: the filename of the file to be mangled
    :return:
    """
    # variable to keep track of latest if-statement scope
    is_os = NON_OS_IF

    with open(os.path.join(IF_MANGLED_FILES,  filename), 'w') as write_file:
        with open(directory, 'r') as read_file:
            for line in read_file:
                new_line, is_os = mangle_os_ifs(line, is_os)
                write_file.write(new_line)


def make_valid_title(title):
    """
    function that makes sure all titles can be used as valid filenames

    :param title: the string that will be used as title and filename
    :return valid_filename: the adapted title that can be used as filename
    """
    # Define a regex pattern for invalid characters on both Windows and Linux
    invalid_chars = r'[<>:"/\\|?*\0]'

    # get rid of extra information between {} brackets
    title = re.sub(r'\{.*?}', '', title)

    # Remove invalid characters
    valid_filename = re.sub(invalid_chars, '', title)

    # Strip leading/trailing whitespace
    valid_filename = valid_filename.strip().strip('-').replace(' ', '-')

    return valid_filename


def write_generic_file(title, paragraphs_text, paragraphs_metadata, title_order, title_order_number, paragraph_numbers):
    """
    Function that writes text and metadata of a generic (non-os-specific) file

    :param title: title of section
    :param paragraphs_text: dictionary containing all paragraphs of text
    :param paragraphs_metadata: dictionary containing the metadata for all paragraphs of text
    :param title_order: list containing all subtitles in order
    :param title_order_number: order number of the title of the section that is being written
    :param paragraph_numbers: dictionary keeping track of the amount of paragraphs that have been written for each OS
    :return:
    """

    if len(paragraphs_text[title]) > 0:
        # make the directory needed for the files that will be written
        filepath = os.path.join(PARSED_MDS, GENERIC_DIR, paragraphs_metadata[title][DIRECTORY])
        os.makedirs(filepath, exist_ok=True)

        write_files(title, paragraphs_text[title], paragraphs_metadata, title_order, title_order_number, filepath, OS=GENERIC, paragraph_numbers=paragraph_numbers)
    else:
        # don't write empty files
        pass


def write_files(title, text, paragraphs_metadata, title_order, title_order_number, filepath, OS, paragraph_numbers):
    """
    Function to write files to a certain filepath

    :param title: title of the section to be written
    :param text: section of text to be written
    :param paragraphs_metadata: dictionary containing the metadata for all paragraphs of text
    :param title_order: list containing all subtitles in order
    :param title_order_number: order number of the title of the section that is being written
    :param filepath: filepath to write files to
    :param OS: OS to be included in the metadata
    :param paragraph_numbers: dictionary keeping track of the amount of paragraphs that have been written for each OS
    :return:
    """

    metadata = copy.deepcopy(paragraphs_metadata[title])

    file_title = paragraphs_metadata[title][MAIN_TITLE] + "_" + OS + "_paragraph_" + str(paragraph_numbers[OS])
    file_title = title

    # write text file
    with open(os.path.join(filepath, file_title + ".txt"), 'w') as writefile:
        if LINKS in paragraphs_metadata[title].keys():
            adapted_text, metadata[LINKS] = insert_links(text, metadata[LINKS])
            writefile.write(adapted_text)
        else:
            writefile.write(text)

    # write metadata
    if title_order_number != 0:
        metadata[PREVIOUS_SUBTITLE] = title_order[title_order_number - 1]
    else:
        metadata[PREVIOUS_SUBTITLE] = None

    if title_order_number != len(title_order) - 1:
        metadata[NEXT_SUBTITLE] = title_order[title_order_number + 1]
    else:
        metadata[NEXT_SUBTITLE] = None

    metadata[METADATA_OS] = OS

    if bool(LINUX_TUTORIAL in paragraphs_metadata[title][DIRECTORY]):
        linux_part = LINUX_TUTORIAL + "/"
    else:
        linux_part = ""
    if OS == GENERIC:
        os_part = ""
    else:
        os_part = OS + "/"
    metadata[REFERENCE_LINK] = DOCS_URL + "/" + os_part + linux_part + paragraphs_metadata[title][MAIN_TITLE] + "/#" + ''.join(char.lower() for char in title if char.isalnum() or char == '-').strip('-')

    with open(os.path.join(filepath, file_title + "_metadata.json"), 'w') as writefile:
        json.dump(metadata, writefile, indent=4)

    paragraph_numbers[OS] += 1


def insert_links(text, links):
    """
    Function that inserts links in the plaintext or takes out the references to the links depending on the value of INCLUDE_LINKS_IN_PLAINTEXT

    :param text: The plaintext that needs to be adapted
    :param links: The links that might need to be inserted
    :return text: The adapted plaintext
    :return links: The links that were actually present in the text
    """

    present_links = []
    new_links = {}
    for link_number in re.finditer(LINK_MARKER + r'([0-9]*?)' + LINK_MARKER, text):
        present_links.append(link_number.group(1))
        if INCLUDE_LINKS_IN_PLAINTEXT:
            text = re.sub(LINK_MARKER + link_number.group(1) + LINK_MARKER, " " + links[link_number.group(1)] + " ", text)
        else:
            text = re.sub(LINK_MARKER + link_number.group(1) + LINK_MARKER, "", text)

    for link_number in links.keys():
        if link_number in present_links:
            new_links[len(new_links.keys())] = links[link_number]

    return text, new_links


def split_and_write_os_specific_section(text, metadata, subtitle_order, title_order_number, paragraph_numbers, all_metadata):
    """
    Function that splits os-specific sections into subtitles, parses them using jinja and writes them away

    :param text: full os specific section
    :param metadata: metadata generated for the full os specific section
    :param subtitle_order: order of the subtitles generated by the splitter
    :param title_order_number: order number of the section
    :param paragraph_numbers: dictionary keeping track of the amount of paragraphs that have been written for each OS
    :param all_metadata: all metadata generated by the splitter
    :return:
    """
    # add first subtitle in front of section again
    text = "#" * metadata[TITLE_DEPTH] + " " + metadata[SUBTITLE] + "\n" + text

    # Unmangle if's to use jinja parser
    text = re.sub(IF_MANGLED_PART, "", text)

    for OS in [LINUX, WINDOWS, MACOS]:

        # slightly alter if-statements to be able to use predefined macros
        text = re.sub(OS, '"' + OS + '"', text)

        # Use jinja to render a different version of the text for each OS
        template = Template(text)
        jinja_text = template.render(OS=OS)

        # re-adjust text to correct overcorrections
        jinja_text = re.sub('"' + OS + '"', OS, jinja_text)

        with open("jinja_file.txt", 'w') as writefile:
            writefile.write(jinja_text)

        # split in right way
        _, os_specific_text, os_specific_metadata, os_subtitle_order = split_text("jinja_file.txt", metadata[MAIN_TITLE])

        # prepare variables to fix metadata
        total_subtitle_order = subtitle_order[:title_order_number] + os_subtitle_order + subtitle_order[title_order_number+1:]
        all_metadata.update(os_specific_metadata)

        # write to files
        for os_i, os_subtitle in enumerate(os_subtitle_order):
            # check that file actually has some content
            if len(os_specific_text[os_subtitle]) > 0:
                # add the links to the metadata
                if LINKS in metadata.keys():
                    os_specific_metadata[os_subtitle][LINKS] = metadata[LINKS]

                # fix parent in the metadata
                parent_i = 0
                parent_depth = os_specific_metadata[os_subtitle][TITLE_DEPTH] - 1
                parent = os_specific_metadata[os_subtitle][MAIN_TITLE]
                while total_subtitle_order[parent_i] != os_subtitle and parent_i != len(total_subtitle_order):
                    if all_metadata[total_subtitle_order[parent_i]][TITLE_DEPTH] == parent_depth:
                        parent = total_subtitle_order[parent_i]
                    parent_i += 1
                os_specific_metadata[os_subtitle][PARENT_TITLE] = parent

                # fix directory in the metadata
                if parent == os_specific_metadata[os_subtitle][MAIN_TITLE]:
                    os_specific_metadata[os_subtitle][DIRECTORY] = os.path.join(parent, os_specific_metadata[os_subtitle][SUBTITLE])
                else:
                    os_specific_metadata[os_subtitle][DIRECTORY] = os.path.join(all_metadata[parent][DIRECTORY], os_specific_metadata[os_subtitle][SUBTITLE])

                # make a directory to save the files
                filepath = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, OS, os_specific_metadata[os_subtitle][DIRECTORY])
                os.makedirs(filepath, exist_ok=True)

                # write to files
                write_files(os_subtitle, os_specific_text[os_subtitle], os_specific_metadata, total_subtitle_order, os_i + title_order_number, filepath, OS, paragraph_numbers)
            else:
                # don't write empty files
                pass


def main():
    """
    main function
    :return:
    """
    # remove the directories from a previous run of the parser if they weren't cleaned up properly for some reason
    shutil.rmtree(PARSED_MDS, ignore_errors=True)
    shutil.rmtree(COPIES, ignore_errors=True)
    shutil.rmtree(IF_MANGLED_FILES, ignore_errors=True)

    # make the necessary directories
    if not os.path.exists(COPIES):
        os.mkdir(COPIES)

    if not os.path.exists(os.path.join(COPIES, LINUX_TUTORIAL)):
        os.mkdir(os.path.join(COPIES, LINUX_TUTORIAL))

    if not os.path.exists(PARSED_MDS):
        os.mkdir(PARSED_MDS)

    if not os.path.exists(IF_MANGLED_FILES):
        os.mkdir(IF_MANGLED_FILES)

    ################### define loop-invariant variables ###################

    # constant that keeps track of the source directories
    source_directories = [os.path.join(RETURN_DIR, RETURN_DIR, MKDOCS_DIR, DOCS_DIR, HPC_DIR),
                          os.path.join(RETURN_DIR, RETURN_DIR, MKDOCS_DIR, DOCS_DIR, HPC_DIR, LINUX_TUTORIAL)]

    # list of all the filenames
    filenames_generic = {}
    filenames_linux = {}
    for source_directory in source_directories:
        all_items = os.listdir(source_directory)
        files = [f for f in all_items if os.path.isfile(os.path.join(source_directory, f)) and ".md" in f[-3:]]
        for file in files:
            if LINUX_TUTORIAL in source_directory:
                filenames_linux[file] = os.path.join(source_directory, file)
            else:
                filenames_generic[file] = os.path.join(source_directory, file)

    # # Temporary variables to test with just one singular file
    # filenames_generic = {}
    # filenames_linux = {}
    # filenames_generic["account.md"] = "C:/HPC_werk/Documentation/local/vsc_user_docs/mkdocs/docs/HPC/account.md"
    # filenames_generic["example_text_1.md"] = "C:/HPC_werk/Documentation/local/vsc_user_docs/scripts/HPC_chatbot_preprocessor/tests/example_files/example_text_1.md"
    # filenames_linux["beyond_the_basics.md"] = "C:/HPC_werk/Documentation/local/vsc_user_docs/mkdocs/docs/HPC/linux-tutorial/beyond_the_basics.md"

    # for loops over all files
    for filenames in [filenames_generic, filenames_linux]:
        for filename in filenames.keys():
            ################### define/reset loop specific variables ###################

            # variable that keeps track of whether file is part of the linux tutorial
            is_linux_tutorial = bool(LINUX_TUTORIAL in filenames[filename])

            # make a copy of the original file in order to make sure the original does not get altered
            if is_linux_tutorial:
                copy_file = os.path.join(COPIES, LINUX_TUTORIAL,  filename)
            else:
                copy_file = os.path.join(COPIES, filename)
            shutil.copyfile(filenames[filename], copy_file)

            # variable that keeps track of the directories that are used to write in at different levels
            if is_linux_tutorial:
                root_dir_generic = os.path.join(PARSED_MDS, GENERIC_DIR, LINUX_TUTORIAL)
                root_dir_os_specific_linux = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, LINUX, LINUX_TUTORIAL)
                root_dir_os_specific_windows = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, WINDOWS, LINUX_TUTORIAL)
                root_dir_os_specific_macos = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, MACOS, LINUX_TUTORIAL)
            else:
                root_dir_generic = os.path.join(PARSED_MDS, GENERIC_DIR)
                root_dir_os_specific_linux = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, LINUX)
                root_dir_os_specific_windows = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, WINDOWS)
                root_dir_os_specific_macos = os.path.join(PARSED_MDS, OS_SPECIFIC_DIR, MACOS)

            # variable for the main title (needed for reference links)
            main_title = filename[:-3]

            # variable that keeps track of the directories that are used to write in at different levels
            curr_dirs = [filename[:-3] for _ in range(5)]

            # dictionary that keeps track of the paragraph numbers
            paragraph_numbers = {GENERIC: 1, LINUX: 1, WINDOWS: 1, MACOS: 1}

            ################### actually parse the md file ###################

            # create directories for the source markdown file
            for directory in [root_dir_generic, os.path.join(PARSED_MDS, OS_SPECIFIC_DIR), root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos, os.path.join(root_dir_generic, curr_dirs[0]), os.path.join(root_dir_os_specific_linux, curr_dirs[0]), os.path.join(root_dir_os_specific_windows, curr_dirs[0]), os.path.join(root_dir_os_specific_macos, curr_dirs[0])]:
                os.makedirs(directory, exist_ok=True)

            # process the jinja macros
            jinja_parser(filename, copy_file)

            # split the text in paragraphs
            paragraphs_os_text, paragraphs_os_free_text, paragraphs_metadata, subtitle_order = split_text(copy_file, main_title)

            # for every section, either make the whole section generic, or create an os-specific file for each OS
            for i, subtitle in enumerate(subtitle_order):

                # generic
                if subtitle in paragraphs_os_free_text.keys():
                    write_generic_file(subtitle, paragraphs_os_free_text, paragraphs_metadata, subtitle_order, i, paragraph_numbers)

                # os-specific
                else:
                    split_and_write_os_specific_section(paragraphs_os_text[subtitle], paragraphs_metadata[subtitle], subtitle_order, i, paragraph_numbers, paragraphs_metadata)

    # clean up temporary directories and files
    shutil.rmtree(COPIES, ignore_errors=True)
    shutil.rmtree(IF_MANGLED_FILES, ignore_errors=True)
    os.remove("jinja_file.txt")


################### run the script ###################
if __name__ == '__main__':
    print("WARNING: This script generates a file structure that contains rather long filepaths. Depending on where the script is ran, some of these paths might exceed the maximum length allowed by the system resulting in problems opening the files.")
    main()
    print("Parsing finished successfully")
