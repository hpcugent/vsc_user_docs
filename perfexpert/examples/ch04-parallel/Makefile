#
# Makefile for 
#

CC=gcc
CFLAGS=-g 
TARGET = mm mm_omp mm_mpi mm_mpi_omp

%: %.c
	$(CC) $(CFLAGS) -o $@ $^

all: $(TARGET)

mm_omp: mm_omp.c
	$(CC) -fopenmp $(CFLAGS) -o mm_omp mm_omp.c 

mm_mpi: mm_mpi.c
	mpicc -o mm_mpi mm_mpi.c

mm_mpi_omp: mm_mpi_omp.c
	mpicc -fopenmp -o mm_mpi_omp mm_mpi_omp.c

.PHONY: clean

clean:
	rm -f *.o $(TARGET)
	rm -r -f .perfexpert-temp*
	rm -r -f *.dSYM

