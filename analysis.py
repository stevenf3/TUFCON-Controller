import matplotlib.pyplot as plt
import numpy as np
import csv

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
count = 0
with open(filename) as file:
    reader = csv.reader(file)
    for row in reader:
        count += 1
        try:
            if float(row[7]) >= 100:
                PowerList.append(float(row[7]))
        except:
            PowerList.append(0)

print(len(PowerList))


#timelist.append(int(row[0]))
#GPList.append(float(row[1]))
#SSList.append(float(row[2]))
#RadList.append(float(row[3]))
#ConvectronList.append(float(row[4]))
#BaratronList.append(float(row[5]))
#IonList.append(float(row[6]))
#PowerList.append(float(row[7]))
#FlowRateList.append(float(row[8]))
