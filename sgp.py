# Required Libraries
import time
# Uses ADD PACKAGE NAME
from sgp30 import SGP30

# Initialize sensor
sgp30 = SGP30(bus=1)

# Functions for reading data:

def eCO2():
	'''Returns eCO2 in ppm'''
	return sgp30.eCO2

def tVOC():
	'''Returns total VOC in ppb'''
	return sgp30.TVOC

def read():
	'''Returns eCO2 (ppm), tVOC (ppb)'''
	return eCO2(), tVOC()

def raw_values():
	'''Returns [Raw H2 Signal, Raw Ethanol Signal].'''
	return [sgp30.H2, sgp30.Ethanol]

def baseline():
	'''Returns current baseline [eCO2, tVOC].'''
	return [sgp30.baseline_eCO2, sgp30.baseline_TVOC]

# Functions for setting values:

def set_baseline(eCO2_baseline, tVOC_baseline):
	'''Sets baseline values for IAQ profile. pass (eCO2 baseline, tVOC baseline).'''
	sgp30.set_iaq_baseline(eCO2_baseline, tVOC_baseline)

def set_rh(humidity, temp_C):
	'''Sets relative humidity for IAQ profile. Pass (humidity, temp C)'''
	sgp30.set_iaq_relative_humidity(temp_C, humidity)
