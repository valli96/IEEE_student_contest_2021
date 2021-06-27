import itertools
from typing import List
from unicodedata import name

import pandas as pd
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from .device import device
from .graph import graph
from .node import node
from .nodeLink import nodeLink

# Static constants-----------------------------------------------------------------------
TL_dict     = { 'L1' : 2,       # TL length [m]
                'L2' : 3,
                'L3' : 5,
                'L4' : 7}

ECU_dict    = { 'ECU1' : 120,   # ECU impedance [Ohm]
                'ECU2' : 1e6,
                'ECU3' : 1e6,
                'ECU4' : 120}
                
TL_NAMES    = ['T0', 'T1', 'T2','T3']
DEVICE_NAMES= ['D0', 'D1', 'D2', 'D3']
ECU_NAMES   = ['ECU1', 'ECU2', 'ECU3', 'ECU4']

DEBUG       = False


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
        node.check_link(node)

        if checkNodeLinkConfig(allNodes) :
            configs_04.append(conf)

        nodeLink.purge(nodeLink)

    # Put list into df and return
    nodeLinkConfigs = pd.DataFrame(configs_04)

    print(str(len(configs_04)) + " nodeLink configurations generated")
    return nodeLinkConfigs

def synthesizeTopology(allNodeLinks : List[nodeLink], allDevices : List[device]) :
    ''' Sets all node cIDs for topology synthesis '''

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

    # Check if all nodes have cID
    node.check_cID(node)

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

def synthesizeCircuit(circName : str, currGraph : graph, paramSet : pd.Series) :
    ''' Synthesizes a circuit object for pyspice simulation from a given topology (fully
        configured graph) and a fixed set of parameters.

        - All LosslessTransmissionLine impedances are 120 Ohm
        - LosslessTransmissionLine length gets converted to a delay with c = 2 * 10e8
        - ECU values: 
            ECU1: 4V step source with 120 Ohm (implemented as pulse source)
            ECU2: 1 MOhm
            ECU3: 1 MOhm
            ECU4: 120 Ohm
    '''
    
    c   = 2 * 10e8

    # Check if graph is fully configured
    nodeLink.check(nodeLink)
    device.check(device)
    node.check_link(node)
    node.check_cID(node)


    # Init circuit 
    circ    = Circuit(circName)


    # Find ground nodes and replace cID
    dvName  = (pd.Series(paramSet.index.values, index=paramSet ))['ECU1']
    dvECU1  = [device for device in currGraph.devices if device.name == dvName][0]
    gndCID  = dvECU1.nodeB.cID
    gndNodes= [n for n in node.allNodes if n.cID == gndCID]

    for n in gndNodes:
        n.cID   = circ.gnd

    # Init LosslessTransmissionLine objects within circuit
    for tl in currGraph.transLines :
        tlName  = '_' + paramSet[tl.name]
        outHigh = tl.nodeB1.cID
        outLow  = tl.nodeB2.cID
        inHigh  = tl.nodeA1.cID
        inLow   = tl.nodeA2.cID
        delay   = TL_dict[paramSet[tl.name]] / c

        circ.LosslessTransmissionLine(tlName, outHigh, outLow, inHigh, inLow, impedance=120, time_delay=delay)
        
    # Init devices
    for dv in currGraph.devices :
        dvConf  = paramSet[dv.name]

        # Special treatment for ECU1 -> source
        if dvConf == 'ECU1' :
            dvName  = '_' + dvConf
            high    = dv.nodeA.cID
            low     = dv.nodeB.cID
            imped   = ECU_dict[dvConf]

            circ.PulseVoltageSource('_pulse', 'v_out', low, 0@u_V, 4@u_V, 30@u_us, 60@u_us, 0@u_us, 2@u_ns, 2@u_us)
            circ.R(dvName, 'v_out', high, imped)

        # Normal ECUs
        else :
            dvName  = '_' + dvConf
            high    = dv.nodeA.cID
            low     = dv.nodeB.cID
            imped   = ECU_dict[dvConf]

            circ.R(dvName, high, low, imped)

    
    return circ
