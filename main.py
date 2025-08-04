import os
import sys
import InputData as di
import NorthWestCorner as nwc
import Optimize as opt
import InputFromExcel as ex
from ConvertToExcel import matrix_to_excel
class Data:
    def __init__(self):
        self.supply_number = 0
        self.demand_number = 0
        self.supply_arr = []
        self.demand_arr = []
        self.cost_matrix = []
        self.initial_result_matrix = []
        self.final_result_matrix = []
        self.initial_cost = 0
        self.final_cost = 0
    
    def __input_data__(self):
        print("INPUT DATA MODES:")
        print("1. Input from Excel(.xlsx) file")
        print("2. Input from terminal")
        choice = input("Input mode: ")
        
        while choice.isalpha() or int(choice) not in [1,2]:
            choice = input("Invalid mode! Input mode again: ")
        
        if int(choice) == 1:
            print("Note: Use given input.xlsx as sample form of input")
            file_path = str(input("Input file path: "))
            
            # Check if file exists right after input
            if not os.path.exists(file_path):
                print(f"Can't find file with path {file_path}")
                sys.exit(1)  # Terminate the program with exit code 1
            
            self.demand_arr, self.supply_arr, self.cost_matrix = ex.input(file_path)
            if not self.demand_arr or not self.supply_arr or not self.cost_matrix:
                print(f"Error in given XLSX file")
                sys.exit(1)  # Terminate the program with exit code 1
        else:
            self.demand_number = int(input("Input number of demands: "))
            self.supply_number = int(input("Input number of supplies: "))

            self.demand_arr, self.supply_arr = di.inputDemandandSupply(self.demand_number, self.supply_number)
            self.cost_matrix = di.inputCostmatrix(self.demand_number, self.supply_number)
        
        return
    
    def __optimize__(self):
        self.initial_result_matrix = nwc.NWC(self.demand_arr, self.supply_arr, self.cost_matrix)
        self.initial_cost = opt.calculate_final_cost(self.initial_result_matrix, self.cost_matrix)
        self.result_matrix = opt.optimize( self.initial_result_matrix,self.cost_matrix)
        self.final_cost = opt.calculate_final_cost(self.result_matrix, self.cost_matrix)
        return
                
    def __printResult__(self):
        print("Initial cost using NWC method: ",self.initial_cost)            
        print("Final cost after optimization: ",self.final_cost)
        print(f"Reduced {self.initial_cost - self.final_cost} ~ {(self.initial_cost - self.final_cost)*100/self.initial_cost}%")        
        print("-"  * 100)
        print("DISTRIBUTION FROM SUPPLIES TO DEMANDS:")
        num_row = len(self.cost_matrix)
        num_col = len(self.cost_matrix[0])
        for i in range(num_row - 1):
            print(f"Supply {i + 1}")
            for j in range(num_col):
                if self.result_matrix[i][j] != 0:
                    print(f"├──Demand {j + 1}: {self.result_matrix[i][j]}")
            print("-"  * 20)
                   
    def __main_loop__(self):
        self.__input_data__()
        
        # Display supply, demand array and cost matrix
        # print("Demand arr:", self.demand_arr)
        # print("Supply arr:", self.supply_arr)
        # print("Cost matrix:")
        # for _ in self.cost_matrix:
        #     print(_)
        
        self.__optimize__()
        # Display optimzed matrix
        # print("-"*20) 
        # print("Final matrix:")
        # for _ in self.result_matrix:
        #     print(_)
        
        self.__printResult__()
        return
    
if __name__ == "__main__":
    data = Data()
    data.__main_loop__()