""" Small controller file for testing the testCase object """

import pandas as pd
from TestCase import TestCase 

testCase    = TestCase()

pd_graphInfo, list_graphEdges   = testCase.loadGraphs('data/graphs.csv')

testCase.generateTopologies(pd_graphInfo.loc[2], list_graphEdges[2])

a = 1
