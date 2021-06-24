from .node import node, port


class transLine :
    ''' TODO Docstring
    '''

    allTransLines   = []

    def __init__(self, name) :
        ''' Initializes transLine object

            name (str):         name of transmission line (choose from T0..T3)
        '''
        
        self.name       = name
        
        self.nodeA1     = node(name + '_nA1')
        self.nodeA2     = node(name + '_nA2')
        self.nodeB1     = node(name + '_nB1')
        self.nodeB2     = node(name + '_nB2')

        self.portA      = port(self.nodeA1, self.nodeA2)
        self.portB      = port(self.nodeB1, self.nodeB2)    

        # Add this instance to allTransLines
        self.allTransLines.append(self)
