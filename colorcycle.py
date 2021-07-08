import numpy as np
import matplotlib.pyplot as plt
from colour import Color

red = Color('red')
green = Color('green')
blue = Color('blue')
colorsRG = list(red.range_to(Color("green"),40))
colorsGB = list(green.range_to(Color("blue"),40))
colorsBR = list(blue.range_to(Color("red"),20))

colorsRB = list(red.range_to(Color(blue),65))
print(colorsRB)
x = np.arange(0,100,10)
y = x

"""
for colorRG in colorsRG:
    newx = colorsRG.index(colorRG) + x
    newy = newx - colorsRG.index(colorRG)
    plt.plot(newx,newy, color=str(colorRG))

for colorGB in colorsGB:
    newx2 = colorsGB.index(colorGB) + newx
    newy2 = newx2 - colorsGB.index(colorGB)
    plt.plot(newx2,newy2, color=str(colorGB))

for colorBR in colorsBR:
    newx3 = colorsBR.index(colorBR) + newx2
    newy3 = newx3 - colorsBR.index(colorBR)
    plt.plot(newx3,newy3, color=str(colorBR))
"""

for colorRB in colorsRB:
    newx = colorsRB.index(colorRB) + x
    newy = newx - colorsRB.index(colorRB)
    plt.plot(newx,newy, color=str(colorRB))

plt.show()
print(colorsRG)
print(colorsGB)
