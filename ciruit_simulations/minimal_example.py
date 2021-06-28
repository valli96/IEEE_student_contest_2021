import os
import matplotlib.pyplot as plt
import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from analysis_tools import *

# Do not run this if in windows environment
if not os.name == 'nt':
    # To fix the error OSError: cannot load library 'libngspice.so'
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  

circuit = Circuit('Transmission Line')

#### the simulation does not throw an error but this one is not correct 

# circuit.PulseVoltageSource('pulse', 'in_high', 'GND', 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
# circuit.LosslessTransmissionLine('TL_1', 'out_high', 'out_low', 'in_high', 'GND', impedance=10, time_delay=2.5e-9)
# circuit.R('R_1','out_high', 'out_low', 20@u_Ohm)


#### Pseudo Ground with a 10e+9 resistance inserted at out_low and it works

# circuit.PulseVoltageSource('pulse', 'in_high', 'GND', 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
# circuit.LosslessTransmissionLine('TL_1', 'out_high', 'out_low', 'in_high', 'GND', impedance=90, time_delay=2.5e-9)
# circuit.R('R_1','out_low', 'out_high', 90@u_Ohm)
# circuit.R('Ground_RES','out_low', 'GND', 10e+9@u_Ohm)

#### Pseudo Ground with a 10e+9 resistance inserted at out_low and at in_low it works

circuit.PulseVoltageSource('pulse', 'vol_out', 'in_low', 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
circuit.LosslessTransmissionLine('TL_1', 'out_high', 'out_low', 'in_high', 'in_low', impedance=90, time_delay=2.5e-9)
circuit.R('R_1','out_low', 'out_high', 42@u_Ohm)

circuit.R('R_0','vol_out', 'in_high', 42@u_Ohm)

# Pseudo_GND
circuit.R('Pseudo_GND_in','in_low', 'GND', 1e+9@u_Ohm)
circuit.R('Pseudo_GND_out','out_low', 'GND', 1e+9@u_Ohm)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1e-11, end_time=100e-9)

# DC_values = get_DC_voltage(analysis)
# print(DC_values)
settling_time = get_settlingtime(analysis)
print(settling_time)

figure, ax = plt.subplots(figsize=(20, 6))
ax.plot(analysis['in_high'])
ax.plot(analysis['out_high'])
# ax.plot(analysis['out_low'])
ax.set_xlabel('Time [ps]')
ax.set_ylabel('Voltage (V)')
ax.grid()
ax.legend(['in_high','out_high'], loc='upper right')
plt.show()
