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
#from colour import Color

running = False
rgbon = False
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

        #self.red = Color('red')
        #self.blue = Color('blue')
        #self.colorlist = list(self.red.range_to(Color('blue'),65))
        #self.colorlistBR = list(self.blue.range_to(Color('red'),65))

        #self.colorlist.append(self.colorlistBR[0])
        #print(self.colorlist)

        self.list =[]
        self.timelist = []
        self.GoldProbeTempList = []
        self.SSProbeTempList = []
        self.RadicalDensityList = []
        self.ConvectronPressureList = []
        self.BaratronPressureList = []
        self.IonGaugePressureList = []
        self.PlasmaPowerList = []
        self.FlowRateList = []
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

        self.LJ = u6.U6()

        self.maxlim1 = 40
        self.maxlim2 = 40
        self.maxlim3 = 2* 10**15
        self.maxlim4 = 2 * 10 **15
        self.pressureylim1 = 850
        self.pressureylim2 = 850

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
        self.plot2 = self.fig1.add_subplot(212, ylim=(0, self.maxlim1))
        self.plot2.set_xlabel('Time (s)')
        self.plot2.set_ylabel('Temperature (deg C)')

        self.fig2 = Figure(figsize=(5,5), dpi=100)
        self.plot3 = self.fig2.add_subplot(211, ylim=(0,self.maxlim3))
        self.plot3.set_xlabel('Time (s)')
        self.plot3.set_ylabel('Radical Density')
        self.plot4 = self.fig2.add_subplot(212, ylim=(0,self.maxlim4))
        self.plot4.set_xlabel('Time (s)')
        self.plot4.set_ylabel('Radical Density')

        self.fig3 = Figure(figsize=(5,5), dpi=100)
        self.plot5 = self.fig3.add_subplot(211, ylim=(0,self.pressureylim1))
        self.plot5.set_xlabel('Time (s)')
        self.plot5.set_ylabel('Pressure (Torr)')
        self.plot6 = self.fig3.add_subplot(212, ylim=(0,self.pressureylim2))
        self.plot6.set_xlabel('Time (s)')
        self.plot6.set_ylabel('Pressure (Torr)')


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
        self.StartScan.grid(row=0, sticky='ew')

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
        self.ExportData.grid(row=11,columnspan=2,sticky='ew')
#        self.ExportData.grid_forget()

        self.ResetPlot = ttk.Button(self.frame3, text='Reset Plot', command=self.reset, state=tk.DISABLED)
        self.ResetPlot.grid(row=12,columnspan=2,sticky='ew')

        self.DarkModeButton = ttk.Button(self.frame2s, text='Dark Mode', command=self.darkmode)
        self.DarkModeButton.grid(row=0, columnspan=2, sticky='ew')

        self.RGBButton = ttk.Button(self.frame2s, text='Gamer Mode', command=self.startrgb)
        self.RGBButton.grid(row=0, column=2, columnspan=2,sticky='ew')

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
        self.PowerEntry.grid(row=6, columnspan=2,sticky='ew')

        self.PowerEntryButton = ttk.Button(self.frame3, text='Log Plasma Power (W)', command=self.logpower)
        self.PowerEntryButton.grid(row=7)

        self.FlowRateEntry = ttk.Entry(self.frame3)
        self.FlowRateEntry.grid(row=8, columnspan=2,sticky='ew')

        self.FlowRateEntryButton = ttk.Button(self.frame3, text='Log Flow Rate (sccm)', command=self.logflow)
        self.FlowRateEntryButton.grid(row=9, columnspan=2,sticky='ew')

