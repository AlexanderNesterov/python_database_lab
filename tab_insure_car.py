import database
import re
from datetime import datetime
from tkinter import ttk
from tkinter import Label, Entry, Button, W, END

def insure_car(tab):
    global car_info_lbl
    car_info_lbl = Label(tab, text = "Insure information ")  
    car_info_lbl.grid(column = 0, row = 8, sticky = W)

    global selected_mark_lbl
    mark_lbl = Label(tab, text = "Mark: ")
    mark_lbl.grid(column = 0, row = 9, sticky = W)
    selected_mark_lbl = Label(tab, text = "")
    selected_mark_lbl.grid(column = 1, row = 9, sticky = W)

    global selected_number_lbl
    number_lbl = Label(tab, text = "Number: ")
    number_lbl.grid(column = 0, row = 10, sticky = W)
    selected_number_lbl = Label(tab, text = "")
    selected_number_lbl.grid(column = 1, row = 10, sticky = W)

    global insurance_cost_txt
    insurance_cost_lbl = Label(tab, text = "Insurance cost: ")  
    insurance_cost_lbl.grid(column = 0, row = 11, sticky = W)
    insurance_cost_txt = Entry(tab, width = 40)
    insurance_cost_txt.grid(column = 1, row = 11)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 7)

    btn = Button(tab, text = "Submit", command = insure_click)  
    btn.grid(column = 0, row = 12, sticky = W)

    btn1 = Button(tab, text = "Clear", command = clear_info_click)  
    btn1.grid(column = 1, row = 12, sticky = W)

def set_values(car):
    global car_to_insure_id
    car_to_insure_id = car['text']
    info = car['values']
    car_info_lbl.configure(text = "Insure car with id: {}".format(car_to_insure_id))

    clear_fields()

    selected_mark_lbl.configure(text = info[0])
    selected_number_lbl.configure(text = info[1])

def check_insurance_cost():
    insurance_cost = insurance_cost_txt.get()
    if (insurance_cost == None or insurance_cost == ""):
        return False

    try:
        if (int(insurance_cost) < 0):
            return False
    except ValueError:
        return False
    return True

def insure_click():
    try:
        if (car_to_insure_id < 0):
            return
    except NameError:
        error_lbl.configure(text = "To insure a car you have to select car from the table above")
        return

    if (not check_insurance_cost()):
        error_lbl.configure(text = "Insurance cost is incorrect: {}".format(insurance_cost_txt.get()))
        return

    error_lbl.configure(text = "")
    now = datetime.now().date()
    database.insert_insurance_car(now, insurance_cost_txt.get(), car_to_insure_id)

def clear_fields():
    selected_mark_lbl.configure(text = "")
    selected_number_lbl.configure(text = "")
    insurance_cost_txt.delete(0, END)

def clear_info_click():
    error_lbl.configure(text = "")
    car_info_lbl.configure(text = "Insure information")
    clear_fields()