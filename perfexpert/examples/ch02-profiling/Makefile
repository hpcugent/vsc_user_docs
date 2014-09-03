#
# Makefile for 
#

CC=gcc
CFLAGS=-g -O3
TARGET = mm test1 test3 test5a test5b test6 

%: %.c
	$(CC) $(CFLAGS) -o $@ $^

all: $(TARGET)

test6: test6.c
	$(CC) $(CFLAGS) -lm -o $@ $^

.PHONY: clean

clean:
	rm -f *.o $(TARGET) 
	rm -r -f .perfexpert-temp*
	rm -r -f *.dSYM

