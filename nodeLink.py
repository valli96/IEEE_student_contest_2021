from node import node

class nodeLink :
    ''' Link between nodes within a vertex.

        Links have permission for different connection types
        - p_short:      Nodes can be connected electrically
        - p_open:       Nodes can be unconnected
    '''

    allNodeLinks   = []

    def __init__(self, name, nodeA : node, nodeB : node, p_short, p_open) :
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

        self.config     = None      # Node configuration (Device, Open, Short)
        

        # Associate nodeLink with node
        nodeA.addLink(name)
        nodeB.addLink(name)

        # Add this instance to allNodeLinks
        self.allNodeLinks.append(self)


class nodeLink_solid(nodeLink) :
    ''' nodeLink child class for solid links. Solid links are 
        - allowed to be electrically short
        - not allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        newName = name + '_nls_' + nodeA.nodeID + '_' + nodeB.nodeID  
        super().__init__(newName, nodeA, nodeB, True, False)

class nodeLink_potential(nodeLink) :
    ''' nodeLink child class for potential links. Potential links are 
        - not allowed to be electrically short
        - allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        newName = name + '_nlp_' + nodeA.nodeID + '_' + nodeB.nodeID
        super().__init__(newName, nodeA, nodeB, False, True)

class nodeLink_terminal(nodeLink) :
    ''' nodeLink child class for terminal links. Terminal links are 
        - allowed to be electrically short
        - allowed to be electrically open
        - allowed to receive ECUs 
    '''

    def __init__(self, name, nodeA : node, nodeB : node,):

        newName = name + '_nlt_' + nodeA.nodeID + '_' + nodeB.nodeID
        super().__init__(newName, nodeA, nodeB, True, True)