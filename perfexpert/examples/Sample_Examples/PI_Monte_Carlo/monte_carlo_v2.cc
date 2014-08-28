
#include <time.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>

#include <stdio.h>
#include <iostream>

#define MAX_THREADS         16
#define REPEAT_COUNT        1000
#define ITERATIONS          10000
#define RANDOM_BUFFER_SIZE  10000

typedef struct
{
    int tid;
} thread_info_t;

float* random_numbers=NULL;
int counts[MAX_THREADS*16]={0};

void* thread_func (void* arg)
{
  float x, y, z;
  thread_info_t* thread_info = (thread_info_t*) arg;

  for (int repeat=0; repeat<REPEAT_COUNT; repeat++)
  {
    srand(time(NULL) + thread_info->tid);
    for (int i=0; i<ITERATIONS; i++)
    {
      x = random_numbers[(i+thread_info->tid)%RANDOM_BUFFER_SIZE];
      y = random_numbers[(1+i+thread_info->tid)%RANDOM_BUFFER_SIZE];

      z = x*x + y*y;
      if (z <= 1) counts[thread_info->tid*16]++;
    }
  }

  pthread_exit(0);
}

int main()
{
  pthread_t threads[MAX_THREADS];
  thread_info_t thread_info[MAX_THREADS];

  // Initialize random numbers
  random_numbers = (float*) malloc(sizeof(float) * RANDOM_BUFFER_SIZE);
  assert (random_numbers && "Failed to allocate memory");

  for (int i=0; i<RANDOM_BUFFER_SIZE; i++)
    random_numbers[i] = ((float) rand()/RAND_MAX);

  timespec ts_beg, ts_end;
  clock_gettime(CLOCK_REALTIME, &ts_beg);

  for (int i=0; i<MAX_THREADS; i++)
  {
    thread_info[i].tid = i;
    pthread_create (&threads[i], NULL, &thread_func, (void *) &thread_info[i]);
  }

  for (int i=0; i<MAX_THREADS; i++)
    pthread_join(threads[i], NULL);

  clock_gettime(CLOCK_REALTIME, &ts_end);

  float time = ts_end.tv_sec-ts_beg.tv_sec + (ts_end.tv_nsec-ts_beg.tv_nsec)/1e9;
  fprintf (stdout, "Computation took %5.2lfs\n", time);

  free(random_numbers);

  // Calculate the final result
  int sum=0;
  for (int i=0; i<MAX_THREADS*16; i++)
    sum += counts[i];

  float pi = ((float) sum)/(REPEAT_COUNT*MAX_THREADS*ITERATIONS) * 4.0;
  std::cout << "Pi = " << pi << std::endl;

  return 0;
}
