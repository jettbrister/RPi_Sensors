import pandas as pd
import time
from datetime import datetime
while True:
	try:
		if datetime.now().second == 15 or datetime.now().second == 45:
			data = pd.read_csv('environmental_log.csv')
			print(data.tail(1).to_string(index=False, header=False))
			time.sleep(1)
		else:
			time.sleep(1)
	except KeyboardInterrupt:
		print('Program stopped')
		break
	except Exception as e:
		print('An unexpected error occurred:', str(e))
		break
