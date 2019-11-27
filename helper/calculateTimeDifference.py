def time_difference_minutes(time2,time1):
    duration = time2 - time1
    duration_s = duration.total_seconds()
    duration_minutes = divmod(duration_s, 60)[0]
    duration_minutes = int(duration_minutes)
    return duration_minutes


def is_overlapped(r1, r2):

    r1_start_notzinfo=r1.start.replace(tzinfo=None)
    r1_end_notzinfo = r1.end.replace(tzinfo=None)

    r2_start_notzinfo = r2.start.replace(tzinfo=None)
    r2_end_notzinfo = r2.end.replace(tzinfo=None)

    if max(r1_start_notzinfo, r2_start_notzinfo) < min(r1_end_notzinfo, r2_end_notzinfo):
        return True
    else:
        return False

