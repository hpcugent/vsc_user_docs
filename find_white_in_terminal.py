#!/usr/bin/env python3
import sys
import re

# Whitelisted '\the' because it's a TeX primitive that doesn't accept {}
whitelist = {'the'}

in_prompt = False

if len(sys.argv) != 2:
    sys.stderr.write("ERROR: Usage %s <path to .tex file>\n", sys.argv[0])
    sys.exit(1)

tex_file = sys.argv[1]

with open(tex_file) as infile:
    for lineno, line in enumerate(infile.read().splitlines()):
        if '\\begin{prompt}' in line:
            in_prompt = True
        if '%' in line and in_prompt:
            # Find content between % %
            latex_interpreted = re.findall(r'%([^%]*)%', line)
            for match in latex_interpreted:
                # Find latex command not ending in {}.
                # Uses a negative lookahead (?!...) to assert that the latex
                #  command doesn't end in a letter or {}
                for latex_command in re.finditer(r'\\(\w+)(?![\w{])', match):
                    # Check if we found a latex command not ending in {}
                    # Allow, since \_ doesn't allow arguments
                    if not latex_command.group(1).startswith('_') and latex_command.group(1) not in whitelist:
                        print("%s line %d: %s" % (tex_file, lineno + 1, latex_command.group(1)))
        if '\\end{prompt}' in line:
            in_prompt = False
