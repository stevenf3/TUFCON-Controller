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
print(lenRadList)

masteravglist = []
avgdiff = []
slopelist = []
interceptlist = []
windowsize = 10

for i in range(int(lenRadList / windowsize)):
    try:
        y2 = RadList[(i + 1)*windowsize]
        y1 = RadList[i*windowsize]
    except IndexError:
        continue

    x2 = (i + 1)*windowsize
    x1 = i*windowsize
    xrange = np.arange(x1, x2, 1)
    slope, intercept = np.polyfit(xrange, RadList[x1:x2], 1)
    print(slope, intercept)
    slopelist.append(slope)
    interceptlist.append(intercept)


line = np.arange(0, len(avgdiff)*windowsize, windowsize)
