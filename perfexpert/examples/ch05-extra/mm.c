#include <stdlib.h>
#include <stdio.h>

#define n 1000

static double a[n][n], b[n][n], c[n][n];

void compute()
{
  register int i, j, k;
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      for (k = 0; k < n; k++)
        c[i][j] = a[i][k] * b[k][j];
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

  return 0;
}
