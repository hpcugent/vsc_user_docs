//
// test3.c
// Test program to invoke Data TLB misses
//
#include <stdlib.h>
#include <stdio.h>

// You can play with this dimension, and see the effect on performance
#define STRIDE 1024
#define MAX_I STRIDE * 16
#define MAX_J STRIDE * 16

static int a[MAX_I * MAX_J];

void compute()
{
  register int i, j;
  for (j = 0; j < MAX_J; j++)
    for (i = 0; i < MAX_I; i++)
      a[i*STRIDE+j] += 2;
}

int main(int argc, char *argv[])
{
  register int i;

  // Initialize the array
  for (i = 0; i < (MAX_I * MAX_J); i++)
    a[i] = 0;

  compute();

  // Some compilers optimize the full "compute" functions away, when it detects that its computed elements are not being used.
  // As such, we print the first and last elements of the generated matrix
  printf ("a[0]=%f\n", a[0]);
  printf ("c[%d]=%f\n", MAX_J*MAX_I-1, a[MAX_J*MAX_I-1]);

  return 0;
}
