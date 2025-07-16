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
    u = [0]
    v = []

    # Calculate u and v values
    for cell in allocated_cells:
        print("Processing cell:", cell)
        i, j = cell
        if i == len(u):
            u.append(cost_matrix[i][j] - v[j])
        if j == len(v):
            v.append(cost_matrix[i][j] - u[i])
    return u, v

def generate_penalty_matrix(cost_matrix, allocated_cells, u, v):
    maximum_positive = 0
    max_pos_cell = []
    penalty_matrix = [[0 for _ in range(len(cost_matrix[0]))] for _ in range(len(cost_matrix))]
    u, v = calculate_u_and_v(cost_matrix, allocated_cells)
    for i in range(len(penalty_matrix)):
        for j in range(len(penalty_matrix[i])):
            penalty_matrix[i][j] = u[i] + v[j] - cost_matrix[i][j]
            if penalty_matrix[i][j] > maximum_positive:
                maximum_positive = max(maximum_positive, penalty_matrix[i][j])
                max_pos_cell = [i,j]
    return penalty_matrix, maximum_positive, max_pos_cell

