#!/usr/bin/env python3
import sys
import re


in_prompt = False

with open(sys.argv[1]) as infile:
    for lineno, line in enumerate(infile.read().splitlines()):
        if '\\begin{prompt}' in line:
            in_prompt = True
        elif '\\end{prompt}' in line:
            in_prompt = False
        elif '%' in line and in_prompt:
            # Find latex commands between % %
            latex_interpreted = re.findall(r'%([^%]*)%', line)
            for match in latex_interpreted:
                # Find latex command not ending in {.
                result = re.search(r'\\[a-zA-Z]+($|[^a-zA-Z{])', match)
                if result is not None:
                    print(f'{sys.argv[1]} {lineno+1}: {line}')
                    break
