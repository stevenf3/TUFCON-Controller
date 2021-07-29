import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter
from math import *
import time
tick = time.time()
filename = 'pressuretest.csv'
powers = [200, 400, 600, 800, 1000]
df = pd.read_csv(filename)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
conlist = df['Convectron Pressure'].tolist()
barlist = df['Baratron Pressure'].tolist()
print(len(conlist), len(barlist))

tick = time.time()
a,b,c,d = np.polyfit(conlist, barlist, 3)

fig, ax = plt.subplots()
ax.plot(conlist, barlist, marker='o')
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('convectron pressure (torr)')
ax.set_ylabel('baratron (true) pressure')
ax.set_yscale('log')
ax.set_xscale('log')
plt.show()
