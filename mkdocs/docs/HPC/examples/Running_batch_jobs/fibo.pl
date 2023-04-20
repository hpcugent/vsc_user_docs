#!/usr/bin/perl
#
# VSC        : Flemish Supercomputing Centre
# Tutorial   : Introduction to HPC
# Description: Fibonacci Generator
#
$a = 0;
$b = 1;
for ($i=0;$i<30;$i++){
  printf "[%d] -> %d\n", $i, $a;
  $sum = $a + $b;
  $a = $b;
  $b = $sum;
}


