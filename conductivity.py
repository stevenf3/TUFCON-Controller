import numpy as np
import matplotlib.pyplot as plt


temps =          [0,    25,   50,   100,  150,  200,  250,  300,  350,  400,  450,  500]
conductivities = [12.1, 12.7, 13.2, 14.1, 15.0,	15.8, 16.6,	17.3, 18.0,	18.8, 19.4, 20.1]

x = np.arange(0,525,25)
y = 12.1 + 0.015 * x
y2 = 12.19905 + 0.01942087*x - 0.000007456439*(x**2)

plt.plot(temps, conductivities)
plt.plot(x, y2, color='green')
plt.show()
