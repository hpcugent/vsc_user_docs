#! /usr/bin/env python
#
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Example showing a write (step#1) and subsequent read (=step#2) operation in the SCRATCH directory
#
import sys
import random
import datetime
import time
import os

start_time = int(time.time())

# PRIMES
def primes(top):
	result = []
	for n in range(2, top):
		for x in range(2, n/2+1):
			if n % x == 0:
				break
		else:
			# loop fell through without finding a factor
			result.append(n)
	return result

# Step #1: Generate a file in the $VSC_SCRATCH directory
#   in order to generate CPU- and disk-IO load, we will
#   1) take a random integer between 1 and 2000
#      and calculate all primes up to that limit
#   2) and repeat this action 30000 times
#   3) and write it to the "primes_1.txt" output file in the SCRATCH-directory
#
scratch_dir = os.environ.get('VSC_SCRATCH')
filename_p1 = scratch_dir + "/primes_1.txt"
print "Output File: ", filename_p1
f_out = open(filename_p1, 'w+')
for i in range(1, 30000):
	# We take a random integer between 1 and 2000
	top = random.randrange(2000)
	# and we calculate all primes up to that limit
	l = primes(top)
	f_out.write('TOP=')
	f_out.write(str(top))
	f_out.write(': ')
	f_out.write(str(l))
	f_out.write('\n')
f_out.close()

# Step #2: Open the previously generated file ("primes_1.txt") again and
#      1) read it line by line
#      2) and calculate the average of primes in the line
#      3) and count the number of primes found
#      4) and write it to the "primes_2.txt" output file in the SCRATCH-directory
filename_p1 = scratch_dir + "/primes_1.txt"
filename_p2 = scratch_dir + "/primes_2.txt"
f_in=open(filename_p1, "r")
f_out=open(filename_p2, "w")
print "Input File: ", filename_p1
print "Output File: ", filename_p2
in_lines=f_in.readlines()          					  #reads it line by line
for line in in_lines:
	delim = line.find("[")
	s = line[delim+1:]
	s = s.replace(']', '')
	list_values=s.split(',')
	tot = 0
	num_primes = len(list_values)
	for i in range(num_primes):
		tot += int(list_values[i])
	avg = tot / num_primes
	f_out.write(line[0:delim])
	f_out.write("#primes=[" + str(num_primes) + "]")
	f_out.write(", AVG=[" + str(avg) + "]\n")
	f_out.write(line)
f_in.close()                        #closes the file
f_out.close()

end_time = int(time.time())
duration = end_time - start_time
print "Duration = " + str(duration) + " seconds."

