import database
from tkinter import ttk

def get_table_with_penalties(tab):
    penalties = database.get_penalties()

    tree = ttk.Treeview(tab)
    tree["columns"]=("description", "cost")

    tree.heading("#0", text = "ID")
    tree.heading("description", text = "Description")
    tree.heading("cost", text = "Cost")

    tree.grid(column = 0, row = 0)

    for penalty in penalties:
        tree.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2]))