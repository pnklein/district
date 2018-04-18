# makefile for cs2
# compileler definitions
# COMP_DUALS to compute prices
# PRINT_ANS to print flow (and prices if COMP_DUAL defined)
# COST_RESTART to be able to restart after a cost function change
# NO_ZERO_CYCLES finds an opeimal flow with no zero-cost cycles
# CHECK_SOLUTION check feasibility/optimality. HIGH OVERHEAD!

# change these to suit your system
#CFLAGS = -g -DCHECK_SOLUTION -Wall
DEBUG = -g 
CFLAGS = -O3 -Wall -g
CPPFLAGS = -O3 -Wall -std=c++11 -g -flto
#CPPFLAGS = -g -Wall -std=c++1z
#CFLAGS = -O4 -DNDEBUG -DNO_ZERO_CYCLES
BIN=cs2 do_redistrict.exe test_initial_centers.exe test_redistrict.exe test_find_weights

do_redistrict.exe: do_redistrict.o redistrict.o initial_centers.o  mincostflow.o check_weights.o rand_point.o rand_float.o point.o print_out_solution.o random.o
	$(CXX) $(CPPFLAGS) do_redistrict.o redistrict.o initial_centers.o mincostflow.o check_weights.o rand_point.o point.o print_out_solution.o rand_float.o random.o -o do_redistrict.exe

clean:
	rm -f $(BIN) *.o *~

rand_float.o: rand_float.cpp rand_float.hpp
	$(CXX) $(CPPFLAGS) -c rand_float.cpp

point.o: point.cpp point.hpp
	$(CXX) $(CPPFLAGS) -c point.cpp

rand_point.o: rand_point.cpp rand_point.hpp
	$(CXX) $(CPPFLAGS) -c rand_point.cpp

random.o: random.cpp random.hpp
	$(CXX) $(CPPFLAGS) -c random.cpp

initial_centers.o: initial_centers.cpp initial_centers.hpp
	$(CXX) $(CPPFLAGS) -c initial_centers.cpp

test_initial_centers.o: test_initial_centers.cpp initial_centers.hpp
	$(CXX) $(CPPFLAGS) -c test_initial_centers.cpp

test_initial_centers.exe: test_initial_centers.o initial_centers.o point.o
	$(CXX) $(CPPFLAGS) test_initial_centers.o initial_centers.o point.o -o test_initial_centers.exe

mincostflow.o: mincostflow.cpp mincostflow.hpp build_graph.h types_cs2.h assignment.hpp
	$(CXX) $(CFLAGS) -c mincostflow.cpp

redistrict.o: redistrict.cpp redistrict.hpp point.hpp assignment.hpp
	$(CXX) $(CPPFLAGS) -c redistrict.cpp

print_out_solution.o: print_out_solution.cpp
	$(CXX) $(CPPFLAGS) -c print_out_solution.cpp

test_redistrict.o: test_redistrict.cpp redistrict.hpp rand_point.hpp
	$(CXX) $(CPPFLAGS) -c test_redistrict.cpp

do_redistrict.o: do_redistrict.cpp redistrict.hpp
	$(CXX) $(CPPFLAGS) -c do_redistrict.cpp

test_redistrict.exe: test_redistrict.o redistrict.o initial_centers.o  mincostflow.o check_weights.o point.o rand_point.o rand_float.o
	$(CXX) $(CPPFLAGS) test_redistrict.o redistrict.o initial_centers.o mincostflow.o check_weights.o rand_point.o point.o rand_float.o -o test_redistrict.exe

do_redistrict: do_redistrict.o redistrict.o initial_centers.o  mincostflow.o check_weights.o rand_point.o rand_float.o point.o print_out_solution.o
	$(CXX) $(CPPFLAGS) do_redistrict.o redistrict.o initial_centers.o mincostflow.o check_weights.o rand_point.o point.o print_out_solution.o rand_float.o -o do_redistrict

find_weights.hpp: point.hpp

find_weights.o: find_weights.cpp find_weights.hpp
	$(CXX) $(CPPFLAGS) -c find_weights.cpp

test_find_weights.o: test_find_weights.cpp find_weights.hpp
	$(CXX) $(CPPFLAGS) -c test_find_weights.cpp

test_find_weights.exe: test_find_weights.o find_weights.o point.o
	$(CXX) $(CPPFLAGS) test_find_weights.o find_weights.o point.o -o test_find_weights.exe

test_mincostflow.o: test_mincostflow.cpp mincostflow.hpp
	$(CXX) $(CPPFLAGS) -c test_mincostflow.cpp

test_mincostflow: test_mincostflow.o mincostflow.o point.o
	$(CXX) $(CPPFLAGS) test_mincostflow.o mincostflow.o point.o -o test_mincostflow

mincostflow.hpp: assignment.hpp types_cs2.h

point.hpp: rand_float.hpp

print_out_solution.hpp: assignment.hpp

rand_point.hpp: point.hpp

redistrict.hpp: assignment.hpp point.hpp

initial_centers.hpp: point.hpp
