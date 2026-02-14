import time
import sgp
import bme

warmup=0
while warmup<16:
	print('Warming Up')
	warmup+=1
	time.sleep(1)

while True:
	try:
		temp, pressure, humidity = bme.read()
		temp_c = bme.temp_c()
		eco2, tvoc = sgp.read()
		sgp.set_rh(humidity, temp_c)
		print(temp, pressure, humidity, eco2, tvoc)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
