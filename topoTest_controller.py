import pdb
pdb.set_trace()
from nodeLink import nodeLink
from vertex import vertex, vertex_type1, vertex_type2
from transLine import transLine
from node import node
from ecu import ecu


T1  = transLine('T1', length=2)
T2  = transLine('T2', length=3)
T3  = transLine('T3', length=3)

v0  = vertex_type1('v0', T1.portA)
v1  = vertex_type2('v1', T1.portB, T2.portA)
v2  = vertex_type2('v2', T2.portB, T3.portA)
v3  = vertex_type1('v3', T3.portB)


def checkNodes(anyNode : node) :
    ''' Checks if all nodes are linked '''

    a = 1


def getLinkConfigList(allLinks) :
    ''' Returns a list of possible nodeLink configurations '''  

    for i in range(0, len(allLinks)) :
        link    = allLinks[i]
        print(link.name)


    a = 1


allNodeLinks    = v0.nodeLink_t1.allNodeLinks
linkConfigList  = getLinkConfigList(allNodeLinks)




a = 1


