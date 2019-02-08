





def time_difference_minutes(time2,time1):
    duration = time2 - time1
    duration_s = duration.total_seconds()
    duration_minutes = divmod(duration_s, 60)[0]
    duration_minutes = int(duration_minutes)  ## difference between current time and date_from
    return duration_minutes



