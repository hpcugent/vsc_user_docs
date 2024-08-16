import json
import os
import re
import shutil
import yaml
from itertools import chain
from jinja2 import FileSystemLoader, Environment, ChoiceLoader


################### define functions ###################
def remove_directory_tree(old_directory):
    """
    function that removes a full directory tree

    :param old_directory: the directory to be removed
    :return:
    """
    if os.path.exists(old_directory):
        shutil.rmtree(old_directory)


def check_for_title(curr_line, main_title, last_directory, last_title, curr_dirs, root_dirs, link_lists, is_linux_tutorial_, in_code_block_):
    """
    function that uses the check_for_title_logic function to create the appropriate directories and update the necessary variables

    :param curr_line: the line to be checked for a title
    :param main_title: the main title of the file, needed in the case where a file is finished
    :param last_directory: the most recently encountered directory
    :param last_title: the most recently encountered title
    :param curr_dirs: the most recent directories at each title level
    :param root_dirs: a list containing the root directories
    :param link_lists: a list containing all four link_lists with the links that will be printed at the bottom of a file
    :param is_linux_tutorial_: boolean to indicate whether the current file is part of the linux tutorial
    :param in_code_block_: boolean to indicate whether the current line is part of a codeblock
    :return: the depth of the title
    :return: the title found in the line if any
    :return: the new directory in which the next file will be written
    :return link_lists: updated link_lists
    """

    # detect titles
    match = re.match(r'^#+ ', curr_line)
    if match and len(match.group(0)) <= 5:
        logic_output = len(match.group(0)) - 1
    else:
        logic_output = 0

    # make necessary changes if a title has been detected
    if logic_output == 0 or in_code_block_:
        return 0, None, None, curr_dirs, link_lists
    else:

        # if a new title is detected, write the end of the previous file
        if last_title is not None:
            for i, OS in enumerate(["", "Linux", "Windows", "macOS"]):
                write_end_of_file(os.path.join(root_dirs[i], last_directory, last_title + ".json"), OS, link_lists[i], is_linux_tutorial_, main_title, last_title)

            # reset the link lists for each OS
            for i in range(4):
                link_lists[i] = []

        # make a new directory corresponding with the new title
        curr_dirs[logic_output] = os.path.join(curr_dirs[logic_output - 1], make_valid_title(curr_line[logic_output + 1:-1].replace(' ', '-')))

        for i in range(4):
            create_directory(os.path.join(root_dirs[i],  curr_dirs[logic_output]))

        # update the higher order current directories
        for i in range(logic_output + 1, 4):
            curr_dirs[i] = curr_dirs[logic_output]

        return logic_output, make_valid_title(curr_line[logic_output + 1:-1].replace(' ', '-')), curr_dirs[logic_output], curr_dirs, link_lists


def create_directory(new_directory):
    """
    function that creates new directories

    :param new_directory: directory to be created
    :return:
    """
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)


