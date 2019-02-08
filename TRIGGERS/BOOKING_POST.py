from django.core.exceptions import ValidationError
from django.db.migrations import serializer
from django.db.models import Q

from Basic_Functions.String_processing import is_all_items_unique, check_query_string
from Basic_Functions.Time_convert import convert_string_date_time

from datetime import datetime

from pages.models import Car, Parking, Booking
from users.models import CustomUser


def get_Cost_Custom(self):
    print("TRIGGER BOOKING COST")
    time1 = self.Date_From
    time2 = self.Date_To
    duration = time2 - time1
    duration_in_s = duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
    minutes = divmod(duration_in_s, 60)[0]
    HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
    Cost = self.booking.parking.HOUR_COST * HOURS
    Cost = round(Cost, 2)
    return Cost


def trigger_booking_post(self):


    
    # raise ValidationError("HEADER TEST")
    ## CREATED BOOKING OBJECT
    ##HEADER TEST
    # print(headers["domain"])
    user_id = CustomUser.objects.get(email=str(self.request.user)).id
    Booking.objects.filter(pk=self.booking.code).update(number_of_cars=self.booking.number_of_cars+1)
    Booking.objects.filter(pk=self.booking.code).update(Cost=get_Cost_Custom(self)+self.booking.Cost)


