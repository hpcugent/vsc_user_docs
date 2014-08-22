#! /usr/bin/env python
#
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Print all primes between 1 and an upper limit, which is entered by the user.
#
import datetime
import time
import sys

#  DATE
def print_time(str):
	now = time.time()
	st = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
	print str, st
	return int(now)

def ask_int(prompt, retries=3):
	while True:
		num = int(input(prompt))
		if num > 1:
			return num
		else:
			print "Please enter an integer which is bigger as one."
			retries = retries - 1
		if retries <= 0:
			print('Too many attempts, try again later.')
			sys.exit()

# PRIMES
print "This program calculates all primes between 1 and your upper limit."
num = ask_int('Enter your upper limit (>1): ')
start_time = print_time("Start Time: ")
print "[Prime#1] = 1"
ctr = 1
for n in range(2, int(num)):
	for x in range(2, n/2+1):
		if n % x == 0:
			break
	else:
		# loop fell through without finding a factor
		ctr += 1
		print "[Prime#%i] = %i" % (ctr,n)
end_time = print_time("End Time: ")
duration = end_time - start_time
s = "Duration:  " + str(duration) + " seconds."
print s