def replace_markdown_markers(curr_line, linklist, in_code_block):
    """
    function that replaces certain markdown structures with the equivalent used on the website

    :param curr_line: the current line on which markdown structures need to be replaced
    :param linklist: the list used to store links that need to be printed at the end of the file
    :param in_code_block: boolean indicating whether the current line is part of a code block
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
            curr_line = curr_line.replace(f"[{match[0]}]({match[1]})", match[0] + "[" + str(len(linklist) + 1) + "]")
            linklist.append(match[1])

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
                # print("<" + content + ">")
                pass

    # structures with !!! (info, tips, warnings)
    if '!!!' in curr_line:
        curr_line = re.sub(r'!!!', "", curr_line)

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


def jinja_parser(filename, copy_location):
    """
    function that let's jinja do its thing to format the files except for the os-related if-statements

    :param filename: the name of the file that needs to be formatted using jinja
    :param copy_location: the location of the file that needs to be formatted using jinja
    :return:
    """
    # YAML file location
    yml_file_path = os.path.join('..', '..', 'mkdocs', 'extra', 'gent.yml')

    # Read the YAML file
    with open(yml_file_path, 'r') as yml_file:
        words_dict = yaml.safe_load(yml_file)

    # ugly fix for index.md error
    additional_context = {
        'config': {
            'repo_url': 'https://github.com/hpcugent/vsc_user_docs'
        }
    }
    combined_context = {**words_dict, **additional_context}

    # Mangle the OS-related if-statements
    mangle_ifs(copy_location, filename)

    # Use Jinja2 to replace the macros
    template_loader = ChoiceLoader([FileSystemLoader(searchpath='if_mangled_files'), FileSystemLoader(searchpath=os.path.join("..", "..", "mkdocs", "docs", "HPC"))])
    templateEnv = Environment(loader=template_loader)
    template = templateEnv.get_template(filename)
    rendered_content = template.render(combined_context)

    # Save the rendered content to a new file
    with open(copy_location, 'w', encoding='utf-8', errors='ignore') as output_file:
        output_file.write(rendered_content)


def mangle_os_ifs(line, is_os):
    """
    function that mangles the os-related if-statements. This is needed because we want to keep these if-statements intact after jinja-parsing to build the directory structure.
    We don't want to mangle all if-related statements (such as else and endif) so we need to keep track of the context of the last few if-statements.

    :param line: the current line to check for os-related if-statements
    :param is_os: boolean keep track of the current os-state of the if-statements. Can be 0, 1, 2 or 3 {0: not in an os-if; 1: in a non-os-if nested in an os-if; 2: in an os-if; 3: in an os-if nested in an os-if}
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
        pos_first_mangle = constr_match.start() + start_index + added_length + 1
        pos_second_mangle = constr_match.end() + start_index + added_length - 1

        # this logic isn't flawless, there are number of nested if-constructions that are technically possible that would break this logic, but these don't appear in the documentation as it doesn't make sense to have these
        if endif_match:
            if is_os == 2 or is_os == 3:
                line = line[:pos_first_mangle] + "-if-" + line[pos_first_mangle:pos_second_mangle] + "-if-" + line[pos_second_mangle:]
                added_length += 8
                if is_os == 2:
                    is_os = 0
                elif is_os == 3:
                    is_os = 2
            elif is_os == 1:
                is_os = 2
        elif if_match:
            if if_os_match:
                line = line[:pos_first_mangle] + "-if-" + line[pos_first_mangle:pos_second_mangle] + "-if-" + line[pos_second_mangle:]
                added_length += 8
                if is_os == 2:
                    is_os = 3
                else:
                    is_os = 2
            else:
                if is_os == 2:
                    is_os = 1
                else:
                    is_os = 0
        else:
            if is_os == 2 or is_os == 3:
                line = line[:pos_first_mangle] + "-if-" + line[pos_first_mangle:pos_second_mangle] + "-if-" + line[pos_second_mangle:]
                added_length += 8

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
    is_os = 0  # Can be 0, 1, 2 or 3 {0: not in an os-if; 1: in a non-os-if nested in an os-if; 2: in an os-if; 3: in an os-if nested in an os-if}

    with open(os.path.join("if_mangled_files",  filename), 'w') as write_file:
        with open(directory, 'r') as read_file:
            for line in read_file:
                new_line, is_os = mangle_os_ifs(line, is_os)
                write_file.write(new_line)


