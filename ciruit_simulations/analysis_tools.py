
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
        DC_values[i] = analysis[i][(number_simulations - 1)].value
    return DC_values


def get_settlingtime(analysis):
    number_simulations = get_data_points(analysis)
    nodes = get_nodes(analysis)
    DC_values = get_DC_voltage(analysis)
    settling_time = {}
    for node in nodes:
        # print(str(DC_values[node])+ 'DC_values of Node' + str(node))   
        if DC_values[node] == 0:
            # pass
            a=1
        else:
            for i in range(number_simulations):
                voltage = analysis[node][number_simulations - 1 - i].value
                if (voltage >= DC_values[node]*1.02 or voltage <= DC_values[node]*0.98):
                    # print("the Settlingtime of "+ node + " is " )
                    # print(number_simulations-i)
                    DC_values[node] = number_simulations-i
                    settling_time[node] = number_simulations-i
                    break
    return settling_time

