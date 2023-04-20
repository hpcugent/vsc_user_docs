#! /usr/bin/env python
#
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Showcase interaction between user and the HPC
#
import subprocess
import sys

def print_cowsay(cowsay):
	lne0 = 4+len(cowsay)
	line0 = "  "
	line0 = line0+"-"*lne0
	lne = 4+len(cowsay)
	line = "-"*lne
	cowtxt= line0+"\n\
  < "+cowsay+" > \n\
  "+line+" \n\
           \   ^__^ \n\
           \  (oo)\_______ \n\
              (__)\       )\/\ \n\
                   ||----w | \n\
                   ||     ||\
                            "
	print cowtxt

# X-Message
cmd = "xmessage -buttons yes:1,no:0 -center -timeout 60 \" Do you want to see a cow? \""
ret = subprocess.call(cmd, shell=True)
if ret == 1:
  print_cowsay("Enjoy the day! Mooh")
else:
  print_cowsay("GET REAL! I am not a cow, I am a bunch of characters.")
