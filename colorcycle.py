import numpy as np
import matplotlib.pyplot as plt
from colour import Color
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from time import sleep
import time
'''
red = Color('red')
green = Color('green')
blue = Color('blue')
colorsRG = list(red.range_to(Color("green"),40))
colorsGB = list(green.range_to(Color("blue"),40))
colorsBR = list(blue.range_to(Color("red"),20))

colorsRB = list(red.range_to(Color(blue),65))
print(colorsRB)

x = np.arange(0,100,10)
y = x

for colorRB in colorsRB:
    newx = colorsRB.index(colorRB) + x
    newy = newx - colorsRB.index(colorRB)
    plt.plot(newx,newy, color=str(colorRB))

plt.show()
print(colorsRG)
print(colorsGB)
'''

class ColorCycle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.onclose)

        self.Frame = ttk.Frame(self)
        self.Frame.grid(column=0,row=0,sticky='news')

        self.s = ttk.Style()
        self.red = Color('red')
        self.blue = Color('blue')
        self.colorsRB = list(self.red.range_to(Color('blue'),12))
        self.colorsBR = list(self.blue.range_to(Color('red'),12))
        self.colorsRB.append(self.colorsBR)


        print(self.colorsRB)
        self.fig1 = Figure(figsize=(5,5), dpi=100)
        self.plot1 = self.fig1.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.Frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    #    self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.Frame)
    #    self.toolbar1.update()

        self.cyclebutton = ttk.Button(self.Frame, text='cycle', command=self.rgbcycle)
        self.cyclebutton.pack()

    def rgbcycle(self):
        tick = time.time()
        for color in self.colorsRB:
            try:
                self.fig1.set_facecolor(str(color))
                self.canvas.draw()
                sleep(0.05)
            except:
                continue
        tock = time.time()
        print(tock-tick)

    def onclose(self):
        plt.close('all')
        self.destroy()

if __name__ == '__main__':
    app = ColorCycle()
    app.wm_title('Color Cycle Test')
    app.mainloop()
