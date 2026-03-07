import time
from utils import bme

while True:
	try:
		temp, pressure, humidity = bme.read(F=False)
		print(temp, pressure, humidity)
		time.sleep(10)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
