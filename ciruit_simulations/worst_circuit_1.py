import os
import matplotlib.pyplot as plt
import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from simulation_entry  import *
# from analysis_tools import *


# import csv

# f = open('./test.csv', 'w')
# writer = csv.writer(f)



# import timeit
# start = timeit.default_timer()


# Do not run this if in windows environment
if not os.name == 'nt':
    # To fix the error OSError: cannot load library 'libngspice.so'
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  


circuit = Circuit('Transmission Line')

# circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 1@u_V, 1@u_ns, 1@u_us)
circuit.PulseVoltageSource('pulse', 'input', circuit.gnd, 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)

circuit.LosslessTransmissionLine('1', 'T1e', circuit.gnd, 'T1b', circuit.gnd,
                                 impedance=120, time_delay=2.5e-9)

circuit.LosslessTransmissionLine('2', 'T2e', circuit.gnd, 'T1e', circuit.gnd,
                                 impedance=120, time_delay=3.75e-9)

circuit.LosslessTransmissionLine('3', 'T3e', circuit.gnd, 'T2e', circuit.gnd,
                                 impedance=120, time_delay=6.25e-9)

circuit.LosslessTransmissionLine('4', 'T4e', circuit.gnd, 'T3e', circuit.gnd,
                                 impedance=120, time_delay=8.25e-9)

circuit.R('1M', 'T1b', circuit.gnd, 1@u_MOhm)
circuit.R('2M', 'T3e', 'T4e', 1@u_MOhm)
circuit.R('1R', 'T1e', 'input', 120@u_Ohm)
circuit.R('2R', 'T4e', circuit.gnd, 120@u_Ohm)

# simulator = circuit.simulator(temperature=25, nominal_temperature=25)
# analysis = simulator.transient(step_time=5e-11, end_time=3e-7)


currAnalysis = circuit_simulation(circuit, step_time=5e-11)
settling_Time, DC_values, max_time   = getMaxSettlingTime(currAnalysis)
plot_voltages(currAnalysis, max_time, save_path=False, resize=True, boundary=True)


# # stop = timeit.default_timer()
# # print('Time: ', stop - start)  



# figure, ax = plt.subplots(figsize=(20, 6))
# ax.plot(analysis['input'])
# ax.plot(analysis['T1b'])
# # import ipdb; ipdb.set_trace()

# ax.plot(analysis['T1e'])
# ax.plot(analysis['T2e'])
# ax.plot(analysis['T3e'])
# ax.plot(analysis['T4e'])
# # ax.plot(analysis['t4#i1'])

# ax.set_xlabel('Time [ps]')
# ax.set_ylabel('Voltage (V)')
# ax.grid()
# ax.legend(['input', 'T1b','T1e','T2e','T3e','T4e'], loc='upper right')

# scale_factor = 1e-11
# end_time=100e-9



# # xmin, xmax = plt.xlim()
# # ymin, ymax = plt.ylim()
# # xmin = xmin*scale_factor; xmax= xmax*scale_factor; 
# # ax.set(xlim=(xmin, end_time), ylim=(ymin, ymax))

# # plt.xlim(xmin * scale_factor, end_time)
# # plt.ylim(ymin, ymax)



# # import ipdb; ipdb.set_trace()

# # print(get_DC_voltage(analysis).keys())
# DC_values = get_DC_voltage(analysis)
# print(DC_values)
# get_settlingtime(analysis)

# # print(*analysis['T4e'])

# # print('ymax = '+ str(ymax))
# # print('ymin = '+ str(ymin))
# # print('xmax = '+ str(xmax))
# # print('xmin = '+ str(xmin))
# # print('xend = '+ str(end_time))




# ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))

# # writer.writerow(analysis.nodes)
# # f.close()

# plt.show()
