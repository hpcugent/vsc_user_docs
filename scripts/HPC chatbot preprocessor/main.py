import os
import re
import shutil

# test_number = int(input("Which test should be run?"))
#
# # Test for strip_markdown (somewhat successful, see findings file)
#
# if test_number == 1:
#     import strip_markdown
#
#     strip_markdown.strip_markdown_file("C:\\HPC werk\\Chatbot\\md_to_plaintext_test.md")
#
# # Test if copy of document doesn't change original document (successful)
# if test_number == 2:
#     import shutil
#
#     shutil.copyfile("C:\\HPC_werk\\Chatbot\\md_to_plaintext_test.txt",
#                     "C:\\HPC_werk\\Chatbot\\md_to_plaintext_test_copy.txt")
#     with open("C:\\HPC_werk\\Chatbot\\md_to_plaintext_test_copy.txt", 'w') as file:
#         file.write('hello')

# Test with actual document

# make a copy of one of the md files to test some things
shutil.copyfile("C:\\HPC_werk\\Documentation\\local\\vsc_user_docs\\mkdocs\\docs\\HPC\\getting_started.md",
                "C:\\HPC_werk\\Chatbot\\getting_started_copy.md")

################### define global variables ###################
# variable for the filename (which will be changed into something else in the final version)
filename = "getting_started_copy.md"

# variable for the main title (needed for reference links)
main_title = filename[:-3]

# variable that keeps track of the directories that are used to write in at different levels
root_dir_generic = "C:\\HPC_werk\\Chatbot\\parsed_mds\\generic\\"
root_dir_os_specific_linux = "C:\\HPC_werk\\Chatbot\\parsed_mds\\os_specific\\linux\\"
root_dir_os_specific_windows = "C:\\HPC_werk\\Chatbot\\parsed_mds\\os_specific\\windows\\"
root_dir_os_specific_macos = "C:\\HPC_werk\\Chatbot\\parsed_mds\\os_specific\\macos\\"
curr_dirs = [filename[:-3] for i in range(4)]

# variable to keep track whether we're dealing with OS-specific info or not
OS_specific = False

# pattern for the regex if-statement to filter out markdown titles
if_pattern = r'^#+ '

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

# dictionaries to keep track of current OS and location
active_OS_if_states = {"linux": "inactive", "windows": "inactive", "macos": "inactive"}
active_site_if_states = {"Gent": "inactive", "not-Gent": "inactive"}

# variable to keep track of the type of if-statement
if_type = "OS"

# variable to keep track of the macro-replacements at the top of markdown files
replacements = {}

# variable that is used to detect whether the first title has been encountered yet
after_first_title = False


################### define functions ###################

# function that removes the previous file structure before starting the process of making a new one
def remove_directory_tree(old_directory):
    if os.path.exists(old_directory):
        shutil.rmtree(old_directory)


# function that checks the first lines of a file until a title is found and saves the macro-replacements to the list
def save_replacements(curr_line):
    global replacements
    match = re.search(r'\{% set (.*?)="(.*?)" %}', curr_line)
    replacements[match.group(1)] = match.group(2)


