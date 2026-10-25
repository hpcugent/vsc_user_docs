#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Showcase interaction between user and the HPC
"""

import subprocess

COW = r'''
        \  ^__^
         \ (oo)\_______
           (__)\       )\/\
               ||----w |
               ||     ||
'''

def print_cowsay(cowsay):
    """Print a cow and let her say something"""
    indent: str = r'    ' # 4 spaces
    cowsay = f"< {cowsay} >"
    line: str = f"{indent}{'-' * len(cowsay)}"
    cowsay = f"{indent}{cowsay}\n"
    cowtxt = line + '\n' + cowsay + line + COW
    print(cowtxt)

# X-Message
CMD = 'xmessage -buttons yes:1,no:0 -center -timeout 60 " Do you want to see a cow? "'
ret: int = subprocess.call(CMD, shell=True)
if ret == 1:
    print_cowsay("Enjoy the day! Mooh")
else:
    print_cowsay("GET REAL! I am not a cow, I am a bunch of characters.")
