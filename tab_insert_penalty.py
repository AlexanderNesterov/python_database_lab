import re
import database
from tkinter import ttk
from tkinter import Label, Entry, Button, W

def insert_penalty(tab):
    insert_lbl = Label(tab, text = "Insert new penalty")
    insert_lbl.grid(column = 0, row = 2, sticky = W)

    global description_txt
    description_lbl = Label(tab, text = "Description: ")  
    description_lbl.grid(column = 0, row = 3, sticky = W)
    description_txt = Entry(tab, width = 40)
    description_txt.grid(column = 1, row = 3)

    global cost_txt
    cost_lbl = Label(tab, text = "Cost: ")
    cost_lbl.grid(column = 0, row = 4, sticky = W)
    cost_txt = Entry(tab, width = 40)
    cost_txt.grid(column = 1, row = 4)

    global error_lbl
    error_lbl = Label(tab, fg = "#FF0000")
    error_lbl.grid(column = 0, row = 9, sticky = W)

    btn = Button(tab, text = "Submit", command = clicked)  
    btn.grid(column = 0, row = 8, sticky = W)

def check_description():
    description = description_txt.get()
    if (description == None or description == ""):
        return False
    return True

def check_cost():
    cost = cost_txt.get()
    if (cost == None or cost == ""):
        return False

    regex = re.compile("[1-9][0-9]{2,6}")
    match = re.search(regex, cost)
    if (match != None and match.group() == cost):
        return True
    else:
        return False

def clicked():
    if (not check_description()):
        error_lbl.configure(text = "Description is incorrect: {}".format(description_txt.get()))
        return

    if (not check_cost()):
        error_lbl.configure(text = "Cost is incorrect: {}".format(cost_txt.get()))
        return

    error_lbl.configure(text = "")
    database.insert_penalty(description_txt.get(), cost_txt.get())
        