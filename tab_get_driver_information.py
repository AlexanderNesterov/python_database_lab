import database
import re
from tkinter import ttk, W, Label, Entry, Button

def get_driver_information(tab1):
    global tab
    tab = tab1

    global passport_txt
    passport_lbl = Label(tab, text = "Input driver's passport: ")
    passport_lbl.grid(column = 0, row = 0, sticky = W)
    passport_txt = Entry(tab, width = 40)
    passport_txt.grid(column = 1, row = 0)

    btn = Button(tab, text = "Submit", command = search_for_driver_click)  
    btn.grid(column = 2, row = 0, sticky = W)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 3, row = 0, sticky = W)

def check_passport():
    passport = passport_txt.get()
    if (passport == None or passport == ""):
        return False

    regex = re.compile("[0-9]{4} [0-9]{6}")
    match = re.search(regex, passport)
    if (match == None or match.group() != passport):
        return False
    return True

def set_driver_info(passport):
    driver = database.get_driver_by_passport(passport)
    if (driver == None):
        error_lbl.configure(text = "Driver with passport {} doesn't exist".format(passport))
        return

    driver_id = driver[0]

    info_lbl = Label(tab, text = "Inforamtion")
    info_lbl.grid(column = 0, row = 1, sticky = W)
    first_name_lbl = Label(tab, text = "First Name: {}".format(driver[1]))
    first_name_lbl.grid(column = 0, row = 2, sticky = W)
    last_name_lbl = Label(tab, text="Last Name: {}".format(driver[2]))
    last_name_lbl.grid(column = 0, row = 3, sticky = W)
    passport_lbl = Label(tab, text="Passport: {}".format(driver[3]))
    passport_lbl.grid(column = 0, row = 4, sticky = W)
    birthdate_lbl = Label(tab, text="Birthdate: {}".format(driver[4]))
    birthdate_lbl.grid(column = 0, row = 5, sticky = W)
    registration_lbl = Label(tab, text="Registration: {}".format(driver[5]))
    registration_lbl.grid(column = 0, row = 6, sticky = W)

    licence = database.get_licence_by_driver_id(driver_id)

    licence_info_lbl = Label(tab, text = "Licence Inforamtion")
    licence_info_lbl.grid(column = 1, row = 1, sticky = W)
    number_lbl = Label(tab, text = "Number: {}".format(licence[1]))
    number_lbl.grid(column = 1, row = 2, sticky = W)
    start_date_lbl = Label(tab, text="Start Date: {}".format(licence[2]))
    start_date_lbl.grid(column = 1, row = 3, sticky = W)
    end_date_lbl = Label(tab, text="End Date: {}".format(licence[3]))
    end_date_lbl.grid(column = 1, row = 4, sticky = W)

    cars = database.get_cars_by_driver_id(driver_id)

    tree = ttk.Treeview(tab)
    tree["columns"]=("mark", "number", "registration_date")

    tree.heading("#0", text = "ID")
    tree.heading("mark", text = "Mark")
    tree.heading("number", text = "Number")
    tree.heading("registration_date", text = "Registration Date")

    tree.grid(column = 0, row = 9, columnspan = 5)

    for car in cars:
        tree.insert(parent = '', index = 'end', text = car[0], values = (car[1], car[2], car[3]))

    car_ids = []
    for car in cars:
        car_ids.append(car[0])
    
    car_ids_str = ("{}".format(car_ids))[1:-1]
    penalties = database.get_penalties_by_car_ids(car_ids_str)

    tree2 = ttk.Treeview(tab)
    tree2["columns"]=("number", "penalty_date", "description", "cost")

    tree2.heading("#0", text = "Mark")
    tree2.heading("number", text = "Number")
    tree2.heading("penalty_date", text = "Peanlty Date")
    tree2.heading("description", text = "Description")
    tree2.heading("cost", text = "Cost")

    tree2.grid(column = 0, row = 10, columnspan = 5)

    for penalty in penalties:
        tree2.insert(parent = '', index = 'end', text = penalty[0], values = (penalty[1], penalty[2], penalty[3], penalty[4]))

def search_for_driver_click():
    error_lbl.configure(text = "")
    if (check_passport()):
        set_driver_info(passport_txt.get())
    else:
        error_lbl.configure(text = "Incorrect passport inforamtion")
            