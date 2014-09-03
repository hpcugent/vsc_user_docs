#
# Makefile for 
#

CC=gcc
CFLAGS=-g -O3
TARGET = mm mm1 test test1 test1_i1 test3 test3_i1 test6 test6_i1

%: %.c
	$(CC) $(CFLAGS) -o $@ $^

all: $(TARGET)

.PHONY: clean

clean:
	rm -f *.o $(TARGET)
	rm -r -f .perfexpert-temp*
	rm -r -f *.dSYM

