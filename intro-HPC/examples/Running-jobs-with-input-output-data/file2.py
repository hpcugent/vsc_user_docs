#! /usr/bin/env python
#
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Write a bigger file to SCRATCH directory
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

# Generate a file in the $VSC_SCRATCH directory
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
# repeat 30000 times
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

end_time = int(time.time())
duration = end_time - start_time
print "Duration = " + str(duration) + " seconds."

