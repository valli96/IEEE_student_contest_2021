import pandas as pd
from tqdm import tqdm
from PySpice.Spice.Netlist import Circuit

import generation.functions as gen_func
import generation.graph as graph
from generation.device import device
from generation.node import node
from generation.nodeLink import nodeLink
from pathlib import Path

from ciruit_simulations.simulation_entry import circuit_simulation, getMaxSettlingTime, plot_voltages 
# from ciruit_simulations.analysis_tools import get_DC_voltage 

import cProfile
import pstats

pr = cProfile.Profile()
pr.enable()

# Settings-------------------------------------------------------------------------------
nlConfig_start  = 33                        # Offset for nlConfig loop
G_type          = "P4"
G               = graph.graph_P4()  	    # Choose graph type
DEBUG           = True                      # Enables debug print-outs

fig_path        = "./simulation_plots/plt_G_" + G_type + "_nl_" + str(nlConfig_start) + "/"
Path(fig_path).mkdir(parents=True, exist_ok=True)

# Initialize-----------------------------------------------------------------------------
node.check_link(node)

allNodes        = node.allNodes
allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nlConfigs       = gen_func.getNodeLinkConfigs(allNodeLinks, allNodes)   # type: pd.DataFrame
paramConfigs    = gen_func.getParameterConfigs(G.TL_count)              # type: pd.DataFrame

pd_results      = pd.DataFrame(columns=['graph','nlConfigID','paramConfigID','maxSettlingTime','nlConfigString','paramConfigString'])

print(nlConfigs)

# Iterate over nlConfigs and paramConfigs--------------------------------------
# ----------
for indx, nlConfig in tqdm( nlConfigs[nlConfig_start:].iterrows(), 
                            position=0, ncols=70,
                            initial=nlConfig_start, 
                            total=nlConfigs.shape[0] - 1, desc='nlConfig    ',
                            disable=DEBUG) :

   
    node.purge(node)
    nodeLink.configure(nodeLink, nlConfig)
        
    gen_func.synthesizeTopology(allNodeLinks, allDevices)
    device.check(device)

    for jndx, paramConfig in tqdm(  paramConfigs.iterrows(), 
                                    position=1, ncols=70,
                                    total=paramConfigs.shape[0] - 1, leave=False, desc='paramConfig ',
                                    disable=DEBUG) :

        # Circuit synth
        circName        = f"{G.name}_nlC{indx:03}_pC{jndx:03}"
        currCircuit     = gen_func.synthesizeCircuit(circName, G, paramConfig)    
        
        # if '1' in circName:
        #     import ipdb; ipdb.set_trace()
        
        # Simulation
        currAnalysis = circuit_simulation(currCircuit)
        settlingTime, DC_values, max_time   = getMaxSettlingTime(currAnalysis)

        print(circName)
        # print(circName)      
        plot_voltages(currAnalysis, max_time, save_path=False, plot_name=circName, boundary=True)
        

        # Save results
        nlConfigString      = str(nlConfig.to_list()).replace("'","")
        paramConfigString   = str(paramConfig.to_list()).replace("'","")


        pd_results.loc[len(pd_results)]     = [G.name, indx, jndx, max_time, nlConfigString, paramConfigString]
        a = 1

    pd_results.to_csv('results_' + G.name + '.csv')

pr.disable()
stats = pstats.Stats(pr).sort_stats('tottime')
stats.print_stats(20)


# TODO: Implement more graphs
# TODO: investigate and fix possible problems for type 3 and 4 vertices in synthesizeNodes

# DONE: Synthesize circuit
# DONE: implement TL permutations
# DONE: ->first make combinations -> config -> set values as permutations for TL and Devices
# DONE: Detect illegal device topologies (adjecent devices)
# DONE: maybe get device combinations instead of permutations
# DONE: Fix synth process 

a = 1
