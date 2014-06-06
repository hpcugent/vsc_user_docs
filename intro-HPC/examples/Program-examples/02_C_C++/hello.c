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

