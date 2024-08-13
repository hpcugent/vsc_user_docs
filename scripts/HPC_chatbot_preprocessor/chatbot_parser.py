import os
import re
import shutil
import pypandoc
import yaml
from jinja2 import FileSystemLoader, Environment, ChoiceLoader

# variables for analytics
succeeded = 0
failed = 0

################### define global variables ###################

# variable that keeps track of the source directories
source_directories = [os.path.join("..", "..", "mkdocs", "docs", "HPC"), os.path.join("..", "..", "mkdocs", "docs", "HPC", "linux-tutorial")]

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

# some files are not written in proper markdown but rather in reST, they will be converted later down the line using pandoc
problem_files = ["getting_started.md", "navigating.md"]

# global variable to keep track of latest if-statement scope
is_os = 0  # Can be 0, 1, 2 or 3 {0: not in an os-if; 1: in a non-os-if nested in an os-if; 2: in an os-if; 3: in an os-if nested in an os-if}


################### define functions ###################
# function that removes the previous file structure before starting the process of making a new one
def remove_directory_tree(old_directory):
    if os.path.exists(old_directory):
        shutil.rmtree(old_directory)


# function that checks whether the current line has a title of level 4 at maximum (returns the level of the title or 0 if the line is not a title)
def check_for_title_logic(curr_line):
    global curr_dirs
    match = re.match(r'^#+ ', curr_line)
    if match and len(match.group(0)) <= 5:
        return len(match.group(0)) - 1
    else:
        return 0


# function that resets the contents of the link_lists
def reset_link_lists():
    global links_generic, links_linux, links_windows, links_macos
    links_generic = []
    links_linux = []
    links_windows = []
    links_macos = []


# function that uses the check_for_title_logic function to create the appropriate directories and update the necessary variables
def check_for_title(curr_line):
    global curr_dirs, last_title, in_code_block
    logic_output = check_for_title_logic(curr_line)
    if logic_output == 0 or in_code_block:
        return 0, None, None
    else:
        if last_title is not None:
            write_end_of_file(os.path.join(root_dir_generic, last_directory, last_title + ".txt"), "", links_generic, is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_linux, last_directory, last_title + ".txt"), "Linux",
                              links_linux, is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_windows, last_directory, last_title + ".txt"), "Windows",
                              links_windows, is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_macos, last_directory, last_title + ".txt"), "macOS",
                              links_macos, is_linux_tutorial)
            reset_link_lists()

        curr_dirs[logic_output] = os.path.join(curr_dirs[logic_output - 1], make_valid_title(curr_line[logic_output + 1:-1].replace(' ', '-')))

        create_directory(os.path.join(root_dir_generic,  curr_dirs[logic_output]))
        create_directory(os.path.join(root_dir_os_specific_linux,  curr_dirs[logic_output]))
        create_directory(os.path.join(root_dir_os_specific_windows,  curr_dirs[logic_output]))
        create_directory(os.path.join(root_dir_os_specific_macos,  curr_dirs[logic_output]))

        update_lower_curr_dir(curr_dirs[logic_output], logic_output)
        return logic_output, make_valid_title(curr_line[logic_output + 1:-1].replace(' ', '-')), curr_dirs[logic_output]


# function used to detect codeblocks and make sure the comments don't get detected as titles
def detect_in_code_block(curr_line):
    global in_code_block
    if '```' in curr_line or (('<pre><code>' in curr_line) ^ ('</code></pre>' in curr_line)):
        in_code_block = not in_code_block


# function that creates directories if needed
def create_directory(new_directory):
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)


# function that updates the curr_dir variables when needed
def update_lower_curr_dir(curr_directory, level):
    global curr_dirs
    for i in range(level + 1, 4):
        curr_dirs[i] = curr_directory


# function that replaces certain markdown structures with the equivalent used on the website
def replace_markdown_markers(curr_line, linklist):
    # replace links with a reference
    matches = re.findall(r'\[(.*?)]\((.*?)\)', curr_line)
    if matches:
        for match in matches:
            curr_line = curr_line.replace(f"[{match[0]}]({match[1]})", match[0] + "[" + str(len(linklist) + 1) + "]")
            linklist.append(match[1])

    # TODO: code-blocks
    # TODO: tips
    # TODO: warnings
    # etc

    return curr_line, linklist


