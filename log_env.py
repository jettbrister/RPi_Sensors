import time
from utils import sgp, bme
import numpy as np

from datetime import datetime
import csv

print('Warming Up SGP30...')
time.sleep(16)

LOG_FILE = 'environmental_log.csv'
BASELINE_INTERVAL = (60*60) * 12  # hours

HEADER = ['timestamp','temp_c','pressure','humidity','eco2','tvoc','raw_H2','raw_Eth','baseline_eco2','baseline_tvoc']

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(HEADER)

next_t = time.monotonic()

while True:
	temp_c, pressure, humidity = bme.read(F=False)
	sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
	eco2, tvoc = sgp.read()
	if tvoc > 0:
		time.sleep(max(0, next_t - time.monotonic()))
		break
	time.sleep(max(0, next_t - time.monotonic()))

if sgp.load_baseline():
	print('Baseline Loaded')
else:
	print('No Baseline Found')
last_baseline = time.time()


current_min = datetime.now().minute

temp_c, pressure, humidity = bme.read(F=False)
sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
eco2, tvoc = sgp.read()
raw_H2, raw_Eth = sgp.raw_values()
baseline_eco2, baseline_tvoc = sgp.read_baseline()
data = [0,temp_c,pressure,humidity,eco2,tvoc,raw_H2,raw_Eth,baseline_eco2,baseline_tvoc]
data_array = np.array(data)

next_t = time.monotonic()
time.sleep(max(0, next_t - time.monotonic()))


while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
		eco2, tvoc = sgp.read()
		raw_H2, raw_Eth = sgp.raw_values()
		baseline_eco2, baseline_tvoc = sgp.read_baseline()
		data = [0,temp_c,pressure,humidity,eco2,tvoc,raw_H2,raw_Eth,baseline_eco2,baseline_tvoc]
		data_array = np.vstack([data_array, data])
		if datetime.now().minute != current_min:
			avg_vals = list(np.mean(data_array, axis=0))
			avg_vals[0] = datetime.now()
			with open(LOG_FILE, 'a') as file:
				writer = csv.writer(file)
				writer.writerow(avg_vals)
			data_array = np.array(data)
			current_min = datetime.now().minute
#			print('Data Point Logged')
		print(f"{temp_c:.2f}", f"{pressure:.2f}", f"{humidity:.2f}", eco2, tvoc, raw_H2, raw_Eth, baseline_eco2, baseline_tvoc)
		if time.time() - last_baseline > BASELINE_INTERVAL:
			sgp.save_baseline()
			last_baseline = time.time()
		next_t += 1
		time.sleep(max(0, next_t - time.monotonic()))
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
