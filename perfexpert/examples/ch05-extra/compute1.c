#include "main.h"

void compute1()
{
  register int i, j, k;
  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
      for (k = 0; k < N; k++)
        d[i][j] += a[i][j] + (b[i][k] * c[k][j]);
}

