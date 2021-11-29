We originally tried to find a network which maximizes reflection coefficients and signal runtime in between components. We quickly realised that this approach was rather unsystematic. After estimating the number of all possible circuits with the given components and constraints, we decided to simply try all arrangements. This approach led to two main challenges:
1. Generation of all possible circuits
2. Simulation and determination of the settling time

### Generation:
For the generation of the different circuits we developed the following approach which we divided into the following steps:
1. Create all allowed graph-structures which could satisfy the task's constraints (There are 9 graphs with 3-5 nodes). Transmission lines correspond to edges of the graph and ECUs could be placed at the vertices of the graph.
2. From a graph create a circuit topology. As transmission lines and ECUs can be connected in different ways, generating topologies from graphs corresponds fixing the connections at vertices.
3. From the topology, we finally generated actual circuits by assigning values to the formally arbitrary transmission lines and ECUs. That way we could test the same topology with every possible transmission line/ECU configuration.

### Simulation:
For the simulation we used PySpice which is an open-source Python library which provides an API to simulate circuits with NgSpice. After we have translated the circuits from Generation into a compatible netlist, we could use PySpice's API to simulate the circuits. From the results of that simulation, we determined the settling time. Since there were occasional errors in the generation and simulation results, we verified the circuits with the longest settling time manually in LTSpice.

### Verdict:
The final winner of our experiment is the circuit described above. As we can see the "reflection-absorbing" 120 Ohm ECU is hidden behind the large 1 MOhm ECU, while a long transmission line leads to the other 1 MOhm ECU. This maximizes signal runtime, while minimizing signal absorption. The largest loss of the signal is due to the 120 Ohm in the source, which is impossible to avoid.

All code can be accessed through valli96/IEEE_student_contest_2021 as well as additional data and a more visual presentation of this project.