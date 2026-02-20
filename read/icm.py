import time
from utils import icm
t = time.perf_counter()
while True:
	try:
		accel, gyro, mag, temp = icm.read()
		print(accel,gyro,mag)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
