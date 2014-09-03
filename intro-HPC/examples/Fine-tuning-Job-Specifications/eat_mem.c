/*
 * VSC        : Flemish Supercomputing Centre
 * Tutorial   : Introduction to HPC
 * Description: Allocate and cConsume a given amount of memory
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define Kb 1024
#define Mb 1024*Kb
#define default_Gb 3
#define max_Gb 12


int main(int argc, char *argv[])
{
  register int i;
	int tot_Gb = default_Gb;
  char* mem[Mb];

	if (argc > 2) {
		printf("Usage: eat_mem [number]\n");
		printf("  Allocate and use [number] Gigabit of memory.\n");
		printf("  Default is %s Gigabit.\n", default_Gb);
	  exit(1);
	}

	// Calculate the amount of memory to allocate
	// Default = 5Gb
	if (argc == 2) {
		tot_Gb = atoi(argv[1]);
		if (tot_Gb <= 0)
		  tot_Gb = default_Gb;
	  else if (tot_Gb > max_Gb) {
			printf("Exceeded maximum, reset to %d Gigabit.\n", max_Gb);
		  tot_Gb = max_Gb;
	  }
	}
	printf("Consuming %d Gigabit of memory.\n", tot_Gb);

	char buffer[Mb];
	// Fill up a buffer of 1 Mb with random digits
	for (i = 0; i < Mb; i++)
	  buffer[i] = rand()%256;

	// Consume memory, 1 Mb at a time
  for (i = 0; i < tot_Gb*1024; i++) {
		mem[i] = (char *)malloc(Mb*sizeof(char));
		if (mem[i] == NULL) {
			printf("ERROR: Out of memory\n");
			return 1;
		}
		else {
			memcpy(mem[i], (void *) buffer, Mb);
		  usleep (20000); // Wait 20 microseconds
	  }
	}

	// Sleep 10 seconds, so that you have time to monitor the full memory allocation
	sleep (10);

	// Free memory, 1 Mb at a time
  for (i = 0; i < tot_Gb*1024; i++) {
		free(mem[i]);
	}
	// Sleep 10 seconds, so that you have time to monitor the freed-up  memory
	sleep (10);
  return 0;
}

