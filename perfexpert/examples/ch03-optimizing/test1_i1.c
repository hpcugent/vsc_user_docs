#include <stdlib.h>
#include <stdio.h>

// You can play with this dimension, and see the effect on performance
#define n 1000

static double a[n][n], b[n][n], c[n][n], d[n][n];

void compute()
{
  register int i, j, k;
  double tmp;
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
    {
      tmp = a[i][j];
      for (k = 0; k < n; k++)
        d[i][j] += tmp + (b[i][k] * c[k][j]);
    }
}

int main(int argc, char *argv[])
{
  register int i, j, k;

  // Initialize the matrices
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i][j] = i+j + 0.1;
      b[i][j] = i-j + 0.2;
      c[i][j] = i*j + 0.3;
      d[i][j] = 0;
    }
  }

  // And do some time-wasting computing
  compute();

  // Some compilers optimize the full "compute" functions away, when it detects that its computed elements are not being used.
  // As such, we print the first and last elements of the generated matrix
  printf ("d[0][0]=%f\n", d[0][0]);
  printf ("d[%d][%d]=%f\n", n-1, n-1, d[n-1][n-1]);

  return 0;
}
