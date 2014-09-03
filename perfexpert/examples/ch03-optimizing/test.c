#include <stdlib.h>
#include <stdio.h>
#include <time.h>

// You can play with this dimension, and see the effect on performance
#define n 1000

static double a[n][n], b[n][n], c[n][n], d[n][n];

// Used for optimization of Category #1: Data Access
void compute1()
{
  register int i, j, k;
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      for (k = 0; k < n; k++)
        d[i][j] += a[i][j] + (b[i][k] * c[k][j]);
}

// Used for optimization of Category #3: Data TLB
void compute3()
{
  register int i, j, k;
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      for (k = 0; k < n; k++)
        d[i][j] += a[i][j] + (b[i][k] * c[k][j]);
}

// Used to demonstrate optimization of Category #6: FP Instructions
void compute6()
{
  register int i, j, k;
  int denominator = 0;

  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++) {
      for (k = 0; k < n; k++) {
        d[i][j] += (a[i][k] * b[k][j]) / c[i][j];
      }
    }
}

int main(int argc, char *argv[])
{
  register int i, j, k;

  // Initialize the matrices
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i][j] = i + j + 0.1; 
      b[i][j] = i - j + 0.2;
      c[i][j] = i * j + 0.3;
      d[i][j] = 0;
    }
  }

  // And do some time-wasting computing
  compute1();
  compute3();
  compute6();

  // Some compilers optimize the full "compute" functions away, when it detects that its computed elements are not being used.
  // As such, we print the first and last elements of the generated matrix
  printf ("d[0][0]=%f\n", d[0][0]);
  printf ("d[%d][%d]=%f\n", n-1, n-1, d[n-1][n-1]);

  return 0;
}
