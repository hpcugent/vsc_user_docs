#include <stdlib.h>
#include <stdio.h>

// You can play with this dimension, and see the effect on performance
#define n 1000

static double a[n][n], b[n][n], c[n][n];

void compute()
{
  register int i, j, k;
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      for (k = 0; k < n; k++)
        c[i][j] = (i+k) * (k-j);
}

int main(int argc, char *argv[])
{
  register int i, j, k;

  // Initialize the matrices
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i][j] = i+j;
      b[i][j] = i-j;
      c[i][j] = 0;
    }
  }

  // And do a matrix multiplication
  compute();

  // Some compilers optimize the full "compute" functions away, when it detects that its computed elements are not being used.
  // As such, we print the first and last elements of the generated matrix
  printf ("c[0][0]=%f\n", c[0][0]);
  printf ("c[%d][%d]=%f\n", n-1, n-1, c[n-1][n-1]);

  return 0;
}
