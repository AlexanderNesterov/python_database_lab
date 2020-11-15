import database
import tab_insert_penalty
from tkinter import ttk, Label, Button, W

def get_table_with_penalties(tab):
    penalties = database.get_penalties()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("description", "cost")

    tree.heading("#0", text = "ID")
    tree.heading("description", text = "Description")
    tree.heading("cost", text = "Cost")

    tree.grid(column = 0, row = 0)

    for penalty in penalties:
        tree.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2]))

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 3, row = 1)

    btn = Button(tab, text = "Refresh", command = refresh_click)  
    btn.grid(column = 0, row = 1, sticky = W)

    btn1 = Button(tab, text = "Remove selected penalty", command = remove_penalty_click)  
    btn1.grid(column = 1, row = 1, sticky = W)

    tab_insert_penalty.insert_penalty(tab)

def refresh_click():
    penalties = database.get_penalties()
    tree.delete(*tree.get_children())
    for penalty in penalties:
        tree.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2]))

def remove_penalty_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        penalty_id = tree.item(id)['text']
        database.remove_penalty_by_id(penalty_id)
    except IndexError:
        error_lbl.configure(text = "Select a penalty to remove")