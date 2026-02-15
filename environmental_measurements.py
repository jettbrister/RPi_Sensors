import time
import sgp
import bme

print('Warming Up SGP30...')
time.sleep(16)

while True:
	try:
		temp_c, pressure, humidity = bme.read(F=False)
		sgp.set_rh(humidity, temp_c)
		eco2, tvoc = sgp.read()
		print(temp_c, pressure, humidity, eco2, tvoc)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