# function that let's jinja do its thing to format the files expect for the os-related if-statements
def jinja_parser(filename, copy_location):

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


def mangle_os_ifs(line):
    global is_os

    match = re.search(r'\{%(.*?)%}(.*)', line)

    start_index = 0
    added_length = 0

    while match:

        constr_match = re.search(r'\{%.*?%}', match.string)
        if_match = re.search(r'if ', match.group(1))
        if_os_match = re.search(r'if OS == ', match.group(1))
        endif_match = re.search(r'endif', match.group(1))

        if endif_match:
            if is_os == 2:
                line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                               constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                     constr_match.end() + start_index + added_length - 1:]
                added_length += 8
                is_os = 0
            if is_os == 3:
                line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                               constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                     constr_match.end() + start_index + added_length - 1:]
                added_length += 8
                is_os = 2
            elif is_os == 1:
                is_os = 2
        elif if_match:
            if if_os_match:
                if is_os == 2:
                    line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                                   constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                         constr_match.end() + start_index + added_length - 1:]
                    added_length += 8
                    is_os = 3
                else:
                    line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                                   constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                         constr_match.end() + start_index + added_length - 1:]
                    added_length += 8
                    is_os = 2
            else:
                if is_os == 2:
                    is_os = 1
                else:
                    is_os = 0
        else:
            if is_os == 2 or is_os == 3:
                line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                               constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                     constr_match.end() + start_index + added_length - 1:]
                added_length += 8
        start_index += constr_match.end()
        match = re.search(r'\{%(.*?)%}(.*)', match.group(2))
    return line


def mangle_ifs(directory, file):
    with open(os.path.join("if_mangled_files",  file), 'w') as write_file:
        with open(directory, 'r') as read_file:
            for line in read_file:
                new_line = mangle_os_ifs(line)
                write_file.write(new_line)


# function that checks for if-statements
def check_if_statements(curr_line):
    # check whether the first part of the line contains information wrt if-statements
    match = re.search(r'^\{-if-%([^%]*)%-if-}(.*)', curr_line)

    # check whether the line contains information wrt if-statements that is not in its first part
    match_large = re.search(r'^(.*)(\{-if-%[^%]*%-if-})(.*)', curr_line)

    if match:
        content = match.group(1)

        # new if-statement wrt OS
        if re.search(r'if OS == ', content):
            OS = content[9:-1]

            # set new active OS
            active_OS_if_states[OS] = "active"

            # set other active ones on inactive
            for other_OS in active_OS_if_states.keys():
                if other_OS != OS and active_OS_if_states[other_OS] == "active":
                    active_OS_if_states[other_OS] = "inactive"

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


# function that writes a line to a file
def write_text_to_file(file_name, curr_line):
    global links_generic, links_linux, links_windows, links_macos
    with open(file_name, "a") as write_file:
        if "generic" in file_name:
            curr_line, links_generic = replace_markdown_markers(curr_line, links_generic)
        elif "linux" in file_name:
            curr_line, links_linux = replace_markdown_markers(curr_line, links_linux)
        elif "windows" in file_name:
            curr_line, links_windows = replace_markdown_markers(curr_line, links_windows)
        else:
            curr_line, links_macos = replace_markdown_markers(curr_line, links_macos)
        write_file.write(curr_line)


# function that decides what file to write text to
def choose_and_write_to_file(curr_line):
    # check that the line is part of the website for gent
    if active_OS_if_states["linux"] == "inactive" and active_OS_if_states["windows"] == "inactive" and \
            active_OS_if_states["macos"] == "inactive":
        write_text_to_file(os.path.join(root_dir_generic, last_directory, last_title + ".txt"), curr_line)
    if active_OS_if_states["linux"] == "active":
        write_text_to_file(os.path.join(root_dir_os_specific_linux, last_directory, last_title + ".txt"), curr_line)
    if active_OS_if_states["windows"] == "active":
        write_text_to_file(os.path.join(root_dir_os_specific_windows, last_directory, last_title + ".txt"), curr_line)
    if active_OS_if_states["macos"] == "active":
        write_text_to_file(os.path.join(root_dir_os_specific_macos, last_directory, last_title + ".txt"), curr_line)


