import time
from utils import sgp, bme

print('Warming Up SGP30')
time.sleep(16)

next_t = time.monotonic()

BASELINE_INTERVAL = (60*60) * 12  # hours

while True:
	temp_c, pressure, humidity = bme.read(F=False)
	sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
	eco2, tvoc = sgp.read()
	if tvoc > 0:
		time.sleep(max(0, next_t - time.monotonic()))
		break
	time.sleep(max(0, next_t - time.monotonic()))

last_baseline = time.time()
sgp.load_baseline()

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.sgp30.set_iaq_relative_humidity(temp_c,humidity)
		eco2, tvoc = sgp.read()
		raw_H2, raw_Eth = sgp.raw_values()
		baseline_eco2, baseline_tvoc = sgp.read_baseline()
		if time.time() - last_baseline > BASELINE_INTERVAL:
			sgp.save_baseline()
			last_baseline = time.time()
		next_t += 1
		time.sleep(max(0, next_t - time.monotonic()))

		print(eco2, tvoc)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
