import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

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
        self.frame2.grid(column=1, row=0, sticky='news')

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(column=3, row=0, sticky='news')

        self.fig, self.ax = plt.subplots(figsize=(5,5))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


    def onclose(self):
        plt.close('all')
        self.destroy()


if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')

    app.mainloop()
