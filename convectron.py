import numpy as np
import math

import u6

def ConvectronVoltage(d, AIN):
    ConVoltage = d.getAIN(AIN)
    return(ConVoltage)

def ConvectronBits(d, AIN):
    ConBits = d.getFeedback(d, u6.AIN(AIN))
    return(ConBits)

def ConvectronPressure(d, AIN):
    voltagepower = (ConvectronVoltage(d, AIN)  - 4)+0.021
    pressure = 10**voltagepower
    return(pressure)
