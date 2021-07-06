import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
# from .analysis_tools import get_DC_voltage, get_settlingtime
from PySpice.Probe.Plot import plot
import matplotlib.pyplot as plt
import os
import PySpice.Probe.WaveForm
import pandas as pd

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

def detective_divergence(voltage):
    # print(voltage.iloc[-1].item())
    if 0.05 < abs(voltage.iloc[-1].item())%1 < 0.95:
        return True
    else:
        return False

def get_settlingtime(analysis):
    ''' TODO: Docstring
    '''
    number_simulations = get_data_points(analysis)
    nodes = get_nodes(analysis)
    DC_values = get_DC_voltage(analysis)
    settling_time = {}
    
    for node in nodes:
        # print(str(DC_values[node])+ 'DC_values of Node')   
        if abs(DC_values[node]) <= 0.05: # 0.1 
            # pass
            a=1
        else:

            voltage     = pd.DataFrame(analysis[node])
            high        = abs(voltage) >= abs(DC_values[node]) * 1.02
            low         = abs(voltage) <= abs(DC_values[node]) * 0.98
            unsettled   = high | low
            # print(unsettled) 
            # print((unsettled[unsettled==True].index.tolist()[-1]))
            # print (unsettled[unsettled==True].index[-1])
                 
            divergence = detective_divergence(voltage)
            if divergence == True:
                # print(node + " divergence")                       
                continue 
            settling_time[node] = unsettled[unsettled==True].last_valid_index()
                # break

            # if settling_time[node]> 1000:
            #     import ipdb; ipdb.set_trace()


            # old approach
            # for i in range(number_simulations):
            #     voltage = analysis[node][number_simulations - 1 - i].value
            #     if (abs(voltage) >= abs(DC_values[node])*1.02 or abs(voltage) <= abs(DC_values[node])*0.98):
            #         DC_values[node] = number_simulations-i
            #         settling_time[node] = number_simulations-i
            #         break
            # print(str(settling_time))
    
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

def getMaxSettlingTime(analysis, ignore_div=True):

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
    
    number_simulations = get_data_points(analysis)
   
    # Ignores the diverging nodes

    # print("number_simulations =  " + str(number_simulations))
    # print("max_time =  " + str(max_time))
    if ignore_div == True and number_simulations == max_time:
        max_time = 0
    
    return settling_time, DC_values, max_time


def resize_plot(plt, settling_time, simulation_steps):
    if settling_time > simulation_steps - 1000:
        plt.xlim(0, simulation_steps)
    else: 
        plt.xlim(0, settling_time+1000)


def plot_voltages(analysis, max_time=False, resize=True, save_path=False, plot_name=False, boundary=True, set_time_min=False):
    ''' TODO: Docstring
    '''
    if max_time < set_time_min:
        pass
    else:
        nodes = get_nodes(analysis)

        # make standard plot 
        figure, ax = plt.subplots(figsize=(20, 6))
        for nd in nodes:
            ax.plot(analysis[nd])

        ax.set_xlabel('Simulation Steps')
        ax.set_ylabel('Voltage (V)')
        ax.grid()
        ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
        
        # add SettlingTime indicator
        if max_time:
            plt.axvline(max_time, 0, 4, label='max_time',linewidth=4,color='r')
            # if max_time > 1000:
            #     plt.xlim
            plt.title("Settling time = "+ str(max_time))

        # display lower and upper boarder of the settling time
        if boundary == True:
            DC_values = get_DC_voltage(analysis)
            
            for nd in nodes:
                if abs(DC_values[nd]) <= 0.05: # 0.1 
                    # pass
                    a=1
                else:
                    # print(DC_values)
                    plt.axhline(y=DC_values[nd]*1.02, ls= '--', color= 'grey', linewidth = 0.5)
                    plt.axhline(y=DC_values[nd]*0.98, ls= '--', color= 'grey', linewidth = 0.5)
        
        

        # import ipdb; ipdb.set_trace()
        if resize == True:
            resize_plot(plt, max_time, get_data_points(analysis))

        # save or plot
        if save_path:
            plt.savefig(save_path + plot_name +"__" +str(max_time)+".png")
        else:
            plt.show()

# ax.legend(['input', 'T1b','T1e','T2e','T3e','T4e'], loc='upper right')

# how to get the corresponding time to the voltage
# analysis.time[-1].value

