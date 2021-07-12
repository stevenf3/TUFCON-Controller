import numpy as np
import math

import u6

def GaugeVoltage(d, AIN):
    ConVoltage = d.getAIN(AIN)
    return(ConVoltage)

def GaugeBits(d, AIN):
    ConBits = d.getFeedback(d, u6.AIN(AIN))
    return(ConBits)

def ConvectronPressure(d, AIN):
    voltagepower = (GaugeVoltage(d, AIN)  - 5) + 0.0155 ##from manual for gauge, plus a corrective factor *test at vacuum to see if constant or variable correction
    pressure = 10**voltagepower
    return(pressure)

def CorrectedConvectronPressure(d, AIN):
    x = ConvectronPressure(d, AIN)
    CorrectedPressure = 0.0318*x**4 - 0.3553*x**3 + 1.3606*x**2 - 1.0397*x + 1.0223
    return(CorrectedPressure)


def BaratronPressure(d, AIN):
    voltage = (GaugeVoltage(d, AIN))
    if voltage >= 10:
        return('over range')
    else:
        pressure = (voltage - 1)*0.094
        return(pressure)

def IonGaugePressure(d, AIN):
    voltage = (GaugeVoltage(d, AIN))
    if voltage <= 1:
        return('Ion Gauge Off')
    else:
        power = -1 * math.floor(voltage)
        mantissa = 1 - (voltage - math.floor(voltage))
        pressure = (mantissa * 10) * 10**(power)
        return(pressure)
