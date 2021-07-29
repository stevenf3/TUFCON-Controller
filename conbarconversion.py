import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = 'pressuretest2.csv'
powers = [200, 400, 600, 800, 1000]
df = pd.read_csv(filename)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
conlist = df['Convectron Pressure'].tolist()
barlist = df['Baratron Pressure'].tolist()
x = np.arange(0.001, 2, 0.01)
y = x
fig, ax = plt.subplots()

savgol = savgol_filter(barlist, 13, 3)
a, b = np.polyfit(conlist, savgol, 1)

ystarlist = []
for i in conlist:
    ystar = a*i + b
    ystarlist.append(ystar)

y2 = barlist[-1]
y1 = barlist[0]
x2 = conlist[-1]
x1 = conlist[0]

slope2 = (y2-y1)/(x2-x1)
print('slope:', a)
print('slope2:', slope2)
ax.plot(conlist,  savgol,  marker='o')
ax.set_xlabel('convectron')
ax.set_ylabel('baratron (true)')
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(x,y)
ax.plot(conlist, ystarlist)
plt.show()
