/*
 * VSC        : Flemish Supercomputing Centre
 * Tutorial   : Introduction to HPC
 * Description: Consume a lot of CPU by doing a matric multiplication
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define n 1500

static double a[n][n], b[n][n], c[n][n];

int main(int argc, char *argv[])
{
  register int i, j, k;
	time_t t;

	/* Intializes random number generator */
	srand((unsigned) time(&t));
	// Fill up the matrices a and b with random values between -500 and +500
	// Initialize the matric c
	printf("Initialize 2 matrices with random values\n");
	for (j = 0; j < n; j++) {
		for (i = 0; i < n; i++) {
			a[i][j] = (rand()%1001) - 500;
			b[i][j] = (rand()%1001) - 500;
			c[i][j] = 0;
    }
  }

	/* 
	 * Matrix multiplication
	 */
	printf("Performing matrix multiplication:\n");
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      for (k = 0; k < n; k++) {
        c[i][j] += a[i][k] * b[k][j];
      }
    }
		// printf(".");
		// fflush(stdout);
  }
  return 0;
}
