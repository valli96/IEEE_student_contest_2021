## How was the solution obtained and why is the proposed network particularly bad?

After estimating the number of possible permutations of the different circuit with the given components, we decided to just try each arrangement. The divided upcoming challenges, with this approach in to 2 categories. 

1. Generation of all possible circuits
2. Simulation and determination of the settling time

### Generation:
For the generation of the different arrangement we proposed a approach which we divided into 3 different stages.
The first thing we did was to create all possible graphs. Where the transmission lines are the branches and the ESU's are located at the nodes. With max 4 branches there are only 9 different graphs. The second step was to create different typologies from a graph. This represents the different connections at the nodes. The last step was to (change)(permute) the position of the ECU's to create every possible circuit.

### Simulation:
For the simulation we used PySpice which is an open Source Python library which provides an API to simulate circuits with NgSpice. After we have brought the circuits in the right format, we could use the API and simulate the circuits. We have calculated the settling time of every simulation which was the metric to compare the circuits. Since there were some occasional errors in the results we verified the circuits with the longest settling time manually in LTSpice.

The final winner of our experiment is the circuit described above 
