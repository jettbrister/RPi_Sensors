import time
import sgp
import bme

from datetime import datetime
import csv

print('Warming Up SGP30...')
time.sleep(16)

LOG_FILE = 'environmental_log.csv'
BASELINE_INTERVAL = 6 * 60 * 60  # 6 hours

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['timestamp','temp_c','pressure','humidity','eco2','tvoc','raw_H2','raw_Eth','baseline_eco2','baseline_tvoc'])

next_t = time.monotonic()

while True:
    eco2, tvoc = sgp.read()
    if tvoc > 0:
        break
    time.sleep(max(0, next_t - time.monotonic()))

#if sgp.load_baseline():
#	print('Baseline Loaded')
#else:
#	print('No Baseline Found')
last_baseline = time.time()

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
		eco2, tvoc = sgp.read()
		raw_H2, raw_Eth = sgp.raw_values()
		baseline_eco2, baseline_tvoc = sgp.read_baseline()
		with open(LOG_FILE, 'a') as file:
			writer = csv.writer(file)
			writer.writerow([datetime.today(), temp_c, pressure, humidity, eco2, tvoc, raw_H2, raw_Eth, baseline_eco2, baseline_tvoc])
		print(f"{temp_c:.2f}", f"{pressure:.2f}", f"{humidity:.2f}", eco2, tvoc, raw_H2, raw_Eth, baseline_eco2, baseline_tvoc)
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
