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


def get_DC_voltage(analysis):
    ''' TODO: Docstring
    '''
    nodes = get_nodes(analysis)
    DC_values = {} 
    for nd in nodes:
        # print(i)
        DC_values[nd] = analysis[nd][-1].value
    return DC_values


def get_data_points(analysis):
    ''' TODO: Docstring
    '''
    return len(analysis.time)


def get_settlingtime(analysis):
    ''' TODO: Docstring
    '''
    number_simulations = get_data_points(analysis)
    nodes = get_nodes(analysis)
    DC_values = get_DC_voltage(analysis)
    settling_time = {}
    for node in nodes:
        # print(str(DC_values[node])+ 'DC_values of Node' + str(node))   
        if abs(DC_values[node]) <= 0.1: # 0.1 
            # pass
            a=1
        else:
            for i in range(number_simulations):
                voltage = analysis[node][number_simulations - 1 - i].value
                if (abs(voltage) >= abs(DC_values[node])*1.02 or abs(voltage) <= abs(DC_values[node])*0.98):
                    # print("the Settlingtime of "+ node + " is " )
                    # print(number_simulations-i)
                    DC_values[node] = number_simulations-i
                    settling_time[node] = number_simulations-i
                    break

    return settling_time


def circuit_simulation(testCircuit : Circuit, step_time=5e-11, end_time=3e-7) :
    ''' TODO: Docstring
    '''
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

    ''' TODO: Docstring
    '''
    # calculation of the settling_time
    DC_values = get_DC_voltage(analysis)
    settling_time = get_settlingtime(analysis)

    # getting the max value of the dic with the settling times off all Nodes
    max_time = 0
    for node, time in settling_time.items():
        if max_time < time:
            max_time = time
    
    return settling_time, DC_values, max_time
   

def plot_voltages(analysis, max_time=False, save=False, plot_name=False, boundary=True):
    ''' TODO: Docstring
    '''
    nodes = get_nodes(analysis)

    # make standard plot 
    figure, ax = plt.subplots(figsize=(20, 6))
    for nd in nodes:
        ax.plot(analysis[nd])

    ax.set_xlabel('Time [ps]')
    ax.set_ylabel('Voltage (V)')
    ax.grid()
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    
    # add SettlingTime indicator
    if max_time != False:
        _dont_care_,_dont_care_,max_time = getMaxSettlingTime(analysis)
        plt.axvline(max_time, 0, 4, label='max_time',linewidth=4,color='r')

    # display lower and upper boarder of the settling time
    if boundary == True:
        DC_values = get_DC_voltage(analysis)
        # print(DC_values)
        # print(type(DC_values))
        for nd in nodes:
            if abs(DC_values[nd]) <= 0.1: # 0.1 
                # pass
                a=1
            else:
                # print(DC_values)
                plt.axhline(y=DC_values[nd]*1.02, ls= '--', color= 'grey', linewidth = 0.5)
                plt.axhline(y=DC_values[nd]*0.98, ls= '--', color= 'grey', linewidth = 0.5)

    # save or plot
    if save == True:
        plt.savefig("./simulation_plots/test/"+ plot_name + ".png")
    else:
        plt.show()


# ax.legend(['input', 'T1b','T1e','T2e','T3e','T4e'], loc='upper right')

# how to get the corresponding time to the voltage
# analysis.time[-1].value
