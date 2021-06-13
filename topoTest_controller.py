from nodeLink import nodeLink
from vertex import vertex_type1, vertex_type2
from transLine import transLine
from node import node
from device import device
from typing import List
import itertools
import pandas as pd


T0  = transLine('T0', length=2)
T1  = transLine('T1', length=3)
T2  = transLine('T2', length=5)

D0  = device('D0')
D1  = device('D1')
D2  = device('D2')
D3  = device('D3')

v0  = vertex_type1('v0', T0.portA)
v1  = vertex_type2('v1', T0.portB, T1.portA)
v2  = vertex_type2('v2', T1.portB, T2.portA)
v3  = vertex_type1('v3', T2.portB)


def getNodeLinkConfigs(allNodeLinks : List[nodeLink]) :
    ''' Returns a list of possible nodeLink configurations '''  

    # Get all allowed configurations for each nodeLink
    allowedConfigsList  = list()

    for i in range(0, len(allNodeLinks)) :
        link    = allNodeLinks[i]
        
        allowed     = ['D']
        if (link.p_open) :
            allowed.append('O')
        if (link.p_short) :
            allowed.append('S')

        allowedConfigsList.append(allowed)

    # Get all permutation of allowed configurations
    configPermutations  = list(itertools.product(*allowedConfigsList))

    # Get config permutation with exactly four 'D' - devices
    validConfigPermutations = list()

    for i in range(0, len(configPermutations)) :
        if configPermutations[i].count('D') == 4 :
            validConfigPermutations.append(configPermutations[i])

    # Get different device permutations for each valid config permutation
    linkConfigList      = list()
    devicePermutations  = list(itertools.permutations(['D0', 'D1', 'D2', 'D3']))

    for validConfig in validConfigPermutations :
        for devicePerm in devicePermutations :

            detConfig   = list(validConfig)
            devicePerm  = list(devicePerm)
            deviceInds  = [index for index, value in enumerate(validConfig) if value == 'D']
            
            for deviceIndx, device in zip(deviceInds, devicePerm) :
                detConfig[deviceIndx] = device
            
            linkConfigList.append(detConfig)

    # Put list into df
    linkConfigs = pd.DataFrame(linkConfigList)

    print(str(len(linkConfigList)) + " nodeLink configurations generated")

    return linkConfigs

def configureNodeLinks(allNodeLinks : List[nodeLink], nodeLinkConfiguration) :
    ''' Configure nodeLinks according to linkConfiguration '''

    for nl, nlConf in zip (allNodeLinks, nodeLinkConfiguration) :
        nl.config   = nlConf

def synthesizeNodes(allNodeLinks : List[nodeLink], allDevices : List[device]) :
    ''' Sets node cID for circuit synthesis '''

    # Iterate over all nodeLinks and convert nodeIDs
    for nl in allNodeLinks :

        config  = nl.config
        
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

node.checkNodes(node)

allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nodeLinkConfigs = getNodeLinkConfigs(allNodeLinks)

configureNodeLinks(allNodeLinks, nodeLinkConfigs.loc[984])
nodeLink.checkNodeLinks(nodeLink)

synthesizeNodes(allNodeLinks, allDevices)


device.checkDevices(device)

# TODO: investigate and fix possible problems for type 3 and 4 vertices in synthesizeNodes
# TODO: implement TL permutations
# TODO: maybe get device combinations instead of permutations
# TODO: ->first make combinations -> config -> set values as permutations for TL and Devices


# DONE: Fix synth process 

[print(n.nodeID + "\t-> " + n.cID) for n in node.allNodes]
a = 1

