from node import node

class nodeLink :
    ''' Link between nodes within a vertex.

        Links have permission for different connection types
        - p_short:      Nodes can be connected electrically
        - p_open:       Nodes can be unconnected
        - p_device:     Nodes can be connected by an ECU

        Links can have a default electric connectiosn
        - solid:        Nodes are connected electrically by default
    '''

    def __init__(self, name, nodeA : node, nodeB : node, p_short, p_open, p_device, solid) :
        ''' Initializes nodeLink object

            name (str):         name of link
            nodeA (node):       connected node
            nodeB (node):       connected node
            p_short (bool):     permission for electric short
            p_open (bool):      permission for electric open
            p_device (bool):    permission to connect to ECU
            solid (bool):       sets connection to electric short by default
        '''

        self.name       = name      

        self.nodeA      = nodeA     
        self.nodeB      = nodeB    

        self.p_short    = p_short   
        self.p_open     = p_open    
        self.p_device   = p_device  
        self.solid      = solid

        # Associate nodeLink with node
        nodeA.addLink(name)
        nodeB.addLink(name)


class nodeLink_solid(nodeLink) :
    ''' nodeLink child class for solid links. Solid links are 
        - allowed to be electrically short
        - not allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        super().__init__(name, nodeA, nodeB, True, False, True, True)

class nodeLink_potential(nodeLink) :
    ''' nodeLink child class for potential links. Potential links are 
        - not allowed to be electrically short
        - allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        super().__init__(name, nodeA, nodeB, False, True, True, False)

class nodeLink_terminal(nodeLink) :
    ''' nodeLink child class for terminal links. Terminal links are 
        - allowed to be electrically short
        - allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        super().__init__(name, nodeA, nodeB, True, True, True, False)