import time
import sgp
import bme

from datetime import datetime
import csv

print('Warming Up SGP30...')
time.sleep(16)

LOG_FILE = 'environmental_log.csv'

with open(LOG_FILE, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['timestamp','temp_c','pressure','humidity','eco2','tvoc'])

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.set_rh(humidity, temp_c)
		eco2, tvoc = sgp.read()
		with open(LOG_FILE, 'a') as file:
			writer = csv.writer(file)
			writer.writerow([datetime.today(), temp_c, pressure, humidity, eco2, tvoc])
		print(datetime.today(), temp_c, pressure, humidity, eco2, tvoc)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
