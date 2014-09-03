#
# Makefile for 
#

CC=gcc
CFLAGS=-g
DEPS = compute1.h compute2.h compute3.h
OBJ = main.o compute1.o compute2.o compute3.o
TARGET=main mm mm_omp

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c -o $@ $< 

all: $(TARGET)

mm: mm.c
	$(CC) $(CFLAGS) -o $@ $< 

mm_omp: mm_omp.c
	$(CC) $(CFLAGS) -fopenmp -o mm_omp mm_omp.c

main: $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean

clean:
	rm -f *.o $(TARGET) mm mm_omp 
	rm -r -f .perfexpert-temp*

