

class ecu :
    ''' TODO docstring
    '''

    # Nodes
    nodes   = { 'nodeA' : None,
                'nodeB' : None}
    nodeA   = None
    nodeB   = None

    def __init__(self, type) :
        ''' Initializes ecu object

        
        '''

        self.type = type
        

    def checkNodes(self) :
        ''' Checks if all nodes are assigned to an ID. Returns list of node IDs if all
            nodes are assigned. Returns False if not.
        '''

        if all(not [self.nodeA, self.nodeB] == None) :
            
            return True