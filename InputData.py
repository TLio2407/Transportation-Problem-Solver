#Check if string of data has been converted into array 
def addSuccess(array):
    if array[0] + 0 == array[0]:
        print("Added data to array successfully.\n")
        return True

    print("Failed to add data to array.")
    return False
#Convert string of data into array
def addDatatoArray(string, number):
    arr = []
    while string.count(" ") + 1 != number:
        string = str(input("Incorrect input! Input again: "))
    for i in string.split(" "):
        arr.append(int(i))
    return arr    

def inputDemandandSupply(demand_number, supply_number):
    print("-----DEMAND & SUPPLY INPUT-----")
    
    demands = str(input("Input demands seperately: "))
    demands_arr = addDatatoArray(demands,demand_number)

    supplies =str(input("Input supplies seperately: "))
    supplies_arr = addDatatoArray(supplies,supply_number)
    if addSuccess(demands_arr) and addSuccess(supplies_arr):
        return(demands_arr,supplies_arr)

def inputCostmatrix(demand_number,supply_number):
    cost_matrix = []
    print("-----COST INPUT-----")
    for i in range(supply_number):
        cost_row_str = str(input("Input row "+ str(i + 1) +" seperately with " + str(demand_number) + " cost(s): "))
        cost_row = addDatatoArray(cost_row_str,demand_number)
        if addSuccess(cost_row):
            cost_matrix.append(cost_row)
    return cost_matrix
#Format arrays of Demands and Supplies into matrix 
def formatData(demand_arr, supply_arr, cost_matrix):
    sum_demand = sum(demand_arr)
    sum_supply = sum(supply_arr)
    if sum_supply > sum_demand:
        demand_arr.append(sum_supply - sum_demand)
        print()
        print(f"==>Added dummy demand of {sum_supply - sum_demand} to balance supply and demand<==")
        for i in cost_matrix:
            i.append(0)
    formated_matrix = []
    row = []
    for i in demand_arr:
        row.append(i)
    formated_matrix.append(row)
    for i in supply_arr:
        row = []
        row.append(i)
        for i in range(len(demand_arr)):
            row.append(0)
        formated_matrix.append(row)
        
    return formated_matrix    

def printData(demand_arr, supply_arr ,cost_matrix):
    choice = str(input("Print input data?[Y/N]: "))
    if choice.upper() == "Y":
        formated = formatData(demand_arr, supply_arr,cost_matrix)
        print()
        formated[0].insert(0,"S|D")
        for i in formated:
            print(i)
        print("Costs: ")
        for i in cost_matrix:
            print(i)
            