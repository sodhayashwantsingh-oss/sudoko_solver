import tkinter as tk
from tkinter import messagebox
import time

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("430x500")
root.configure(bg="white")

entries = [[None for _ in range(9)] for _ in range(9)]


# Function to determine background color based on 3x3 block
def get_bg_color(i, j):
    if (i // 3 + j // 3) % 2 == 0:
        return "#e3f2fd"  # light blue
    else:
        return "#ffffff"  # white


# Build the Sudoku grid
for i in range(9):
    for j in range(9):
        e = tk.Entry(root, width=2, font=('Arial', 18), justify='center', bd=1, relief="solid",
                     bg=get_bg_color(i, j))
        e.grid(row=i, column=j, padx=2, pady=2, ipady=5)
        entries[i][j] = e


# Extract the grid from user input
def get_grid():
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val == '':
                row.append(0)
            elif val.isdigit() and 1 <= int(val) <= 9:
                row.append(int(val))
            else:
                entries[i][j].config(bg='salmon')
                messagebox.showerror("Invalid Input", f"Invalid entry at row {i + 1}, column {j + 1}")
                return None
        grid.append(row)
    return grid


# Check if placing a number is valid
def is_valid(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


# Recursive backtracking solver (with optional animation)
def solve_board(board, step_by_step=False):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if step_by_step:
                            entries[i][j].delete(0, tk.END)
                            entries[i][j].insert(0, str(num))
                            entries[i][j].config(bg="#c8e6c9")  # greenish highlight
                            root.update()
                            time.sleep(0.05)
                        if solve_board(board, step_by_step):
                            return True
                        board[i][j] = 0
                        if step_by_step:
                            entries[i][j].delete(0, tk.END)
                            entries[i][j].config(bg=get_bg_color(i, j))
                            root.update()
                            time.sleep(0.05)
                return False
    return True


# Display solution on grid
def display_solution(board):
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]))
            entries[i][j].config(bg=get_bg_color(i, j))


# Solve the board
def solve(step_by_step=False):
    board = get_grid()
    if board:
        if solve_board(board, step_by_step):
            display_solution(board)
            messagebox.showinfo("Solved", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Unsolvable", "No solution exists for this puzzle.")


# Clear board
def clear():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].config(bg=get_bg_color(i, j))


# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.grid(row=9, column=0, columnspan=9, pady=20)

tk.Button(btn_frame, text="Solve Instantly", command=lambda: solve(False),
          bg="#4CAF50", fg="white", font=('Arial', 12), padx=10, pady=5).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Solve Step-by-Step", command=lambda: solve(True),
          bg="#2196F3", fg="white", font=('Arial', 12), padx=10, pady=5).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Clear", command=clear,
          bg="#f44336", fg="white", font=('Arial', 12), padx=10, pady=5).grid(row=0, column=2, padx=10)

# Add title label
title_label = tk.Label(root, text="Sudoku Solver", font=('Arial', 16, 'bold'),
                       bg="white", fg="#333333")
title_label.grid(row=10, column=0, columnspan=9, pady=10)

root.mainloop()
