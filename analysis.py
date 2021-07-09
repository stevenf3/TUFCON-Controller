import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

filename = '070921-100mT.csv'

df = pd.read_csv(filename)
print(df)
#df.plot('Time', 'Radical Density', logy=True, ylim=(1e19, 1e21))
timelist = df['Time'].tolist()
RadList = df['Radical Density'].tolist()

fig, ax = plt.subplots()
ax.plot(timelist, RadList)
ax.set_xlabel('Time')
ax.set_ylabel('Radical Density')
ax.set_yscale('log')
ax.set_ylim(1e19, 1e21)
plt.show()
