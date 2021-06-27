import os
import matplotlib.pyplot as plt
import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from simulation_entry import *


circuit = Circuit('Transmission Line')


circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
# circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 1@u_V, 1@u_ns, 1@u_us)

# TODO: Check if ground is correct 
#  

circuit.LosslessTransmissionLine('1', '2', circuit.gnd, '1', circuit.gnd,
                                 impedance=120, time_delay=2.5e-9)

circuit.LosslessTransmissionLine('2', '4', circuit.gnd, '3', circuit.gnd,
                                 impedance=120, time_delay=3.75e-9)

circuit.LosslessTransmissionLine('3', '6', circuit.gnd, '5', circuit.gnd,
                                 impedance=120, time_delay=6.25e-9)

circuit.LosslessTransmissionLine('4', '7', circuit.gnd, '6', circuit.gnd,
                                 impedance=120, time_delay=8.25e-9)

circuit.R('1', 'input', '1', 120@u_Ohm)
circuit.R('2', '3', '2', 1@u_MOhm)
circuit.R('3', '5', '4', 1@u_MOhm)
circuit.R('4', '7', circuit.gnd, 120@u_Ohm)


settling_time = getMaxSettlingTime(circuit)




figure, ax = plt.subplots(figsize=(20, 6))
ax.plot(analysis['input'])
ax.plot(analysis['1'])
ax.plot(analysis['2'])
ax.plot(analysis['3'])
ax.plot(analysis['4'])
ax.plot(analysis['5'])
ax.plot(analysis['6'])
ax.plot(analysis['7'])
ax.set_xlabel('Time [ps]')
ax.set_ylabel('Voltage (V)')
ax.grid()
ax.legend(['input', '1','2','3','4','5','6','7'], loc='upper right')

plt.show()
