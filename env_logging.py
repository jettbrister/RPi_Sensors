import time
import sgp
import bme

from datetime import datetime
import csv

print('Warming Up SGP30...')
time.sleep(16)

sgp.sgp30.iaq_init()

LOG_FILE = 'environmental_log.csv'
BASELINE_INTERVAL = 6 * 60 * 60  # 6 hours

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['timestamp','temp_c','pressure','humidity','eco2','tvoc'])

if sgp.load_baseline():
	print('Baseline Loaded')
else:
	print('No Baseline Found')
last_baseline = time.time()

next_t = time.monotonic()

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.set_rh(humidity, temp_c)
		eco2, tvoc = sgp.read()
		with open(LOG_FILE, 'a') as file:
			writer = csv.writer(file)
			writer.writerow([datetime.today(), temp_c, pressure, humidity, eco2, tvoc])
		print(datetime.today(), temp_c, pressure, humidity, eco2, tvoc)
		if time.time() - last_baseline > BASELINE_INTERVAL:
			sgp.save_baseline()
			last_baseline = time.time()
		next_t += 1
		time.sleep(max(0, next_t - time.monotonic()))
	except KeyboardInterrupt:
		print('Program stopped')
		sgp.save_baseline()
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
