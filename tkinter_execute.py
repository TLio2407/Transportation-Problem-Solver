import tkinter as tk
import sys
from tkinter import ttk, messagebox
import Optimize as opt
import NorthWestCorner as nwc
class MatrixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Input and Display")
        self.root.geometry("600x500")
        self.result_matrix = []
        self.supply_number = 0  # rows
        self.demand_number = 0  # columns
        self.entry_widgets = []
        self.cost_matrix = []
        self.supply_array = []  # Array of size m
        self.demand_array = []  # Array of size n
        self.supply_array_widgets = []
        self.demand_array_widgets = []
        self.initial_cost = 0
        self.final_cost = 0
        
        self.setup_dimension_input()
    
    def setup_dimension_input(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame for dimension input
        dim_frame = ttk.Frame(self.root, padding="20")
        dim_frame.pack(pady=20)
        
        ttk.Label(dim_frame, text="Enter Matrix Dimensions", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        
        ttk.Label(dim_frame, text="Number of supply:").grid(row=1, column=0, padx=5, pady=5)
        self.supply_number_entry = ttk.Entry(dim_frame, width=10)
        self.supply_number_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dim_frame, text="Number of demand:").grid(row=1, column=2, padx=5, pady=5)
        self.demand_number_entry = ttk.Entry(dim_frame, width=10)
        self.demand_number_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(dim_frame, text="Create Arrays Input", command=self.create_arrays_input).grid(row=2, column=0, columnspan=4, pady=20)
    
    def create_arrays_input(self):
        try:
            self.supply_number = int(self.supply_number_entry.get())
            self.demand_number = int(self.demand_number_entry.get())
            
            if self.supply_number <= 0 or self.demand_number <= 0:
                messagebox.showerror("Error", "Dimensions must be positive integers!")
                return
            
            if self.supply_number > 50 or self.demand_number > 50:
                messagebox.showwarning("Warning", "Large arrays may not display well. Consider smaller dimensions.")
            
            self.setup_arrays_input()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for dimensions!")
    
    def setup_arrays_input(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Enter Arrays", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Array M frame
        supply_array_frame = ttk.LabelFrame(main_frame, text=f"Array of Supplies (size {self.supply_number})", padding="10")
        supply_array_frame.pack(pady=10, fill="x")
        
        # Create scrollable frame for Array M if needed
        if self.supply_number > 10:
            m_canvas = tk.Canvas(supply_array_frame, height=100)
            m_scrollbar = ttk.Scrollbar(supply_array_frame, orient="horizontal", command=m_canvas.xview)
            m_scrollable_frame = ttk.Frame(m_canvas)
            m_canvas.configure(xscrollcommand=m_scrollbar.set)
            m_canvas.create_window((0, 0), window=m_scrollable_frame, anchor="nw")
            
            m_scrollbar.pack(side="bottom", fill="x")
            m_canvas.pack(side="top", fill="both", expand=True)
            m_parent = m_scrollable_frame
        else:
            m_parent = supply_array_frame
        
        # Create Array M inputs
        self.supply_array_widgets = []
        for i in range(self.supply_number):
            entry = ttk.Entry(m_parent, width=8, justify='center')
            entry.grid(row=0, column=i, padx=2, pady=2)
            self.supply_array_widgets.append(entry)
        
        # Update scroll region for Array M
        if self.supply_number > 10:
            m_scrollable_frame.bind("<Configure>", lambda e: m_canvas.configure(scrollregion=m_canvas.bbox("all")))
        
        # Array N frame
        demand_array_frame = ttk.LabelFrame(main_frame, text=f"Array of Demands (size {self.demand_number})", padding="10")
        demand_array_frame.pack(pady=10, fill="x")
        
        # Create scrollable frame for Array N if needed
        if self.demand_number > 10:
            n_canvas = tk.Canvas(demand_array_frame, height=100)
            n_scrollbar = ttk.Scrollbar(demand_array_frame, orient="horizontal", command=n_canvas.xview)
            n_scrollable_frame = ttk.Frame(n_canvas)
            n_canvas.configure(xscrollcommand=n_scrollbar.set)
            n_canvas.create_window((0, 0), window=n_scrollable_frame, anchor="nw")
            
            n_scrollbar.pack(side="bottom", fill="x")
            n_canvas.pack(side="top", fill="both", expand=True)
            n_parent = n_scrollable_frame
        else:
            n_parent = demand_array_frame
        
        # Create Array N inputs
        self.demand_array_widgets = []
        for j in range(self.demand_number):
            entry = ttk.Entry(n_parent, width=8, justify='center')
            entry.grid(row=0, column=j, padx=2, pady=2)
            self.demand_array_widgets.append(entry)
        
        # Update scroll region for Array N
        if self.demand_number > 10:
            n_scrollable_frame.bind("<Configure>", lambda e: n_canvas.configure(scrollregion=n_canvas.bbox("all")))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Proceed to Matrix Input", command=self.process_arrays_and_create_matrix).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear Arrays", command=self.clear_arrays).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="New Dimensions", command=self.setup_dimension_input).pack(side=tk.LEFT, padx=10)
    
    def clear_arrays(self):
        for widget in self.supply_array_widgets:
            widget.delete(0, tk.END)
        for widget in self.demand_array_widgets:
            widget.delete(0, tk.END)
    
    def process_arrays_and_create_matrix(self):
        try:
            # Validate and get Array M values
            self.supply_array = []
            for i, widget in enumerate(self.supply_array_widgets):
                value = widget.get().strip()
                if value == "":
                    messagebox.showerror("Error", f"Empty input in Array M at position {i+1}. Please enter a number.")
                    widget.focus_set()
                    return
                
                try:
                    num_value = float(value)
                except:
                    messagebox.showerror("Error", f"Invalid input in Array M at position {i+1} with input >{value}<. Please enter a valid number.")
                    widget.focus_set()
                    widget.select_range(0, tk.END)
                    return
                
                # Format the number
                
                self.supply_array.append(num_value)
            
            # Validate and get Array N values
            self.demand_array = []
            for j, widget in enumerate(self.demand_array_widgets):
                value = widget.get().strip()
                if value == "":
                    messagebox.showerror("Error", f"Empty input in Array N at position {j+1}. Please enter a number.")
                    widget.focus_set()
                    return
                
                try:
                    num_value = float(value)
                except:
                    messagebox.showerror("Error", f"Invalid input in Array N at position {j+1} with input >{value}<. Please enter a valid number.")
                    widget.focus_set()
                    widget.select_range(0, tk.END)
                    return
                
                self.demand_array.append(num_value)
            
            # If we reach here, all inputs are valid, proceed to matrix input
            self.setup_matrix_input()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing arrays: {str(e)}")

    def create_matrix_input(self):
        try:
            self.supply_number = int(self.supply_number_entry.get())
            self.demand_number = int(self.demand_number_entry.get())
            
            if self.supply_number <= 0 or self.demand_number <= 0:
                messagebox.showerror("Error", "Dimensions must be positive integers!")
                return
            
            if self.supply_number > 10 or self.demand_number > 10:
                messagebox.showwarning("Warning", "Large matrices may not display well. Consider smaller dimensions.")
            
            self.setup_matrix_input()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for dimensions!")
    
    def setup_matrix_input(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Enter Matrix Elements ({self.supply_number} x {self.demand_number})", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Show arrays info
        arrays_info_frame = ttk.Frame(main_frame)
        arrays_info_frame.pack(pady=5)
        
        ttk.Label(arrays_info_frame, text=f"Array M: {self.supply_array}", 
                 font=("Arial", 10), foreground="blue").pack()
        ttk.Label(arrays_info_frame, text=f"Array N: {self.demand_array}", 
                 font=("Arial", 10), foreground="green").pack()
        
        # Frame for matrix input
        matrix_frame = ttk.Frame(main_frame)
        matrix_frame.pack(pady=20)
        
        # Clear and reinitialize entry widgets
        self.entry_widgets = []
        
        # Create input grid with simplified approach
        for i in range(self.supply_number):
            row_entries = []
            for j in range(self.demand_number):
                entry = ttk.Entry(matrix_frame, width=8, justify='center')
                # Use simple grid without additional parameters that might cause issues
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entry_widgets.append(row_entries)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Display Matrix", command=self.input_cost_matrix).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear Matrix", command=self.clear_inputs).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Arrays", command=self.setup_arrays_input).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="New Dimensions", command=self.setup_dimension_input).pack(side=tk.LEFT, padx=10)
    
    def clear_inputs(self):
        try:
            if self.entry_widgets:
                for i in range(len(self.entry_widgets)):
                    for j in range(len(self.entry_widgets[i])):
                        if self.entry_widgets[i][j]:
                            self.entry_widgets[i][j].delete(0, tk.END)
        except Exception as e:
            print(f"Error clearing inputs: {e}")
            # If there's an error clearing, reinitialize the matrix input
            self.setup_matrix_input()
    
    def input_cost_matrix(self):
        try:
            # Debug information
            print(f"Debug - Starting input_cost_matrix with m={self.supply_number}, n={self.demand_number}")
            print(f"Debug - entry_widgets structure: {len(self.entry_widgets)} rows")
            for i, row in enumerate(self.entry_widgets):
                print(f"Debug - Row {i}: {len(row)} columns")
            
            # Validate that entry_widgets is properly initialized
            if not self.entry_widgets or len(self.entry_widgets) != self.supply_number:
                messagebox.showerror("Error", "Matrix input not properly initialized. Please try again.")
                self.setup_matrix_input()
                return
            
            # Get matrix values
            self.cost_matrix = []
            for i in range(self.supply_number):
                print(f"Debug - Processing row {i}")
                
                if i >= len(self.entry_widgets) or len(self.entry_widgets[i]) != self.demand_number:
                    messagebox.showerror("Error", f"Row {i+1} input not properly initialized. Please try again.")
                    self.setup_matrix_input()
                    return
                
                row = []
                for j in range(self.demand_number):
                    print(f"Debug - Processing cell [{i},{j}]")
                    
                    if j >= len(self.entry_widgets[i]):
                        messagebox.showerror("Error", f"Column {j+1} in row {i+1} not found. Please try again.")
                        self.setup_matrix_input()
                        return
                    
                    try:
                        # Get the widget and its value
                        widget = self.entry_widgets[i][j]
                        print(f"Debug - Widget at [{i},{j}]: {widget}")
                        
                        # Force update the widget to ensure it's properly displayed
                        widget.update_idletasks()
                        
                        # Get the value
                        value = widget.get().strip()
                        print(f"Debug - Value at [{i},{j}]: '{value}'")
                        
                    except Exception as widget_error:
                        print(f"Debug - Widget error at [{i},{j}]: {widget_error}")
                        messagebox.showerror("Error", f"Error accessing cell [{i+1},{j+1}]: {str(widget_error)}")
                        self.setup_matrix_input()
                        return
                    
                    if value == "":
                        messagebox.showerror("Error", f"Empty input at cell [{i+1},{j+1}]. Please enter a number.")
                        try:
                            self.entry_widgets[i][j].focus_set()
                        except:
                            pass
                        return
                    
                    # Validate numeric input
                    try:
                        num_value = float(value)
                        print(f"Debug - Parsed number at [{i},{j}]: {num_value}")
                    except ValueError as num_error:
                        print(f"Debug - Number parsing error at [{i},{j}]: {num_error}")
                        messagebox.showerror("Error", f"Invalid input at cell [{i+1},{j+1}] with input >{value}<. Please enter a valid number.")
                        try:
                            self.entry_widgets[i][j].focus_set()
                            self.entry_widgets[i][j].select_range(0, tk.END)
                        except:
                            pass
                        return
                    
                    row.append(num_value)
                    print(f"Debug - Added to row: {num_value}")
                
                self.cost_matrix.append(row)
                print(f"Debug - Completed row: {row}")
            
            print("Debug - Matrix processing completed successfully")
            print(f"Debug - Cost matrix: {self.cost_matrix}")
            
            # If we reach here, all inputs are valid
            self.result_matrix = nwc.NWC(self.demand_array,self.supply_array, self.cost_matrix)
            self.initial_cost = opt.calculate_final_cost(self.result_matrix, self.cost_matrix)
            self.result_matrix = opt.optimize(self.result_matrix, self.cost_matrix)
            self.final_cost = opt.calculate_final_cost(self.result_matrix, self.cost_matrix)
            self.show_matrix_display()
            
        except Exception as e:
            print(f"Debug - Unexpected error in input_cost_matrix: {e}")
            print(f"Debug - Error type: {type(e)}")
            import traceback
            print(f"Debug - Traceback: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Error processing matrix: {str(e)}")
            # Stay in input phase for any other unexpected errors
    
    def show_matrix_display(self):
        # Create new window for matrix display 
        display_window = tk.Toplevel(self.root)
        display_window.title("Matrix Display")

        # Make window fullscreen
        display_window.state('zoomed') 

        # Bind Escape key to exit fullscreen
        display_window.bind('<Escape>', lambda e: display_window.destroy())

        # Main frame
        main_frame = ttk.Frame(display_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Optimized Matrix", 
                                font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # === Cost Summary Section ===
        cost_frame = ttk.Frame(main_frame)
        cost_frame.pack(pady=10)

        initial_cost = getattr(self, "initial_cost", 0)
        final_cost = getattr(self, "final_cost", 0)
        reduction = initial_cost - final_cost
        reduction_percent = (reduction / initial_cost * 100) if initial_cost != 0 else 0

        summary_text = (
            f"Initial Cost: {initial_cost:,.2f}     "
            f"Final Cost: {final_cost:,.2f}     "
            f"Reduction: {reduction:,.2f} ({reduction_percent:.2f}%)"
        )

        cost_label = ttk.Label(cost_frame, text=summary_text, font=("Arial", 14))
        cost_label.pack()
        # === End Cost Summary Section ===

        # Create scrollable frame for matrix
        canvas = tk.Canvas(main_frame, bg="white")
        scrollable_frame = ttk.Frame(canvas)

        # Configure scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Pack scrollbars and canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        # Frame for matrix display inside scrollable area 
        matrix_frame = ttk.Frame(scrollable_frame)
        matrix_frame.pack(padx=20, pady=20)

        # Default cell values
        cell_width = 10
        cell_height = 2
        font_size = 12

        # Fit smaller matrices
        if self.supply_number <= 20 and self.demand_number <= 20:
            screen_width = display_window.winfo_screenwidth()
            screen_height = display_window.winfo_screenheight()
            available_width = screen_width - 200
            available_height = screen_height - 300

            max_cell_width = available_width // (self.demand_number + 1)
            max_cell_height = available_height // (self.supply_number + 1)

            if max_cell_width >= 96 and max_cell_height >= 60:
                cell_width = min(10, min(20, max_cell_width // 8))
                cell_height = min(2, min(5, max_cell_height // 20))
                font_size = min(12, min(18, min(max_cell_width // 6, max_cell_height // 3)))

        # Empty top-left cell
        empty_label = tk.Label(matrix_frame, text="", width=cell_width, height=cell_height, 
                            relief=tk.RIDGE, bg="lightgray", font=("Arial", font_size, "bold"))
        empty_label.grid(row=0, column=0, padx=2, pady=2)

        # Column headers
        for j in range(self.demand_number):
            header_label = tk.Label(matrix_frame, text=str(j+1), width=cell_width, height=cell_height,
                                    relief=tk.RIDGE, bg="lightblue", font=("Arial", font_size, "bold"))
            header_label.grid(row=0, column=j+1, padx=2, pady=2)

        # Row headers and matrix values
        for i in range(self.supply_number):
            row_header = tk.Label(matrix_frame, text=str(i+1), width=cell_width, height=cell_height,
                                relief=tk.RIDGE, bg="lightgreen", font=("Arial", font_size, "bold"))
            row_header.grid(row=i+1, column=0, padx=2, pady=2)
            for j in range(self.demand_number):
                value_label = tk.Label(matrix_frame, text=self.result_matrix[i][j], width=cell_width, height=cell_height,
                                    relief=tk.RIDGE, bg="white", font=("Arial", font_size))
                value_label.grid(row=i+1, column=j+1, padx=2, pady=2)
        exit_frame = ttk.Frame(main_frame)
        exit_frame.pack(pady=20)

        exit_button = ttk.Button(exit_frame, text="Exit Program", command=sys.exit)
        exit_button.pack()

        # Configure scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        # Mousewheel bindings
        def on_mousewheel_vertical(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_mousewheel_horizontal(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel_vertical)
        canvas.bind("<Shift-MouseWheel>", on_mousewheel_horizontal)

        # Update scroll region
        display_window.after(100, configure_scroll_region)

        # Print debug info
        print(f"\nSupply Array: {self.supply_array}")
        print(f"Demand Array: {self.demand_array}")
        print("Result Matrix:")
        for row in self.result_matrix:
            print(row)
        print(f"Initial Cost: {initial_cost}")
        print(f"Final Cost: {final_cost}")
        print(f"Reduction: {reduction:.2f} ({reduction_percent:.2f}%)")


def main():
    root = tk.Tk()
    app = MatrixGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()