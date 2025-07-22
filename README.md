# Transportation Problem Solver by PDC

This project provides a complete implementation of the **Transportation Problem** using Python. It includes tools for reading input data manually or from Excel, generating an initial feasible solution using the **North-West Corner Rule**, optimizing the solution, and visualizing the optimization path.

---

## Project Structure

```
.
├── InputData.py          # Manually input demands, supplies, and costs
├── InputFromExcel.py     # Extracts data from Excel file (path input from keyboard)
├── NorthWestCorner.py    # Generates initial solution using North-West Corner method
├── Optimize.py           # Optimizes the transportation plan
├── PathFinder.py         # Builds an optimization path from the current plan
├── main.py               # Entry point of the program
├── input.xlsx            # Sample input form
```

---

## How to Run

1. **Install required packages:**

   ```bash
   pip install openpyxl 
   ```

2. **Run the main script:**

   ```bash
   python main.py
   ```

3. **Choose Input Mode:**
   - **Manual Input**: Uses logic from `InputData.py`
   - **Excel Input**: Enter Excel file path when prompted (uses `InputFromExcel.py`)

---

## Features

- ✅ Manual and Excel-based data input
- ✅ North-West Corner Rule for initial feasible solution
- ✅ Path-based optimization method
- ✅ Modular, extensible code structure

---

## Algorithms Used

- **North-West Corner Rule** for initial solution
- **Stepping Stone or MODI-like optimization approach**
- **Path generation** to determine adjustments in allocation

---

## 📂 Requirements

- Python 3.7+
- `openpyxl` (for Excel file reading)


## 🛠️ Author

Developed by PhanDinhCuong
Contact at phandinhcuong02@gmail.com
Feel free to contribute, suggest improvements, or raise issues!

---
