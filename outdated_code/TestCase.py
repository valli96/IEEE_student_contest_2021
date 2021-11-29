import pandas as pd
import numpy as np
import itertools

from pandas._config import config

dict_vertexConfig    = {0 : 0,  #'nothing'),
                        1 : 1,  #'upperSeriesECU'),
                        2 : 1,  #'lowerSeriesECU'),
                        3 : 2,  #'bothSeriesECU'),
                        4 : 1,  #'parallelECU')
                        }

class TestCase :
    """ TODO: docString

    """

    class TM :
        """ Transmission line """

        def __init__(self, name, node1, node2, node3, node4) :
            a = 2

    def __init__(self) :
        """ Generic init to instantiate object vars. 
        """

        self.pd_graphs          = pd.DataFrame()
        self.list_graphEdges    = list()

    def loadGraphs(self, relFilePath) :
        """ Load topology graphs from csv file and process data into usable format.
            Return results and store results as object attributes.
        """

        pd_graphInfo    = pd.read_csv(relFilePath, sep=";")
        list_graphEdges = list()

        print("Loading graphs from " + relFilePath)

        # Iterate over each topology
        for _, graph in pd_graphInfo.iterrows() :

            edgeString  = graph['edges']
            n_vertices  = graph['n_vertices']

            edgeMatrix  = np.zeros(shape=(n_vertices, n_vertices))

            # Iterate over edges and fill in edgeMatrix
            for edge in edgeString.split(',') :
                vertices    = edge.split('-')
                vertexA     = int(vertices[0])
                vertexB     = int(vertices[1])

                edgeMatrix[vertexA, vertexB] = 1
            
            list_graphEdges.append(edgeMatrix)
            print("\tLoaded graph: " + graph['name'])

        self.pd_graphInfo       = pd_graphInfo  
        self.list_graphEdges    = list_graphEdges

        return pd_graphInfo, list_graphEdges

    def generateTopologies(self, graphInfo, graphMatrix) :
        """ Generate topologies from graph.

            graphInfo (pd.sr):      Information regarding graph (row from pd_graphInfo)
            graphMatrix (np.arr):   Matrix defining edges of graph (entry from list_graphEdges)
        """

        maxVertex   = graphInfo['n_vertices']   # Max number of vertices
        tmUsed      = 0                         # Used transmission lines (for error check)

        # Get every possible combination of vertex-configurations
        pd_vertexConfigs    = pd.DataFrame(itertools.combinations_with_replacement(dict_vertexConfig, r=maxVertex))
        
        # Keep only configurations with 4 ECUs
        pd_vertexConfigs['sum'] = pd_vertexConfigs.replace(dict_vertexConfig).sum(axis=1)
        pd_vertexConfigs        = pd_vertexConfigs.drop(pd_vertexConfigs[~ (pd_vertexConfigs['sum'] == 4)].index)
        pd_vertexConfigs        = pd_vertexConfigs.drop(columns=['sum'])

        # Translate vertex configuration into nodes
        
        
        for _, vertexConfig in pd_vertexConfigs.iterrows() :
            
            # Get information about topology
            pd_vertexInfo   = pd.DataFrame(columns=['vertex', 'connectedEdges', 'configuration'])
            
            for i in range(0, maxVertex) :

                connections = sum(graphMatrix[i, :]) + sum(graphMatrix[:, i])

                pd_vertexInfo.loc[i]    = [i, int(connections), vertexConfig[i]]


            a = 1


        # Each graph vertex is translated into two topology nodes
        # Transmission lines have 2 ports -> 4 nodes
        # ECUs have 2 nodes





