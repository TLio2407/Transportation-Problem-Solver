def try_solve_u_v(cost_matrix, allocated_cells, m, n, max_iterations=100):
    """
    Try to solve for u and v values given allocated cells.
    
    Returns:
        tuple: (u_values, v_values, success)
               success: True if all u and v values were determined, False otherwise
    """
    # Initialize u and v arrays with None values
    u = [None] * m
    v = [None] * n
    
    # Set u[0] = 0 as starting point (common convention)
    u[0] = 0
    
    # Keep iterating until all u and v values are determined or max iterations reached
    iteration_count = 0
    changed = True
    while changed and iteration_count < max_iterations:
        changed = False
        iteration_count += 1
        
        # For each allocated cell, try to calculate missing u or v values
        for cell in allocated_cells:
            i, j = cell[0], cell[1]
            cost = cost_matrix[i][j]
            
            # If u[i] is known but v[j] is not, calculate v[j]
            if u[i] is not None and v[j] is None:
                v[j] = cost - u[i]
                changed = True
            
            # If v[j] is known but u[i] is not, calculate u[i]
            elif v[j] is not None and u[i] is None:
                u[i] = cost - v[j]
                changed = True
    
    # Check if we successfully solved for all u and v values
    success = all(val is not None for val in u) and all(val is not None for val in v)
    
    # If not successful, set remaining None values to 0
    if not success:
        for i in range(m):
            if u[i] is None:
                u[i] = 0
        for j in range(n):
            if v[j] is None:
                v[j] = 0
    
    return u, v, success

def calculate_u_v_degeneracy(cost_matrix, allocated_cells, sorted_dict):
    """
    Calculate u and v values for degeneracy resolution in transportation problem.
    """
    # Get matrix dimensions
    m = len(cost_matrix)  # number of rows (sources)
    n = len(cost_matrix[0])  # number of columns (destinations)
    
    # Create a copy of allocated cells to avoid modifying original
    new_allocated_cells = allocated_cells.copy()
    
    # Try different cells from cell_dict until we can solve for u and v
    if sorted_dict:
        for key in sorted_dict.keys():
            # Try adding this cell
            test_cell = [int(key.split()[0]), int(key.split()[1])]
            test_allocated_cells = new_allocated_cells + [test_cell]
            
            # Try to solve u and v with this cell added
            u, v, success = try_solve_u_v(cost_matrix, test_allocated_cells, m, n)
            
            if success:
                # Successfully solved u and v, use this cell
                new_allocated_cells.append(test_cell)
                return u, v, new_allocated_cells
        
        # If no cell from dict works, add the first one anyway and return partial solution
        first_key = next(iter(sorted_dict))
        new_cell = [int(first_key.split()[0]), int(first_key.split()[1])]
        new_allocated_cells.append(new_cell)
    
    # Solve u and v with current allocated cells (may have None values)
    u, v, _ = try_solve_u_v(cost_matrix, new_allocated_cells, m, n)
    
    return u, v, new_allocated_cells
