import tkinter as tk
from tkinter import ttk, messagebox
from data.db import FinanceDB

class FinanceApp:
    def __init__(self, root):
        self.db = FinanceDB()
        self.root = root
        self.root.title("Smart Finance Tracker")
        self._build_ui()

    def _build_ui(self):
        # Input variables
        self.type_var = tk.StringVar(value="Expense")
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        # Form
        ttk.Label(self.root, text="Type").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self.root, textvariable=self.type_var, values=["Income", "Expense"]).grid(row=0, column=1)

        ttk.Label(self.root, text="Category").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.category_var).grid(row=1, column=1)

        ttk.Label(self.root, text="Amount").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.root, textvariable=self.amount_var)
        self.amount_entry.grid(row=2, column=1)

        ttk.Label(self.root, text="Description").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.desc_var).grid(row=3, column=1)

        # Buttons
        ttk.Button(self.root, text="Save Transaction", command=self.save_transaction).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.root, text="View Transactions", command=self.show_transactions).grid(row=5, column=0, columnspan=2, pady=5)

        # Balance
        self.balance_label = ttk.Label(self.root, text="")
        self.balance_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.update_balance()

    def save_transaction(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid numeric amount.")
            return

        self.db.add_transaction(
            self.type_var.get(),
            self.category_var.get(),
            amount,
            self.desc_var.get()
        )

        self.amount_entry.delete(0, tk.END)
        self.desc_var.set("")
        self.update_balance()

    def update_balance(self):
        balance = self.db.get_balance()
        self.balance_label.config(text=f"Current Balance: ${balance:.2f}")

    def show_transactions(self):
        transactions = self.db.get_all_transactions()
        top = tk.Toplevel(self.root)
        top.title("All Transactions")
        text = tk.Text(top, width=80, height=20)
        text.pack()

        text.insert(tk.END, f"{'Date':<20} {'Type':<10} {'Category':<15} {'Amount':<10} Description\n")
        text.insert(tk.END, "-"*80 + "\n")
        for row in transactions:
            date, ttype, category, amount, desc = row
            text.insert(tk.END, f"{date:<20} {ttype:<10} {category:<15} ${amount:<10.2f} {desc}\n")
