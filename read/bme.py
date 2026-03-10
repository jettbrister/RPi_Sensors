import time
from utils import bme

while True:
	try:
		temp, pressure, humidity = bme.read(F=False)
		raw_humidity = bme.raw_humidity()
		raw_pressure = bme.raw_pressure()
		print(temp, pressure, raw_pressure, humidity, raw_humidity)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
