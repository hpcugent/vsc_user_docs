#include <stdlib.h>
#include <stdio.h>
#include <time.h>
 
// You can play with this dimension, and see the effect on performance
#define ARRAY_LEN 400000000
int a[ARRAY_LEN];
 
void compute()
{
  int i;
  int zero = 0, one = 0, two = 0, three = 0;
  
  for(i = 0; i < ARRAY_LEN; ++i)
  {
    if (a[i] == 0)
      ++zero;
    else if (a[i] == 1)
      ++one;
    else if (a[i] == 2)
      ++two;
    else 
      ++three;
  }
  printf ("zero (%d), one (%d), two (%d), three (%d)\n", zero, one, two, three);
}

int main()
{
  int i;
    
  // Generate a new array...
  srand ((unsigned int)time(NULL));
  for(i = 0; i < ARRAY_LEN; ++i)
    a[i] = rand() % 4;

  compute();
}
            
            


