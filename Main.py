import os
import sys
import InputData as data
import NorthWestCorner as nwc
import Optimize as opt
import InputFromExcel as ex
def isSolveable(supply_arr = [], demand_arr = []):
    return sum(supply_arr) >= sum(demand_arr)
demand_arr, supply_arr, cost_matrix = [], [], []
print("1. Input from Excel")
print("2. Input manually/ from keyboard")
choose = int(input("1 or 2: "))
if choose == 1:
    file_path = str(input("Input file path: "))
    
    # Check if file exists right after input
    if not os.path.exists(file_path):
        print(f"Can't find file with path {file_path}")
        sys.exit(1)  # Terminate the program with exit code 1
    
    demand_arr, supply_arr, cost_matrix = ex.input(file_path)
    if not demand_arr or not supply_arr or not cost_matrix:
        print(f"Error in given XLSX file")
        sys.exit(1)  # Terminate the program with exit code 1
        
if choose == 2:
    demand_number = int(input("Input number of demands: "))
    supply_number = int(input("Input number of supplies: "))

    demand_arr, supply_arr = data.inputDemandandSupply(demand_number,supply_number)
    cost_matrix = data.inputCostmatrix(demand_number,supply_number)

if not isSolveable(supply_arr, demand_arr):
    print("Sum of demands > sum of supplies => Can't solve.")
    print("Please reconfigure the data.")
    sys.exit(1)
data.printData(demand_arr, supply_arr, cost_matrix)

nwc_matrix = nwc.NWC(demand_arr, supply_arr, cost_matrix)
result_matrix = opt.optimize(nwc_matrix,cost_matrix)
print("FINAL MATRIX:")
for _ in result_matrix:
    print(_)
print(f"FINAL COST: {opt.calculate_final_cost(result_matrix,cost_matrix)}")

