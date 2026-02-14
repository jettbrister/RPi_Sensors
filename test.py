import time
from sgp30 import SGP30

sgp30 = SGP30(bus=1)

print("Warming up sensor (15s)...")

#eco2_base = sgp30.baseline_eCO2
#tvoc_base = sgp30.baseline_TVOC

#print("Baseline:", eco2_base, tvoc_base)
#sgp30.set_iaq_baseline(eco2_base, tvoc_base)

for i in range(2000):
    eco2 = sgp30.eCO2

    print(f"{i:02d}s  eCO2: {eco2} ppm |")
    time.sleep(1)

