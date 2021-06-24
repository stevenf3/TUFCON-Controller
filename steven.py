import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from labjack import ljm
import matplotlib.animation as animation
from matplotlib import style
from time import sleep
from Andrew import *
import csv

#f = Figure(figsize=(5,5), dpi=100)
#a = f.add_subplot(111)
running = False
GoldProbeTemp = 0.00

class controller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.onclose)


        self.list =[]
        self.timelist = []
        self.GoldProbeTempList = []
        self.SSProbeTempList = []
        s = ttk.Style()
        s.configure('.', font=('Cambria'), fontsize=16)
        s.configure('TButton')
        self.grid_rowconfigure(0,w=1)
        self.grid_columnconfigure(0,w=1)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky='news')

        self.frame2 = ttk.Frame(self)
        self.frame2.grid(column=1, row=0, sticky='nsew')

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(column=2, row=0, sticky='news')

        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(111)


        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.frame2)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        print('working')

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame2)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.RadicalDensityLabel = ttk.Label(self.frame1, text='Radical Density')
        self.RadicalDensityLabel.grid(row=0,columnspan=2)

        self.StartScan = ttk.Button(self.frame3, text='Start Scan', command=self.startscan)
        self.StartScan.grid(row=0, columnspan=2, sticky='ew')

        self.StopScan = ttk.Button(self.frame3, text='Stop Scan', command=self.stopscan)
        self.StopScan.grid(row=1, columnspan=2, sticky='ew')

        self.GoldProbeLabel = ttk.Label(self.frame1, text='Gold Probe (deg C):')
        self.GoldProbeLabel.grid(row=1, columnspan=2, sticky='ew')

        self.GoldProbe = ttk.Label(self.frame1, text='0.00')
        self.GoldProbe.grid(row=2, columnspan=2, sticky='ew')

        self.SSProbeLabel = ttk.Label(self.frame1, text='SS Probe (deg C):')
        self.SSProbeLabel.grid(row=3, columnspan=2, sticky='ew')

        self.SSProbe = ttk.Label(self.frame1, text='0.00')
        self.SSProbe.grid(row=4, columnspan=2, sticky='ew')

        self.ExportData = ttk.Button(self.frame3, text='Export Data')
        self.ExportData.grid()
        self.ExportData.grid_forget()

    def onclose(self):
        plt.close('all')
        self.destroy()

    def startscan(self):
        global running
        running = True
        print('Scan Started')

    def stopscan(self):
        global running
        running = False
        print('Scan Finished')
        print(self.list)
        self.ExportData.grid(row=2, columnspan=2, sticky='ew')


    def scanning(self):
        with open('temps.txt','a') as temptxt:
            if running:
                self.list.append(RadicalTemps(u6.U6(), 0, 1))
                self.timelist.append(len(self.list))
                self.GoldProbeTemp = round(self.list[-1][0], 3)
                self.SSProbeTemp = round(self.list[-1][1], 3)

                self.GoldProbeTempList.append(self.GoldProbeTemp)
                self.SSProbeTempList.append(self.SSProbeTemp)

                print(self.GoldProbeTemp, self.SSProbeTemp)
                print(self.timelist[-1])
                self.GoldProbe['text'] = str(self.GoldProbeTemp)
                self.SSProbe['text'] = str(self.SSProbeTemp)
                L = "{},{}\n".format(self.GoldProbeTemp, self.SSProbeTemp)
                temptxt.write(L)


                self.plot1.plot(self.timelist, self.GoldProbeTempList, color='orange')
                self.plot1.plot(self.timelist, self.SSProbeTempList, color='blue')
                self.canvas.draw()

        self.after(1000, self.scanning)


if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')
    app.after(1000, app.scanning)
    app.mainloop()
