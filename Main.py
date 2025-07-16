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

allocated_cells = opt.get_allocated_cells(nwc_matrix)
print(allocated_cells)
u,v = opt.calculate_u_and_v(cost_matrix,allocated_cells)
print("U:", end = "")
print(u)
print("V:", end = "")
print(v)
penalty_matrix, max_pos_val, max_pos_cell = opt.generate_penalty_matrix(cost_matrix,allocated_cells,u,v)
for i in penalty_matrix:
    print(i)
print(f"Maximum positive value is {max_pos_val} at cell {max_pos_cell}")


