import database
import tab_insert_driver
import tab_update_driver
from tkinter import ttk, Button, Menu, Label, W

def get_table_with_drivers(tab):
    drivers = database.get_drivers()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("first_name", "last_name", "passport", "birthdate", "registration")

    tree.heading("#0", text = "ID")
    tree.heading("first_name", text = "First Name")
    tree.heading("last_name", text = "Last Name")
    tree.heading("passport", text = "Passport")
    tree.heading("birthdate", text = "Birthdate")
    tree.heading("registration", text = "Registration")

    tree.grid(column = 0, row = 0, columnspan = 15)

    for driver in drivers:
        tree.insert(parent = '', index = 'end', text = driver[0], values = (driver[1], driver[2], driver[3], driver[4], driver[5]))

    btn = Button(tab, text = "Refresh", command = refresh_click)  
    btn.grid(column = 0, row = 1)

    btn1 = Button(tab, text = "Update selected driver", command = update_driver_click)  
    btn1.grid(column = 2, row = 1)

    btn2 = Button(tab, text = "Remove selected driver", command = remove_driver_click)  
    btn2.grid(column = 3, row = 1)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")  
    error_lbl.grid(column = 4, row = 1, sticky = W)

    tab_insert_driver.insert_driver(tab)
    tab_update_driver.update_driver(tab)

def refresh_click():
    drivers = database.get_drivers()
    tree.delete(*tree.get_children())
    for driver in drivers:
        tree.insert(parent = '', index = 'end', text = driver[0], values = (driver[1], driver[2], driver[3], driver[4], driver[5]))

def update_driver_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        tab_update_driver.set_values(tree.item(id))
    except IndexError:
        error_lbl.configure(text = "Select a driver to update")

def remove_driver_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        driver_id = tree.item(id)['text']
        database.remove_driver_by_id(driver_id)
    except IndexError:
        error_lbl.configure(text = "Select a driver to delete")
