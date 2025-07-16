from collections import deque
def clean_path(path = []):
    done= False
    while not done:
        done = True
        # print(path)
        for i in range(1, len(path) -1):
            if (path[i][0] == path[i - 1][0] and path[i][0] == path[i + 1][0]) or (path[i][1] == path[i - 1][1] and path[i][1] == path[i + 1][1]):
                path.remove(path[i])
                done = False
                break
    return path

def find_path(allocated_cells, start, end):
    """
    Find a path from start to end using only allocated cells.
    Moves as far as possible vertically or horizontally, alternating directions.
    
    Args:
        allocated_cells: List of [x, y] coordinates representing valid cells
        start: [x, y] starting position
        end: [x, y] ending position
    
    Returns:
        List of [x, y] coordinates representing the path from start to end,
        or None if no path exists
    """
    # Convert allocated_cells to a set for O(1) lookup
    valid_cells = set(tuple(cell) for cell in allocated_cells)
    
    # Check if start and end are in allocated cells
    if tuple(start) not in valid_cells or tuple(end) not in valid_cells:
        return None
    
    # If start and end are the same
    if start == end:
        return [start]
    
    # Try both starting directions: vertical first, then horizontal first
    for start_vertical in [True, False]:
        result = bfs_alternating_path(valid_cells, start, end, start_vertical)
        if result:
            return clean_path(result)
    
    return None

def get_max_move_in_direction(valid_cells, start_pos, dx, dy):
    """Get all positions reachable in one direction from start_pos"""
    positions = []
    x, y = start_pos
    
    # Keep trying positions in this direction until we find all valid ones
    distance = 1
    while True:
        test_x = x + (dx * distance)
        test_y = y + (dy * distance)
        
        if (test_x, test_y) in valid_cells:
            positions.append((test_x, test_y))
            distance += 1
        else:
            # If this position is not valid, try the next distance
            # But if we've gone too far without finding anything, stop
            distance += 1
            if distance > 10:  # Reasonable limit to prevent infinite loop
                break
    
    return positions

def bfs_alternating_path(valid_cells, start, end, start_vertical):
    """BFS with alternating vertical/horizontal moves"""
    queue = deque([(tuple(start), [start], start_vertical)])
    visited = set()
    
    while queue:
        current_pos, path, is_vertical_turn = queue.popleft()
        
        # Create state for visited tracking
        state = (current_pos, is_vertical_turn)
        if state in visited:
            continue
        visited.add(state)
        
        # Define directions based on current turn
        if is_vertical_turn:
            directions = [(0, -1), (0, 1)]  # down, up (decreasing y, increasing y)
        else:
            directions = [(-1, 0), (1, 0)]  # left, right (decreasing x, increasing x)
        
        # Try each direction
        for dx, dy in directions:
            # Get all positions reachable in this direction
            reachable = get_max_move_in_direction(valid_cells, current_pos, dx, dy)
            
            # Add each reachable position as a potential next state
            for i, pos in enumerate(reachable):
                new_path = path + [list(p) for p in reachable[:i+1]]
                
                # Check if we reached the destination
                if list(pos) == end:
                    return new_path
                
                # Add to queue for next turn (opposite direction)
                next_state = (pos, not is_vertical_turn)
                if next_state not in visited:
                    queue.append((pos, new_path, not is_vertical_turn))
    
    return None
