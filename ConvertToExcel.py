import pandas as pd
import os
# Convert matrix to Excel using pandas
def matrix_to_excel(matrix, filename='output.xlsx'):
    """
    Convert matrix to Excel file using pandas
    
    Args:
        matrix: list of lists
        filename: output Excel filename
    """
    if os.path.exists(filename):
        os.remove(filename)
    # Option 1: If first row contains headers
    df = pd.DataFrame(matrix)
    # Option 2: If no headers (uncomment this and comment above)
    # df = pd.DataFrame(matrix)
    
    # Write to Excel file
    df.to_excel(filename)
    print(f"Matrix successfully saved to {filename}")
