import pandas as pd
def input(filepath = str()):
    # Read Excel file
    df = pd.read_excel(filepath, header=None)
    print(df)
    print(df.shape)
    # Get last row as list
    demand_arr = df.iloc[-1].tolist()

    cost_matrix = df.iloc[:-1, :-1].values.tolist()

    # Get last column as list  
    last_column = df.iloc[:, -1].tolist()

    # If you want to remove NaN values:
    demand_arr = [int(x) for x in demand_arr if pd.notna(x)]
    supply_arr = [int(x) for x in last_column if pd.notna(x)]

    print("Demand_arr:", demand_arr)
    print("Supply_arr:", supply_arr)
    for _ in cost_matrix:
        print(_)
    return demand_arr, supply_arr, cost_matrix