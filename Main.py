import InputData as data
import NorthWestCorner as nwc
import LeastCostCell as lcc
import Optimize as opt
# demand_number = int(input("Input number of demands: "))
# supply_number = int(input("Input number of supplies: "))

# # demand_arr, supply_arr = data.inputDemandandSupply(demand_number,supply_number)
# # cost_matrix = data.inputCostmatrix(demand_number,supply_number)
        
demand_arr = [20, 20, 40, 10, 35]
supply_arr = [35, 40, 20, 30]
cost_matrix = [[10, 2, 3, 15, 9],
               [5, 10, 15, 2, 4],
               [15, 5, 14, 7, 15],
               [20, 15, 13, 25, 8]]

data.printData(demand_arr, supply_arr, cost_matrix)
nwc_matrix = nwc.NWC(demand_arr, supply_arr, cost_matrix)
lcc_matrix = lcc.LCC(demand_arr, supply_arr, cost_matrix)
for _ in lcc_matrix:
    print(_)
opt.optimize(lcc_matrix,cost_matrix)

