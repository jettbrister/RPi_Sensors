import time
from utils import icm
import numpy as np

from datetime import datetime
import csv
LOG_FILE = 'logfiles/icm.csv'

HEADER = ['timestamp','temp_c','pressure','raw_pres','humidity','raw_humidity']

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(HEADER)

t = time.perf_counter()

while True:
	try:
		dt = time.perf_counter() - t
		t = time.perf_counter()
		accel, gyro, mag, temp, total_accel = icm.full_read()
		data = [dt, accel, gyro, mag, temp, total_accel]
		with open(LOG_FILE, 'a') as file:
			writer = csv.writer(file)
			writer.writerow(data)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
