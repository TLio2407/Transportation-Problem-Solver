import InputData as data
import NorthWestCorner as nwc
import Optimize as opt
demand_number = int(input("Input number of demands: "))
supply_number = int(input("Input number of supplies: "))

demand_arr, supply_arr = data.inputDemandandSupply(demand_number,supply_number)
cost_matrix = data.inputCostmatrix(demand_number,supply_number)
data.printData(demand_arr, supply_arr, cost_matrix)
nwc_matrix = nwc.NWC(demand_arr, supply_arr, cost_matrix)
print("North West Corner Method Result:")
for row in nwc_matrix:
    print(row)
opt.optimize(nwc_matrix,cost_matrix)

