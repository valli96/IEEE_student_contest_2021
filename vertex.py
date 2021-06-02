from node import port
from nodeLink import nodeLink_solid, nodeLink_potential, nodeLink_terminal


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


    def getPossibleLinkConfigs(self) :
        ''' Returns a list of possible nodeLink configurations '''

        a = 1


class vertex_type1(vertex) :
    ''' TODO docstring
    '''

    def __init__(self, name, TAport : port) :

        self.name   = name
        self.TAport = TAport

        # Connect nodeLinks
        self.nodeLink_t1    = nodeLink_terminal(name, TAport.node1, TAport.node2)

        nodeLinks   = [self.nodeLink_t1]

        super().__init__(name, nodeLinks)


class vertex_type2(vertex) :
    ''' TODO docstring
    '''

    def __init__(self, name, TAport : port, TBport : port) :
        ''' TODO
        '''

        self.name   = name
        self.TAport = TAport
        self.TBport = TBport

        # Connect nodeLinks
        self.nodeLink_s1    = nodeLink_solid(name, TAport.node1, TBport.node1)
        self.nodeLink_s2    = nodeLink_solid(name, TAport.node2, TBport.node2)
        self.nodeLink_p1    = nodeLink_potential(name, TAport.node1, TAport.node2)

        nodeLinks   = [self.nodeLink_s1, self.nodeLink_s2, self.nodeLink_p1]

        super().__init__(name, nodeLinks)

    


        

        

       
