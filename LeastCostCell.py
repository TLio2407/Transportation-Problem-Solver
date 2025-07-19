import copy
def isDone(result_matrix = [], demand_arr = [], ):
    sum = 0
    sum_of_demand = 0
    for i in range(len(result_matrix)):
        for j in range(len(result_matrix[0])):
            sum += result_matrix[i][j]
    for demand in demand_arr:
        sum_of_demand += demand
    return sum == sum_of_demand
    
def LCC(demand_arr = [], supply_arr = [], cost_matrix = []):
    result_matrix = [[0 for _ in range(len(demand_arr))] for _ in range(len(supply_arr))]

    dem = copy.deepcopy(demand_arr)
    sup = copy.deepcopy(supply_arr)
    cost_dict = {}
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            cost_dict.update({ f"{i} {j}": cost_matrix[i][j]})
    sorted_dict= dict(sorted(cost_dict.items(), key=lambda item: item[1]))
    
    for key in sorted_dict.keys():
        i, j = int(key.split()[0]), int(key.split()[1]) 
        print(f"Value {sorted_dict[key]} at cell [{key}]")
        result_matrix[i][j] = min(sup[i], dem[j])
        sup[i] -= result_matrix[i][j]
        dem[j] -= result_matrix[i][j]
        if isDone(result_matrix,demand_arr):
            break
    return result_matrix


        
