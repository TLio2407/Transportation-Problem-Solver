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

def calculate_u_v_degeneracy(cost_matrix, allocated_cells, cell_dict):
    """
    Calculate u and v values for degeneracy resolution in transportation problem.
    """
    # Get matrix dimensions
    m = len(cost_matrix)  # number of rows (sources)
    n = len(cost_matrix[0])  # number of columns (destinations)
    
    # Create a copy of allocated cells to avoid modifying original
    new_allocated_cells = allocated_cells.copy()
    
    # Try different cells from cell_dict until we can solve for u and v
    if cell_dict:
        # Sort the dictionary by cost values (ascending)
        sorted_dict = dict(sorted(cell_dict.items(), key=lambda item: item[1]))
        
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

# Test the specific user case
def test_user_case():
    cost_matrix = [
        [14, 2, 5, 7],
        [5, 6, 21, 3],
        [24, 1, 10, 3],
        [7, 4, 9, 8]
    ]
    
    allocated_cells = [[0, 2], [1, 0], [1, 1], [2, 3], [3, 1], [3, 3]]
    
    cell_dict = {
        '2 1': 1, '0 1': 2, '1 3': 3, '0 3': 7, '3 0': 7, 
        '3 2': 9, '2 2': 10, '0 0': 14, '1 2': 21, '2 0': 24
    }
    
    print("--- Testing User's Specific Case ---")
    print("Cost matrix:")
    for i, row in enumerate(cost_matrix):
        print(f"Row {i}: {row}")
    
    print(f"\nOriginal allocated cells: {allocated_cells}")
    print(f"Number of allocated cells: {len(allocated_cells)}")
    print(f"Expected for non-degenerate: {len(cost_matrix) + len(cost_matrix[0]) - 1}")
    
    # Check current solution
    u_test, v_test, success = try_solve_u_v(cost_matrix, allocated_cells, 4, 4)
    print(f"\nCan solve u,v with current cells? {success}")
    
    if not success:
        print("Degeneracy detected! Testing each cell from dictionary...")
        
        sorted_dict = dict(sorted(cell_dict.items(), key=lambda item: item[1]))
        for key, cost in sorted_dict.items():
            test_cell = [int(key.split()[0]), int(key.split()[1])]
            test_cells = allocated_cells + [test_cell]
            u, v, test_success = try_solve_u_v(cost_matrix, test_cells, 4, 4)
            
            print(f"  Testing cell {test_cell} (cost {cost}): {'SUCCESS' if test_success else 'FAILED'}")
            if test_success:
                print(f"    U values: {u}")
                print(f"    V values: {v}")
                break
    
    # Run the full function
    print(f"\n--- Running calculate_u_v_degeneracy ---")
    u_vals, v_vals, new_cells = calculate_u_v_degeneracy(cost_matrix, allocated_cells, cell_dict)
    
    print(f"Final allocated cells: {new_cells}")
    print(f"Added cell: {[cell for cell in new_cells if cell not in allocated_cells]}")
    print(f"U values: {u_vals}")
    print(f"V values: {v_vals}")
    
    # Verify
    print(f"\nVerification:")
    for cell in new_cells:
        i, j = cell[0], cell[1]
        calculated = u_vals[i] + v_vals[j]
        actual = cost_matrix[i][j]
        print(f"Cell ({i},{j}): {u_vals[i]} + {v_vals[j]} = {calculated}, cost = {actual}")

# Run the test
# test_user_case()