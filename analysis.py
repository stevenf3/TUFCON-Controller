import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = '070921-100mT.csv'
powers = [200, 400, 600, 800, 1000]
df = pd.read_csv(filename)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
RadList = df['Radical Density'].tolist()
PowerList = df['Plasma Power'].tolist()

Radsavgol = savgol_filter(RadList, 51, 2)
fig, ax = plt.subplots()
ax.plot(timelist, RadList, label='Radical Density (n/m3)')
ax.set_xlabel('Time (s, approximate)')
ax.set_ylabel('Radical Density (n/m3)')
ax.set_yscale('log')
ax.set_ylim([5e19, 1e21])
ax.set_title('Radical Density vs Time')

AvgList = []

for power in powers:
    changes = timelist[PowerList.index(power)]
    ax.vlines(changes, ymin=5e19, ymax=1e21)


    if power != 1000:
        firstpoint = PowerList.index(power+200) - 45
        lastpoint = PowerList.index(power+200) - 5
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        AvgList.append(Avg)
        min = PowerList.index(power)
        max = timelist[PowerList.index(power+200)]
        ax.plot([min,max], [Avg, Avg], color='orange')

        power1 = PowerList.index(power)
        power2 = PowerList.index(power+200)
        atavg = []
        for rad in RadList[power1:power2]:
            diff = abs(Avg - rad)
            percdiff = diff/Avg
            if percdiff <= 0.01:
                if percdiff >= -0.01:
                    atavg.append(RadList.index(rad))
                    ax.vlines(RadList.index(rad), ymin=0.5*rad, ymax = 1.5*rad, color='silver')

    else:
        firstpoint = timelist[-45]
        lastpoint = timelist[-5]
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        AvgList.append(Avg)
        min = PowerList.index(power)
        max = timelist[-1]
        ax.plot([min,max], [Avg, Avg], color='orange')

        power1 = PowerList.index(power)
        power2 = timelist[-1]
        atavg = []
        for rad in RadList[power1:power2]:
            diff = abs(Avg - rad)
            percdiff = diff/Avg
            if percdiff <= 0.01:
                if percdiff >= -0.01:
                    atavg.append(RadList.index(rad))
                    ax.vlines(RadList.index(rad), ymin=0.5*rad, ymax = 1.5*rad, color='silver')

ax.vlines(changes, ymin=5e19, ymax=1e21, label='Power Changes')
ax.plot([min,max], [Avg, Avg], color='orange', label='Average Value')
ax.vlines(5000, ymin=1e20, ymax = 1.01e20, color='silver', label='Equilibrium region')
ax.legend()
plt.show()
