from PathFinder import find_path
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

cost_matrix = [[3, 1, 7, 4],
               [2, 6, 5, 9],
               [8, 3, 3, 2]]     
max_pos_cell = [0,3]
allocated_cells = [[0,0],[0,1],[1,1],[1,2],[2,2],[2,3]] 
v,h = find_vertical_and_horizontal_match_cell(max_pos_cell,allocated_cells)
path = []
min_path_len = len(allocated_cells)
for i in v:
    for j in h:
        p = find_path(allocated_cells,i,j)
        if len(p) < min_path_len:
            path = p
            min_path_len = len(p)
print(path)