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
import math
from Gauges import *
import matplotlib.colors
from tkintercolorlist import *
import random
import time
from conbarconversion import *
from colour import Color
from tkinter.colorchooser import askcolor

running = False
rgbon = False
randon = False
WD = 7.18 * (10**-19) ##J/molecule, dissociation energy
L = 6.35 * (10**-3) ##m length of exposed probe
D = 0.508 * (10**-3) ##m (diameter of probe)

A = np.pi * (D/2)**2
SA = 2*np.pi * D/2 * (L + D/2)

GammaGold = 0.115
GammaSS = 0.100

color = 'empty'

class controller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.onclose)
        self.plasmapower = 'None Logged'
        self.flowrate = 'None Logged'

        self.time = -1
        self.j = -1
        self.coloriter = -1

        self.tempfileheader = ['Time','Gold Probe Temperature','Stainless Steel Probe Temperature','Radical Density','Convectron Pressure','BaratronPressure','Ion Gauge Pressure','Plasma Power','Flow Rate']

        self.temporaryfile = 'temporary.csv'

        self.s = ttk.Style()
        self.s.configure('.', font=('Cambria'), fontsize=16)
        self.s.configure('TButton')
        self.grid_rowconfigure(0,w=1)
        self.grid_columnconfigure(1,w=1)
        self.matplotcolorlist = []
        for name in matplotlib.colors.cnames.items():
            self.matplotcolorlist.append(name[0])

        self.tkintercolorlist = tkintercolorlist()
        self.rgbvalue = 0
        self.randvalue = 0
        self.DataTable = np.zeros((10, 9))
        self.StoredAvg = np.zeros((1,2))
        self.alternator = 0

        self.red = Color('red')
        self.colorcycle = list(self.red.range_to(Color('blue'),288))

        for color in reversed(self.colorcycle):
            self.colorcycle.append(color)
        excludedcolorindex = []
        for i in range(len(self.colorcycle)):
            if len(str(self.colorcycle[i])) != 7:
                excludedcolorindex.append(i)

        for excolor in reversed(excludedcolorindex):
            self.colorcycle.pop(excolor)


        self.LJ = u6.U6()

        self.maxlim1 = 40
        self.maxlim2 = 40
        self.maxlim3 = 2* 10**15
        self.maxlim4 = 2 * 10 **15
        self.pressureylim1 = 850
        self.pressureylim2 = 850

        self.maxconpressure = 0.01
        self.radmax = 1e19
        self.xmax2 = 1
        self.xmax1 = 0
        self.xmax3 = 0
        self.xmax4 = 1

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky='news')

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=1, row=0, sticky='news')

        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2, text='Temperatures')

        self.frame2b = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2b, text='Radical Density')

        self.frame2c = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2c, text='Pressure')

        self.frame2s = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2s, text='Settings')

        self.frame3 = ttk.Frame(self)
        self.frame3.grid(column=2, row=0, sticky='news')

        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(211, ylim=(0,self.maxlim1))
        self.plot1.set_xlabel('Time (s)')
        self.plot1.set_ylabel('Temperature (deg C)')
        self.goldline, = self.plot1.plot([],[],'orange')
        self.ssline, = self.plot1.plot([],[],'blue')

        self.plot2 = self.fig1.add_subplot(212, ylim=(0, self.maxlim1))
        self.plot2.set_xlabel('Time (s)')
        self.plot2.set_ylabel('Temperature (deg C)')
        self.goldline60, = self.plot2.plot([],[],'orange')
        self.ssline60, = self.plot2.plot([],[],'blue')

        self.fig2 = Figure(figsize=(5,5), dpi=100)
        self.plot3 = self.fig2.add_subplot(211, ylim=(0,self.maxlim3))
        self.plot3.set_xlabel('Time (s)')
        self.plot3.set_ylabel('Radical Density')
        self.radline, = self.plot3.plot([],[],'green')

        self.plot4 = self.fig2.add_subplot(212, ylim=(0,self.maxlim4))
        self.plot4.set_xlabel('Time (s)')
        self.plot4.set_ylabel('Radical Density')
        self.radline60, = self.plot4.plot([],[],'green')

        self.fig3 = Figure(figsize=(5,5), dpi=100)
        self.plot5 = self.fig3.add_subplot(211, ylim=(0,self.pressureylim1))
        self.plot5.set_xlabel('Time (s)')
        self.plot5.set_ylabel('Pressure (Torr)')
        self.pressureline, = self.plot5.plot([],[],'purple')

        self.plot6 = self.fig3.add_subplot(212, ylim=(0,self.pressureylim2))
        self.plot6.set_xlabel('Time (s)')
        self.plot6.set_ylabel('Pressure (Torr)')
        self.pressureline60, = self.plot6.plot([],[],'purple')

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.frame2)
        self.canvas.draw()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame2b)
        self.canvas2.draw()

        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.frame2c)
        self.canvas3.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas2.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas3.get_tk_widget().pack(side='top',fill='both',expand=1)

        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.frame2)
        self.toolbar1.update()
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame2b)
        self.toolbar2.update()
        self.toolbar3 = NavigationToolbar2Tk(self.canvas3, self.frame2c)
        self.toolbar3.update()

        self.RadicalDensityLabel = ttk.Label(self.frame1, text='Radical Density (n/m3)')
        self.RadicalDensityLabel.grid(row=0,column=0, columnspan=2, sticky='ew')

        self.RadicalDensity = ttk.Label(self.frame1, text='0.00')
        self.RadicalDensity.grid(row=0,column=1, sticky='ew')

        self.StartScan = ttk.Button(self.frame3, text='Start Scan', command=self.startscan)
        self.StartScan.grid(row=0,column=0,columnspan=2, sticky='ew')

        self.StopScan = ttk.Button(self.frame3, text='Stop Scan', command=self.stopscan)
        self.StopScan.grid(row=1, sticky='ew')
        self.StopScan.grid_forget()

        self.GoldProbeLabel = ttk.Label(self.frame1, text='Gold Probe (deg C):')
        self.GoldProbeLabel.grid(row=1, sticky='ew')

        self.GoldProbe = ttk.Label(self.frame1, text='0.00')
        self.GoldProbe.grid(row=1, column=1,sticky='ew')

        self.SSProbeLabel = ttk.Label(self.frame1, text='SS Probe (deg C):')
        self.SSProbeLabel.grid(row=2, sticky='ew')

        self.SSProbe = ttk.Label(self.frame1, text='0.00')
        self.SSProbe.grid(row=2, column=1,sticky='ew')

        self.DifferenceLabel = ttk.Label(self.frame1, text = 'Difference (deg C):')
        self.DifferenceLabel.grid(row=3, sticky='ew')

        self.Difference = ttk.Label(self.frame1, text = '0.00')
        self.Difference.grid(row=3,column=1, sticky='ew')

        self.ExportData = ttk.Button(self.frame3, text='Export Data', command=self.choosefile, state=tk.DISABLED)
        self.ExportData.grid(row=11,column=0,columnspan=2,sticky='ew')
        self.ExportData.grid_forget()

        self.ResetPlot = ttk.Button(self.frame3, text='Reset Plot', command=self.resetconfirm, state=tk.DISABLED)
        self.ResetPlot.grid(row=15,column=0,columnspan=2,sticky='ew')
        self.ResetPlot.grid_forget()

        self.DarkModeButton = ttk.Button(self.frame2s, text='Dark Mode', command=self.darkmode)
        self.DarkModeButton.grid(row=0,column=0, columnspan=1, sticky='ew')

        self.RGBButton = ttk.Button(self.frame2s, text='RGB Mode', command=self.startrgb)
        self.RGBButton.grid(row=0, column=2, columnspan=1,sticky='ew')

        self.RandButton = ttk.Button(self.frame2s, text='Random Mode', command=self.startrand)
        self.RandButton.grid(row=0, column=1, columnspan=1,sticky='ew')

        self.ConvectronPressureLabel = ttk.Label(self.frame1, text='Convectron Pressure (Torr):')
        self.ConvectronPressureLabel.grid(row=4, column=0,sticky='ew')

        self.ConvectronPressure = ttk.Label(self.frame1, text='0.00')
        self.ConvectronPressure.grid(row=4,column=1,sticky='ew')

        self.BaratronPressureLabel = ttk.Label(self.frame1, text='Baratron Pressure (Torr):')
        self.BaratronPressureLabel.grid(row=5,sticky='ew')

        self.BaratronPressure = ttk.Label(self.frame1, text='0.00')
        self.BaratronPressure.grid(row=5,column=1,sticky='ew')

        self.IonGaugePressureLabel = ttk.Label(self.frame1, text='Ion Gauge Pressure (Torr):')
        self.IonGaugePressureLabel.grid(row=6,sticky='ew')

        self.IonGaugePressure = ttk.Label(self.frame1, text='0.00')
        self.IonGaugePressure.grid(row=6,column=1,columnspan=2,sticky='ew')

        self.PlasmaPowerLabel = ttk.Label(self.frame1, text='Plasma Power (W)')
        self.PlasmaPowerLabel.grid(row=7,sticky='ew')

        self.PlasmaPower = ttk.Label(self.frame1, text='0.00')
        self.PlasmaPower.grid(row=7,column=1,sticky='ew')

        self.FlowRateLabel = ttk.Label(self.frame1, text='Flow Rate (sccm)')
        self.FlowRateLabel.grid(row=8,sticky='ew')

        self.FlowRate = ttk.Label(self.frame1, text='0.00')
        self.FlowRate.grid(row=8,column=1,sticky='ew')

        self.PowerEntry = ttk.Entry(self.frame3)
        self.PowerEntry.grid(row=6,column=0, columnspan=2,sticky='ew')

        self.PowerEntryButton = ttk.Button(self.frame3, text='Log Plasma Power (W)', command=self.logpower)
        self.PowerEntryButton.grid(row=7,column=0,columnspan=2,sticky='ew')

        self.FlowRateEntry = ttk.Entry(self.frame3)
        self.FlowRateEntry.grid(row=8,column=0, columnspan=2,sticky='ew')

        self.FlowRateEntryButton = ttk.Button(self.frame3, text='Log Flow Rate (sccm)', command=self.logflow)
        self.FlowRateEntryButton.grid(row=9,column=0, columnspan=2,sticky='ew')

        self.selectedBGcolor = tk.StringVar()
        self.selectedTextcolor = tk.StringVar()
        self.selectedFigcolor = tk.StringVar()

        self.BGColor = ttk.Label(self.frame2s, text='Background Color:')
        self.BGColor.grid(row=1, column=0,sticky='ew')

        self.BGColorDropdown = ttk.Combobox(self.frame2s, textvariable=self.selectedBGcolor, values=self.tkintercolorlist)
        self.BGColorDropdown.grid(row=1, column=1, sticky='ew')

        self.ChangeBGButton = ttk.Button(self.frame2s, text='Change',command=self.changebgcolor)
        self.ChangeBGButton.grid(row=1, column=2)

        self.TextColor = ttk.Label(self.frame2s, text='Text Color:')
        self.TextColor.grid(row=2, column=0,sticky='ew')

        self.TextColorDropdown = ttk.Combobox(self.frame2s, textvariable=self.selectedTextcolor, values=self.tkintercolorlist)
        self.TextColorDropdown.grid(row=2, column=1, sticky='ew')

        self.ChangeTextButton = ttk.Button(self.frame2s, text='Change',command=self.changetextcolor)
        self.ChangeTextButton.grid(row=2, column=2)

        self.FigureColor = ttk.Label(self.frame2s, text='Figure Background Color:')
        self.FigureColor.grid(row=3, column=0,sticky='ew')

        self.ChangeFigureColorButton = ttk.Button(self.frame2s, text='Change',command=self.changefigurecolor)
        self.ChangeFigureColorButton.grid(row=3, column=2)

        self.MatplotColorDropdown = ttk.Combobox(self.frame2s, textvariable=self.selectedFigcolor, values=self.matplotcolorlist)
        self.MatplotColorDropdown.grid(row=3, column=1)

        self.ResetConfirm = ttk.Button(self.frame3, text='Confirm', command=self.reset)
        self.ResetConfirm.grid(row=15, column=0, columnspan=1)
        self.ResetConfirm.grid_forget()

        self.ResetCancel = ttk.Button(self.frame3, text='Cancel', command=self.resetcancel)
        self.ResetConfirm.grid(row=15, column=1, columnspan=1)
        self.ResetConfirm.grid_forget()

        self.BGColorChooser = ttk.Button(self.frame2s, text='Color Chooser', command=self.bgcolorchooser)
        self.BGColorChooser.grid(row=1, column=3)

        self.FigureColorChooser = ttk.Button(self.frame2s, text='Color Chooser', command=self.figurecolorchooser)
        self.FigureColorChooser.grid(row=3, column=3)

        self.TextColorChooser = ttk.Button(self.frame2s, text='Color Chooser', command=self.textcolorchooser)
        self.TextColorChooser.grid(row=2, column=3)

        self.SteadyStateIndicatorLabel = ttk.Label(self.frame1, text='Steady State Detector:')
        self.SteadyStateIndicatorLabel.grid(row=9, column=0, columnspan=2, sticky='ew')

        self.SteadyStateIndicator = ttk.Label(self.frame1, text='', background='red')
        self.SteadyStateIndicator.grid(row=9, column=1, columnspan=1, sticky='ew')

    def onclose(self):
        plt.close('all')
        self.destroy()

    def startscan(self):
        print('button pressed')
        tempfile=open('temporary.csv', 'w')
        tempfile.truncate(0)
        tempfilewriter = csv.writer(tempfile)
        tempfilewriter.writerow(self.tempfileheader)
        tempfile.close()
        if self.flowrate == 'None Logged' and self.plasmapower == 'None Logged':
            tk.messagebox.showinfo('Log Power','There is no logged plasma power or flow rate.')

        elif self.flowrate == 'None Logged':
            tk.messagebox.showinfo('Log Flow Rate','There is no logged flow rate')

        elif self.plasmapower == 'None Logged':
            tk.messagebox.showinfo('Logging Error','There is no logged plasma power.')
        else:
            global running
            running = True
            self.StartScan.grid_forget()
            self.StopScan.grid(row=0, columnspan=2,sticky='ew')
            self.PowerEntry['state']='normal'
            self.PowerEntryButton['state']='normal'
            self.FlowRateEntry['state']='normal'
            self.FlowRateEntryButton['state']='normal'
            self.ExportData['state']=tk.DISABLED
            self.ResetPlot['state']=tk.DISABLED

        self.readstart = time.time()

    def stopscan(self):
        global running
        running = False
        self.ExportData.grid(row=14, columnspan=2, sticky='ew')
        self.ResetPlot.grid(row=15, columnspan=2, sticky='ew')
        self.PowerEntry['state'] = tk.DISABLED
        self.PowerEntryButton['state'] = tk.DISABLED
        self.FlowRateEntry['state'] = tk.DISABLED
        self.FlowRateEntryButton['state'] = tk.DISABLED
        self.StopScan.grid_forget()
        self.StartScan.grid(row=0, columnspan=2, sticky='ew')
        self.ExportData['state']='normal'
        self.ResetPlot['state']='normal'
        df = pd.read_csv('temporary.csv')
        print('RD:',df['Radical Density'])
        print('CP:', df['Convectron Pressure'])
        print(df)

        self.readstop = time.time()
        print('total time:', self.readstop - self.readstart)
        print('time lost', (self.readstop - self.readstart) - self.time)

    def logpower(self):
        self.plasmapower = self.PowerEntry.get()
        self.PlasmaPower['text'] = str(self.plasmapower)

    def logflow(self):
        self.flowrate = self.FlowRateEntry.get()
        self.FlowRate['text'] = str(self.flowrate)

    def changebgcolor(self):
        self.color = str(self.BGColorDropdown.get())
        self.s.configure('TFrame', background=self.color)
        self.s.configure('TLabel', background=self.color)
        self.s.configure('TButton', background=self.color, disabledbackground=self.color, disabledforeground=self.color)
        self.s.configure('TEntry', background=self.color)

    def changetextcolor(self):
        self.textcolor = str(self.TextColorDropdown.get())
        self.s.configure('TFrame', foreground=self.textcolor)
        self.s.configure('TLabel', foreground=self.textcolor)
        self.s.configure('TButton', foreground=self.textcolor)
        self.s.configure('TEntry', foreground=self.textcolor)

    def changefigurecolor(self):
        self.figurecolor = self.MatplotColorDropdown.get()
        self.fig1.set_facecolor(self.figurecolor)
        self.fig2.set_facecolor(self.figurecolor)
        self.fig3.set_facecolor(self.figurecolor)
        self.canvas.draw()
        self.canvas2.draw()
        self.canvas3.draw()
    def darkmode(self):
        if self.DarkModeButton['text'] == 'Dark Mode':
            self.s.configure('TFrame', background='gray23')
            self.s.configure('TLabel', background='gray23', foreground='gainsboro')
            self.s.configure('TButton', background='gray26', foreground='black')
            self.s.configure('TEntry', background='gray40', foreground='gainsboro')
            self.s.configure('TNotebook', background='gray23', foreground='black')
            self.fig1.set_facecolor('darkgray')
            self.fig2.set_facecolor('darkgray')
            self.fig3.set_facecolor('darkgray')
            self.canvas.draw()
            self.canvas2.draw()
            self.canvas3.draw()
            self.DarkModeButton['text'] = 'Light Mode'
        elif self.DarkModeButton['text'] == 'Light Mode':
            self.s.configure('TFrame', background='gray82')
            self.s.configure('TLabel', background='gray82', foreground='black')
            self.s.configure('TButton', background='gray82', foreground='black')
            self.s.configure('TEntry', background='gray82', foreground='black')
            self.s.configure('TNotebook', background='gray82', foreground='gray80')
            self.fig1.set_facecolor('white')
            self.fig2.set_facecolor('white')
            self.fig3.set_facecolor('white')
            self.canvas.draw()
            self.canvas2.draw()
            self.canvas3.draw()
            self.DarkModeButton['text'] = 'Dark Mode'

    def startrand(self):
        global randon
        if self.randvalue == 0:
            self.randvalue = 1
            randon = True

        elif self.randvalue == 1:
            self.randvalue = 0
            randon = False

    def startrgb(self):
        global rgbon
        if self.rgbvalue == 0:
            self.rgbvalue = 1
            rgbon = True

        elif self.rgbvalue == 1:
            self.rgbvalue = 0
            rgbon = False

        self.s.configure('TFrame', background='gray10')
        self.s.configure('TLabel', background='gray10', foreground='gainsboro')
        self.s.configure('TButton', background='gray8', foreground='black')
        self.s.configure('TEntry', background='gray12', foreground='gainsboro')
        self.s.configure('TNotebook', background='gray10', foreground='black')

    def randmode(self):
        if randon:
            self.randombg = random.choice(self.tkintercolorlist)
            self.randomtxt = random.choice(self.tkintercolorlist)
            self.randomfigcolor = random.choice(self.matplotcolorlist)

            self.s.configure('TFrame', background=self.randombg)
            self.s.configure('TLabel', background=self.randombg, foreground=self.randomtxt)
            self.s.configure('TButton', background=self.randombg, foreground=self.randomtxt)
            self.s.configure('TEntry', background=self.randombg, foreground=self.randomtxt)
            self.s.configure('TNotebook', background=self.randombg, foreground=self.randomtxt)
            self.fig1.set_facecolor(self.randomfigcolor)
            self.fig2.set_facecolor(self.randomfigcolor)
            self.fig3.set_facecolor(self.randomfigcolor)
            self.canvas.draw()
            self.canvas2.draw()
            self.canvas3.draw()

        self.after(500, self.randmode)

    def rgbcycle(self):
        if rgbon:

            self.coloriter += 1

            color = self.colorcycle[self.coloriter]

            try:
                self.fig1.set_facecolor(str(color))
                self.fig2.set_facecolor(str(color))
                self.fig3.set_facecolor(str(color))
            except:
                print('bad color')

            self.canvas.draw()
            self.canvas2.draw()
            self.canvas3.draw()


            if self.coloriter == len(self.colorcycle) - 1:
                self.coloriter = -1

        self.after(50, self.rgbcycle)

    def bgcolorchooser(self):
        colors = askcolor(title='Background Color Chooser')
        self.s.configure('TFrame', background=colors[1])
        self.s.configure('TNotebook', background=colors[1])
        self.s.configure('TLabel', background=colors[1])
        self.s.configure('TButton', background=colors[1])

    def figurecolorchooser(self):
        colors = askcolor(title='Button Color Chooser')
        self.fig1.set_facecolor(str(colors[1]))
        self.fig2.set_facecolor(str(colors[1]))
        self.fig3.set_facecolor(str(colors[1]))
        self.canvas.draw()
        self.canvas2.draw()
        self.canvas3.draw()


    def textcolorchooser(self):
        colors = askcolor(title='Button Color Chooser')
        self.s.configure('TFrame', foreground=colors[1])
        self.s.configure('TButton', foreground=colors[1])
        self.s.configure('TNotebook', foreground=colors[1])
        self.s.configure('TLabel', foreground=colors[1])
        self.s.configure('TEntry', foreground=colors[1])


    def scanning(self):
        with open('temporary.csv', 'a') as file:
            if running:
                tick = time.time()
                self.time += 1
                self.j += 1
                if self.j == 10:
                    if self.alternator == 0:
                        self.alternator = 1
                        self.StoredAvg[0,0] = np.mean(self.DataTable[:,3])
                    if self.alternator == 1:
                        self.alternator = 0
                        self.StoredAvg[0,1] = np.mean(self.DataTable[:,3])

                    self.percchange = 1 - abs(self.StoredAvg[0,1] / self.StoredAvg[0,0])
                    if self.percchange <= 1:
                        self.SteadyStateIndicator.config(background='green2')
                    elif self.percchange >=1:
                        self.SteadyStateIndicator.config(background='red')



                    self.j = 0
                    np.savetxt(file, self.DataTable, delimiter=',')
                    self.DataTable = np.zeros((10,9))

                self.temperatures = RadicalTemps(self.LJ, 0, 1)
                self.GoldProbeTemp = self.temperatures[0]
                self.SSProbeTemp = self.temperatures[1]
                self.DifferenceTemp = round((self.GoldProbeTemp - self.SSProbeTemp), 3)

                self.GoldProbe['text'] = "{:0.3e}".format(self.GoldProbeTemp)
                self.SSProbe['text'] = "{:0.3e}".format(self.SSProbeTemp)
                self.Difference['text'] = "{:0.3e}".format(self.DifferenceTemp)

                if self.time == 0:
                    self.xmax2 = 1
                else:
                    self.xmax2 = self.time

                if self.time <= 60:
                    self.xmax1 = 0
                else:
                    self.xmax1 = self.time - 60


                self.chi = 12.19905 + 0.01942087*self.SSProbeTemp - 0.000007456439*(self.SSProbeTemp**2)
                #    self.Conductivity['text'] = str(round(self.chi, 3))


                self.RadicalDensityValue = GetRadicalDensity(TempA=self.GoldProbeTemp, TempB=self.SSProbeTemp, S=A, Chi=self.chi, W_D=WD, A=SA, L=L, LambdaA=GammaGold, LambdaB=GammaSS)
                self.RadicalDensity['text'] = "{:0.3e}".format(self.RadicalDensityValue)
                if self.RadicalDensityValue >= self.radmax:
                    self.radmax = self.RadicalDensityValue

                self.ConvectronPressureValue = correct(ConvectronPressure(self.LJ, 2))
                self.ConvectronPressure['text'] = str(round(self.ConvectronPressureValue,3))
                if self.ConvectronPressureValue >= self.maxconpressure:
                    self.maxconpressure = self.ConvectronPressureValue

                self.BaratronPressureValue = BaratronPressure(self.LJ, 3)
                self.BaratronPressure['text'] = "{:0.3e}".format(self.BaratronPressureValue)

                self.IonGaugePressureValue = IonGaugePressure(self.LJ, 4)
                try:
                    self.IonGaugePressure['text'] = "{:0.3e}".format(self.IonGaugePressureValue)
                except:
                    self.IonGaugePressure['text'] = str(self.IonGaugePressureValue)

                self.DataTable[self.j, 0] = self.time
                self.DataTable[self.j, 1] = self.GoldProbeTemp
                self.DataTable[self.j, 2] = self.SSProbeTemp
                self.DataTable[self.j, 3] = self.RadicalDensityValue
                self.DataTable[self.j, 4] = self.ConvectronPressureValue
                self.DataTable[self.j, 5] = self.BaratronPressureValue
                try:
                    self.DataTable[self.j, 6] = self.IonGaugePressureValue
                except:
                    self.DataTable[self.j, 6] = np.nan
                self.DataTable[self.j, 7] = self.plasmapower
                self.DataTable[self.j, 8] = self.flowrate

                self.goldline.set_xdata(np.append(self.goldline.get_xdata(), self.time))
                self.goldline.set_ydata(np.append(self.goldline.get_ydata(), self.GoldProbeTemp))
                self.ssline.set_xdata(np.append(self.ssline.get_xdata(), self.time))
                self.ssline.set_ydata(np.append(self.ssline.get_ydata(), self.SSProbeTemp))
                self.plot1.relim()
                self.plot1.autoscale_view()

                self.goldline60.set_xdata(np.append(self.goldline60.get_xdata(), self.time))
                self.goldline60.set_ydata(np.append(self.goldline60.get_ydata(), self.GoldProbeTemp))
                self.ssline60.set_xdata(np.append(self.ssline60.get_xdata(), self.time))
                self.ssline60.set_ydata(np.append(self.ssline60.get_ydata(), self.SSProbeTemp))
                self.plot2.relim()
                self.plot2.set_xlim(self.xmax1, self.xmax2)
                self.plot2.autoscale_view()

                self.radline.set_xdata(np.append(self.radline.get_xdata(), self.time))
                self.radline.set_ydata(np.append(self.radline.get_ydata(), self.RadicalDensityValue))
                self.plot3.relim()
                self.plot3.set_ylim(1e17, self.radmax*5)
                self.plot3.autoscale_view()
                #self.plot3.set_yscale('log')

                self.radline60.set_xdata(np.append(self.radline60.get_xdata(), self.time))
                self.radline60.set_ydata(np.append(self.radline60.get_ydata(), self.RadicalDensityValue))
                self.plot4.set_ylim(1e17, self.radmax*5)
                self.plot4.set_xlim(self.xmax1, self.xmax2)
                self.plot4.autoscale_view()
                #self.plot4.set_yscale('log')

                self.pressureline.set_xdata(np.append(self.pressureline.get_xdata(), self.time))
                self.pressureline.set_ydata(np.append(self.pressureline.get_ydata(), self.ConvectronPressureValue))
                self.plot5.relim()
                self.plot5.set_ylim(0.0001, self.maxconpressure * 5)
                self.plot5.autoscale_view()
                #self.plot5.set_yscale('log')

                self.pressureline60.set_xdata(np.append(self.pressureline60.get_xdata(), self.time))
                self.pressureline60.set_ydata(np.append(self.pressureline60.get_ydata(), self.ConvectronPressureValue))
                self.plot6.set_ylim(0.0001, self.maxconpressure * 5)
                self.plot6.set_xlim(self.xmax1, self.xmax2)
                self.plot6.autoscale_view()
                #self.plot6.set_yscale('log')

                if self.time  >= 2:
                    self.plot5.set_yscale('log')
                    self.plot6.set_yscale('log')

                self.canvas.draw()
                self.canvas2.draw()
                self.canvas3.draw()

                tock = time.time()
                delay = int(1000 * (tock - tick))
                print(delay)
        try:
            self.after(1000 - delay, self.scanning)
        except UnboundLocalError:
            self.after(1000, self.scanning)

    def choosefile(self):
        self.totallist = []
        self.fields = ['Time', 'Gold Probe Temperature', 'Stainless Steel Probe Temperature', 'Radical Density' 'Convectron Pressure', 'Baratron Pressure', 'Ion Gauge Pressure', 'Plasma Power', 'Flow Rate']
        self.file = tkfd.asksaveasfilename(
            parent=self, initialdir='.',
            title='Choose File',
            filetypes=[
                ('CSV Files', '.csv'),
                ('Text Files', '.txt')
            ])

        self.timelist = df['Time'].tolist()
        self.GoldProbeTempList = df['Gold Probe Temperature'].tolist()
        self.SSProbeTempList = df['Stainless Steel Probe Temperature'].tolist()
        self.PlasmaPowerList = df['Plasma Power'].tolist()
        self.FlowRateList = df['Flow Rate'].tolist()
        self.ConvectronPressureList = df['Convectron Pressure'].tolist()
        self.BaratronPressureList = df['Baratron Pressure'].tolist()
        self.IonGaugePressureList = df['Ion Gauge Pressure'].tolist()
        self.RadicalDensityList = df['Radical Density'].tolist()

        for i in range(len(self.timelist)):
            newentry = [self.timelist[i], self.GoldProbeTempList[i], self.SSProbeTempList[i], self.RadicalDensityList[i], self.ConvectronPressureList[i], self.BaratronPressureList[i], self.IonGaugePressureList[i], self.PlasmaPowerList[i], self.FlowRateList[i]]
            self.totallist.append(newentry)

        with open(self.file, 'w') as savefile:
            filewriter = csv.writer(savefile)

            filewriter.writerow(self.fields)
            filewriter.writerows(self.totallist)

        self.ExportData.grid_forget()

    def resetconfirm(self):
        self.ResetPlot.grid_forget()
        self.ResetConfirm.grid(row=15,column=0,columnspan=1,sticky='ew')
        self.ResetCancel.grid(row=15,column=1,columnspan=1,sticky='ew')

    def resetcancel(self):
        self.ResetConfirm.grid_forget()
        self.ResetCancel.grid_forget()
        self.ResetPlot.grid(row=15, columnspan=2,sticky='ew')

    def reset(self):
        self.ResetConfirm.grid_forget()
        self.ResetCancel.grid_forget()
        self.ExportData.grid(row=14, columnspan=2,sticky='ew')
        self.ResetPlot.grid(row=15, columnspan=2,sticky='ew')

        self.plot1.remove()
        self.plot1 = self.fig1.add_subplot(211, ylim=(0,self.maxlim1))
        self.plot1.set_xlabel('Time (s)')
        self.plot1.set_ylabel('Temperature (deg C)')
        self.goldline, = self.plot1.plot([],[],'orange')
        self.ssline, = self.plot1.plot([],[],'blue')

        self.plot2.remove()
        self.plot2 = self.fig1.add_subplot(212, ylim=(0, self.maxlim1))
        self.plot2.set_xlabel('Time (s)')
        self.plot2.set_ylabel('Temperature (deg C)')
        self.goldline60, = self.plot2.plot([],[],'orange')
        self.ssline60, = self.plot2.plot([],[],'blue')

        self.plot3.remove()
        self.plot3 = self.fig2.add_subplot(211, ylim=(0,self.maxlim3))
        self.plot3.set_xlabel('Time (s)')
        self.plot3.set_ylabel('Radical Density')
        self.radline, = self.plot3.plot([],[],'green')

        self.plot4.remove()
        self.plot4 = self.fig2.add_subplot(212, ylim=(0,self.maxlim4))
        self.plot4.set_xlabel('Time (s)')
        self.plot4.set_ylabel('Radical Density')
        self.radline60, = self.plot4.plot([],[],'green')

        self.plot5.remove()
        self.plot5 = self.fig3.add_subplot(211, ylim=(0,self.pressureylim1))
        self.plot5.set_xlabel('Time (s)')
        self.plot5.set_ylabel('Pressure (Torr)')
        self.pressureline, = self.plot5.plot([],[],'purple')

        self.plot6.remove()
        self.plot6 = self.fig3.add_subplot(212, ylim=(0,self.pressureylim2))
        self.plot6.set_xlabel('Time (s)')
        self.plot6.set_ylabel('Pressure (Torr)')
        self.pressureline60, = self.plot6.plot([],[],'purple')

        self.canvas.draw()
        self.canvas2.draw()
        self.canvas3.draw()

        resetfile=open('temporary.csv', 'w')
        resetfile.truncate(0)

        self.DataTable = np.zeros((10, 9))

        self.time = 0


if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')
    app.after(1000, app.scanning)
    app.after(50, app.randmode)
    app.after(50, app.rgbcycle)
    app.mainloop()
