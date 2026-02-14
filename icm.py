# Required Libraries
# https://github.com/pimoroni/icm20948-python
import icm20948
import math

# Initialize icm object
imu = icm20948.ICM20948()
imu.set_accelerometer_sample_rate()
imu.set_gyro_sample_rate()

# Read magnetometer calibration data into dict
mag_calibration = []
with open('mag_calibration.csv', 'r') as file:
    for line in file:
        mag_calibration.append(line.strip().split(','))
mag_calibration = dict(zip(mag_calibration[0],(float(x) for x in mag_calibration[1])))


# Calibration Functions:

def mag_calibrate():
    '''Update magnetometer calibration from mag_calibration.csv'''
    global mag_calibration
    mag_calibration = []
    with open('mag_calibration.csv', 'r') as file:
        for line in file:
            mag_calibration.append(line.strip().split(','))
    mag_calibration = dict(zip(mag_calibration[0],(float(x) for x in mag_calibration[1])))


# Functions for Reading Data:

def mag_uncal():
    '''Return uncalibrated magnetometer data'''
    return list(imu.read_magnetometer_data())

def mag(calibration_dict=mag_calibration):
    '''Return magnetometer data calibrated with mag_calibration.csv data'''
    x, y, z = imu.read_magnetometer_data()
    return [(x+calibration_dict['xoffset'])/calibration_dict['xscale'], \
            (y+calibration_dict['yoffset'])/calibration_dict['yoffset'], \
            (z+calibration_dict['zoffset'])/calibration_dict['zoffset']]

def accel():
    '''Returns acceleration scalars X, Y, Z'''
    return list(imu.read_accelerometer_gyro_data()[:3])

def gyro():
    '''Returns gyroscope scalars X, Y, Z'''
    return list(imu.read_accelerometer_gyro_data()[3:])

def temp(Fahrenheit=True):
    '''Returns temperature. Fahrenheit=False for C.'''
    if Fahrenheit:
        return (imu.read_temperature() * 9/5) + 32
    else:
        return imu.read_temperature

def total_accel():
    '''Returns total acceleration scalar'''
    return math.sqrt(sum(number ** 2 for number in accel()))

def read():
    '''Returns scalars X, Y, Z for accel, gyro, temp in F.'''
    return accel(), gyro(), temp()

def full_read():
    '''Returns scalars X, Y, Z for accel, gyro, mag, temp in F.'''
    return accel(), gyro(), mag(), temp()
