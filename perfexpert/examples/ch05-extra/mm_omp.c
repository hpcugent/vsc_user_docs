#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

#define N 1000  /* size of matrices */
static double  a[N][N], b[N][N], c[N][N];     

void compute()
{
  int  tid, nthreads;
  register int i, j, k;
  int chunk = 10;                    /* set loop iteration chunk size */

  /*** Spawn a parallel region explicitly scoping all variables ***/
  #pragma omp parallel shared(a,b,c,nthreads,chunk) private(tid,i,j,k)
  {
    tid = omp_get_thread_num();
    if (tid == 0)
      nthreads = omp_get_num_threads();
    #pragma omp for schedule (static, chunk)
    for (i=0; i<N; i++)    
      for (j=0; j<N; j++)       
        for (k=0; k<N; k++)
          c[i][j] += a[i][k] * b[k][j];
  }
}

int main (int argc, char *argv[]) 
{
  register int  i, j;

  /*** Initialize matrices ***/
  for (i=0; i<N; i++) {
    for (j=0; j<N; j++) {
      a[i][j]= i+j;
      b[i][j]= i-j;
      c[i][j]= 0;
    }
  }

  compute();
}

