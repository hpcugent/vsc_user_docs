###########################
#   Compiler definitions  #
###########################

##### Fortran compiler
FC=ifort

##### C compiler
CC=icc

##### Fortran compiler options
FOPT= -g 

##### Fortran Linker options
FLIN= 

##### C compiler options
COPT= 

###########################
#   Library definitions   #
###########################

##### PVM library
LIBPVM= -L$(PVM_ROOT)/lib/LINUX64 -lfpvm3 -lpvm3

##### BLAS library
LIBBLAS= 

##### OpenMP
LIBOMP= 

######################################
#   Object/header file collections   #
######################################


###############
#   Targets   #
###############

default : master.x slave.x spmd.x

master.x : master.o 
	$(FC) -o $@ master.o $(LIBBLAS) $(LIBPVM) 

slave.x : slave.o 
	$(FC) -o $@ slave.o $(LIBBLAS) $(LIBPVM) 

spmd.x : spmd.o 
	$(FC) -o $@ spmd.o $(LIBBLAS) $(LIBPVM) 

.PHONY : clean
clean :
	rm *.o *.x 

#####################
#   Pattern rules   #
#####################

%.o : %.f
	$(FC) -c $< $(FOPT)

####################
#   Dependencies   #
####################

master.f: fpvm3.h
slave1.f: fpvm3.h
