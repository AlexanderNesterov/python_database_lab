import database
import tab_insert_car
import tab_insure_car
from tkinter import ttk, Button, Menu, Label, W

def get_table_with_cars(tab):
    cars = database.get_cars_with_insurance()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("mark", "number", "registration_date", "insurance_id", "insurance_date", "insurance_cost", "payment")

    tree.heading("#0", text = "Id")
    tree.heading("mark", text = "Mark")
    tree.heading("number", text = "Number")
    tree.heading("registration_date", text = "Registration date")
    tree.heading("insurance_id", text = "Insurance id")
    tree.heading("insurance_date", text = "Insurance date")
    tree.heading("insurance_cost", text = "Insurance cost")
    tree.heading("payment", text = "Payment")

    tree.grid(column = 0, row = 0, columnspan = 4)

    for car in cars:
        payment = "not insured"
        if (car[6] != None):
            payment = car[6] / 10

        tree.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3], "not insured" if car[4] == None else car[4], "not insured" if car[5] == None else car[5], "not insured" if car[6] == None else car[6], payment))

    btn = Button(tab, text = "Refresh", command = refresh_click)  
    btn.grid(column = 0, row = 1, sticky = W)

    btn1 = Button(tab, text = "Insure selected car", command = insure_car_click)  
    btn1.grid(column = 1, row = 1, sticky = W)

    btn2 = Button(tab, text = "Remove selected car", command = remove_car_click)  
    btn2.grid(column = 2, row = 1, sticky = W)

    btn3 = Button(tab, text = "Remove selected insurance", command = remove_insurance_click)  
    btn3.grid(column = 3, row = 1, sticky = W)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 4, row = 1)

    tab_insert_car.insert_car(tab)
    tab_insure_car.insure_car(tab)

def refresh_click():
    cars = database.get_cars_with_insurance()
    tree.delete(*tree.get_children())
    for car in cars:
        payment = "not insured"
        if (car[6] != None):
            payment = car[6] / 10

        tree.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3], "not insured" if car[4] == None else car[4], "not insured" if car[5] == None else car[5], "not insured" if car[6] == None else car[6], payment))

def insure_car_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        tab_insure_car.set_values(tree.item(id))
    except IndexError:
        error_lbl.configure(text = "Select a car to insure")

def remove_car_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        car_id = tree.item(id)['text']
        database.remove_car_by_id(car_id)
    except IndexError:
        error_lbl.configure(text = "Select a car to remove")

def remove_insurance_click():
    error_lbl.configure(text = "")
    try:
        id = tree.selection()[0]
        insurance_id = tree.item(id)['values'][3]
        if (insurance_id == "not insured"):
            error_lbl.configure(text = "Cannot remove insurance due to car hasn't insurance")
            return
        database.remove_insurance_by_id(insurance_id)
    except IndexError:
        error_lbl.configure(text = "Select a insurance to remove")
