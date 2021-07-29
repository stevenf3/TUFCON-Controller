import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter
from math import *
import time
tick = time.time()
filename = '070921-20mT.csv'
powers = [200, 400, 600, 800, 1000]
df = pd.read_csv(filename)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
conlist = df['Convectron Pressure'].tolist()
barlist = df['Baratron Pressure'].tolist()
print(len(conlist), len(barlist))

tick = time.time()
a,b,c,d = np.polyfit(conlist, barlist, 3)
#a,b,c,d = -1409.902032370218, 481.11910544438706, -54.23512869636659, 2.083175260377376
#a,b,c,d = -1146.0773239928094, 163.08697146624561, -7.0813813387058175, 0.11726060922857344
tock = time.time()
print(tock-tick)
print(a,b,c,d)
xplottinglist = []
yplottinglist = []
ylist = []
for i in range(len(conlist)):
    x = conlist[i]
    y = a*x**3 + b*x**2 + c*x + d
    ylist.append(y)
    if x >= 0.01:
        xplottinglist.append(x)
        yplottinglist.append(y)

errorlist = []
for i in range(len(ylist)):
    if conlist[i] >= 0.01:
        diff = ylist[i] - barlist[i]
        percerr = abs(100 * (diff/barlist[i]))
        errorlist.append(percerr)

avgerr = np.mean(errorlist)
errmax = max(errorlist)
errmin = min(errorlist)
print(avgerr, 'max:', errmax, 'min:', errmin)
fig, ax = plt.subplots()
ax.plot(conlist, barlist)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(xplottinglist, yplottinglist)
plt.show()
