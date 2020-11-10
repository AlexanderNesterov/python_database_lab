import database
import re
from datetime import datetime
from tkinter import ttk
from tkinter import Label, Entry, Button, W

def insert_driver(tab):
    insert_lbl = Label(tab, text = "Insert new driver")
    insert_lbl.grid(column = 0, row = 2, sticky = W)

    global first_name_txt
    first_name_lbl = Label(tab, text = "First Name: ")  
    first_name_lbl.grid(column = 0, row = 3, sticky = W)
    first_name_txt = Entry(tab, width = 40)
    first_name_txt.grid(column = 1, row = 3)

    global last_name_txt
    last_name_lbl = Label(tab, text = "Last Name: ")
    last_name_lbl.grid(column = 0, row = 4, sticky = W)
    last_name_txt = Entry(tab, width = 40)
    last_name_txt.grid(column = 1, row = 4)

    global passport_txt 
    passport_lbl = Label(tab, text = "Passport: ")
    passport_lbl.grid(column = 0, row = 5, sticky = W)
    passport_txt = Entry(tab, width = 40)
    passport_txt.grid(column = 1, row = 5)

    global registration_txt
    registration_lbl = Label(tab, text = "Registration: ")
    registration_lbl.grid(column = 0, row = 6, sticky = W)
    registration_txt = Entry(tab, width = 40)
    registration_txt.grid(column = 1, row = 6)

    global birthdate_txt
    birthdate_lbl = Label(tab, text = "Birthdate: ")
    birthdate_lbl.grid(column = 0, row = 7, sticky = W)
    birthdate_txt = Entry(tab, width = 40)
    birthdate_txt.grid(column = 1, row = 7)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 9, sticky = W)

    btn = Button(tab, text = "Submit", command = clicked)  
    btn.grid(column = 0, row = 8, sticky = W)

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
    if (driver != None):
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

def clicked():
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
    database.insert_driver(first_name_txt.get(), last_name_txt.get(), passport_txt.get(), birthdate_txt.get(), registration_txt.get())
        