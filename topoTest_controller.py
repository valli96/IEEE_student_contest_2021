import pdb
from nodeLink import nodeLink
from vertex import vertex_type1, vertex_type2
from transLine import transLine
from node import node
from device import device
from typing import List
import itertools
import pandas as pd


T0  = transLine('T0')
T1  = transLine('T1')
T2  = transLine('T2')

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

        if checkNodeLinkConfig(node.allNodes) :
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


# Do once
node.check(node)

allNodes        = node.allNodes
allNodeLinks    = nodeLink.allNodeLinks
allDevices      = device.allDevices

nlConfigs       = getNodeLinkConfigs(allNodeLinks)



nodeLink.purge(nodeLink)
nodeLink.configure(node, nlConfigs.loc[0])

synthesizeTopology(allNodeLinks, allDevices)
device.checkDevices(device)






# TODO: investigate and fix possible problems for type 3 and 4 vertices in synthesizeNodes
# TODO: implement TL permutations
# TODO: ->first make combinations -> config -> set values as permutations for TL and Devices
# TODO: Detect illegal device topologies (adjecent devices)

# DONE: maybe get device combinations instead of permutations
# DONE: Fix synth process 

print(nodeLinkConfigs)
[print(n.nodeID + "\t-> " + n.cID) for n in node.allNodes]
a = 1


