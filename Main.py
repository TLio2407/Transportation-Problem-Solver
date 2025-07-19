import InputData as data
import NorthWestCorner as nwc
import LeastCostCell as lcc
import Optimize as opt
demand_number = int(input("Input number of demands: "))
supply_number = int(input("Input number of supplies: "))

demand_arr, supply_arr = data.inputDemandandSupply(demand_number,supply_number)
cost_matrix = data.inputCostmatrix(demand_number,supply_number)
data.printData(demand_arr, supply_arr, cost_matrix)
nwc_matrix = nwc.NWC(demand_arr, supply_arr, cost_matrix)
lcc_matrix = lcc.LCC(demand_arr, supply_arr, cost_matrix)
result_matrix = opt.optimize(nwc_matrix,cost_matrix)
print("FINAL MATRIX:")
for _ in result_matrix:
    print(_)
print(f"FINAL COST: {opt.calculate_final_cost(result_matrix,cost_matrix)}")

