import time
from utils import bme
import numpy as np

from datetime import datetime
import csv

LOG_FILE = 'logfiles/bme.csv'

HEADER = ['timestamp','temp_c','pressure','raw_pres','humidity','raw_humidity']

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(HEADER)

next_t = time.monotonic()

temp_c, pressure, humidity = bme.read(F=False)
raw_pressure = bme.raw_pressure()
raw_humidity = bme.raw_humidity()
data = [0,temp_c,pressure,raw_pressure,humidity,raw_humidity]
data_array = data

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		raw_pressure = bme.raw_pressure()
		raw_humidity = bme.raw_pressure()
		data = [0,temp_c,pressure,raw_pressure,humidity,raw_humidity]
		data_array = np.vstack([data_array, data])
		if datetime.now().second in [0,30]:
			avg_vals = list(np.mean(data_array, axis=0))
			avg_vals[0] = datetime.now()
			with open(LOG_FILE, 'a') as file:
				writer = csv.writer(file)
				writer.writerow(avg_vals)
			data_array = np.array(data)
			current_min = datetime.now().minute
		next_t += 1
		time.sleep(max(0, next_t - time.monotonic()))
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
