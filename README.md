
# Transportation Problem Solver by PDC

This project provides a complete implementation of the **Transportation Problem** using Python. It includes tools for reading input data manually or from Excel, generating an initial feasible solution using the **North-West Corner Rule**, optimizing the solution, handling degeneracy, and visualizing the optimization path.

---

## 📁 Project Structure

```
.
├── InputData.py           # Manually input demands, supplies, and costs
├── InputFromExcel.py      # Extracts data from Excel file (path input from keyboard)
├── NorthWestCorner.py     # Generates initial solution using North-West Corner method
├── U_V_Degeneracy.py      # Calculates u & v for degeneracy matrix
├── Optimize.py            # Optimizes the transportation plan
├── PathFinder.py          # Builds an optimization path from the current plan
├── Terminal_Execute.py    # Terminal-based execution for input, optimization and output result
├── Popup_Execute.py       # GUI-based execution using Tkinter
├── ConvertToExcel.py      # Converts result to Excel format
├── input.xlsx             # Sample input data (cost, supply, demand)
├── output.xlsx            # Output file with the result matrix
├── main.py                # Entry point of the program (optional)
├── README.md              # Project documentation
```

---

## ▶️ How to Run

1. **Install required package:**

   ```bash
   pip install openpyxl
   ```

2. **Run the program:**

   - **GUI (Popup)**:
     ```bash
     python Popup_Execute.py
     ```
   - **Terminal**:
     ```bash
     python Terminal_Execute.py
     ```

3. **Choose Input Mode:**
   - **Manual Input**: Uses logic from `InputData.py`
   - **Excel Input**: Enter Excel file path when prompted (uses `InputFromExcel.py`)

---

## ✨ Features

- Manual and Excel-based data input
- North-West Corner Rule for initial feasible solution
- Optimization using a path-based improvement method
- Modular and extensible code structure
- Degeneracy handling using U-V method
- GUI and terminal-based execution modes
- Automatically writes result matrix to `output.xlsx`
- Compares initial and optimized cost

---

## 🧠 Algorithms Used

- **North-West Corner Rule** for initial feasible solution
- **Stepping Stone / MODI-like optimization** for cost reduction
- **Closed loop path generation** to identify reallocation paths

---

## 📦 Requirements

- Python 3.7+
- `openpyxl` (for reading/writing Excel files)

---

## 👤 Author

- Developed by **Phan Dinh Cuong**
- 📧 Contact: **phandinhcuong02@gmail.com**
- Contributions and feedback are welcome!
