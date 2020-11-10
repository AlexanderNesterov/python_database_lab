import database
from datetime import datetime
from tkinter import ttk, W, Label, Button

def get_penalties_with_info(tab):
    penalties_info = database.get_penalties_with_info()

    global tree
    tree = ttk.Treeview(tab)
    tree["columns"]=("penalty_date", "description", "mark", "cost", "name")

    tree.heading("#0", text = "Number")
    tree.heading("penalty_date", text = "Date")
    tree.heading("description", text = "Description")
    tree.heading("mark", text = "Mark")
    tree.heading("cost", text = "Cost")
    tree.heading("name", text = "Name")

    tree.grid(column = 0, row = 0, columnspan = 10)

    for penalty in penalties_info:
        tree.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2], penalty[3], penalty[4], penalty[5] + ' ' + penalty[6]))

    refresh_btn = Button(tab, text = "Refresh", command = refresh_click)  
    refresh_btn.grid(column = 2, row = 1, sticky = W)

    cars = database.get_cars()

    global tree1
    tree1 = ttk.Treeview(tab)
    tree1["columns"]=("mark", "number", "registration_date")

    tree1.heading("#0", text = "Id")
    tree1.heading("mark", text = "Mark")
    tree1.heading("number", text = "Number")
    tree1.heading("registration_date", text = "Registration date")

    tree1.grid(column = 0, row = 2, columnspan = 4)

    for car in cars:
        tree1.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3]))
    
    btn = Button(tab, text = "Select car", command = select_car_click)  
    btn.grid(column = 0, row = 3, sticky = W)

    global car_error_lbl
    car_error_lbl = Label(tab, fg = "#FF0000")  
    car_error_lbl.grid(column = 1, row = 3, sticky = W)

    penalties = database.get_penalties()

    global tree2
    tree2 = ttk.Treeview(tab)
    tree2["columns"]=("description", "cost")

    tree2.heading("#0", text = "ID")
    tree2.heading("description", text = "Description")
    tree2.heading("cost", text = "Cost")

    tree2.grid(column = 6, row = 2, columnspan = 4)

    for penalty in penalties:
        tree2.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2]))

    btn1 = Button(tab, text = "Select penalty", command = select_penalty_click)  
    btn1.grid(column = 6, row = 3, sticky = W)

    global penalty_error_lbl
    penalty_error_lbl = Label(tab, fg = "#FF0000")  
    penalty_error_lbl.grid(column = 7, row = 3, sticky = W)
        
    car_info_lbl = Label(tab, text = "Car information")
    car_info_lbl.grid(column = 0, row = 4, sticky = W)

    global selected_number_lbl
    number_lbl = Label(tab, text = "Number: ")
    number_lbl.grid(column = 0, row = 5, sticky = W)
    selected_number_lbl = Label(tab, text = "")
    selected_number_lbl.grid(column = 1, row = 5, sticky = W)

    global selected_mark_lbl
    mark_lbl = Label(tab, text = "Mark: ")
    mark_lbl.grid(column = 0, row = 6, sticky = W)
    selected_mark_lbl = Label(tab, text = "")
    selected_mark_lbl.grid(column = 1, row = 6, sticky = W)

    penalty_info_lbl = Label(tab, text = "Penalty information")
    penalty_info_lbl.grid(column = 6, row = 4, sticky = W)
  
    global selected_penalty_description_lbl
    penalty_description_lbl = Label(tab, text = "Penalty description: ")
    penalty_description_lbl.grid(column = 6, row = 5, sticky = W)
    selected_penalty_description_lbl = Label(tab, text = "")
    selected_penalty_description_lbl.grid(column = 7, row = 5, sticky = W)

    global selected_penalty_cost_lbl
    penalty_cost_lbl = Label(tab, text = "Penalty cost: ")
    penalty_cost_lbl.grid(column = 6, row = 6, sticky = W)
    selected_penalty_cost_lbl = Label(tab, text = "")
    selected_penalty_cost_lbl.grid(column = 7, row = 6, sticky = W)

    btn1 = Button(tab, text = "Add selected penalty to selected car", command = add_penalty_to_car)  
    btn1.grid(column = 3, row = 7, sticky = W)

def refresh_click():
    penalties_info = database.get_penalties_with_info()
    tree.delete(*tree.get_children())
    for penalty in penalties_info:
        tree.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2], penalty[3], penalty[4], penalty[5] + ' ' + penalty[6]))

def select_car_click():
    car_error_lbl.configure(text = "")
    try:
        id = tree1.selection()[0]
        global selected_car
        selected_car = tree1.item(id)
        selected_car_info = selected_car['values']

        selected_mark_lbl.configure(text = selected_car_info[0])
        selected_number_lbl.configure(text = selected_car_info[1])
    except IndexError:
        car_error_lbl.configure(text = "Select a car from the table above")

def select_penalty_click():
    penalty_error_lbl.configure(text = "")
    try:
        id = tree2.selection()[0]
        global selected_penalty
        selected_penalty = tree2.item(id)
        selected_penalty_info = selected_penalty['values']

        selected_penalty_description_lbl.configure(text = selected_penalty_info[0])
        selected_penalty_cost_lbl.configure(text = selected_penalty_info[1])
    except IndexError:
        penalty_error_lbl.configure(text = "Select a penalty from the table above")

def add_penalty_to_car():
    now = datetime.now().date()
    database.insert_penalty_car(selected_penalty['text'], selected_car['text'], now)