#        self.LabelList= [self.RadicalDensityLabel, self.RadicalDensity, self.GoldProbeLabel,
#        self.GoldProbe, self.SSProbeLabel, self.SSProbe, self.DifferenceLabel,
#        self.Difference, self.ConvectronPressureLabel, self.ConvectronPressure,
#        self.BaratronPressureLabel,self.BaratronPressure,
#        self.IonGaugePressureLabel, self.IonGaugePressure, self.PlasmaPowerLabel,
#        self.PlasmaPower, self.FlowRateLabel, self.FlowRate]

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

    #    self.FigureColorEntry = ttk.Entry(self.frame2s)
    #    self.FigureColorEntry.grid(row=3, column=1, sticky='ew')

        self.ChangeFigureColorButton = ttk.Button(self.frame2s, text='Change',command=self.changefigurecolor)
        self.ChangeFigureColorButton.grid(row=3, column=2)


        self.MatplotColorDropdown = ttk.Combobox(self.frame2s, textvariable=self.selectedFigcolor, values=self.matplotcolorlist)
        self.MatplotColorDropdown.grid(row=3, column=1)





    def onclose(self):
        plt.close('all')
        self.destroy()

    def startscan(self):
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
            self.PowerEntry.grid(row=6, columnspan=2,sticky='ew')
            self.PowerEntryButton.grid(row=7,columnspan=2,sticky='ew')
            self.FlowRateEntry.grid(row=8, columnspan=2,sticky='ew')
            self.FlowRateEntryButton.grid(row=9,columnspan=2,sticky='ew')
            self.ExportData['state']=tk.DISABLED
            self.ResetPlot['state']=tk.DISABLED

    def stopscan(self):
        global running
        running = False
        self.ExportData.grid(row=14, columnspan=2, sticky='ew')
        self.ResetPlot.grid(row=15, columnspan=2, sticky='ew')
        self.PowerEntry.grid_forget()
        self.PowerEntryButton.grid_forget()
        self.FlowRateEntry.grid_forget()
        self.FlowRateEntryButton.grid_forget()
        self.StopScan.grid_forget()
        self.StartScan.grid(row=0, columnspan=2, sticky='ew')
        self.ExportData['state']='normal'
        self.ResetPlot['state']='normal'

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
            #for label in self.LabelList:
            #    label['background']='gray23'

    def startrgb(self):
        global rgbon
        if self.rgbvalue == 0:
            self.rgbvalue = 1
            rgbon = True

        elif self.rgbvalue == 1:
            self.rgbvalue = 0
            rgbon = False


    def rgbmode(self):
        if rgbon:
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

        self.after(500, self.rgbmode)

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
                self.PlasmaPowerList.append(self.plasmapower)
                self.FlowRateList.append(self.flowrate)

                self.GoldProbe['text'] = str(self.GoldProbeTemp)
                self.SSProbe['text'] = str(self.SSProbeTemp)
                self.Difference['text'] = str(self.DifferenceTemp)
                self.maxlim1 = 1.25 * max(max(self.list))


                self.last60 = self.list[-60:]
                self.maxlim2 = 1.25 * max(max(self.last60))

                self.xmax2 = self.timelist[-1]

                if (self.timelist[-1] - 60) <= 0:
                    self.xmax1 = 0
                else:
                    self.xmax1 = self.xmax2 - 60


                self.chi = 12.19905 + 0.01942087*self.SSProbeTemp - 0.000007456439*(self.SSProbeTemp**2)
            #    self.Conductivity['text'] = str(round(self.chi, 3))


                self.RadicalDensityValue = GetRadicalDensity(TempA=self.GoldProbeTemp, TempB=self.SSProbeTemp, S=A, Chi=self.chi, W_D=WD, A=SA, L=L, LambdaA=GammaGold, LambdaB=GammaSS)
                self.RadicalDensity['text'] = "{:0.3e}".format(self.RadicalDensityValue)
                self.RadicalDensityList.append(self.RadicalDensityValue)
                self.maxlim3 = 10 * max(self.RadicalDensityList)
                self.Radical60 = self.RadicalDensityList[-60:]
                self.maxlim4 = 10 * max(self.Radical60)

                self.ConvectronPressureValue = ConvectronPressure(self.LJ, 2)
                self.ConvectronPressureList.append(self.ConvectronPressureValue)
                self.ConvectronPressure['text'] = str(round(self.ConvectronPressureValue,3))
                self.pressureylim1 = 10 * max(self.ConvectronPressureList)
                self.pressureylim2 = 10 * max(self.ConvectronPressureList[-60:])

                self.BaratronPressureValue = BaratronPressure(self.LJ, 3)
                self.BaratronPressureList.append(self.BaratronPressureValue)
                self.BaratronPressure['text'] = "{:0.3e}".format(self.BaratronPressureValue)

                self.IonGaugePressureValue = IonGaugePressure(self.LJ, 4)
                if self.IonGaugePressureValue == 'Ion Gauge Off':
                    self.IonGaugePressureList.append(np.nan)
                    self.IonGaugePressure['text'] = 'Ion Gauge Off'
                else:
                    self.IonGaugePressureList.append(self.IonGaugePressureValue)
                    try:
                        self.IonGaugePressure['text'] = "{:0.3e}".format(self.IonGaugePressureValue)
                    except:
                        self.IonGaugePressure['text'] = str(self.IonGaugePressureValue)


                self.plot1.remove()
                self.plot1 = self.fig1.add_subplot(211, ylim=(0,self.maxlim1))
                self.plot1.set_xlabel('Time (s)')
                self.plot1.set_ylabel('Temperature (deg C)')
                self.plot1.set_title('Temperature(deg C)')
                self.plot1.plot(self.timelist, self.GoldProbeTempList, color='orange')
                self.plot1.plot(self.timelist, self.SSProbeTempList, color='blue')


                self.plot2.remove()
                self.plot2 = self.fig1.add_subplot(212, xlim=(self.xmax1, self.xmax2), ylim=(0, self.maxlim2))
                self.plot2.set_xlabel('Time (s)')
                self.plot2.set_ylabel('Temperature (deg C)')
                self.plot2.set_title('Temperature(deg C)')
                self.plot2.plot(self.timelist[-60:], self.GoldProbeTempList[-60:], color='orange')
                self.plot2.plot(self.timelist[-60:], self.SSProbeTempList[-60:], color='blue')

                self.canvas.draw()

                self.plot3.remove()
                self.plot3 = self.fig2.add_subplot(211, ylim=(1e19,self.maxlim3),yscale='log')
                self.plot3.set_xlabel('Time (s)')
                self.plot3.set_ylabel('Radical Density')
                #self.plot3.set_yscale('log')
                self.plot3.set_title('Radical Density')
                self.plot3.plot(self.timelist, self.RadicalDensityList, color='green')

                self.plot4.remove()
                self.plot4 = self.fig2.add_subplot(212, xlim=(self.xmax1, self.xmax2), ylim=(1e19,self.maxlim4),yscale='log')
                self.plot4.set_xlabel('Time (s)')
                self.plot4.set_ylabel('Radical Density')
                #self.plot4.set_yscale('log')
                self.plot4.set_title('Radical Density (n/m3)')
                self.plot4.plot(self.timelist[-60:], self.RadicalDensityList[-60:], color='red')


                self.canvas2.draw()

                self.plot5.remove()
                self.plot5 = self.fig3.add_subplot(211, ylim=(1e-6,self.pressureylim1))
                self.plot5.set_xlabel('Time (s)')
                self.plot5.set_ylabel('Pressure (Torr)')
                #self.plot5.set_yscale('log')
                self.plot5.set_title('Pressure')
                self.plot5.plot(self.timelist, self.ConvectronPressureList, color='purple')
                self.plot5.plot(self.timelist, self.BaratronPressureList, color='blue')
                for pressure in self.IonGaugePressureList:
                    self.plot5.plot(self.timelist, self.IonGaugePressureList, color='green')


                self.plot6.remove()
                self.plot6 = self.fig3.add_subplot(212, xlim=(self.xmax1, self.xmax2), ylim=(1e-6,self.pressureylim2),yscale='log')
                self.plot6.set_xlabel('Time (s)')
                self.plot6.set_ylabel('Pressure (Torr)')
            #    self.plot6.set_yscale('log')
                self.plot6.set_title('Pressure')
                self.plot6.plot(self.timelist[-60:], self.ConvectronPressureList[-60:], color='gold')
                self.canvas3.draw()





        self.after(1000, self.scanning)

    def exportdata(self):
        self.totallist = []
        self.fields = ['Time', 'Gold Probe Temperature', 'Stainless Steel Probe Temperature', 'Radical Density']
        for i in range(len(self.list)):
            newentry = [self.timelist[i], self.GoldProbeTempList[i], self.SSProbeTempList[i], self.RadicalDensityList[i]]
            self.totallist.append(newentry)
        print(self.totallist)
        with open('TemperatureList.csv', 'a') as templist:
            writer = csv.writer(templist)

            writer.writerow(self.fields)
            writer.writerows(self.totallist)

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
        print(os.path.basename(self.file))
        for i in range(len(self.list)):
            newentry = [self.timelist[i], self.GoldProbeTempList[i], self.SSProbeTempList[i], self.RadicalDensityList[i], self.ConvectronPressureList[i], self.BaratronPressureList[i], self.IonGaugePressureList[i], self.PlasmaPowerList[i], self.FlowRateList[i]]
            self.totallist.append(newentry)

        with open(self.file, 'w') as savefile:
            filewriter = csv.writer(savefile)

            filewriter.writerow(self.fields)
            filewriter.writerows(self.totallist)

        self.ExportData.grid_forget()

    def reset(self):
        self.list.clear()
        self.timelist.clear()
        self.GoldProbeTempList.clear()
        self.SSProbeTempList.clear()
        self.PlasmaPowerList.clear()
        self.FlowRateList.clear()
        self.ConvectronPressureList.clear()
        self.BaratronPressureList.clear()
        self.IonGaugePressureList.clear()

        print(self.list)





if __name__ == '__main__':
    app = controller()
    app.wm_title('TUFCON Controller')
    app.after(1000, app.scanning)
    app.after(1000, app.rgbmode)
    app.mainloop()
