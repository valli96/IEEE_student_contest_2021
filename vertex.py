from transLine import transLine
from node import port
from nodeLink import nodeLink_solid, nodeLink_potential


# Only type 2 vertex implemented for testing and development

class vertex_type2 :
    ''' TODO docstring
    '''

    def __init__(self, name, portA : port, portB : port) :
        '''
            TODO
        '''

        self.name   = name

        self.portA  = portA
        self.portB  = portB

        # Connect solid nodeLinks
        self.nodeLink_s1    = nodeLink_solid(name + '_nlsA1B1', portA.node1, portB.node1)
        self.nodeLink_s2    = nodeLink_solid(name + '_nlsA2B2', portA.node2, portB.node2)

        # Connect potential nodeLinks
        self.nodeLink_p1    = nodeLink_potential(name + '_nlpA1A2', portA.node1, portA.node2)

        

        

       
