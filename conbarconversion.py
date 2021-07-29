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

plt.plot(conlist,  barlist,  marker='o')
plt.show()
