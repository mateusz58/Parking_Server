

from datetime import datetime
import time


time1 = datetime(2019, 2, 1, 12, 8, 15)
time2 = datetime.now()

duration = time2 - time1                         # For build-in functions
duration_in_s = duration.total_seconds()
hours = divmod(duration_in_s, 3600)[0]       ## HOURS DURATION
minutes = divmod(duration_in_s, 60)[0]        # MINUTE DURATION
 # waited a few minutes before pressing enter




print(hours)
print(minutes)
print(hours+((minutes/60)-hours))

g = float("{0:.2f}".format(hours+((minutes/60)-hours)))

print(g)



# divmod returns quotient and remainder