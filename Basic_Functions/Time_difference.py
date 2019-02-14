





def time_difference_minutes(time2,time1):
    duration = time2 - time1
    duration_s = duration.total_seconds()
    duration_minutes = divmod(duration_s, 60)[0]
    duration_minutes = int(duration_minutes)  ## difference between current time and date_from
    return duration_minutes


from datetime import datetime
from collections import namedtuple

# Range = namedtuple('Range', ['start', 'end'])
# r1 = Range(start=datetime(2012, 1, 14,8,0,0).replace(tzinfo=None), end=datetime(2012, 5, 20,8,0,0).replace(tzinfo=None))
# r2 = Range(start=datetime(2012, 3, 16,8,0,0).replace(tzinfo=None), end=datetime(2012, 9, 17,8,0,0).replace(tzinfo=None))
#

def is_overlapped(r1, r2):
    if max(r1.start, r2.start) < min(r1.end, r2.end):
        return True
    else:
        return False


#
#
# def check_overlaps(r1,r2):
#     latest_start = max(r1.start, r2.start)
#     earliest_end = min(r1.end, r2.end)
#     delta = (earliest_end - latest_start)
#     overlap = max(0, delta).days
#     return overlap
#
#
#
#
#
# print(is_overlapped(r1, r2))