def check_if_statements(curr_line, active_OS_if_states):
    """
    function that checks for if-statements

    :param curr_line: the line to be checked for if-statements to build the directory structure
    :param active_OS_if_states: dictionary keeping track of the active OS states according to the if-statements
    :return: the next action to be done with the line:
                "done": An if-statement has been found at the start of the line, the active os list has been updated, processing of the current line is finished and a following line can be processed.
                "check_extra_message": An if-statement has been found at the start of the line, the active os list has been updated, more text has been detected after the if-statement that also needs to be checked.
                "write_text": No if-statement has been found, write the current line to a file (can also be part of the current line)
                "write_text_and_check_extra_message": An if statement has been found not at the start of the line. Firstly, write the text up until the if-statement to a file, then check the rest of the line.
    :return: the extra message to be checked, if any
    :return: the text to be written to the file, if any
    """
    # check whether the first part of the line contains information wrt if-statements
    match = re.search(r'^\{-if-%(.*?)%-if-}(.*)', curr_line)

    # check whether the line contains information wrt if-statements that is not in its first part
    match_large = re.search(r'^(.*)(\{-if-%.*?%-if-})(.*)', curr_line)

    if match:
        content = match.group(1)

        # new if-statement wrt OS with '=='
        if re.search(r'if OS == ', content):
            OS = content.split()[-1]

            # set new active OS
            active_OS_if_states[OS] = "active"

            # set other active ones on inactive
            for other_OS in active_OS_if_states.keys():
                if other_OS != OS and active_OS_if_states[other_OS] == "active":
                    active_OS_if_states[other_OS] = "inactive"

        # new if-statement wrt OS with '!='
        elif re.search(r'if OS != ', content):
            OS = content.split()[-1]

            # set new active OS
            active_OS_if_states[OS] = "inactive"

            # set other inactive ones on active
            for other_OS in active_OS_if_states.keys():
                if other_OS != OS and active_OS_if_states[other_OS] == "inactive":
                    active_OS_if_states[other_OS] = "active"

        # endif statement wrt OS
        elif re.search(r'endif', content):
            if str(1) in active_OS_if_states.values():
                active_OS_if_states[
                    list(active_OS_if_states.keys())[list(active_OS_if_states.values()).index(str(1))]] = "active"
            else:
                for key in active_OS_if_states.keys():
                    active_OS_if_states[key] = "inactive"

        # else statement wrt OS
        elif re.search(r'else', content):

            i = 0
            for i in range(3):
                if str(i) not in active_OS_if_states.values():
                    break

            # set the previously active one on inactive until the next endif
            key_list = list(active_OS_if_states.keys())
            position = list(active_OS_if_states.values()).index("active")
            active_OS_if_states[key_list[position]] = str(i)

            # set inactive ones on active
            while "inactive" in active_OS_if_states.values():
                position = list(active_OS_if_states.values()).index("inactive")
                active_OS_if_states[key_list[position]] = "active"

        if len(match.group(2)) != 0:
            extra_message = match.group(2).lstrip()
            return "check_extra_message", extra_message, None

        else:
            return "done", None, None

    elif match_large:
        return "write_text_and_check_extra_message", match_large.group(2), match_large.group(1)

    else:
        return "write_text", None, curr_line


def write_text_to_file(file_name, curr_line, link_lists, in_code_block):
    """
    function that writes a line to a file

    :param file_name: target file to write the line to
    :param curr_line: line to be written to the file
    :param link_lists: list containing all the links that will be printed at the end of files
    :param in_code_block: boolean indicating whether the current line is in a codeblock
    :return link_lists: updated link_lists
    """

    if os.path.exists(file_name) or curr_line.strip():
        if os.path.exists(file_name):
            with open(file_name, "r") as read_file:
                data = json.load(read_file)
        else:
            data = {}

        if "generic" in file_name:
            curr_line, link_lists[0] = replace_markdown_markers(curr_line, link_lists[0], in_code_block)
        elif "linux" in file_name:
            curr_line, link_lists[1] = replace_markdown_markers(curr_line, link_lists[1], in_code_block)
        elif "windows" in file_name:
            curr_line, link_lists[2] = replace_markdown_markers(curr_line, link_lists[2], in_code_block)
        else:
            curr_line, link_lists[3] = replace_markdown_markers(curr_line, link_lists[3], in_code_block)

        if 'content' in data:
            data['content'] += curr_line
        else:
            data['content'] = curr_line

        with open(file_name, "w") as write_file:
            json.dump(data, write_file, indent=4)

    return link_lists


def choose_and_write_to_file(curr_line, active_OS_if_states, last_directory, last_title, root_dirs, link_lists, in_code_block):
    """
    function that decides what file to write text to

    :param curr_line: line to be written to a file
    :param active_OS_if_states: dictionary keeping track of which OSes are active according to the if-statements
    :param last_directory: most recently made directory
    :param last_title: the most recently encountered title
    :param root_dirs: a list with all root directories
    :param link_lists: list of links that need to be written at the end of the files
    :param in_code_block: boolean indicating whether the current line is in a code block
    :return link_lists: an updated link_lists
    """
    # check that the line is part of the website for gent
    if active_OS_if_states["linux"] == "inactive" and active_OS_if_states["windows"] == "inactive" and active_OS_if_states["macos"] == "inactive":
        link_lists = write_text_to_file(os.path.join(root_dirs[0], last_directory, last_title + ".json"), curr_line, link_lists, in_code_block)
    if active_OS_if_states["linux"] == "active":
        link_lists = write_text_to_file(os.path.join(root_dirs[1], last_directory, last_title + ".json"), curr_line, link_lists, in_code_block)
    if active_OS_if_states["windows"] == "active":
        link_lists = write_text_to_file(os.path.join(root_dirs[2], last_directory, last_title + ".json"), curr_line, link_lists, in_code_block)
    if active_OS_if_states["macos"] == "active":
        link_lists = write_text_to_file(os.path.join(root_dirs[3], last_directory, last_title + ".json"), curr_line, link_lists, in_code_block)

    return link_lists


