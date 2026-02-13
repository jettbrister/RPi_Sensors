import numpy as np
import imufusion, sys, time, icm

ahrs = imufusion.Ahrs()
ahrs.settings = imufusion.Settings(
	imufusion.CONVENTION_ENU,  # convention
	0.8,  # gain
	2000,  # gyroscope range
	10,  # acceleration rejection
	10,  # magnetic rejection
	100,  # recovery trigger period = 5 seconds
)
t = time.perf_counter()
while True:
	try:
		dt = time.perf_counter() - t
		t = time.perf_counter()
		accel, gyro, temp_f = icm.read()
		mag = icm.mag()
		gyro = imufusion.Offset(round(1/dt)).update(np.array(gyro))
		ahrs.update(gyro, np.array(accel), np.array(mag), dt)
		euler = ahrs.quaternion.to_euler()
		#button_state = button.state()
		print(euler)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
