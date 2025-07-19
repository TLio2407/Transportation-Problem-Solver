from PathFinder import find_path
import copy
def get_allocated_cells(matrix):
    allocated_cells = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0 :
                allocated_cells.append([i,j])
    return allocated_cells

#Return true if degeneracy
def is_Degeneracy(cost_matrix, allocated_cells):
    return len(allocated_cells) != len(cost_matrix) + len(cost_matrix[0]) - 1

#Calculate and return U and V as lists
def calculate_u_and_v(cost_matrix, allocated_cells):
    n = len(cost_matrix)
    u = [None] * (len(cost_matrix) - 1)
    v = [None] * len(cost_matrix[0])
    u.insert(0, 0)
    # Calculate u and v values
    for cell in allocated_cells:
        i, j = cell
        if i == 0:
            v.pop(j)
            v.insert(j, cost_matrix[i][j])
        else:
            if v[j] != None:
                u.pop(i)
                u.insert(i,cost_matrix[i][j] - v[j])
    while None in v or None in u:
        for cell in allocated_cells:
            i, j = cell
            if u[i] != None and v[j] == None:
                v.pop(j)
                v.insert(j, cost_matrix[i][j] - u[i])
            elif u[i] == None and v[j] != None:
                u.pop(i)
                u.insert(i, cost_matrix[i][j] - v[j])
            

    print("U = ")
    for i in u:
        print(i)
    print("V = ", v)

    
    return u, v

def calculate_final_cost(sup_dem_matrix = [], cost_matrix = []):
    cost = 0
    allocated_cells = get_allocated_cells(sup_dem_matrix)
    for cell in allocated_cells:
        i, j = cell
        cost += sup_dem_matrix[i][j] * cost_matrix[i][j]
    return cost

def generate_penalty_matrix(cost_matrix, allocated_cells, u, v):
    maximum_positive = 0
    max_pos_cell = []
    penalty_matrix = [["-" for _ in range(len(cost_matrix[0]))] for _ in range(len(cost_matrix))]
    u, v = calculate_u_and_v(cost_matrix, allocated_cells)
    for i in range(len(penalty_matrix)):
        for j in range(len(penalty_matrix[i])):
            if [i,j] not in allocated_cells:
                penalty_matrix[i][j] = u[i] + v[j] - cost_matrix[i][j]
                if penalty_matrix[i][j] > maximum_positive:
                    maximum_positive = max(maximum_positive, penalty_matrix[i][j])
                    max_pos_cell = [i,j]
    return penalty_matrix, maximum_positive, max_pos_cell

def matrix_transform(supply_demand_matrix = [],path = []):
    plus_cells = path[::2]
    minus_cells = path[1::2]
    min_minus_cells_value = supply_demand_matrix[minus_cells[0][0]][minus_cells[0][1]]
    for cell in minus_cells[1:]:
        min_minus_cells_value = min(min_minus_cells_value,
                                    supply_demand_matrix[cell[0]][cell[1]])
    for cell in plus_cells:
        supply_demand_matrix[cell[0]][cell[1]] += min_minus_cells_value
    for cell in minus_cells:
        supply_demand_matrix[cell[0]][cell[1]] -= min_minus_cells_value

def matrix_transform_copy(supply_demand_matrix=[], path=[]):
    # Deep copy to avoid modifying the original
    new_matrix = copy.deepcopy(supply_demand_matrix)

    plus_cells = path[::2]
    minus_cells = path[1::2]

    min_minus_cells_value = new_matrix[minus_cells[0][0]][minus_cells[0][1]]
    for cell in minus_cells[1:]:
        min_minus_cells_value = min(min_minus_cells_value, new_matrix[cell[0]][cell[1]])

    for cell in plus_cells:
        new_matrix[cell[0]][cell[1]] += min_minus_cells_value
    for cell in minus_cells:
        new_matrix[cell[0]][cell[1]] -= min_minus_cells_value

    return new_matrix

def find_vertical_and_horizontal_match_cell(target_cell = [], allocated_cells = []): 
    vertical = []
    horizontal = []
    for cell in allocated_cells:
        if cell != target_cell:
            if cell[0] == target_cell[0]:
                vertical.append(cell)
            elif cell[1] == target_cell[1]:
                horizontal.append(cell)
    return vertical, horizontal

