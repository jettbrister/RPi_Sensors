# Required Libraries
import time
# Uses RPI.bme280 package https://github.com/rm-hull/bme280
import bme280

# Load calibration parameters to use for pulling samples
calibration_params = bme280.load_calibration_params()

# Functions for reading data:

def temp():
    '''Returns temperature in F.'''
    return (bme280.sample(calibration_params).temperature * 9/5) + 32

def temp_c():
    '''Returns temperature in C.'''
    return bme280.sample(calibration_params).temperature

def pressure():
    '''Returns pressure. Units: hPa.'''
    return bme280.sample(calibration_params).pressure

def humidity():
    '''Returns RH in %.'''
    return bme280.sample(calibration_params).humidity

def read(F=True):
    '''Returns temp (F), pressure (hPa), humidity (%)'''
    if F:
        return temp(), pressure(), humidity()
    else:
        return temp_c(), pressure(), humidity()

