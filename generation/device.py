from node import node

class device :
    ''' The device object is a placeholder object for an ECU. 
        No concrete ECU parameters are set here, this must be done later in synthesis.
    '''

    allDevices  = []

    def __init__(self, name) :
        ''' Initializes device object

            name (str):         name of device (choose from D0..D3)
        '''

        self.name       = name    

        self.nodeA      = node(name + "_nA")
        self.nodeB      = node(name + "_nB")

        self.nodeA.addLink('dummy device link ' + name + "_nA")
        self.nodeB.addLink('dummy device link ' + name + "_nB")

        # Add this instance to allDevices
        self.allDevices.append(self)

    def checkDevices(cls) :
        ''' Checks if all devices are connected '''

        for d in cls.allDevices :
            assert (not d.nodeA == None) and (not d.nodeB == None), 'device ' + d.name + ' is not connected'

    def connect(self, nodeA : node, nodeB : node) :
        ''' Connects device nodes to transmission line nodes

            nodeA (node):       connected node
            nodeB (node):       connected node
        '''

        self.nodeA  = nodeA
        self.nodeB  = nodeB

  
