import database
import re
from datetime import datetime
from tkinter import ttk
from tkinter import Label, Entry, Button, W, END

def update_driver(tab):
    # global updating_driver_id
    # updating_driver_id = None

    global update_lbl
    update_lbl = Label(tab, text = "Update driver")
    update_lbl.grid(column = 3, row = 2, sticky = W)

    global first_name_txt
    first_name_lbl = Label(tab, text = "First Name: ")  
    first_name_lbl.grid(column = 3, row = 3, sticky = W)
    first_name_txt = Entry(tab, width = 40)
    first_name_txt.grid(column = 4, row = 3)

    global last_name_txt
    last_name_lbl = Label(tab, text = "Last Name: ")
    last_name_lbl.grid(column = 3, row = 4, sticky = W)
    last_name_txt = Entry(tab, width = 40)
    last_name_txt.grid(column = 4, row = 4)

    global passport_txt 
    passport_lbl = Label(tab, text = "Passport: ")
    passport_lbl.grid(column = 3, row = 5, sticky = W)
    passport_txt = Entry(tab, width = 40)
    passport_txt.grid(column = 4, row = 5)

    global registration_txt
    registration_lbl = Label(tab, text = "Registration: ")
    registration_lbl.grid(column = 3, row = 6, sticky = W)
    registration_txt = Entry(tab, width = 40)
    registration_txt.grid(column = 4, row = 6)

    global birthdate_txt
    birthdate_lbl = Label(tab, text = "Birthdate: ")
    birthdate_lbl.grid(column = 3, row = 7, sticky = W)
    birthdate_txt = Entry(tab, width = 40)
    birthdate_txt.grid(column = 4, row = 7)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 3, row = 9, sticky = W)

    btn = Button(tab, text = "Submit", command = update_click)  
    btn.grid(column = 3, row = 8, sticky = W)

    clear_btn = Button(tab, text = "Clear", command = clear_info_click)  
    clear_btn.grid(column = 4, row = 8, sticky = W)

def set_values(driver):
    global updating_driver_id
    updating_driver_id = driver['text']
    info = driver['values']
    update_lbl.configure(text = "Update driver with id: {}".format(updating_driver_id))

    clear_fields()

    first_name_txt.insert(0, info[0])
    last_name_txt.insert(0, info[1])
    passport_txt.insert(0, info[2])

    date = datetime.strptime(info[3], "%Y-%m-%d")
    birthdate_txt.insert(0, datetime.strftime(date, "%d-%m-%Y"))

    registration_txt.insert(0, info[4])

def clear_fields():
    first_name_txt.delete(0, END)
    last_name_txt.delete(0, END)
    passport_txt.delete(0, END)
    birthdate_txt.delete(0, END)
    registration_txt.delete(0, END)

def check_first_name():
    first_name = first_name_txt.get()
    if (first_name == None or first_name == ""):
        return False

    regex = re.compile("[A-Z][a-z]+")
    match = re.search(regex, first_name)
    if (match != None and match.group() == first_name):
        return True
    else:
        return False

def check_last_name():
    last_name = last_name_txt.get()
    if (last_name == None or last_name == ""):
        return False

    regex = re.compile("[A-Z][a-z]+")
    match = re.search(regex, last_name)
    if (match != None and match.group() == last_name):
        return True
    else:
        return False

def check_passport():
    passport = passport_txt.get()
    if (passport == None or passport == ""):
        return False

    regex = re.compile("[0-9]{4} [0-9]{6}")
    match = re.search(regex, passport)
    if (match == None or match.group() != passport):
        return False

    driver = database.get_driver_by_passport(passport_txt.get())
    if (driver != None and driver[0] != updating_driver_id):
        return False
    return True

def check_birthdate():
    birthdate = birthdate_txt.get()
    if (birthdate == None or birthdate == ""):
        return False

    regex = re.compile("(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](19|20)\d\d")
    match = re.search(regex, birthdate)
    if (match == None or match.group() != birthdate):
        return False

    now = datetime.now().date()
    check = datetime.strptime(birthdate, "%d-%m-%Y").date()

    if (check >= now):
        return False
    return True

def check_registration():
    registration = registration_txt.get()
    if (registration == None or registration == ""):
        return False
    return True

def update_click():
    try:
        if (updating_driver_id < 0):
            return
    except NameError:
        error_lbl.configure(text = "To update a driver you have to select driver from the table above")
        return

    if (not check_first_name()):
        error_lbl.configure(text = "First name is empty or incorrect: {}".format(first_name_txt.get()))
        return

    if (not check_last_name()):
        error_lbl.configure(text = "Last name is empty or incorrect: {}".format(last_name_txt.get()))
        return

    if (not check_passport()):
        error_lbl.configure(text = "Driver with passport already exists or passport info is incorrect: {}".format(passport_txt.get()))
        return

    if (not check_registration()):
        error_lbl.configure(text = "Registration is incorrect: {}".format(registration_txt.get()))
        return

    if (not check_birthdate()):
        error_lbl.configure(text = "Birthdate is incorrect: {}".format(birthdate_txt.get()))
        return

    error_lbl.configure(text = "")
    database.update_driver(updating_driver_id, first_name_txt.get(), last_name_txt.get(), passport_txt.get(), registration_txt.get(), birthdate_txt.get())
        
def clear_info_click():
    error_lbl.configure(text = "")
    update_lbl.configure(text = "Update driver")
    clear_fields()