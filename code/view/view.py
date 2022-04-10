

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


import code.view.histogram
import code.view.line_graph_full_time
import code.view.table_of_instruments

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TRACE: View: __init__")

        # placeholder for controller
        self.controller = None


        ######################
        # create widgets
        ######################

        self.frame1 = tk.Frame(self, padx=5, pady=5)
        self.frame1.pack(side=tk.LEFT)
        self.checkbutton_fee_state = tk.IntVar()
        self.checkbutton = tk.Checkbutton(self.frame1, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.pack()

        self.label = tk.Label(self.frame1, text='Years')
        self.label.pack()

        #Spinbox
        self.spin = tk.Spinbox(self.frame1, from_=0, to=100, width=5,command=self.update_limit)
        self.spin.pack()

        #Slide
        self.scale = tk.Scale(self.frame1, from_=0, to=100, orient='horizontal', command=self.update_amount)
        self.scale.pack()

        # Histogram
        code.view.histogram.__init__(self)

        # Line Graph
        code.view.line_graph_full_time.__init__(self)
       
        #Table of Stock Markets
        code.view.table_of_instruments.__init__(self)


    ###############
    # Commands
    ###############

    def set_controller(self, controller):
        print("TRACE: View: set_controller")
        self.controller = controller

    def update_fee_status(self):
        print("TRACE: View: update_fee_status")
        print("View, fee_status:", self.checkbutton_fee_state.get())
        self.controller.update_fee_status(self.checkbutton_fee_state.get())
        tk.messagebox.showinfo('Error', 'Not fully implemented')
    
    def update_limit(self):
        print("TRACE: View: update_limit")
        tk.messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def update_amount(self, value):
        print("TRACE: View: update_amount")
        tk.messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def draw_histogram(self, data):
        print("TRACE: View: draw_histogram")
        code.view.histogram.draw_histogram(self,data)

    def draw_line_graph(self, values, time_span):
        print("TRACE: View: draw_line_graph")
        code.view.line_graph_full_time.draw_line_graph(self, values, time_span)

    def set_market_table(self, markets):
        print("TRACE: View: set_market_table")
        code.view.table_of_instruments.set_market_table(self, markets)
        
    def update_table_item_focused(self, _ ):
        print("TRACE: View: table_item_focused")
        code.view.table_of_instruments.update_item_color(self)
        table_focus_item = code.view.table_of_instruments.get_table_item_focused(self)
        self.controller.update_instrument_selected(table_focus_item)