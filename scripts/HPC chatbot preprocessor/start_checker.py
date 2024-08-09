# THIS IS NOT AN IMPORTANT FILE, DON'T WORRY ABOUT IT, I JUST USED IT TO TEST SOME THINGS

import os

directory = "C:\\HPC_werk\\Documentation\\local\\vsc_user_docs\\mkdocs\\docs\\HPC"

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        # if filename.endswith("xdmod.md"):
        #     break
        if filename.endswith(".md"):
            lines_until_title = 0
            with open(directory + "\\" + filename, "r") as file:
                for line in file:
                    if line[0] == "#":
                        break
                    lines_until_title += 1
            print(filename + " : " + str(lines_until_title))
    break

directory = "C:\\HPC_werk\\Documentation\\local\\vsc_user_docs\\mkdocs\\docs\\HPC\\linux-tutorial"

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        # if filename.endswith("xdmod.md"):
        #     break
        if filename.endswith(".md"):
            lines_until_title = 0
            with open(directory + "\\" + filename, "r") as file:
                for line in file:
                    if line[0] == "#":
                        break
                    lines_until_title += 1
            print(filename + " : " + str(lines_until_title))
    break
