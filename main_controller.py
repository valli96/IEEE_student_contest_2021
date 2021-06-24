import time

import pandas as pd
from tqdm import tqdm


import generation.graph as graph
from generation.device import device
from generation.node import node
from generation.nodeLink import nodeLink
import generation.functions as gen_func


# Settings-------------------------------------------------------------------------------
G               = graph.graph_P4()
nlConfigOffset  = 0


# Initialize-----------------------------------------------------------------------------
node.check(node)

allNodes        = node.allNodes
allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nlConfigs       = gen_func.getNodeLinkConfigs(allNodeLinks, allNodes)   # type: pd.DataFrame
paramConfigs    = gen_func.getParameterConfigs(G.TL_count)              # type: pd.DataFrame

print(nlConfigs)

# Iterate over nlConfigs and paramConfigs------------------------------------------------
for indx, nlConfig in tqdm( nlConfigs[nlConfigOffset:].iterrows(), position=0, ncols=70, 
                            total=nlConfigs.shape[0] - 1 - nlConfigOffset, desc='nlConfig    ') :
   
    node.purge(node)
    nodeLink.configure(nodeLink, nlConfig)
        
    gen_func.synthesizeTopology(allNodeLinks, allDevices)
    device.checkDevices(device)

    for jndx, paramConfig in tqdm(paramConfigs.iterrows(), position=1, ncols=70,
                                  total=paramConfigs.shape[0] - 1, leave=False, desc='paramConfig ') :

        time.sleep(0.01)
        a = 1



# TODO: Synthesize circuit
# TODO: investigate and fix possible problems for type 3 and 4 vertices in synthesizeNodes

# DONE: implement TL permutations
# DONE: ->first make combinations -> config -> set values as permutations for TL and Devices
# DONE: Detect illegal device topologies (adjecent devices)
# DONE: maybe get device combinations instead of permutations
# DONE: Fix synth process 



a = 1


