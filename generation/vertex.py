from .node import port
from .nodeLink import nodeLink_solid, nodeLink_potential, nodeLink_terminal


# Only type 2 vertex implemented for testing and development

class vertex :
    ''' TODO
    '''

    def __init__(self, name, nodeLinks) :
        ''' TODO
        '''

        self.name       = name
        self.nodeLinks  = nodeLinks


    def printLinkNames(self) :
        ''' Prints the name of all nodeLinks within the vertex '''

        for nl in self.nodeLinks :
            print(nl.name)


class vertex_type1(vertex) :
    ''' Terminal vertex connecting to 1 port
    '''

    def __init__(self, name, TAport : port) :

        self.name   = name
        self.TAport = TAport

        # Connect nodeLinks
        self.nodeLink_t0    = nodeLink_terminal(name, TAport.node1, TAport.node2)

        nodeLinks   = [self.nodeLink_t0]

        super().__init__(name, nodeLinks)

class vertex_type2(vertex) :
    ''' Vertex connecting 2 ports
    '''

    def __init__(self, name, TAport : port, TBport : port) :
        ''' TODO
        '''

        self.name   = name
        self.TAport = TAport
        self.TBport = TBport

        # Connect nodeLinks
        self.nodeLink_s0    = nodeLink_solid(name, TAport.node1, TBport.node1)
        self.nodeLink_s1    = nodeLink_solid(name, TAport.node2, TBport.node2)
        self.nodeLink_p0    = nodeLink_potential(name, TAport.node1, TAport.node2)

        nodeLinks   = [self.nodeLink_s0, self.nodeLink_s1, self.nodeLink_p0]

        super().__init__(name, nodeLinks)
    
class vertex_type3a(vertex) :
    ''' Vertex connecting 3 ports in serial configuration (a)
    '''

    def __init__(self, name, TAport : port, TBport : port, TCport : port) :
        ''' TODO
        '''

        self.name   = name
        self.TAport = TAport
        self.TBport = TBport
        self.TCport = TCport

        # Connect nodeLinks
        self.nodeLink_s0    = nodeLink_solid(name, TAport.node1, TBport.node1)
        self.nodeLink_s1    = nodeLink_solid(name, TBport.node2, TCport.node1)
        self.nodeLink_s2    = nodeLink_solid(name, TCport.node2, TAport.node2)

        self.nodeLink_p0    = nodeLink_potential(name, TAport.node1, TAport.node2)
        self.nodeLink_p1    = nodeLink_potential(name, TBport.node1, TBport.node2)
        self.nodeLink_p2    = nodeLink_potential(name, TCport.node1, TCport.node2)

        nodeLinks   = [self.nodeLink_s0, self.nodeLink_s1, self.nodeLink_s2,
                       self.nodeLink_p0, self.nodeLink_p1, self.nodeLink_p2]

        super().__init__(name, nodeLinks)

class vertex_type3b(vertex) :
    ''' Vertex connecting 3 ports in parallel configuration (b)
        NOT IMPLEMENTED YET
    '''

    def __init__(self) :
        ''' TODO
        '''

        assert 0, 'vertex type 3b not implemented yet'

class vertex_type4a(vertex) :
    ''' Vertex connecting 4 ports in purley serial configuration (a)
    '''

    def __init__(self, name, TAport : port, TBport : port, TCport : port, TDport : port) :
        ''' TODO
        '''

        self.name   = name
        self.TAport = TAport
        self.TBport = TBport
        self.TCport = TCport
        self.TDport = TDport

        # Connect nodeLinks
        self.nodeLink_s0    = nodeLink_solid(name, TAport.node1, TBport.node2)
        self.nodeLink_s1    = nodeLink_solid(name, TBport.node1, TCport.node2)
        self.nodeLink_s2    = nodeLink_solid(name, TCport.node1, TDport.node2)
        self.nodeLink_s3    = nodeLink_solid(name, TDport.node1, TAport.node2)

        self.nodeLink_p0    = nodeLink_potential(name, TAport.node1, TAport.node2)
        self.nodeLink_p1    = nodeLink_potential(name, TBport.node1, TBport.node2)
        self.nodeLink_p2    = nodeLink_potential(name, TCport.node1, TCport.node2)
        self.nodeLink_p3    = nodeLink_potential(name, TDport.node1, TDport.node2)

        nodeLinks   = [self.nodeLink_s0, self.nodeLink_s1, self.nodeLink_s2, self.nodeLink_s3,
                       self.nodeLink_p0, self.nodeLink_p1, self.nodeLink_p2, self.nodeLink_p3]

        super().__init__(name, nodeLinks)

class vertex_type4b(vertex) :
    ''' Vertex connecting 4 ports in partially parallel and serial configuration (b)
        NOT IMPLEMENTED YET
    '''

    def __init__(self) :
        ''' TODO
        '''

        assert 0, 'vertex type 4b not implemented yet'

class vertex_type4c(vertex) :
    ''' Vertex connecting 4 ports in purely parallel configuration (c)
        NOT IMPLEMENTED YET
    '''

    def __init__(self) :
        ''' TODO
        '''

        assert 0, 'vertex type 4c not implemented yet'

