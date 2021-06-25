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
from Andrew import *
import csv
import tkinter.filedialog as tkfd
import os

running = False

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

        self.LJ = u6.U6()

        self.maxlim1 = 40
        self.maxlim2 = 40

        self.xmax2 = 1
        self.xmax1 = self.xmax2 - 60

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky='news')

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=1, row=0, sticky='news')

        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2, text='Temperatures')

        self.frame2b = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2b, text='Radical Density')

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(column=2, row=0, sticky='news')

        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(211, ylim=(0,self.maxlim1))
        self.plot2 = self.fig1.add_subplot(212, ylim=(0, self.maxlim1))


        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.frame2)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        print('working')

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame2)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.RadicalDensityLabel = ttk.Label(self.frame1, text='Radical Density')
        self.RadicalDensityLabel.grid(row=0,columnspan=2)

        self.RadicalDensity = ttk.Label(self.frame1, text='0.00')
        self.RadicalDensity.grid(row=1, columnspan=2)

        self.StartScan = ttk.Button(self.frame3, text='Start Scan', command=self.startscan)
        self.StartScan.grid(row=0, columnspan=2, sticky='ew')

        self.StopScan = ttk.Button(self.frame3, text='Stop Scan', command=self.stopscan)
        self.StopScan.grid(row=1, columnspan=2, sticky='ew')

        self.GoldProbeLabel = ttk.Label(self.frame1, text='Gold Probe (deg C):')
        self.GoldProbeLabel.grid(row=2, columnspan=2, sticky='ew')

        self.GoldProbe = ttk.Label(self.frame1, text='0.00')
        self.GoldProbe.grid(row=3, columnspan=2, sticky='ew')

        self.SSProbeLabel = ttk.Label(self.frame1, text='SS Probe (deg C):')
        self.SSProbeLabel.grid(row=4, columnspan=2, sticky='ew')

        self.SSProbe = ttk.Label(self.frame1, text='0.00')
        self.SSProbe.grid(row=5, columnspan=2, sticky='ew')

        self.DifferenceLabel = ttk.Label(self.frame1, text = 'Difference (deg C):')
        self.DifferenceLabel.grid(row=6, columnspan=2, sticky='ew')

        self.Difference = ttk.Label(self.frame1, text = '0.00')
        self.Difference.grid(row=7, columnspan=2, sticky='ew')

        self.ExportData = ttk.Button(self.frame3, text='Export Data', command=self.choosefile)
        self.ExportData.grid()
        self.ExportData.grid_forget()

        self.ResetPlot = ttk.Button(self.frame3, text='Reset Plot', command=self.reset)
        self.ResetPlot.grid()
        self.ResetPlot.grid_forget()



    def onclose(self):
        plt.close('all')
        self.destroy()

    def startscan(self):
        global running
        running = True

    def stopscan(self):
        global running
        running = False
        self.ExportData.grid(row=2, columnspan=2, sticky='ew')
        self.ResetPlot.grid(row=3, columnspan=2, sticky='ew')


    def scanning(self):
        with open('temps.txt','a') as temptxt:
            if running:
                self.list.append(RadicalTemps(self.LJ, 0, 1))
                self.timelist.append(len(self.list))
                self.GoldProbeTemp = round(self.list[-1][0], 3)
                self.SSProbeTemp = round(self.list[-1][1], 3)
                self.DifferenceTemp = round((self.GoldProbeTemp - self.SSProbeTemp), 3)
                self.GoldProbeTempList.append(self.GoldProbeTemp)
                self.SSProbeTempList.append(self.SSProbeTemp)

                self.GoldProbe['text'] = str(self.GoldProbeTemp)
                self.SSProbe['text'] = str(self.SSProbeTemp)
                self.Difference['text'] = str(self.DifferenceTemp)
                self.maxlim1 = max(max(self.list)) + 5

                self.last60 = self.list[-60:]
                self.maxlim2 = max(max(self.last60)) + 5

                self.xmax2 = self.timelist[-1]

                if (self.timelist[-1] - 60) <= 0:
                    self.xmax1 = 0
                else:
                    self.xmax1 = self.xmax2 - 60


                self.plot1.remove()
                self.plot1 = self.fig1.add_subplot(211, ylim=(0,self.maxlim1))
                self.plot1.plot(self.timelist, self.GoldProbeTempList, color='orange')
                self.plot1.plot(self.timelist, self.SSProbeTempList, color='blue')


                self.plot2.remove()
                self.plot2 = self.fig1.add_subplot(212, xlim=(self.xmax1, self.xmax2), ylim=(0, self.maxlim2))
                self.plot2.plot(self.timelist, self.GoldProbeTempList, color='orange')
                self.plot2.plot(self.timelist, self.SSProbeTempList, color='blue')
                self.canvas.draw()


        self.after(1000, self.scanning)

    def exportdata(self):
        self.totallist = []
        self.fields = ['Time', 'Gold Probe Temperature', 'Stainless Steel Probe Temperature']
        for i in range(len(self.list)):
            newentry = [self.timelist[i], self.GoldProbeTempList[i], self.SSProbeTempList[i]]
            self.totallist.append(newentry)
        print(self.totallist)
        with open('TemperatureList.csv', 'a') as templist:
            writer = csv.writer(templist)

            writer.writerow(self.fields)
            writer.writerows(self.totallist)

    def choosefile(self):
        self.totallist = []
        self.fields = ['Time', 'Gold Probe Temperature', 'Stainless Steel Probe Temperature']
        self.file = tkfd.asksaveasfilename(
            parent=self, initialdir='.',
            title='Choose File',
            filetype=[
                ('CSV Files', '.csv'),
                ('Text Files', '.txt')
            ])
        print(os.path.basename(self.file))
        for i in range(len(self.list)):
            newentry = [self.timelist[i], self.GoldProbeTempList[i], self.SSProbeTempList[i]]
            self.totallist.append(newentry)

        with open(self.file, 'w') as savefile:
            filewriter = csv.writer(savefile)

            filewriter.writerow(self.fields)
            filewriter.writerows(self.totallist)

    def reset(self):
        self.list.clear()





if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')
    app.after(1000, app.scanning)
    app.mainloop()
