# TODO: This is broken due to relative imports


import itertools
import time
from typing import List

import pandas as pd
from tqdm import tqdm

from .graph import *
from .device import device
from .node import node
from .nodeLink import nodeLink


# Static constants-----------------------------------------------------------------------
TL_dict     = { 'L1' : 2,
                'L2' : 3,
                'L3' : 5,
                'L4' : 7}
                
TL_NAMES    = ['T0', 'T1', 'T2','T3']
DEVICE_NAMES= ['D0', 'D1', 'D2', 'D3']
ECU_NAMES   = ['ECU1', 'ECU2', 'ECU3', 'ECU4']

# Main functions-------------------------------------------------------------------------
def getNodeLinkConfigs(allNodeLinks : List[nodeLink], allNodes : List[node]) :
    ''' Returns a list of possible nodeLink configurations '''  

    def checkNodeLinkConfig(allNodes : List[node]) :
        ''' Checks if two devices are connected to each other. Returns bolean. '''

        n   = ...   # type: node
        nl  = ...   # type: nodeLink

        for n in allNodes :
            
            # Check if node has more than one link
            if len(n.links) == 1 :
                continue

            # Check if more than 1 nodeLink has device configuration
            devicesFound    = 0

            for nl in n.links :
                if (nl.config[0] == 'D') :
                    devicesFound    = devicesFound + 1

                if devicesFound > 1 :
                    return False

        return True

    # Get all allowed configurations for each nodeLink
    configs_01  = list()

    for nl in allNodeLinks :
        
        allowed     = ['D']
        if (nl.p_open) :
            allowed.append('O')
        if (nl.p_short) :
            allowed.append('S')

        configs_01.append(allowed)

    # Get all permutation of allowed configurations
    configs_02  = list(itertools.product(*configs_01))

    # Get config permutation with exactly four 'D' - devices
    configs_03  = list()

    for conf in configs_02 :
        if conf.count('D') == 4 :
            configs_03.append(list(conf))

    # Assign names D0 .. D3 to device placeholders
    deviceNames = ['D0', 'D1', 'D2', 'D3']

    for conf in configs_03 :
        deviceInds  = [index for index, value in enumerate(conf) if value == 'D']

        for deviceIndx, deviceName in zip(deviceInds, deviceNames) :
            conf[deviceIndx]   = deviceName

    # Temporarily configure nodeLinks to check for illegal device connections
    configs_04  = list()

    for conf in configs_03 :
        nodeLink.configure(nodeLink, conf) 
        node.check(node)

        if checkNodeLinkConfig(allNodes) :
            configs_04.append(conf)

        nodeLink.purge(nodeLink)

    # Put list into df and return
    nodeLinkConfigs = pd.DataFrame(configs_04)

    print(str(len(configs_04)) + " nodeLink configurations generated")
    return nodeLinkConfigs

def synthesizeTopology(allNodeLinks : List[nodeLink], allDevices : List[device]) :
    ''' Sets node cID for topology synthesis '''

    # Iterate over all nodeLinks and convert nodeIDs
    for nl in allNodeLinks :

        config  = nl.config

        if DEBUG :
            print('\n' + nl.name + ' with config ' + config)
                
        # Short circuit - directly connect nodes
        if (config == "S") :

            # TODO this will probably cause problems for type 3 and 4 vertices 
            # Check if nodes cID is still empty 
            assert (nl.nodeA.cID == None) and (nl.nodeB.cID == None), 'Nodes of nodeLink >' + nl.name + '< already have cID'
            
            newID   = nl.nodeA.nodeID + '__' + nl.nodeB.nodeID
            nl.nodeA.cID = newID
            nl.nodeB.cID = newID


        # Open circuit - add open suffix
        if (config == "O") :
            
            # Check if nodes cID is still empty
            if nl.nodeA.cID == None :
                nl.nodeA.cID = nl.nodeA.nodeID + '__O'
                
            if nl.nodeB.cID == None :
                nl.nodeB.cID = nl.nodeB.nodeID + '__O'


        # Device connected - connect nodes via device
        if (config.find("D") == 0) :

            # Get device object
            d   = ... # type: device     
            d   = [d for d in allDevices if d.name == config]
            d   = d[0]

            # Check if nodes cID is still empty
            if nl.nodeA.cID == None :
                nl.nodeA.cID    = nl.nodeA.nodeID + '__' + d.nodeA.nodeID

            if nl.nodeB.cID == None :
                nl.nodeB.cID    = nl.nodeB.nodeID + '__' + d.nodeB.nodeID

            d.nodeA.cID     = nl.nodeA.cID 
            d.nodeB.cID     = nl.nodeB.cID 

        if DEBUG :
            [print(n.nodeID + "\t-> " + str(n.cID)) for n in node.allNodes]

def getParameterConfigs(TL_count : int) :
    ''' Returns a list of all combinations from possible transmission line values
        and device names.

        TL_count (int):         Number of transmission lines used in current graph
    '''

    tl_perms    = list(itertools.permutations(list(TL_dict.keys()), TL_count))
    ecu_perms   = list(itertools.permutations(ECU_NAMES, 4))

    paraConfigs = list(itertools.product(tl_perms, ecu_perms))
    paraConfigs = [list(paraConfigRow[0] + paraConfigRow[1]) for paraConfigRow in paraConfigs] 
    paraConfigs = pd.DataFrame(paraConfigs, columns=(TL_NAMES[:TL_count] + DEVICE_NAMES))

    print(str(len(paraConfigs)) + " parameter configurations generated")
    return paraConfigs


# Settings-------------------------------------------------------------------------------
DEBUG       = False
G           = graph.graph_P4()

nlConfigOffset  = 0


# Initialize-----------------------------------------------------------------------------
node.check(node)

allNodes        = node.allNodes
allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nlConfigs       = getNodeLinkConfigs(allNodeLinks, allNodes)
paramConfigs    = getParameterConfigs(G.TL_count)

print(nlConfigs)

# Iterate over nlConfigs and paramConfigs------------------------------------------------
for indx, nlConfig in tqdm( nlConfigs[nlConfigOffset:].iterrows(), position=0, ncols=70, 
                            total=nlConfigs.shape[0] - 1 - nlConfigOffset, desc='nlConfig    ') :
   
    node.purge(node)
    nodeLink.configure(nodeLink, nlConfig)
        
    synthesizeTopology(allNodeLinks, allDevices)
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


