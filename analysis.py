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
ax.plot(timelist, RadList)
ax.set_xlabel('Time')
ax.set_ylabel('Radical Density')
ax.set_yscale('log')
ax.set_ylim([1e19, 1e21])

for power in powers:
    ax.vlines(timelist[PowerList.index(power)], ymin=1e19, ymax=1e21)


    if power != 1000:
        firstpoint = PowerList.index(power) - 45
        lastpoint = PowerList.index(power) - 5
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        min = timelist[PowerList.index(power)]
        max = timelist[PowerList.index(power+200)] +1
        print(min, max)
        ax.hlines(Avg, xmin=485, xmax=1892)

    else:
        firstpoint = timelist[-45]
        lastpoint = timelist[-5]
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        min = PowerList.index(power)
        max = timelist[-1]
        print(min, max)
        ax.hlines(Avg, xmin=min, xmax=max)

plt.show()
