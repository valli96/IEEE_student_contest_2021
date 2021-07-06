import cProfile
import pstats
from pathlib import Path
import random
import csv

# For Time Out hander----------------------------------------
# import time
# from multiprocessing import Process, Queue
#------------------------------------------------------------

import pandas as pd
from PySpice.Spice.Netlist import Circuit
from tqdm import tqdm

import generation.functions as gen_func
import generation.graph as graph
from ciruit_simulations.simulation_entry import (circuit_simulation,
                                                 getMaxSettlingTime,
                                                 plot_voltages)
from generation.device import device
from generation.node import node
from generation.nodeLink import nodeLink



# Def Time Out hander-------------------------------------------------
# def analysis_timeout_handler(Circuit):

#     Analysis = circuit_simulation(Circuit.get(), end_time=3e-7)
#     Circuit.put(Analysis) 


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

# Settings-------------------------------------------------------------------------------
    Nr_of_simulations   = 50
    G                   = graph.graph_P3()  	    # Choose graph type
    DEBUG               = True                      # Enables debug print-outs
    stepTime            = 5e-11

# Initialize-----------------------------------------------------------------------------
    fig_path        = "./simulation_plots/plt_G_" + G.name + "_monteC" + "/"

    Path(fig_path).mkdir(parents=True, exist_ok=True)

    node.check_link(node)

    allNodes        = node.allNodes
    allNodeLinks    = nodeLink.allNodeLinks
    allDevices      = device.allDevices

    nlConfigs       = gen_func.getNodeLinkConfigs(allNodeLinks, allNodes)   # type: pd.DataFrame
    paramConfigs    = gen_func.getParameterConfigs(G.TL_count)              # type: pd.DataFrame

    pd_results      = pd.DataFrame(columns=['graph','nlConfigID','paramConfigID','maxSettlingTime','nlConfigString','paramConfigString'])

    if DEBUG :
        print(nlConfigs)


# Iterate over random nlConfigs and paramConfigs-----------------------------------------
    for i in tqdm(range(0, Nr_of_simulations), 
                                position=0, ncols=70,
                                total=Nr_of_simulations, desc='randomConfig ',
                                disable=DEBUG) :

        # Assignments
        nlC_indx    = random.randint(0, len(nlConfigs) - 1)
        pC_indx     = random.randint(0, len(paramConfigs) - 1)

        nlConfig    = nlConfigs.loc[nlC_indx]
        paramConfig = paramConfigs.loc[pC_indx]

        # Init
        node.purge(node)
        nodeLink.configure(nodeLink, nlConfig)
            
        gen_func.synthesizeTopology(allNodeLinks, allDevices)
        device.check(device)     

        # Circuit synth
        circName        = f"{G.name}_nlC{nlC_indx:03}_pC{pC_indx:03}"
        currCircuit     = gen_func.synthesizeCircuit(circName, G, paramConfig)    
     

        if DEBUG :
            print(circName + ': ', end='')
            
        try:
            currAnalysis = circuit_simulation(currCircuit, step_time=stepTime, end_time=5e-7)

        except NameError:
            print("___ Error Timestep too small ___" )
            continue

        # Get max settling time and plot if useful
        settlingTime, DC_values, max_time   = getMaxSettlingTime(currAnalysis)   
        plot_voltages(currAnalysis, max_time, save_path=fig_path, plot_name=circName, boundary=True, set_time_min=4000)
        
        if DEBUG :
            print(str(max_time))


        # Save results
        nlConfigString      = str(nlConfig.to_list()).replace("'","")
        paramConfigString   = str(paramConfig.to_list()).replace("'","")


        with open('./results/resultsMC_' + G.name + '.csv', 'a', newline='') as csvfile:
            writer  = csv.writer(csvfile)
            row     = [G.name, nlC_indx, pC_indx, max_time, nlConfigString, paramConfigString]
            writer.writerow(row)
        
        
    pr.disable()
    if DEBUG :
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
