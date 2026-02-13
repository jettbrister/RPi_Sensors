import time, bme

while True:
	try:
		temp, pressure, humidity = bme.read()
		print(temp, pressure, humidity)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
