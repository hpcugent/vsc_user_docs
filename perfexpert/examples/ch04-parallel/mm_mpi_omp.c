#include <omp.h>
#include <mpi.h>
#include <stdlib.h>
#define TAG 13

double **a, **b, **c, *tmp;
int numElements, offset, stripSize, myrank, numnodes, i, j, k;

void compute() {
    #pragma omp parallel for shared( a, b, c) private(i, j, k)
    for (i = 0; i < stripSize; i++)
        for (j = 0; j < 2000; j++)
            for (k = 0; k < 2000; k++)
                c[i][j] += a[i][k] * b[k][j];
}

int main(int argc, char *argv[]) {  
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &numnodes);

    stripSize = 2000 / numnodes;

    if (0 == myrank) {
        tmp = (double *) malloc (sizeof(double ) * 2000 * 2000);
        a = (double **) malloc (sizeof(double *) * 2000);
        #pragma omp parallel for shared(a) private(i)
        for (i = 0; i < 2000; i++)
            a[i] = &tmp[i * 2000];
    } else {
        tmp = (double *) malloc (sizeof(double ) * 2000 * stripSize);
        a = (double **) malloc (sizeof(double *) * stripSize);
        #pragma omp parallel for shared(a) private(i)
        for (i = 0; i < 2000 / numnodes; i++)
            a[i] = &tmp[i * 2000];
    }

    tmp = (double *) malloc (sizeof(double ) * 2000 * 2000);
    b = (double **) malloc (sizeof(double *) * 2000);
    #pragma omp parallel for shared(b) private(i)
    for (i = 0; i < 2000; i++)
        b[i] = &tmp[i * 2000];
  
    if (0 == myrank) {
        tmp = (double *) malloc (sizeof(double ) * 2000 * 2000);
        c = (double **) malloc (sizeof(double *) * 2000);
        #pragma omp parallel for shared(c) private(i)
        for (i = 0; i < 2000; i++)
            c[i] = &tmp[i * 2000];
    } else {
        tmp = (double *) malloc (sizeof(double ) * 2000 * stripSize);
        c = (double **) malloc (sizeof(double *) * stripSize);
        #pragma omp parallel for shared(c) private(i)
        for (i = 0; i < 2000 / numnodes; i++)
            c[i] = &tmp[i * 2000];
    }

    if (0 == myrank) {
        #pragma omp parallel for shared(a) private(i, j)
        for (i = 0; i < 2000; i++)
            for (j = 0; j < 2000; j++)
                a[i][j] = (i + j);

        #pragma omp parallel for shared(b) private(i, j)
        for (i = 0; i < 2000; i++)
            for (j = 0; j < 2000; j++)
                b[i][j] = (i * j);
    }

    if (0 == myrank) {
        offset = stripSize;
        numElements = stripSize * 2000;
        for (i = 1; i < numnodes; i++) {
            MPI_Send(a[offset], numElements, MPI_DOUBLE, i, TAG, MPI_COMM_WORLD);
            offset += stripSize;
        }
    } else {
        MPI_Recv(a[0], stripSize * 2000, MPI_DOUBLE, 0, TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
  
    MPI_Bcast(b[0], 2000 * 2000, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    #pragma omp parallel for shared(c) private(i, j)
    for (i = 0; i < stripSize; i++)
        for (j = 0; j < 2000; j++)
            c[i][j] = 0;

    compute();

    if (0 == myrank) {
        offset = stripSize; 
        numElements = stripSize * 2000;
        for (i=1; i<numnodes; i++) {
            MPI_Recv(c[offset], numElements, MPI_DOUBLE, i, TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            offset += stripSize;
        }
    } else {
        MPI_Send(c[0], stripSize * 2000, MPI_DOUBLE, 0, TAG, MPI_COMM_WORLD);
    }

  MPI_Finalize();
  return 0;
}