# function that checks whether the current line has a title of level 3 at maximum (returns the level of the title or 0 if the line is not a title)
def check_for_title_logic(curr_line):
    global curr_dirs
    match = re.match(if_pattern, curr_line)
    if match and len(match.group(0)) <= 4:
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
    global curr_dirs, last_title
    logic_output = check_for_title_logic(curr_line)
    if logic_output == 0:
        return 0, None, None
    else:
        if last_title is not None:
            write_end_of_file(root_dir_generic + last_directory + "\\" + last_title + ".txt", "", links_generic)
            write_end_of_file(root_dir_os_specific_linux + last_directory + "\\" + last_title + ".txt", "Linux", links_linux)
            write_end_of_file(root_dir_os_specific_windows + last_directory + "\\" + last_title + ".txt", "Windows", links_windows)
            write_end_of_file(root_dir_os_specific_macos + last_directory + "\\" + last_title + ".txt", "macOS", links_macos)
            reset_link_lists()

        curr_dirs[logic_output] = curr_dirs[logic_output - 1] + "\\" + curr_line[logic_output + 1:-1].replace(' ', '-')

        create_directory(root_dir_generic + curr_dirs[logic_output])
        create_directory(root_dir_os_specific_linux + curr_dirs[logic_output])
        create_directory(root_dir_os_specific_windows + curr_dirs[logic_output])
        create_directory(root_dir_os_specific_macos + curr_dirs[logic_output])

        update_lower_curr_dir(curr_dirs[logic_output], logic_output)
        return logic_output, curr_line[logic_output + 1:-1].replace(' ', '-'), curr_dirs[logic_output]


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

    # replace {{hpcinfra}}
    curr_line = re.sub(r'\{\{\s*hpcinfra\s*}}', "HPC-UGent infrastructure", curr_line)

    # replace other replacement macros
    for macro in replacements.keys():
        curr_line = re.sub(r'\{\{\s*' + re.escape(macro) + r'\s*}}', replacements[macro], curr_line)

    # replace links with a reference
    matches = re.findall(r'\[(.*?)]\((.*?)\)', curr_line)
    if matches:
        for match in matches:
            print(f"[{match[0]}]({match[1]})")
            curr_line = curr_line.replace(f"[{match[0]}]({match[1]})", match[0] + "[" + str(len(linklist) + 1) + "]")
            linklist.append(match[1])

    return curr_line, linklist


# function that checks for if-statements
def check_if_statements(curr_line):
    global if_type

    # check whether the first part of the line contains information wrt if-statements
    match = re.search(r'^\{%-\s([^%]*)%}(.*)', curr_line)

    # check whether the line contains information wrt if-statements that is not in its first part
    match_large = re.search(r'^(.*)(\{%-\s[^%]*%})(.*)', curr_line)

    if match:
        print("################################################################################")
        content = match.group(1)
        print(content)

        # new if-statement wrt OS
        if re.match(r'if OS == ', content):
            OS = content[9:-1]

            # set new active OS
            active_OS_if_states[OS] = "active"

            # set other active ones on inactive
            for other_OS in active_OS_if_states.keys():
                if other_OS != OS and active_OS_if_states[other_OS] == "active":
                    active_OS_if_states[other_OS] = "inactive"

            if_type = "OS"

        # new if-statement wrt site
        elif re.match(r'if site == ', content):
            if re.search(r'(?i)gent', content):
                active_site_if_states["Gent"] = "active"
                active_site_if_states["not-Gent"] = "inactive"
            else:
                active_site_if_states["not-Gent"] = "active"
                if active_site_if_states["Gent"] == "active":
                    active_site_if_states["Gent"] = "inactive"
            if_type = "site"

        # endif statement wrt OS
        elif re.match(r'endif ', content) and if_type == "OS":
            if str(1) in active_OS_if_states.values():
                active_OS_if_states[list(active_OS_if_states.keys())[list(active_OS_if_states.values()).index(str(1))]] = "active"
            else:
                for key in active_OS_if_states.keys():
                    active_OS_if_states[key] = "inactive"

        # endif statement wrt site
        elif re.match(r'endif ', content) and if_type == "site":
            for key in active_site_if_states.keys():
                active_site_if_states[key] = "inactive"

        # else statement wrt OS
        elif re.match(r'else ', content) and if_type == "OS":

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

        # else statement wrt site
        elif re.match(r'else ', content) and if_type == "site":

            # change state of "Gent" and set not-Gent on active
            if active_site_if_states["Gent"] == "inactive":
                active_site_if_states["Gent"] = "active"
            elif active_site_if_states["Gent"] == "active":
                active_site_if_states["Gent"] = str(0)
            active_site_if_states["not-Gent"] = "active"

        print(active_OS_if_states)
        print(active_site_if_states)

        if len(match.group(2)) != 0:
            extra_message = match.group(2).lstrip()
            print(extra_message)
            # check_if_statements(extra_message)
            print("check_extra_message")
            return "check_extra_message", extra_message, None

        else:
            print("done")
            return "done", None, None

    elif match_large:
        print("################################################################################")
        print(active_OS_if_states)
        print(active_site_if_states)
        print(match_large.group(1))
        print(match_large.group(2))
        print("write_text_and_check_extra_message")
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
    if active_site_if_states["Gent"] == "active" or active_site_if_states["Gent"] == "inactive" and active_site_if_states["not-Gent"] == "inactive":
        if active_OS_if_states["linux"] == "inactive" and active_OS_if_states["windows"] == "inactive" and active_OS_if_states["macos"] == "inactive":
            write_text_to_file(root_dir_generic + last_directory + "\\" + last_title + ".txt", curr_line)
        if active_OS_if_states["linux"] == "active":
            write_text_to_file(root_dir_os_specific_linux + last_directory + "\\" + last_title + ".txt", curr_line)
        if active_OS_if_states["windows"] == "active":
            write_text_to_file(root_dir_os_specific_windows + last_directory + "\\" + last_title + ".txt", curr_line)
        if active_OS_if_states["macos"] == "active":
            write_text_to_file(root_dir_os_specific_macos + last_directory + "\\" + last_title + ".txt", curr_line)


