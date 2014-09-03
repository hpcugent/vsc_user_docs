#include "main.h"

void compute3()
{
  register int i, j, k;
  int denominator = 0;

  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++) {
      for (k = 0; k < N; k++) {
        d[i][j] += (a[i][k] * b[k][j]) / c[i][j];
      }
    }
}

