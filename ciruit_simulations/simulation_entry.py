import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from .analysis_tools import get_DC_voltage, get_settlingtime
from PySpice.Probe.Plot import plot
import matplotlib.pyplot as plt
import os


def get_nodes(analysis):
    ''' TODO: Docstring
    '''
    nodes = []
    for i in analysis.nodes.keys():
        # print(i)
        if '#' in i:
            pass
        else:
            nodes.append(i)
    return nodes

def circuit_simulation(testCircuit : Circuit, step_time=1e-11, end_time=100e-9) :
    ''' TODO: Docstring
    '''
    end_time=100e-8
    # initialize the simulation
    # Do not run this if in windows environment
    # To fix the error OSError: cannot load library 'libngspice.so'
    if not os.name == 'nt':
        PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  
    
    simulator = testCircuit.simulator(temperature=25, nominal_temperature=25)
   
   # simulation 
    analysis = simulator.transient(step_time, end_time)
    return analysis

def getMaxSettlingTime(analysis):

    # calculation of the settling_time
    DC_values = get_DC_voltage(analysis)
    settling_time = get_settlingtime(analysis)

    # getting the max value of the dic with the settling times off all Nodes
    max_time = 0
    for node, time in settling_time.items():
        if max_time < time:
            max_time = time
    
    return settling_time, DC_values, max_time
   

def plot_voltages(analysis):
    _dont_care_,_dont_care_,max_time = getMaxSettlingTime(analysis)
    nodes = get_nodes(analysis)

    # import ipdb; ipdb.set_trace()

    # voltages = [len(node)][len(analysis.time]
    #     for i in range(len(analysis.time)):
    #         voltages[nd][i]= analysis[nd][i].value
            # globals()[f"voltage_{nd}"] = analysis[nd][i].value
   
    figure, ax = plt.subplots(figsize=(20, 6))
    for nd in nodes:
        ax.plot(analysis[nd])
    
    ax.set_xlabel('Time [ps]')
    ax.set_ylabel('Voltage (V)')
    ax.grid()
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    plt.show()


# ax.legend(['input', 'T1b','T1e','T2e','T3e','T4e'], loc='upper right')

# how to get the corresponding time to the voltage
# analysis.time[-1].value
