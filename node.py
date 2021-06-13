

class node :
    ''' The node is the basic connection unit. All nodes are unique during topology
        generation. Nodes may be merged after all nodeLinks have been established.
    '''

    allNodes    = []

    def __init__(self, nodeID) :
        ''' Initialize node object '''

        self.nodeID = nodeID
        self.links  = list()

        # Add this instance to allNodes
        self.allNodes.append(self)

    def checkNodes(cls) :
        ''' Checks if all nodes are linked '''

        for n in cls.allNodes :
            assert n.hasLink(), 'Node ' + n.nodeID + ' is not linked'
        
        print("All nodes are linked")

    def addLink(self, linkName) :
        ''' Add a linkName to node connections '''

        self.links.append(linkName)

    def hasLink(self) :
        ''' Returns if node is associated with a nodeLink '''

        return not (len(self.links) == 0)


class port :
    ''' Groups two nodes together. Ports are passed to vertex '''

    def __init__(self, node1 : node, node2 : node) :

        self.node1  = node1
        self.node2  = node2
