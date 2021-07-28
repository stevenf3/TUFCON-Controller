import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter
from math import *
import time
tick = time.time()
filename = '070921-100mT.csv'
powers = [200, 400, 600, 800, 1000]
df = pd.read_csv(filename)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
RadList = df['Radical Density'].tolist()
PowerList = df['Plasma Power'].tolist()
GoldTempList = df['Gold Probe Temperature'].tolist()
SSTempList = df['Stainless Steel Probe Temperature'].tolist()
Radsavgol = savgol_filter(RadList, 51, 2)
fig, ax = plt.subplots()

lenRadList = int(len(RadList))
masteravglist = []
avgdiff = []
sslist = []
indlist = []
windowsize = 10

for i in range(int(lenRadList / windowsize)):
    try:
        y2 = RadList[(i + 1)*windowsize]
        y1 = RadList[i*windowsize]
    except IndexError:
        continue

    x2 = (i + 1)*windowsize
    x1 = i*windowsize

    IncAvgList = []
    for val in RadList[x1:x2]:
        IncAvgList.append(val)

    IncAvg = np.mean(IncAvgList)
    masteravglist.append(IncAvg)

for ind in range(len(masteravglist)):
    try:
        avg2 = masteravglist[ind+1]
        avg1 = masteravglist[ind]
    except IndexError:
        continue

    comp = avg2/avg1

    if abs(comp) <= 1.001:
        sslist.append(comp)
        indlist.append(ind)
    elif abs(comp) >= 1.001:
        sslist.append(np.nan)
        indlist.append(ind)

    avgdiff.append(comp)

line = np.arange(0, len(avgdiff)*windowsize, windowsize)

ax.plot(timelist, RadList, label='Radical Density')

agglist = [[],[],[],[],[]]
for powdex in range(len(powers)):
    try:
        powstart = ceil(PowerList.index(powers[powdex]) / windowsize)
        powend = floor(PowerList.index(powers[powdex+1])/ windowsize)
    except IndexError:
        powend = floor(timelist[-1] / windowsize)

    print(powdex, powstart, powend)

    for i in sslist[powstart:powend]:
        index = sslist.index(i)
        if index != 0:
            agglist[powdex].append(index * 10)

avgRadList = []
stdList = []
for agg in agglist:
    x1 = agg[0]
    x2 = agg[-1]
    xrange = np.arange(x1, x2, 1)
    #print(x1, x2)
    ax.plot(xrange, RadList[x1:x2], color='orange')
    validRads = RadList[x1:x2]
    avgs = np.mean(validRads)
    stds = np.std(validRads)
    print(avgs)
    avgRadList.append(avgs)
    stdList.append(stds)

print('agglist:', agglist[0][-1])
print('avgradlist:', avgRadList)
print('stdList:', stdList)

ax.set_xlabel('Time (s, approximate)')
ax.set_ylabel('Radical Density (m-3)')
ax.set_yscale('log')
ax.set_ylim([7e19, 3e21])

ax.set_title('Radical Density vs Time (60 mTorr)')

AvgList = []
firstatavg = []
changeslist = []
for power in powers:
    change = timelist[PowerList.index(power)]
    changeslist.append(change)
    ax.vlines(change, ymin=7e19, ymax=3e21)

    if power != 1000:
        firstpoint = PowerList.index(power+200) - 45
        lastpoint = PowerList.index(power+200) - 5
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        AvgList.append(Avg)
        min = PowerList.index(power)
        max = timelist[PowerList.index(power+200)]
        #ax.plot([min,max], [Avg, Avg], color='orange')

        power1 = PowerList.index(power)
        power2 = PowerList.index(power+200)
        atavg = []
        for rad in RadList[power1:power2]:
            diff = abs(Avg - rad)
            percdiff = diff/Avg
            if percdiff <= 0.01:
                if percdiff >= -0.01:
                    atavg.append(RadList.index(rad))
                    #ax.vlines(RadList.index(rad), ymin=0.5*rad, ymax = 1.5*rad, color='silver')
        firstatavg.append(atavg[0])
    else:
        firstpoint = timelist[-45]
        lastpoint = timelist[-5]
        RadRange = np.array(RadList[firstpoint:lastpoint])
        Avg = np.mean(RadRange)
        AvgList.append(Avg)
        min = PowerList.index(power)
        max = timelist[-1]
        #ax.plot([min,max], [Avg, Avg], color='orange')

        power1 = PowerList.index(power)
        power2 = timelist[-1]
        atavg = []
        for rad in RadList[power1:power2]:
            diff = abs(Avg - rad)
            percdiff = diff/Avg
            if percdiff <= 0.01:
                if percdiff >= -0.01:
                    atavg.append(RadList.index(rad))

        firstatavg.append(atavg[0])

timetolist = []
for i in range(len(firstatavg)):
    timeto = firstatavg[i] - changeslist[i]
    timetolist.append(timeto)


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
ax.plot([0,1], [0,1], color='orange', label='Equilibrium Region')
#ax.vlines(1200, ymin=1e20, ymax = 1.01e20, color='silver', label='Equilibrium Region')
ax.legend(loc='upper left')
plt.show()

fig2, ax2 = plt.subplots()
ax2.errorbar(powers, avgRadList, marker='o', yerr=stdList, capsize=7)
ax2.set_title('Average Radical Density (60 mTorr)')
ax2.set_yscale('log')
ax2.set_ylabel('Radical Density (m-3)')
ax2.set_xlabel('Power (W)')
ax2.set_ylim([7e19, 3e21])
plt.show()
tock = time.time()
