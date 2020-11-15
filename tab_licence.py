import database
import tab_insert_licence
from tkinter import ttk, Button, Menu, Label, W

def licence(tab):
    drivers = database.get_drivers_with_licence()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("name", "passport", "licence_id", "number", "start_date", "end_date")

    tree.heading("#0", text = "Id")
    tree.heading("name", text = "Name")
    tree.heading("passport", text = "Passport")
    tree.heading("licence_id", text = "Licence Id")
    tree.heading("number", text = "Number")
    tree.heading("start_date", text = "Start Date")
    tree.heading("end_date", text = "End Date")

    tree.grid(column = 0, row = 0, columnspan = 4)

    for driver in drivers:
        tree.insert(parent = '', index = 'end', text = driver[0], values = (driver[1] + ' ' + driver[2], driver[3], "doesn't have licence" if driver[4] == None else driver[4], "doesn't have licence" if driver[5] == None else driver[5], "doesn't have licence" if driver[6] == None else driver[6], "doesn't have licence" if driver[7] == None else driver[7]))

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 3, row = 1)

    btn = Button(tab, text = "Refresh", command = refresh_click)  
    btn.grid(column = 0, row = 1, sticky = W)

    btn1 = Button(tab, text = "Add licence to selected driver", command = add_licence_to_driver_click)  
    btn1.grid(column = 1, row = 1, sticky = W)

    btn2 = Button(tab, text = "Remove licence from selected driver", command = remove_licence_from_driver_click)  
    btn2.grid(column = 2, row = 1, sticky = W)

    tab_insert_licence.insert_licence(tab)

def refresh_click():
    drivers = database.get_drivers_with_licence()
    tree.delete(*tree.get_children())
    for driver in drivers:
        tree.insert(parent = '', index = 'end', text = driver[0], values = (driver[1] + ' ' + driver[2], driver[3], "doesn't have licence" if driver[4] == None else driver[4], "doesn't have licence" if driver[5] == None else driver[5], "doesn't have licence" if driver[6] == None else driver[6]))

def add_licence_to_driver_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        tab_insert_licence.set_values(tree.item(id))
    except IndexError:
        error_lbl.configure(text = "Select a driver to add licence")

def remove_licence_from_driver_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        licence_id = tree.item(id)['values'][2]
        if (licence_id == "doesn't have licence"):
            error_lbl.configure(text = "Selected driver hasn't licence")
            return
        database.remove_licence_by_id(licence_id)
    except IndexError:
        error_lbl.configure(text = "Select a driver to remove licence")