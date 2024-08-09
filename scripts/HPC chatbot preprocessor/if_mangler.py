import re
import os


def create_directory(new_directory):
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)

create_directory(".\\if_mangled_files")

# global variable to keep track of latest if-statement scope
is_os = False


def mangle_os_ifs(line):
    global is_os

    match = re.search(r'\{%-\s[^%]*%}', line)
    if_match = re.search(r'\{%-\sif [^%]*%}', line)
    if_os_match = re.search(r'\{%-\sif OS == [^%]*%}', line)

    if match:
        if if_match:
            if if_os_match:
                is_os = True
                line = line[:match.start() + 1] + "-if-" + line[match.start() + 1:match.end() - 1] + "-if-" + line[match.end() - 1:]
            else:
                is_os = False
        else:
            if is_os:
                line = line[:match.start() + 1] + "-if-" + line[match.start() + 1:match.end() - 1] + "-if-" + line[match.end() - 1:]

    match = re.search(r'\{%-\s[^%]*%}', line)

    while match and is_os:
        line = line[:match.start() + 1] + "-if-" + line[match.start() + 1:match.end() - 1] + "-if-" + line[match.end() - 1:]
        match = re.search(r'\{%-\s[^%]*%}', line)

    return line


def mangle_ifs(directory, file):
    with open(".\\if_mangled_files\\" + file, 'w') as write_file:
        with open(directory + "\\" + file, 'r') as read_file:
            for line in read_file:
                new_line = mangle_os_ifs(line)
                write_file.write(new_line)
