# import numpy as np
# import matplotliv.pyplot as plt
# import sys

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import * # nessasary if Volt, Ohm, And Amere should be used (10@u_V)

PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # to fix the error OSError: cannot load library 'libngspice.so'


logger = Logging.setup_logging()

# creat the circuit 
circuit = Circuit('Voltage Divider')

# add components 
circuit.V('input', 'in', circuit.gnd, 10@u_V)
circuit.R('1', 'in', 'out', 9@u_kOhm)
circuit.R('2', 'out', circuit.gnd, 1@u_kOhm)

# print circuit 
print("the circuit netlist: \n\n", circuit)
# exit()

# creat a simulator instace
# simulator = circuit.simulator(temperature=25, norminal_temperatur=25)
simulator = circuit.simulator()

# print simulator details 
print("The simulator \n", simulator)

# run the analysis
analysis = simulator.operating_point()

# get the voltage at node out
print(analysis.nodes['out']) # this vector contain all voltages of every node
print(str(analysis.nodes['out']))
print(float(analysis.nodes['out'])) # if the variable is forced in to a float is will give the voltage

print(analysis)
