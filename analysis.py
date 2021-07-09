import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

filename = '070821-Test1.csv'

timelist = []
GPList = []
SSList = []
RadList = []
ConvectronList = []
BaratronList = []
IonList = []
PowerList = []
FlowRateList = []

df = pd.read_csv(filename)

print(df)
