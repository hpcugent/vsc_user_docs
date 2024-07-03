%
% ./examples/ex01-matlab
% Script to calculate and print the first 50 fibonacci numbers
% This script is used as an example to demonstrate the UA-HPC.
%
%Clear screen and memory
clear; clc; format compact 

% Initialize the first two values
f(1) = 1;
f(2) = 1; 

% Create the first 30 Fibonacci numbers
for i = 3 : 30
	% Perform the sum of terms accordingly
	f(i) = f(i-1) + f(i-2);
	% Calculate and display the ratio of 2 consecutive elements of the series
	golden_ratio = f(i)/f(i-1);
	str = ['Step(' num2str(i) '): ' num2str(f(i)) ' ' num2str(f(i-1)) ' ' ...
	num2str(golden_ratio, 10)];
	disp(str)
end

