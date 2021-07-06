import pandas as pd
from PySpice.Spice.Netlist import Circuit

import generation.functions as gen_func
import generation.graph as graph
from generation.device import device
from generation.node import node
from generation.nodeLink import nodeLink

from ciruit_simulations.simulation_entry import circuit_simulation, getMaxSettlingTime, plot_voltages 
# from ciruit_simulations.analysis_tools import get_DC_voltage 

graph_dict      = { 'P3' : graph.graph_P3,
                    'P4' : graph.graph_P4,
                    'P5' : graph.graph_P5,
                    'K3' : graph.graph_K3,
                    'K2,2'  : graph.graph_K2x2,
                    'K1,3a' : graph.graph_K1x3a,
                    '3-PANa': graph.graph_3PANa,
                    'CHAIRa': graph.graph_CHAIRa,
                    'K1,4a' : graph.graph_K1x4a} 

# Settings-------------------------------------------------------------------------------
inputCircName   = 'P4_nlC020_pC002'         # Input circuit name
reRunSimulation = False                     

#----------------------------------------------------------------------------------------


# Initialize
circProps   = inputCircName.split('_')

G           = graph_dict[circProps[0]]()
nlC         = int(circProps[1][3:])
pC          = int(circProps[2][2:])

node.check_link(node)

allNodes        = node.allNodes
allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nlConfigs       = gen_func.getNodeLinkConfigs(allNodeLinks, allNodes)   # type: pd.DataFrame
paramConfigs    = gen_func.getParameterConfigs(G.TL_count)              # type: pd.DataFrame

pd_results      = pd.DataFrame(columns=['graph','nlConfigID','paramConfigID','maxSettlingTime','nlConfigString','paramConfigString'])

nlConfig        = nlConfigs.loc[nlC]
paramConfig     = paramConfigs.loc[pC]


# Build graph
node.purge(node)
nodeLink.configure(nodeLink, nlConfig)

gen_func.synthesizeTopology(allNodeLinks, allDevices)
device.check(device)


# Circuit synth
circName        = f"{G.name}_nlC{nlC:03}_pC{pC:03}"
currCircuit     = gen_func.synthesizeCircuit(circName, G, paramConfig)    


# Print results
nlConfigString      = str(nlConfig.to_list()).replace("'","")
paramConfigString   = str(paramConfig.to_list()).replace("'","")

print('\ngraph: ' + G.name)

print('\nnode link config: ' + str(nlC))
print(nlConfigString)

print('\nparam config: ' + str(pC))
print(paramConfigString)

print('\nNetlist:')
print(currCircuit)


# Simulation
if reRunSimulation :

    currAnalysis = circuit_simulation(currCircuit)
    settlingTime, DC_values, max_time   = getMaxSettlingTime(currAnalysis)
    
    print(circName)      
    plot_voltages(currAnalysis, max_time, save=False, plot_name=circName, boundary=True)


