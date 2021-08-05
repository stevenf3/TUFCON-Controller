import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = 'pressuretest2.csv'

dfp = pd.read_csv(filename)

timelist = dfp['Time'].tolist()
conlist = dfp['Convectron Pressure'].tolist()
barlist = dfp['Baratron Pressure'].tolist()

def correct(val):
    correctedpressure = np.interp(val, conlist, barlist)
    return(correctedpressure)
