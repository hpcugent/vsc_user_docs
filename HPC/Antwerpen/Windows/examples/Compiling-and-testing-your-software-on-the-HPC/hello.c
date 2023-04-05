/*
 * VSC        : Flemish Supercomputing Centre
 * Tutorial   : Introduction to HPC
 * Description: Print 500 numbers, whilst waiting 1 second in between
 */
#include "stdio.h"
int main( int argc, char *argv[] )
{
  int i;
  for (i=0; i<500; i++)
  {
    printf("Hello #%d\n", i);
    fflush(stdout);
    sleep(1);
  }
}

