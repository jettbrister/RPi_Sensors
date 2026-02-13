# Required Libraries
import time
# Uses RPI.bme280 package https://github.com/rm-hull/bme280
import bme280

# Load calibration parameters to use for pulling samples
calibration_params = bme280.load_calibration_params()

# Functions for reading data:

def temp():
    '''Returns temperature. Fahrenheit=False for C. Default 4x oversampling.'''
    return (bme280.sample(calibration_params).temperature * 9/5) + 32

def pressure():
    '''Returns pressure. Units: hPa. Default 4x oversampling.'''
    return bme280.sample(calibration_params).pressure

def humidity():
    '''Returns RH in %. Default 4x oversampling.'''
    return bme280.sample(calibration_params).humidity

def read():
    '''Returns temp (F), pressure (hPa), humidity (%)'''
    return temp(), pressure(), humidity()
