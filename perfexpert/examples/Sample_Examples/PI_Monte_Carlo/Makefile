CC=gcc
LDFLAGS=-lpthread -lrt

all:	monte_carlo	monte_carlo_v2

monte_carlo:	monte_carlo.o
	$(CXX)	$< -o $@ $(LDFLAGS)

monte_carlo_v2:	monte_carlo_v2.o
	$(CXX)	$< -o $@ $(LDFLAGS)

clean:
	$(RM) *.o monte_carlo monte_carlo_v2 
