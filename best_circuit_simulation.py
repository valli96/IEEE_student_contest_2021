import os
import matplotlib.pyplot as plt
import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Do not run this if in windows environment
if not os.name == 'nt':
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # to fix the error OSError: cannot load library 'libngspice.so'


circuit = Circuit('Transmission Line')

# TODO: Not sure if this is correct. A "Step Voltage Source" seems more appropriate
circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 1@u_V, 1@u_ns, 1@u_us)

circuit.LosslessTransmissionLine('tl_1', '2', circuit.gnd, '1', circuit.gnd,
                                 impedance=120, time_delay=2.5e-9)

circuit.LosslessTransmissionLine('tl_2', '4', circuit.gnd, '3', circuit.gnd,
                                 impedance=120, time_delay=3.75e-9)

circuit.LosslessTransmissionLine('tl_3', '6', circuit.gnd, '5', circuit.gnd,
                                 impedance=120, time_delay=6.25e-9)

circuit.LosslessTransmissionLine('tl_4', '7', circuit.gnd, '6', circuit.gnd,
                                 impedance=120, time_delay=8.25e-9)


circuit.R('R_1', 'input', '1', 120@u_Ω)
circuit.R('R_2', '3', '2', 120@u_Ω)
circuit.R('R_3', '5', '4', 120@u_Ω)
circuit.R('R_4', '7', circuit.gnd, 120@u_Ω)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1e-11, end_time=100e-9)


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
