
def get_nodes(analysis):
    nodes = []
    for i in analysis.nodes.keys():
        # print(i)
        if '#' in i:
            pass
        else:
            nodes.append(i)
    return nodes


def get_data_points(analysis):
    return len(analysis.time)


def get_DC_voltage(analysis):
    number_simulations = get_data_points(analysis)
    nodes = get_nodes(analysis)
    DC_values = {} 
    for i in nodes:
        # print(i)
        DC_values[i] = analysis[i][(number_simulations - 1)]

    return DC_values

