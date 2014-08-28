#include "main.h"
#include "compute1.h"
#include "compute2.h"
#include "compute3.h"

double a[N][N], b[N][N], c[N][N], d[N][N];

int main(int argc, char *argv[])
{
  register int i, j, k;

  // Initialize the matrices
  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) {
      a[i][j] = i + j + 0.1; 
      b[i][j] = i - j + 0.2;
      c[i][j] = i * j + 0.3;
      d[i][j] = 0;
    }
  }

  // And do some time-wasting computing
  compute1();
  compute2();
  compute3();

  return 0;
}
