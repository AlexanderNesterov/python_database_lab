import database
import re
from datetime import datetime
from tkinter import ttk
from tkinter import Label, Entry, Button

def insert_insurance(tab):
    insurance_info_lbl = Label(tab, text = "Insurance information: ")  
    insurance_info_lbl.grid(column = 0, row = 0)

    global insurance_date_txt
    insurance_date_lbl = Label(tab, text = "Insurance Date: ")  
    insurance_date_lbl.grid(column = 0, row = 1)
    insurance_date_txt = Entry(tab, width = 10)
    insurance_date_txt.grid(column = 1, row = 1)

    global insurance_cost_txt
    insurance_cost_lbl = Label(tab, text = "Insurance Cost: ")  
    insurance_cost_lbl.grid(column = 0, row = 2)
    insurance_cost_txt = Entry(tab, width = 10)
    insurance_cost_txt.grid(column = 1, row = 2)

    driver_info_lbl = Label(tab, text = "Car information: ")  
    driver_info_lbl.grid(column = 2, row = 0)

    global car_number_txt 
    car_number_lbl = Label(tab, text = "Car Number: ")
    car_number_lbl.grid(column = 2, row = 3)
    car_number_txt = Entry(tab, width = 10)
    car_number_txt.grid(column = 3, row = 3)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 6)

    btn = Button(tab, text = "Submit", command = clicked)  
    btn.grid(column = 0, row = 5)

def check_insurance_date():
    insurance_date = insurance_date_txt.get()
    if (insurance_date == None or insurance_date == ""):
        return False

    regex = re.compile("(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](19|20)\d\d")
    match = re.search(regex, insurance_date)
    if (match == None or match.group() != insurance_date):
        return False

    now = datetime.now().date()
    check = datetime.strptime(insurance_date, "%d-%m-%Y").date()

    if (check >= now):
        return False
    return True

def check_insurance_cost():
    insurance_cost = insurance_cost_txt.get()
    if (insurance_cost == None or insurance_cost == ""):
        return False

    regex = re.compile("[0-1]{4..}")
    match = re.search(regex, insurance_cost)
    if (match == None or match.group() != insurance_cost):
        return False
    return True

def check_number():
    car_number = car_number_txt.get()
    if (car_number == None or car_number == ""):
        return False

    regex = re.compile("[a-z]{2}[0-9]{3}[a-z]")
    match = re.search(regex, car_number)
    if (match == None or match.group() != car_number):
        return False

    car = database.get_car_by_number(car_number)
    if (car != None):
        return False
    return car[0]

def clicked():
    if (not check_insurance_date()):
        error_lbl.configure(text = "Insurance date is incorrect: {}".format(insurance_date_txt.get()))
        return

    if (not check_insurance_cost()):
        error_lbl.configure(text = "Insurance cost is incorrect: {}".format(insurance_cost_txt.get()))
        return
    
    car_id = check_number()
    if (not car_id):
        error_lbl.configure(text = "Car numbber is incorrect: {}".format(car_number_txt.get()))
        return

    error_lbl.configure(text = "")
    database.insert_insurance(insurance_date_txt.get(), insurance_cost_txt.get(), car_id)
        