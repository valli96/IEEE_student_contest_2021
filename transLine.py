from node import node, port


class transLine :
    ''' TODO Docstring
    '''

    def __init__(self, name, length=None, delay=None, impedance=120) :
        ''' Initializes transLine object

            length (float):     Length of transmission line in meters
            delay (float):      Delay of transmission line in ns
            impedance (float):  Impedance of transmission line

            Either length or delay must be given. In case both are given, delay takes
            priority. In case only length is given, c = 2 * 10e8 is assumed.

        '''
        
        self.name       = name
        self.impedance  = impedance
        
        self.nodeA1     = node(name + '_nA1')
        self.nodeA2     = node(name + '_nA2')
        self.nodeB1     = node(name + '_nB1')
        self.nodeB2     = node(name + '_nB2')

        self.portA      = port(self.nodeA1, self.nodeA2)
        self.portB      = port(self.nodeB1, self.nodeB2)
        
        # Get delay parameter
        if not delay == None :
            self.delay  = delay

        elif not length == None :
            self.delay  = length / (2 * 10e8) * 10e9

        else :
            assert 0, 'transLine needs length and/or delay parameter'
        

        

