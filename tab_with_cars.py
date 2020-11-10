import database
import tab_insert_car
import tab_insure_car
from tkinter import ttk, Button, Menu, Label

def get_table_with_cars(tab):
    cars = database.get_cars_with_insurance()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("mark", "number", "registration_date", "insurance_date", "insurance_cost")

    tree.heading("#0", text = "Id")
    tree.heading("mark", text = "Mark")
    tree.heading("number", text = "Number")
    tree.heading("registration_date", text = "Registration date")
    tree.heading("insurance_date", text = "Insurance date")
    tree.heading("insurance_cost", text = "Insurance cost")

    tree.grid(column = 0, row = 0, columnspan = 4)

    for car in cars:
        tree.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3], "not insured" if car[4] == None else car[4], "not insured" if car[5] == None else car[5]))

    btn = Button(tab, text = "Refresh", command = refresh_click)  
    btn.grid(column = 0, row = 1)

    btn1 = Button(tab, text = "Insure selected car", command = insure_car_click)  
    btn1.grid(column = 1, row = 1)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 2, row = 1)

    tab_insert_car.insert_car(tab)
    tab_insure_car.insure_car(tab)

def refresh_click():
    cars = database.get_cars_with_insurance()
    tree.delete(*tree.get_children())
    for car in cars:
        tree.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3], "not insured" if car[4] == None else car[4], "not insured" if car[5] == None else car[5]))

def insure_car_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        tab_insure_car.set_values(tree.item(id))
    except IndexError:
        error_lbl.configure(text = "Select a car to insure")
