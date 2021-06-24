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
style.use('ggplot')

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot()
list = []
running = False
GoldProbeTemp = 0.00
def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)





class controller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol('WM_DELETE_WINDOW', self.onclose)

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

        self.y = [i**3 for i in range(101)]
        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(111)

        self.plot1.plot(self.y)

        self.canvas = FigureCanvasTkAgg(f, master=self.frame2)
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

        self.GoldProbeLabel = ttk.Label(self.frame1, text='Gold Probe:')
        self.GoldProbeLabel.grid(row=1, columnspan=2, sticky='ew')

        self.GoldProbe = ttk.Label(self.frame1, text='0.00')
        self.GoldProbe.grid(row=2, columnspan=2, sticky='ew')

        self.SSProbeLabel = ttk.Label(self.frame1, text='SS Probe:')
        self.SSProbeLabel.grid(row=3, columnspan=2, sticky='ew')

        self.SSProbe = ttk.Label(self.frame1, text='0.00')
        self.SSProbe.grid(row=4, columnspan=2, sticky='ew')

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
        print(list)

    def update(self):
        global GP
        GP = str(GoldProbeTemp)
        SP = str(SSProbeTemp)
        self.GoldProbe['text'] = GP
        self.SSProbe['text'] = SP


def scanning():
    tempsfile = open("temps.txt","w")
    global GoldProbeTemp
    global SSProbeTemp
    if running:
        list.append(RadicalTemps(u6.U6(), 0, 1))
        GoldProbeTemp = round(list[-1][0], 3)
        SSProbeTemp = round(list[-1][1], 3)
        print(GoldProbeTemp, SSProbeTemp)
        app.GoldProbe['text'] = str(GoldProbeTemp)
        app.SSProbe['text'] = str(SSProbeTemp)


    app.after(1000, scanning)





if __name__ == '__main__':
    app = controller()
    ani = animation.FuncAnimation(f,animate, interval=1000)
    app.wm_title('TUFCON Controller')
    app.after(1000, scanning)
    app.mainloop()
