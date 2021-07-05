from .vertex import vertex, vertex_type1, vertex_type2
from .transLine import transLine
from .device import device

from typing import List


class graph :
    ''' Stores vertices and transLines and their relationship in a graph structure.
        Additionally stores devices and a name.

        This class should be treated as an abstract class. Only one child should be
        initialized at a given time to avoid creating nodes with the same ID.
    '''

    initCount   = 0     # Counts the initialisations, should never exceed 1

    def __init__(self, name, transLines : List[transLine], vertices : List[vertex]) :
        
        graph.initCount  = graph.initCount + 1

        assert graph.initCount <= 1, 'One graph has already been initialised. Only one graph init is permissible.' 

        self.name   = name

        D0  = device('D0')
        D1  = device('D1')
        D2  = device('D2')
        D3  = device('D3')

        self.devices    = [D0, D1, D2, D3]
        self.transLines = transLines
        self.vertices   = vertices

        self.TL_count   = len(transLines)


class graph_P3(graph) : 
    ''' P3 graph '''

    def __init__(self) :

        T0  = transLine('T0')
        T1  = transLine('T1')

        v0  = vertex_type1('v0', T0.portA)
        v1  = vertex_type2('v1', T0.portB, T1.portA)
        v2  = vertex_type1('v2', T1.portB)

        super().__init__('P3', [T0, T1], [v0, v1, v2])

class graph_P4(graph) :
    ''' P4 graph '''

    def __init__(self) :

        T0  = transLine('T0')
        T1  = transLine('T1')
        T2  = transLine('T2')

        v0  = vertex_type1('v0', T0.portA)
        v1  = vertex_type2('v1', T0.portB, T1.portA)
        v2  = vertex_type2('v2', T1.portB, T2.portA)
        v3  = vertex_type1('v3', T2.portB)

        super().__init__('P4', [T0, T1, T2], [v0, v1, v2, v3])
