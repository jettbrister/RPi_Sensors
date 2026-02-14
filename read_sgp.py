import time
import sgp

warmup=0
while warmup<16:
	print('Warming Up')
	warmup+=1
	time.sleep(1)

while True:
	try:
		eco2 = sgp.eCO2()
		tvoc = sgp.tVOC()
		print(eco2, tvoc)
		time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
