import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from scipy.signal import savgol_filter

filename = 'pressuretest2.csv'

df = pd.read_csv(filename)

timelist = df['Time'].tolist()
conlist = df['Convectron Pressure'].tolist()
barlist = df['Baratron Pressure'].tolist()

def correct(val):
    correctedpressure = np.interp(val, conlist, barlist)
    return(correctedpressure)
