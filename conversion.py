import numpy as np
import scipy as sp
import scipy.interpolate
import pandas as pd

def log_interp1d(xx, yy, kind='linear'):
    logx = np.log10(xx)
    logy = np.log10(yy)
    lin_interp = sp.interpolate.interp1d(logx, logy, kind=kind)
    log_interp = lambda zz: np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp

df = pd.read_csv('convertedpressure.csv')

D2 = df['D2'].tolist()
N2 = df['N2'].tolist()

interpD = sp.interpolate.interp1d(D2, 100, kind='linear')
interpN = sp.interpolate.interp1d(N2, 100, kind='linear')
