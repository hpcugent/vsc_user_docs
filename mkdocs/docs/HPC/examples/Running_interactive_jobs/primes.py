#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Print all primes between 1 and an upper limit, which is entered by the user.
"""

import datetime
import time
import sys


#  DATE
def print_time(text):
    """Print a string followed by timestamp"""
    now = time.time()
    st = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{text} {st}")
    return int(now)


def ask_int(prompt, retries=3):
    """Ask the user for a number"""
    while True:
        number = int(input(prompt))
        if number > 1:
            return number
        print("Please enter an number which is greater than one.")
        retries = retries - 1
        if retries <= 0:
            print("Too many attempts, try again later.")
            sys.exit()


# PRIMES
print("This program calculates all primes between 1 and your upper limit.")
num = ask_int("Enter your upper limit (>1): ")
start_time = print_time("Start Time: ")
print("[Prime#1] = 1")
ctr: int  = 1
for n in range(2, int(num)):
    for x in range(2, n // 2 + 1):
        if n % x == 0:
            break
    else:
        # loop fell through without finding a factor
        ctr += 1
        print(f"[Prime#{ctr}] = {n}")
end_time = print_time("End Time: ")
duration = end_time - start_time
print(f"Duration: {str(duration)} seconds.")
