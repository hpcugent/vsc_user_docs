import re

# global variable to keep track of latest if-statement scope
is_os = 0 # Can be 0, 1 or 2 {0: not in an os-if; 1: in a non-os-if nested in an os-if; 2: in an os-if}


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
            elif is_os == 1:
                is_os = 2
        elif if_match:
            if if_os_match:
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
            if is_os == 2:
                line = line[:constr_match.start() + start_index + added_length + 1] + "-if-" + line[
                                                                                               constr_match.start() + start_index + added_length + 1:constr_match.end() + start_index + added_length - 1] + "-if-" + line[
                                                                                                                                                                                                                     constr_match.end() + start_index + added_length - 1:]
                added_length += 8
        start_index += constr_match.end()
        match = re.search(r'\{%(.*?)%}(.*)', match.group(2))
    return line


def mangle_ifs(directory, file):
    with open(".\\if_mangled_files\\" + file, 'w') as write_file:
        with open(directory + "\\" + file, 'r') as read_file:
            for line in read_file:
                new_line = mangle_os_ifs(line)
                write_file.write(new_line)
