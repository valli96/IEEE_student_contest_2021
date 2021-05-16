
import matplotlib.pyplot as plt

import PySpice
import os
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

#Do not run this if in windows environment
if not os.name == 'nt':
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # to fix the error OSError: cannot load library 'libngspice.so'
    

circuit = Circuit('Transmission Line')

# syntax pulse(name, v_inital, v_pulsed, pulse_width, period, delay_time, rise_time, fall_time)
circuit.PulseVoltageSource('pulse', 'N_1', 'N_5', 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
circuit.R('1', 'N_2', 'N_1', 25@u_Ω)
circuit.R('2', 'N_4', 'N_3', 50@u_Ω)
circuit.LosslessTransmissionLine('delay', 'N_3','N_2' , 'N_4', 'N_5', impedance=120, time_delay=40e-9)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1e-10, end_time=1e-6)


dc_circuit = Circuit('Steady State')
dc_circuit.PulseVoltageSource('pulse', 'N_1', dc_circuit.gnd, 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
dc_circuit.R('1', 'N_1', 'N_2', 25@u_Ω)
dc_circuit.R('2', 'N_2', dc_circuit.gnd, 50@u_Ω)

# import ipdb
# ipdb.set_trace()
# ipdb.set_trace(context=3)

dc_simulator = dc_circuit.simulator(temperature=25, nominal_temperature=25)
# dc_analysis = dc_simulator.transient(step_time=1e-10, end_time=1e-6)
dc_analysis = dc_simulator.operating_point()



figure, ax = plt.subplots(figsize=(20, 6))
ax.plot(analysis['N_1'])
ax.plot(analysis['N_3'])
# ax.plot(dc_analysis['N_1'])
# ax.plot(dc_analysis['N_2'])
ax.set_xlabel('Time [s]')
ax.set_ylabel('Voltage (V)')
ax.grid()
ax.legend(['N_1', 'N_3','N_1_DC','N_2_DC'], loc='upper right')

# import ipdb
# ipdb.set_trace()
# ipdb.set_trace(context=3)

plt.show()
