import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = '070921-20mT.csv'
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
ax.set_ylim([5e19, 3e21])

ax.set_title('Radical Density vs Time (20 mTorr)')

AvgList = []
firstatavg = []
changeslist = []
for power in powers:
    change = timelist[PowerList.index(power)]
    changeslist.append(change)
    ax.vlines(change, ymin=5e19, ymax=3e21)


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
        firstatavg.append(atavg[0])
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

        firstatavg.append(atavg[0])

print(AvgList)
timetolist = []
for i in range(len(firstatavg)):
    timeto = firstatavg[i] - changeslist[i]
    timetolist.append(timeto)
    print(timeto)


writerfile = '070921-20mT-Analyzed'
csvheader = ['Pressure', 'Power', 'Equilibrium Radical Density', 'Time to Equilibrium' ]

totallist = []
for j in range(len(powers)):
    newentry = [60, powers[j], AvgList[j], timetolist[j]]
    totallist.append(newentry)

with open(writerfile, 'w') as file:
    filewriter = csv.writer(file)

    filewriter.writerow(csvheader)
    filewriter.writerows(totallist)






ax.vlines(change, ymin=8e19, ymax=3e21, label='Power Changes')
ax.plot([min,max], [Avg, Avg], color='orange', label='Average Radical Density')
ax.vlines(1200, ymin=1e20, ymax = 1.01e20, color='silver', label='Equilibrium Region')
ax.legend(loc='upper left')
plt.show()
