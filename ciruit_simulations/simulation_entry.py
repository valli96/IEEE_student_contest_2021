import PySpice
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from .analysis_tools import get_DC_voltage, get_settlingtime
import os



def getMaxSettlingTime(testCircuit : Circuit, step_time=1e-11, end_time=100e-9) :
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
    
    # calculation of the settling_time
    DC_values = get_DC_voltage(analysis)
    settling_time = get_settlingtime(analysis)
    return settling_time
    
   

