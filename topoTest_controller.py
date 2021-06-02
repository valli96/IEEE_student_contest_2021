from nodeLink import nodeLink
from vertex import vertex_type2
from transLine import transLine
from ecu import ecu


T1  = transLine('T1', length=2)
T2  = transLine('T2', length=3)


v1  = vertex_type2('v1', T1.portA, T2.portB)


a = 1

