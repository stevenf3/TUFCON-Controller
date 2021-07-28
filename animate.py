import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.animation as animation
from matplotlib import style
from time import sleep
import time
import pandas as pd

running = False
df = pd.read_csv('070921-60mTorr.csv')
GP = df['Gold Probe Temperature']
SS = df['Stainless Steel Probe Temperature']
plt.ion()
class animation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.onclose)

        self.running = False
        self.i=-1
        self.j = -1
        self.TempData = np.zeros((10,2))

        self.s = ttk.Style()
        self.s.configure('.', font=('Cambria'), fontsize=16)
        self.s.configure('TButton')
        self.grid_rowconfigure(0,w=1)
        self.grid_columnconfigure(0,w=2)
        self.grid_columnconfigure(1, w=0)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky='news')

        self.frame2 = ttk.Frame(self)
        self.frame2.grid(column=1, row=0, sticky='news')

        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(211)
        self.line1, = self.plot1.plot([],[],'gold')
        self.line2, = self.plot1.plot([],[],'blue')

        self.plot2 = self.fig1.add_subplot(212)
        self.line3, = self.plot2.plot([],[],'gold')

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.frame1)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas.draw()

        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.toolbar1.update()

        self.StartScan = ttk.Button(self.frame2, text='Start Scan', command=self.startscan)
        self.StartScan.grid(row=0, sticky='ew')

        self.StopScan = ttk.Button(self.frame2, text='Stop Scan', command=self.stopscan)
        self.StopScan.grid()
        self.StopScan.grid_forget()


    def onclose(self):
        plt.close('all')
        self.destroy()

    def startscan(self):
        print('started scan')
        self.running = True
        self.StartScan.grid_forget()
        self.StopScan.grid(row=0, columnspan=2,sticky='ew')

    def stopscan(self):
        print('stopped scan')
        self.running = False
        self.StopScan.grid_forget()
        self.StartScan.grid(row=0, columnspan=2,sticky='ew')

    def scanning(self):
        with open('tempwriter.csv', 'a') as file:
            if self.running:
                tick = time.time()
                self.i += 1
                self.j += 1
                if self.j == 10:
                    self.j = 0
                    np.savetxt(file, self.TempData)
                    self.TempData = np.zeros((10,2))
                self.TempData[self.j, 0] = GP[self.i]
                self.TempData[self.j, 1] = SS[self.i]

                if self.i <= 60:
                    minutemin = 0
                    minutemax = self.i
                else:
                    minutemin = self.i-60
                    minutemax = self.i

                self.line1.set_xdata(np.append(self.line1.get_xdata(), self.i))
                self.line1.set_ydata(np.append(self.line1.get_ydata(), GP[self.i]))
                self.line2.set_xdata(np.append(self.line2.get_xdata(), self.i))
                self.line2.set_ydata(np.append(self.line2.get_ydata(), SS[self.i]))
                self.plot1.relim()
                self.plot1.autoscale_view()

                self.line3.set_xdata(np.append(self.line1.get_xdata(), self.i))
                self.line3.set_ydata(np.append(self.line2.get_ydata(), GP[self.i]))
                self.plot2.relim()
                self.plot2.set_xlim(minutemin, minutemax)
                self.plot2.autoscale_view()
                self.canvas.draw()
                tock = time.time()
                delay = int(1000 * (tock - tick))
                print(delay)

            try:
                self.after(1000 - delay, self.scanning)
            except UnboundLocalError:
                self.after(1000, self.scanning)

if __name__ == '__main__':
    app = animation()
    app.wm_title('Animation Test')
    app.after(1000, app.scanning)
    app.mainloop()
