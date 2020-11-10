from tkinter import Tk, ttk, Menu
import database
import tab_with_drivers
import tab_with_penalties
import tab_get_driver_information
import tab_insert_car
import tab_car_penalties
import tab_with_cars

def start():
    global window
    window = Tk()
    window.geometry('1500x800')
    window.title("ПДД")

    tab_control = ttk.Notebook(window)  

    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab5 = ttk.Frame(tab_control)
    tab6 = ttk.Frame(tab_control)
    
    tab_control.add(tab1, text = 'Drivers')  
    tab_control.add(tab2, text = 'Penalties')
    tab_control.add(tab4, text = 'Get penalties with info')
    tab_control.add(tab5, text = 'Get driver\'s inforamtion')
    tab_control.add(tab6, text = 'Cars')
    tab_control.pack(expand = 1, fill = 'both')

    tab_with_drivers.get_table_with_drivers(tab1)
    tab_with_penalties.get_table_with_penalties(tab2)
    tab_car_penalties.get_penalties_with_info(tab4)
    tab_get_driver_information.get_driver_information(tab5)
    tab_with_cars.get_table_with_cars(tab6)

    window.mainloop()
    