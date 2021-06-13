

class node :
    ''' The node is the basic connection unit. All nodes are unique during topology
        generation. Nodes may be merged after all nodeLinks have been established.
    '''

    allNodes    = []

    def __init__(self, nodeID) :
        ''' Initialize node object '''

        self.nodeID = nodeID
        self.links  = list()
        self.cID    = None      # ID used for circuit synth, changes for each config

        # Add this instance to allNodes
        self.allNodes.append(self)

    def checkNodes(cls) :
        ''' Checks if all nodes are linked '''

        for n in cls.allNodes :
            assert len(n.links) > 0, 'Node >' + n.nodeID + '< is not linked'
        
        print("All nodes are linked")

    def addLink(self, linkName) :
        ''' Add a linkName to node connections '''

        self.links.append(linkName)



class port :
    ''' Groups two nodes together. Ports are passed to vertex '''

    def __init__(self, node1 : node, node2 : node) :

        self.node1  = node1
        self.node2  = node2