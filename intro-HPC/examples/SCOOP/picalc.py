from math import hypot
from random import random
from scoop import futures

NAME = 'SCOOP_piCalc'

# A range is used in this function for python3. If you are using python2,
# an xrange might be more efficient.
try:
    range_fn = xrange
except:
    range_fn = range


def test(tries):
    return sum(hypot(random(), random()) < 1 for i in range_fn(tries))

# Calculates pi with a Monte-Carlo method. This function calls the function
# test "n" times with an argument of "t". Scoop dispatches these
# functions interactively accross the available resources.
def calcPi(workers, tries):
    expr = futures.map(test, [tries] * workers)
    piValue = 4. * sum(expr) / float(workers * tries)
    return piValue


if __name__ == '__main__':
    import sys
    nr_batches = 3000
    batch_size = 5000

    # Program name and two arguments
    if len(sys.argv) == 3:
        try:
            nr_batches = int(sys.argv[1])
            batch_size = int(sys.argv[2])
        except ValueError as ex:
            sys.stderr.write("ERROR: Two integers expected as arguments: %s\n" % ex)
            sys.exit(1)
    elif len(sys.argv) != 1:
        sys.stderr.write("ERROR: Expects either zero or two integers as arguments.\n")
        sys.exit(1)

    print("PI=%f (in nr_batches=%d,batch_size=%d)" % (calcPi(nr_batches, batch_size), nr_batches, batch_size))
