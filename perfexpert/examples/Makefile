#
# Global makefile for the PerfExpert Exercises
#

.PHONY: all
all:
	@test -d ch02-profiling && $(MAKE) $@ -C ch02-profiling 
	@test -d ch03-optimizing && $(MAKE) $@ -C ch03-optimizing 
	@test -d ch04-parallel && $(MAKE) $@ -C ch04-parallel 
	@test -d ch05-extra && $(MAKE) $@ -C ch05-extra 

.PHONY: clean
clean:
	@test -d ch02-profiling && $(MAKE) $@ -C ch02-profiling 
	@test -d ch03-optimizing && $(MAKE) $@ -C ch03-optimizing 
	@test -d ch04-parallel && $(MAKE) $@ -C ch04-parallel 
	@test -d ch05-extra && $(MAKE) $@ -C ch05-extra 