def optimize(sup_dem_matrix = [], cost_matrix = []):
    allocated_cells = get_allocated_cells(sup_dem_matrix)
    if is_Degeneracy(cost_matrix, allocated_cells):
        list_unallocated_cells_ascending = {}
        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[0])):
                if [i, j] not in allocated_cells:
                    list_unallocated_cells_ascending.update({f"{i} {j}" : cost_matrix[i][j]})
        sorted_dict = dict(sorted(list_unallocated_cells_ascending.items(), key=lambda item: item[1]))
        first_key = next(iter(sorted_dict))
        new_cell = [int(first_key.split()[0]), int(first_key.split()[1])]
        allocated_cells.insert(0, new_cell)
        u,v = calculate_u_and_v(cost_matrix,allocated_cells)
        penalty_matrix, maximum_positive, max_pos_cell = generate_penalty_matrix(cost_matrix, allocated_cells, u,v)
        print(allocated_cells)
        for _ in penalty_matrix:
            print(_)
        print(f"Maximum value is {maximum_positive} at cell {max_pos_cell}")
        if not max_pos_cell:
            return sup_dem_matrix
        ver,hor = find_vertical_and_horizontal_match_cell(max_pos_cell,allocated_cells)
        path = []
        min_path_len = len(allocated_cells)
        for start in ver:
            for end in hor:
                p = find_path(allocated_cells, start, end)
                if len(p) < min_path_len:
                    path = p
                    min_path_len = len(p)
        path.insert(0,max_pos_cell)        
        print(path)
        for _ in sup_dem_matrix:
            print(_)
        print(calculate_final_cost(sup_dem_matrix,cost_matrix))
        return sup_dem_matrix
    u,v = calculate_u_and_v(cost_matrix,allocated_cells)
    penalty_matrix, maximum_positive, max_pos_cell = generate_penalty_matrix(cost_matrix, allocated_cells, u,v)
    for _ in penalty_matrix:
        print(_)
    print(f"Maximum value is {maximum_positive} at cell {max_pos_cell}")
    done = False            
    while maximum_positive > 0 or done:
        ver,hor = find_vertical_and_horizontal_match_cell(max_pos_cell,allocated_cells)
        path = []
        min_path_len = len(allocated_cells)
        for start in ver:
            for end in hor:
                p = find_path(allocated_cells, start, end)
                if len(p) < min_path_len:
                    path = p
                    min_path_len = len(p)
        path.insert(0,max_pos_cell)        
        print(path)
        matrix_transform(sup_dem_matrix, path)
        for _ in sup_dem_matrix:
            print(_)
        allocated_cells = get_allocated_cells(sup_dem_matrix)
        if is_Degeneracy(cost_matrix, allocated_cells):
            list_unallocated_cells_ascending = {}
            for i in range(len(cost_matrix)):
                for j in range(len(cost_matrix[0])):
                    if [i, j] not in allocated_cells:
                        list_unallocated_cells_ascending.update({f"{i} {j}" : cost_matrix[i][j]})
            sorted_dict = dict(sorted(list_unallocated_cells_ascending.items(), key=lambda item: item[1]))
            first_key = next(iter(sorted_dict))
            new_cell = [int(first_key.split()[0]), int(first_key.split()[1])]
            allocated_cells.insert(0, new_cell)
            u,v = calculate_u_and_v(cost_matrix,allocated_cells)
            penalty_matrix, maximum_positive, max_pos_cell = generate_penalty_matrix(cost_matrix, allocated_cells, u,v)
            print(allocated_cells)
            for _ in penalty_matrix:
                print(_)
            print(f"Maximum value is {maximum_positive} at cell {max_pos_cell}")
            if not max_pos_cell:
                return sup_dem_matrix
            ver,hor = find_vertical_and_horizontal_match_cell(max_pos_cell,allocated_cells)
            path = []
            min_path_len = len(allocated_cells)
            for start in ver:
                for end in hor:
                    p = find_path(allocated_cells, start, end)
                    if len(p) < min_path_len:
                        path = p
                        min_path_len = len(p)
            path.insert(0,max_pos_cell)        
            print(path)
            matrix_transform(sup_dem_matrix, path)
            for _ in sup_dem_matrix:
                print(_)
            print(calculate_final_cost(sup_dem_matrix,cost_matrix))
            return sup_dem_matrix   
        u,v = calculate_u_and_v(cost_matrix,allocated_cells)
        penalty_matrix, maximum_positive, max_pos_cell = generate_penalty_matrix(cost_matrix, allocated_cells, u,v)
        for _ in penalty_matrix:
            print(_)
        print(f"Maximum value is {maximum_positive} at cell {max_pos_cell}")
    return sup_dem_matrix