# function that adds a reference link at the end of every txt file
def add_reference_link(file_location, reference_link):
    with open(file_location, 'a') as write_file:
        write_file.write("\nreference: " + reference_link + "\n")


# function that adds the links that should be at the end of a file
def write_end_of_file(file_location, OS, linklist):
    if len(OS) > 0:
        OS = OS + "/"

    # add the links from within the document
    with open(file_location, 'a') as write_file:
        for i, link in enumerate(linklist):
            write_file.write("[" + str(i + 1) + "]: " + str(link) + "\n")

    # finally add the reference link
    add_reference_link(file_location, "docs.hpc.ugent.be/" + OS + main_title + "/#" + last_title.lower())


################### actually parse the md file ###################

# remove the old directories if needed
remove_directory_tree(root_dir_generic)
remove_directory_tree(root_dir_os_specific_linux)
remove_directory_tree(root_dir_os_specific_windows)
remove_directory_tree(root_dir_os_specific_macos)

# create directories for the source markdown file
create_directory(root_dir_generic)
create_directory(root_dir_os_specific_linux)
create_directory(root_dir_os_specific_windows)
create_directory(root_dir_os_specific_macos)
create_directory(root_dir_generic + curr_dirs[0])
create_directory(root_dir_os_specific_linux + curr_dirs[0])
create_directory(root_dir_os_specific_windows + curr_dirs[0])
create_directory(root_dir_os_specific_macos + curr_dirs[0])

# open the file and store line by line in the right file
with open("C:\\HPC_werk\\Chatbot\\getting_started_copy.md", 'r') as readfile:

    for line in readfile:
        title_level, title, directory = check_for_title(line)

        # line is a title with a maximum depth of 3
        if title_level > 0:
            last_title_level = title_level
            last_title = title
            last_directory = directory
            after_first_title = True

        # line is not a title
        else:
            if after_first_title:
                # check for if-statements and write the appropriate lines in the right files
                next_action = check_if_statements(line)
                while next_action[0] == "write_text_and_check_extra_message" or next_action[0] == "check_extra_message":
                    if next_action[0] == "write_text_and_check_extra_message":
                        choose_and_write_to_file(next_action[2])
                    next_action = check_if_statements(next_action[1])

                if next_action[0] == "write_text":
                    choose_and_write_to_file(next_action[2])
            else:
                save_replacements(line)

# write end of file for the last file
write_end_of_file(root_dir_generic + last_directory + "\\" + last_title + ".txt", "", links_generic)
write_end_of_file(root_dir_os_specific_linux + last_directory + "\\" + last_title + ".txt", "Linux", links_linux)
write_end_of_file(root_dir_os_specific_windows + last_directory + "\\" + last_title + ".txt", "Windows", links_windows)
write_end_of_file(root_dir_os_specific_macos + last_directory + "\\" + last_title + ".txt", "macOS", links_macos)
