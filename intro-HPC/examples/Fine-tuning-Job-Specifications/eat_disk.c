/*
 * VSC        : Flemish Supercomputing Centre
 * Tutorial   : Introduction to HPC
 * Description: Write a big file in a temporary directory
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define lines 100000000

int main(int argc, char *argv[])
{
  FILE * fp = NULL;
	unsigned long i;
  char file_name[256] = "/tmp";

	char *value = getenv ("VSC_SCRATCH");
	if (value)
		strcpy(file_name, value);
  strcat(file_name, "/test.txt");
	printf ("Writing in file <%s>\n", file_name);

	fp = fopen (file_name, "w+");
	if (fp == NULL)
    printf ("ERROR: Could not open file <%s>\n", file_name);
	for (i = 0; i < lines; i++)
		fprintf(fp, "Line <%ld>: Random number: %d\n", i, rand()%1000);
	fclose(fp);

  return 0;
}
