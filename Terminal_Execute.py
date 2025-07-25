import os
import sys
import InputData as data
import NorthWestCorner as nwc
import Optimize as opt
import InputFromExcel as ex
from ConvertToExcel import matrix_to_excel
def isSolveable(supply_arr = [], demand_arr = []):
    return sum(supply_arr) >= sum(demand_arr)

def printResult(result_matrix = [], cost_matrix = []):
    num_row = len(cost_matrix)
    num_col = len(cost_matrix[0])
    for i in range(num_row - 1):
        print(f"Supply {i + 1}")
        for j in range(num_col):
            if result_matrix[i][j] != 0:
                print(f"├──Demand {j + 1}: {result_matrix[i][j]}")
        print("-"  * 20)
demand_arr, supply_arr, cost_matrix = [], [], []
print("NOTICE: Ensure total of supplies >= total of demands")
print("1. Input from Excel")
print("2. Input manually/ from keyboard")
choose = int(input("1 or 2: "))
if choose == 1:
    print("Note: Use given input.xlsx as sample form of input")
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
initial_cost = opt.calculate_final_cost(nwc_matrix, cost_matrix)
result_matrix = opt.optimize(nwc_matrix,cost_matrix)

print("-"  * 100)
print("FINAL MATRIX:")
if len(result_matrix[0]) > len(cost_matrix[0]):
    result_matrix = [row[:-1] for row in result_matrix]
for _ in result_matrix:
    print(_)
print(demand_arr)
final_cost = opt.calculate_final_cost(result_matrix,cost_matrix)

print("-"  * 100)
print(f"Initial Cost: {initial_cost}")
print(f"FINAL COST: {final_cost}")
print(f"Decreased by {(initial_cost - final_cost)} => {round((((initial_cost - final_cost)/ initial_cost) * 100),2)} %")

print("-"  * 100)
print("DISTRIBUTION FROM SUPPLIES TO DEMAND:")
printResult(result_matrix, cost_matrix)

output_path = str(input("Output Excel Path: "))
matrix_to_excel(result_matrix, output_path)