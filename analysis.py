import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = '070921-60mTorr.csv'
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
ax.plot(timelist, RadList, label='Radical Density (n/m3)')
ax.set_xlabel('Time (s, approximate)')
ax.set_ylabel('Radical Density (n/m3)')
ax.set_yscale('log')
ax.set_ylim([7e19, 3e21])

ax.set_title('Radical Density vs Time (60 mTorr)')

figT, axT = plt.subplots()
axT.plot(timelist, GoldTempList, label='Gold Probe Temperature')
axT.plot(timelist, SSTempList, label='SS Probe Temperature')
axT.set_title('Probe Temperatures in 60 mTorr Plasma')
axT.set_xlabel('Time (s)')
axT.set_ylabel('Temperature (deg C)')
axT.legend()
plt.show()
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

timetolist = []
for i in range(len(firstatavg)):
    timeto = firstatavg[i] - changeslist[i]
    timetolist.append(timeto)


writerfile = '070921-60mT-Analyzed'
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




TruePressure = [0.0001,
0.0002,
0.0005,
0.001,
0.002,
0.005,
0.01,
0.02,
0.05,
0.1,
0.2,
0.5,
1,
2,
5,
10

]
N2Voltage = [1.699,2,2.301,2.699,3,3.301,3.699,4,4.301]

D2Voltage = [1.699,2.114,2.38,2.778,3.083,3.386,3.778,4.083,4.398]
N2Pressure = []
for voltage in N2Voltage:
    pressure = 10**(voltage - 5)
    N2Pressure.append(pressure)

D2Pressure = []
for DVoltage in D2Voltage:
    pressure = 10**(DVoltage-5)
    D2Pressure.append(pressure)

difflist = []
errorlist = []
pressureslist = []
D2ConvList = []
for i in range(len(N2Pressure)):
    x = D2Pressure[i]
    D2Conv = 14.559*x**4 - 6.7341*x**3 + 0.7327*x**2 + 0.8099*x + 4E-05
    #D2Conv = 0.829*x**1.0034
    diff = D2Conv - N2Pressure[i]
    error = abs(diff/N2Pressure[i])
    errorlist.append(error)
    difflist.append(diff)
    D2ConvList.append(D2Conv)

    newentry2 = [D2Pressure[i], N2Pressure[i]]
    pressureslist.append(newentry2)

avg = np.mean(errorlist)
print(errorlist)
print(avg)

print(len(D2Voltage), len(N2Voltage))
fig2, ax2 = plt.subplots()
ax2.plot(D2Pressure, N2Pressure, marker='o')
ax2.plot(D2ConvList, N2Pressure)
ax2.set_title('D2 vs N2 Pressure')
ax2.set_xlabel('D2 Pressure')
ax2.set_ylabel('N2 Pressure')
ax2.set_yscale('log')
ax2.set_xscale('log')
ax.set_ylim(1e-4, 2.5e-1)
ax.set_xlim(1e-4, 2e-1)
plt.show()

with open('convertedpressure.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(pressureslist)