def write_end_of_file(file_location, OS, linklist, is_linux_tutorial_, main_title, last_title):
    """
    function that adds the links that should be at the end of a file

    :param file_location: the location of the file
    :param OS: the OS of the file
    :param linklist: the links that should be at the end of the file
    :param is_linux_tutorial_: boolean indicating whether the file is part of the linux tutorial
    :param main_title: the main title of the file, to be used in the reference link
    :param last_title: the most recently encountered title
    :return:
    """

    if os.path.exists(file_location):

        if len(OS) > 0:
            OS = OS + "/"

        with open(file_location, "r") as read_file:
            data = json.load(read_file)

        # add the links from within the document
        data['links'] = {}
        for i, link in enumerate(linklist):
            data['links'][str(i + 1)] = str(link)

        if is_linux_tutorial_:
            linux_part = "linux-tutorial/"
        else:
            linux_part = ""

        # add the reference link
        data['reference_link'] = ("docs.hpc.ugent.be/" + OS + linux_part + main_title + "/#" + ''.join(char.lower() for char in last_title if char.isalnum() or char == '-').strip('-'))

        with open(file_location, 'w') as write_file:
            json.dump(data, write_file, indent=4)


def make_valid_title(title):
    """
    function that makes sure all titles can be used as valid filenames

    :param title: the string that will be used as title and filename
    :return valid_filename: the adapted title that can be used as filename
    """
    # Define a regex pattern for invalid characters on both Windows and Linux
    invalid_chars = r'[<>:"/\\|?*\0()]'

    # get rid of extra information between {} brackets
    title = re.sub(r'\{.*?}', '', title)

    # Remove invalid characters
    valid_filename = re.sub(invalid_chars, '', title)

    # Strip leading/trailing whitespace
    valid_filename = valid_filename.strip().strip('-')

    return valid_filename


