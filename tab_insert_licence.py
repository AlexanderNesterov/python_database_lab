import database
import re
from datetime import datetime
from datetime import timedelta
from tkinter import ttk
from tkinter import Label, Entry, Button, END, W

def insert_licence(tab):
    global licence_info_lbl
    licence_info_lbl = Label(tab, text = "Licence information: ")  
    licence_info_lbl.grid(column = 0, row = 2, sticky = W)

    global licence_number_txt
    licence_number_lbl = Label(tab, text = "Licence number: ")  
    licence_number_lbl.grid(column = 0, row = 3, sticky = W)
    licence_number_txt = Entry(tab, width = 40)
    licence_number_txt.grid(column = 1, row = 3, sticky = W)

    global selected_licence_start_date_lbl
    licence_start_date_lbl = Label(tab, text = "Licence start date: ")  
    licence_start_date_lbl.grid(column = 0, row = 4, sticky = W)
    selected_licence_start_date_lbl = Label(tab, width = 10)
    selected_licence_start_date_lbl.grid(column = 1, row = 4, sticky = W)

    global selected_licence_end_date_lbl
    licence_end_date_lbl = Label(tab, text = "Licence end date: ")  
    licence_end_date_lbl.grid(column = 0, row = 5, sticky = W)
    selected_licence_end_date_lbl = Label(tab, width = 10)
    selected_licence_end_date_lbl.grid(column = 1, row = 5, sticky = W)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 7)

    btn = Button(tab, text = "Submit", command = clicked)  
    btn.grid(column = 0, row = 6, sticky = W)

    btn1 = Button(tab, text = "Clear", command = clear_info_click)  
    btn1.grid(column = 1, row = 6, sticky = W)

def set_values(driver):
    global driver_to_add_licence_id
    driver_to_add_licence_id = driver['text']
    licence_info_lbl.configure(text = "Add licence to driver with id: {}".format(driver_to_add_licence_id))

    clear_fields()

    start_date = datetime.now().date()
    selected_licence_start_date_lbl.configure(text = start_date)
    end_date = start_date + timedelta(days = 3650)
    selected_licence_end_date_lbl.configure(text = end_date)

def check_licence_number():
    licence_number = licence_number_txt.get()
    if (licence_number == None or licence_number == ""):
        return False

    regex = re.compile("[0-9]{10}")
    match = re.search(regex, licence_number)
    if (match == None or match.group() != licence_number):
        return False

    existed_licence = database.get_driver_by_licence(licence_number)

    if (existed_licence != None):
        return False
    return True

def clicked():
    try:
        if (driver_to_add_licence_id < 0):
            return
    except NameError:
        error_lbl.configure(text = "To add a licence to a driver you have to select driver from the table above")
        return
    if (not check_licence_number()):
        error_lbl.configure(text = "Licence number is incorrect or exist: {}".format(licence_number_txt.get()))
        return

    error_lbl.configure(text = "")
    database.insert_licence(licence_number_txt.get(), selected_licence_start_date_lbl['text'], selected_licence_end_date_lbl['text'], driver_to_add_licence_id)
    clear_fields()

def clear_fields():
    selected_licence_start_date_lbl.configure(text = "")
    selected_licence_end_date_lbl.configure(text = "")
    licence_number_txt.delete(0, END)

def clear_info_click():
    driver_to_add_licence_id = None
    error_lbl.configure(text = "")
    licence_info_lbl.configure(text = "Insure information")
    clear_fields()
        