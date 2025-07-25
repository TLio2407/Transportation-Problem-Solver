import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import InputData as data
import NorthWestCorner as nwc
import Optimize as opt
import InputFromExcel as ex
from ConvertToExcel import matrix_to_excel
def get_array(size, array_name):
    """Get array elements from user input"""
    root = tk.Tk()
    root.withdraw()
    
    try:
        array_str = simpledialog.askstring("Input", 
            f"Enter {size} elements of {array_name} (separated by spaces):")
        
        if array_str is None:
            return None
        
        elements = list(map(float, array_str.split()))
        
        if len(elements) != size:
            messagebox.showerror("Error", f"Expected {size} elements, got {len(elements)}")
            return None
        
        return elements
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numbers separated by spaces.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error processing array: {e}")
        return None

def get_matrix(rows, cols):
    """Get matrix elements from user input"""
    root = tk.Tk()
    root.withdraw()
    
    matrix = []
    
    try:
        for i in range(rows):
            row_str = simpledialog.askstring("Input", 
                f"Enter {cols} elements for row {i+1} of the matrix (separated by spaces):")
            
            if row_str is None:
                return None
            
            row_elements = list(map(float, row_str.split()))
            
            if len(row_elements) != cols:
                messagebox.showerror("Error", f"Expected {cols} elements for row {i+1}, got {len(row_elements)}")
                return None
            
            matrix.append(row_elements)
        
        return matrix
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numbers separated by spaces.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error processing matrix: {e}")
        return None

def isSolveable(supply_arr=[], demand_arr=[]):
    return sum(supply_arr) >= sum(demand_arr)

def formatResult(result_matrix=[], cost_matrix=[]):
    """Format result as string for display in messagebox"""
    result_text = ""
    num_row = len(cost_matrix)
    num_col = len(cost_matrix[0])
    
    for i in range(num_row - 1):
        result_text += f"Supply {i + 1}:\n"
        for j in range(num_col):
            if result_matrix[i][j] != 0:
                result_text += f"  ├──Demand {j + 1}: {result_matrix[i][j]}\n"
        result_text += "-" * 20 + "\n"
    
    return result_text

def show_matrix(title, matrix, additional_info=""):
    """Display matrix in a formatted messagebox"""
    matrix_text = f"{title}\n" + "=" * 50 + "\n"
    for row in matrix:
        matrix_text += str(row) + "\n"
    if additional_info:
        matrix_text += "\n" + additional_info
    
    messagebox.showinfo(title, matrix_text)

def get_manual_input():
    """Get manual input using tkinter dialogs"""
    try:
        demand_number = simpledialog.askinteger("Input", "Enter number of demands:", minvalue=1)
        if demand_number is None:
            return None, None, None
            
        supply_number = simpledialog.askinteger("Input", "Enter number of supplies:", minvalue=1)
        if supply_number is None:
            return None, None, None
        
        demand_arr = get_array(demand_number, "demand_arr")
        supply_arr = get_array(supply_number, "supply_arr")
        cost_matrix = get_matrix(supply_number, demand_number)
        
        return demand_arr, supply_arr, cost_matrix
    except Exception as e:
        messagebox.showerror("Error", f"Error getting manual input: {str(e)}")
        return None, None, None

def get_excel_input():
    """Get input from Excel file using file dialog"""
    try:
        messagebox.showinfo("Notice", "Use given input.xlsx as sample form of input")
        
        file_path = filedialog.askopenfilename(
            title="Select Excel Input File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if not file_path:
            return None, None, None
            
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"Can't find file with path {file_path}")
            return None, None, None
        
        demand_arr, supply_arr, cost_matrix = ex.input(file_path)
        
        if not demand_arr or not supply_arr or not cost_matrix:
            messagebox.showerror("Error", "Error in given XLSX file")
            return None, None, None
            
        return demand_arr, supply_arr, cost_matrix
        
    except Exception as e:
        messagebox.showerror("Error", f"Error reading Excel file: {str(e)}")
        return None, None, None

def save_output(result_matrix):
    """Save output to Excel file using file dialog"""
    try:
        output_path = filedialog.asksaveasfilename(
            title="Save Excel Output File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if output_path:
            matrix_to_excel(result_matrix, output_path)
            messagebox.showinfo("Success", f"Output saved to: {output_path}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error saving output: {str(e)}")

def main():
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show initial notice
    messagebox.showinfo("Notice", "TRANSPORTATION PROBLEM SOLVER\n\nEnsure total of supplies >= total of demands")
    
    # Get input method choice
    choice = messagebox.askyesnocancel(
        "Input Method", 
        "Choose input method:\n\nYes - Input from Excel\nNo - Input manually\nCancel - Exit"
    )
    
    if choice is None:  # User clicked Cancel
        return
    
    demand_arr, supply_arr, cost_matrix = [], [], []
    
    if choice:  # Yes - Excel input
        demand_arr, supply_arr, cost_matrix = get_excel_input()
    else:  # No - Manual input
        demand_arr, supply_arr, cost_matrix = get_manual_input()
    
    # Check if input was successful
    if not demand_arr or not supply_arr or not cost_matrix:
        messagebox.showwarning("Warning", "No valid input received. Exiting.")
        return
    
    # Check if problem is solveable
    if not isSolveable(supply_arr, demand_arr):
        messagebox.showerror(
            "Error", 
            "Sum of demands > sum of supplies => Can't solve.\nPlease reconfigure the data."
        )
        return
    
    # Show input data
    input_info = f"Demands: {demand_arr}\nSupplies: {supply_arr}"
    show_matrix("INPUT DATA", cost_matrix, input_info)
    
    try:
        # Calculate initial solution using North-West Corner method
        nwc_matrix = nwc.NWC(demand_arr, supply_arr, cost_matrix)
        initial_cost = opt.calculate_final_cost(nwc_matrix, cost_matrix)
        
        # Optimize the solution
        result_matrix = opt.optimize(nwc_matrix, cost_matrix)
        
        # Clean up result matrix if needed
        if len(result_matrix[0]) > len(cost_matrix[0]):
            result_matrix = [row[:-1] for row in result_matrix]
        
        # Calculate final cost
        final_cost = opt.calculate_final_cost(result_matrix, cost_matrix)
        
        # Show final matrix
        show_matrix("FINAL MATRIX", result_matrix, f"Demands: {demand_arr}")
        
        # Show cost comparison
        cost_reduction = initial_cost - final_cost
        percentage_reduction = round(((cost_reduction / initial_cost) * 100), 2) if initial_cost > 0 else 0
        
        cost_info = (f"Initial Cost: {initial_cost}\n"
                    f"Final Cost: {final_cost}\n"
                    f"Decreased by: {cost_reduction}\n"
                    f"Percentage Reduction: {percentage_reduction}%")
        
        messagebox.showinfo("COST ANALYSIS", cost_info)
        
        # Show distribution results
        distribution_text = formatResult(result_matrix, cost_matrix)
        messagebox.showinfo("DISTRIBUTION FROM SUPPLIES TO DEMAND", distribution_text)
        
        # Ask if user wants to save output
        save_choice = messagebox.askyesno("Save Output", "Do you want to save the results to an Excel file?")
        if save_choice:
            save_output(result_matrix)
            
    except Exception as e:
        messagebox.showerror("Error", f"Error during calculation: {str(e)}")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    main()