def main():
    """
    main function
    :return:
    """
    # remove the directories from a previous run of the parser if they weren't cleaned up properly for some reason
    remove_directory_tree("parsed_mds")
    remove_directory_tree("copies")
    remove_directory_tree("if_mangled_files")

    # make the necessary directories
    if not os.path.exists("copies"):
        os.mkdir("copies")

    if not os.path.exists(os.path.join("copies", "linux")):
        os.mkdir(os.path.join("copies", "linux"))

    if not os.path.exists("parsed_mds"):
        os.mkdir("parsed_mds")

    if not os.path.exists("if_mangled_files"):
        os.mkdir("if_mangled_files")

    ################### define loop-invariant variables ###################

    # variable that keeps track of the source directories
    source_directories = [os.path.join("..", "..", "mkdocs", "docs", "HPC"),
                          os.path.join("..", "..", "mkdocs", "docs", "HPC", "linux-tutorial")]

    # list of all the filenames
    filenames_generic = {}
    filenames_linux = {}
    for source_directory in source_directories:
        all_items = os.listdir(source_directory)
        files = [f for f in all_items if os.path.isfile(os.path.join(source_directory, f)) and ".md" in f[-3:]]
        for file in files:
            if "linux-tutorial" in source_directory:
                filenames_linux[file] = os.path.join(source_directory, file)
            else:
                filenames_generic[file] = os.path.join(source_directory, file)

    # for loops over all files
    for filenames in [filenames_generic, filenames_linux]:
        for filename in filenames.keys():
            ################### define/reset loop specific variables ###################

            # variable that keeps track of whether file is part of the linux tutorial
            is_linux_tutorial = bool("linux-tutorial" in filenames[filename])

            # make a copy of the original file in order to make sure the original does not get altered
            if is_linux_tutorial:
                copy_file = os.path.join("copies", "linux",  filename)
            else:
                copy_file = os.path.join("copies", filename)
            shutil.copyfile(filenames[filename], copy_file)

            # variable that keeps track of the directories that are used to write in at different levels
            if is_linux_tutorial:
                root_dir_generic = os.path.join("parsed_mds", "generic", "linux_tutorial")
                root_dir_os_specific_linux = os.path.join("parsed_mds", "os_specific", "linux", "linux_tutorial")
                root_dir_os_specific_windows = os.path.join("parsed_mds", "os_specific", "windows", "linux_tutorial")
                root_dir_os_specific_macos = os.path.join("parsed_mds", "os_specific", "macos", "linux_tutorial")
            else:
                root_dir_generic = os.path.join("parsed_mds", "generic")
                root_dir_os_specific_linux = os.path.join("parsed_mds", "os_specific", "linux")
                root_dir_os_specific_windows = os.path.join("parsed_mds", "os_specific", "windows")
                root_dir_os_specific_macos = os.path.join("parsed_mds", "os_specific", "macos")
            root_dirs = [root_dir_generic, root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos]

            # variable for the main title (needed for reference links)
            main_title = filename[:-3]

            # variable that keeps track of the directories that are used to write in at different levels
            curr_dirs = [filename[:-3] for _ in range(5)]

            # variable that keeps track of the latest non-zero level title and corresponding directory
            last_title = None
            last_directory = None

            # list to keep track of links in the text
            links_generic = []
            links_linux = []
            links_windows = []
            links_macos = []
            link_lists = [links_generic, links_linux, links_windows, links_macos]

            # dictionaries to keep track of current OS
            active_OS_if_states = {"linux": "inactive", "windows": "inactive", "macos": "inactive"}

            # variable that shows whether the first title has been reached yet
            after_first_title = False

            # variable that is used to be sure that we are detecting titles and not comments from codeblocks
            in_code_block = False

            ################### actually parse the md file ###################

            # create directories for the source markdown file
            create_directory(root_dir_generic)
            create_directory(os.path.join("parsed_mds", "os_specific"))
            create_directory(root_dir_os_specific_linux)
            create_directory(root_dir_os_specific_windows)
            create_directory(root_dir_os_specific_macos)
            create_directory(os.path.join(root_dir_generic, curr_dirs[0]))
            create_directory(os.path.join(root_dir_os_specific_linux, curr_dirs[0]))
            create_directory(os.path.join(root_dir_os_specific_windows, curr_dirs[0]))
            create_directory(os.path.join(root_dir_os_specific_macos, curr_dirs[0]))

            # process the jinja macros
            jinja_parser(filename, copy_file)

            # open the file and store line by line in the right file
            with open(copy_file, 'r') as readfile:

                for line in readfile:
                    title_level, title, directory, curr_dirs, link_lists = check_for_title(line, main_title, last_directory, last_title, curr_dirs, [root_dir_generic, root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos], link_lists, is_linux_tutorial, in_code_block)

                    # detect codeblocks to make sure titles aren't detected in them
                    if '```' in line or (('<pre><code>' in line) ^ ('</code></pre>' in line)):
                        in_code_block = not in_code_block

                    # line is a title with a maximum depth of 4
                    if title_level > 0:
                        last_title = title
                        last_directory = directory
                        after_first_title = True

                    # line is not a title
                    elif after_first_title:
                        # check for if-statements and write the appropriate lines in the right files
                        next_action = check_if_statements(line, active_OS_if_states)
                        while next_action[0] == "write_text_and_check_extra_message" or next_action[0] == "check_extra_message":
                            if next_action[0] == "write_text_and_check_extra_message":
                                link_lists = choose_and_write_to_file(next_action[2], active_OS_if_states, last_directory, last_title, [root_dir_generic, root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos], link_lists, in_code_block)
                            next_action = check_if_statements(next_action[1], active_OS_if_states)

                        if next_action[0] == "write_text":
                            link_lists = choose_and_write_to_file(next_action[2], active_OS_if_states, last_directory, last_title, [root_dir_generic, root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos], link_lists, in_code_block)

            # write end of file for the last file
            for i, OS in enumerate(["", "Linux", "Windows", "macOS"]):
                write_end_of_file(os.path.join(root_dirs[i], last_directory, last_title + ".json"), OS, link_lists[i], is_linux_tutorial, main_title, last_title)

    # remove_directory_tree("copies")
    # remove_directory_tree("if_mangled_files")


print("WARNING: This script generates a file structure that contains rather long filepaths. Depending on where the script is ran, some of these paths might exceed the maximum length allowed by the system resulting in problems opening the files.")
main()
print("Parsing finished successfully")
