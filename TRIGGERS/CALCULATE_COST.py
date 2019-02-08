from django.db.models import Sum, Q

from Basic_Functions.Time_difference import time_difference_minutes
from pages.models import Booking, Car
from datetime import datetime
#

def calculate(self):
    time=time_difference_minutes(self.Date_To, self.Date_From)
    time=time/60
    Cost=self.booking.parking.HOUR_COST*time
    Cost=round(Cost, 2)
    return Cost

def calculate_cost(query):
    sum=0
    for record in query:
        sum=sum+calculate(record)


def calculate_count(Booking_object):

    query=Car.objects.filter(booking=Booking_object.code)
    count=0
    for record in query:
        if record.status=='ACTIVE':
            count=count+1
        if record.status=='RESERVED_L':
            count = count + 1
        if record.status=='RESERVED_L':
            count=count+1

    return count


def Booking_calculate_cost(Car_object):
    query = Car.objects.filter(booking=Car_object.code)
    count = 0
    for record in query:
        if record.status == 'ACTIVE':
            count = count + 1
        if record.status == 'RESERVED_L':
            count = count + 1
        if record.status == 'RESERVED_L':
            count = count + 1

    return count


