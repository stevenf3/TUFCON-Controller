import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from labjack import ljm

class controller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', self.onclose)

        s = ttk.Style()
        s.configure('.', font=('Cambria'), fontsize=16)
        s.configure('TButton')

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky='news')

        self.frame2 = ttk.Frame(self)
        self.frame2.grid(column=4, row=0, sticky='ew')

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(column=6, row=0, sticky='news')

        self.y = [i**3 for i in range(101)]
        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(111)

        self.plot1.plot(self.y)

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.frame2)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        print('working')

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame2)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.RadicalDensityLabel = ttk.Label(self.frame1, text='Radical Density')
        self.RadicalDensityLabel.grid(row=0,columnspan=2,sticky='ew')

        self.PlotButton = ttk.Button(self.frame3, text='Plot')
        self.PlotButton.grid(row=0, columnspan=2, sticky='ew')


    def onclose(self):
        plt.close('all')
        self.destroy()


if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')

    app.mainloop()
