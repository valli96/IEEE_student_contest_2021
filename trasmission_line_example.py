import matplotlib.pyplot as plt

import PySpice
# import sys
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # to fix the error OSError: cannot load library 'libngspice.so'

circuit = Circuit('Transmission Line')

# import ipdbp
# ipdb.set_trace()
# ipdb.set_trace(context=3)

# syntax pulse(name, v_inital, v_pulsed, pulse_width, period, delay_time, rise_time, fall_time)

circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
circuit.LosslessTransmissionLine('delay', 'output', circuit.gnd, 'input', circuit.gnd,
                                 impedance=120, time_delay=40e-9)
circuit.R('load', 'output', circuit.gnd, 50@u_Ω)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1e-10, end_time=1e-6)


figure, ax = plt.subplots(figsize=(20, 6))
ax.plot(analysis['input'])
ax.plot(analysis['output'])
ax.set_xlabel('Time [s]')
ax.set_ylabel('Voltage (V)')
ax.grid()
ax.legend(['input', 'output'], loc='upper right')

plt.show()