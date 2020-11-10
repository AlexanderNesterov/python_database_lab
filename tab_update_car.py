import database
import re
from datetime import datetime
from tkinter import ttk
from tkinter import Label, Entry, Button

def update_car(tab):
    car_info_lbl = Label(tab, text = "Car information: ")  
    car_info_lbl.grid(column = 0, row = 0)

    global mark_txt
    mark_lbl = Label(tab, text = "Mark: ")  
    mark_lbl.grid(column = 0, row = 1)
    mark_txt = Entry(tab, width = 10)
    mark_txt.grid(column = 1, row = 1)

    global number_txt
    number_lbl = Label(tab, text = "Number: ")  
    number_lbl.grid(column = 0, row = 2)
    number_txt = Entry(tab, width = 10)
    number_txt.grid(column = 1, row = 2)

    driver_info_lbl = Label(tab, text = "Driver information: ")  
    driver_info_lbl.grid(column = 2, row = 0)

    global passport_txt 
    passport_lbl = Label(tab, text = "Passport: ")
    passport_lbl.grid(column = 0, row = 3)
    passport_txt = Entry(tab, width = 10)
    passport_txt.grid(column = 1, row = 3)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 6)

    btn = Button(tab, text = "Submit", command = clicked)  
    btn.grid(column = 0, row = 5)

def check_mark():
    mark = mark_txt.get()
    if (mark == None or mark == ""):
        return False
    return True

def check_number():
    number = number_txt.get()
    if (number == None or number == ""):
        return False

    regex = re.compile("[a-z]{2}[0-9]{3}[a-z]")
    match = re.search(regex, number)
    if (match == None or match.group() != number):
        return False

    car = database.get_car_by_number(number)
    if (car != None):
        return False
    return True

def check_passport():
    passport = passport_txt.get()
    if (passport == None or passport == ""):
        return False

    regex = re.compile("[0-9]{4} [0-9]{6}")
    match = re.search(regex, passport)
    if (match == None or match.group() != passport):
        return False

    driver = database.get_driver_by_passport(passport_txt.get())
    if (driver == None):
        return False
    return driver[0]

def clicked():
    driver_id = check_passport()
    if (not driver_id):
        error_lbl.configure(text = "Driver with passport already exists or passport info is incorrect: {}".format(passport_txt.get()))
        return

    if (not check_mark()):
        error_lbl.configure(text = "Mark is incorrect: {}".format(mark_txt.get()))
        return

    if (not check_number()):
        error_lbl.configure(text = "Number is incorrect: {}".format(number_txt.get()))
        return
    
    # if (not check_registration_date()):
    #     error_lbl.configure(text = "Registration is incorrect: {}".format(registration_date_txt.get()))
    #     return

    # error_lbl.configure(text = "")
    # database.insert_car(mark_txt.get(), number_txt.get(), registration_date_txt.get(), driver_id)
        