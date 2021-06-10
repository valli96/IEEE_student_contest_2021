import pdb
pdb.set_trace()
from nodeLink import nodeLink
from vertex import vertex_type1, vertex_type2
from transLine import transLine
from node import node
from ecu import ecu
from typing import List
import itertools
import pandas as pd


T1  = transLine('T1', length=2)
T2  = transLine('T2', length=3)
T3  = transLine('T3', length=5)

v0  = vertex_type1('v0', T1.portA)
v1  = vertex_type2('v1', T1.portB, T2.portA)
v2  = vertex_type2('v2', T2.portB, T3.portA)
v3  = vertex_type1('v3', T3.portB)


def getNodeLinkConfig(allNodeLinks : List[nodeLink]) :
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

    return linkConfigs

def configureNodeLinks(allNodeLinks : List[nodeLink], nodeLinkConfiguration) :
    ''' Configure nodeLinks according to linkConfiguration '''

    for nl, nlConf in zip (allNodeLinks, nodeLinkConfiguration) :
        nl.config   = nlConf



node.checkNodes(node)

allNodeLinks    = nodeLink.allNodeLinks
nodeLinkConfigs = getNodeLinkConfig(allNodeLinks)

configureNodeLinks(allNodeLinks, nodeLinkConfigs.loc[0])
nodeLink.checkNodeLinks(nodeLink)

# TODO: Implement ECUs or Devices with two nodes and a name
# TODO: Use configuration of nodeLinks to connect nodes to each other (or to ECUs) 

a = 1