# function that adds a reference link at the end of every txt file
def add_reference_link(file_location, reference_link):
    with open(file_location, 'a') as write_file:
        write_file.write("\nreference: " + reference_link + "\n")


# function that adds the links that should be at the end of a file
def write_end_of_file(file_location, OS, linklist, is_linux_tutorial_):
    if len(OS) > 0:
        OS = OS + "/"

    # add the links from within the document
    with open(file_location, 'a') as write_file:
        write_file.write("\n\n")
        for i, link in enumerate(linklist):
            write_file.write("[" + str(i + 1) + "]: " + str(link) + "\n")

    if is_linux_tutorial_:
        linux_part = "linux-tutorial/"
    else:
        linux_part = ""

    # finally add the reference link
    add_reference_link(file_location, "docs.hpc.ugent.be/" + OS + linux_part + main_title + "/#" + ''.join(char.lower() for char in last_title if char.isalnum() or char == '-').strip('-'))


# function that makes sure all titles can be used as valid filenames
def make_valid_title(s):
    # Define a regex pattern for invalid characters on both Windows and Linux
    invalid_chars = r'[<>:"/\\|?*\0()]'

    # get rid of extra information between {} brackets
    s = re.sub(r'\{.*?}', '', s)

    # Remove invalid characters
    valid_filename = re.sub(invalid_chars, '', s)

    # Strip leading/trailing whitespace
    valid_filename = valid_filename.strip().strip('-')

    return valid_filename


def main():
    global main_title, active_OS_if_states, last_directory, root_dir_generic, root_dir_os_specific_linux, root_dir_os_specific_windows, root_dir_os_specific_macos, is_linux_tutorial, in_code_block, last_title, curr_dirs, links_generic, links_linux, links_windows, links_macos
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

            # variable for the main title (needed for reference links)
            main_title = filename[:-3]

            # variable that keeps track of the directories that are used to write in at different levels
            curr_dirs = [filename[:-3] for i in range(5)]

            # variable to keep track whether we're dealing with OS-specific info or not
            OS_specific = False

            # variable that keeps track of the latest non-zero level title and corresponding directory
            last_title_level = 1
            last_title = None
            last_directory = None
            last_was_title = False

            # list to keep track of links in the text
            links_generic = []
            links_linux = []
            links_windows = []
            links_macos = []

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

            # convert the files without proper markdown layout into markdown using pandoc
            if "linux-tutorial" in filenames[filename] and filename in problem_files:
                pypandoc.convert_file(copy_file, 'markdown', outputfile=copy_file)

            # open the file and store line by line in the right file
            with open(copy_file, 'r') as readfile:

                for line in readfile:
                    title_level, title, directory = check_for_title(line)

                    detect_in_code_block(line)

                    # line is a title with a maximum depth of 4
                    if title_level > 0:
                        last_title_level = title_level
                        last_title = title
                        last_directory = directory
                        after_first_title = True

                    # line is not a title
                    elif after_first_title:
                        # check for if-statements and write the appropriate lines in the right files
                        next_action = check_if_statements(line)
                        while next_action[0] == "write_text_and_check_extra_message" or next_action[0] == "check_extra_message":
                            if next_action[0] == "write_text_and_check_extra_message":
                                choose_and_write_to_file(next_action[2])
                            next_action = check_if_statements(next_action[1])

                        if next_action[0] == "write_text":
                            choose_and_write_to_file(next_action[2])

            # write end of file for the last file
            write_end_of_file(os.path.join(root_dir_generic, last_directory, last_title + ".txt"), "", links_generic,
                              is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_linux, last_directory, last_title + ".txt"), "Linux",
                              links_linux, is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_windows, last_directory, last_title + ".txt"),
                              "Windows",
                              links_windows, is_linux_tutorial)
            write_end_of_file(os.path.join(root_dir_os_specific_macos, last_directory, last_title + ".txt"), "macOS",
                              links_macos, is_linux_tutorial)

    remove_directory_tree("copies")
    remove_directory_tree("if_mangled_files")


main()
# TODO: reconsider maximum depth to be detected as title (now at four)
# TODO: adapt script to be used from command line
