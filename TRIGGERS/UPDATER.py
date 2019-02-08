#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

import time

import re
from django.db.models import Q, Sum

from pages.models import Booking, Parking, Car

#
# import warnings
#
# warnings.filterwarnings("ignore", category=RuntimeWarning)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def update_parking():
    print("UPDATE PARKING"+str(datetime.now()))
    for x in Parking.objects.raw('SELECT pages_parking.id FROM pages_parking'):
        _b1 = Car.objects
        _b1 = _b1.filter(Q(Date_From__lt=datetime.now())
                         & Q(Date_To__gt=datetime.now()) & Q(booking__parking=x.id
                                                                     ) & (Q(status='ACTIVE')
                                                                             | Q(status='RESERVED') | Q(
            status='RESERVED_L'
            )))
        if not hasNumbers(str(_b1)): continue
        _b1 = _b1.all().aggregate(Sum('booking__number_of_cars'))
        _b1 = re.sub("\D", '', str(_b1))
        _b1 = int(_b1)
        parking_free_places = Parking.objects.get(pk=x.id).number_of_places - _b1
        Parking.objects.filter(pk=x.id).update(free_places=parking_free_places)
        print("UPDATE PARKING:"+Parking.objects.get(pk=x.id).parking_name +"UPDATED FREE PLACES FROM:"+Parking.objects.get(pk=x.id).free_places+"TO:"+Parking.objects.get(pk=x.id).free_places++"AT"+ str(datetime.now()))


def update_booking():
    print("UPDATE BOOKING" + str(datetime.now()))

    for x in Car.objects.raw('SELECT pages_car.id FROM pages_car'):
        # print("Booking ID :" + str(x.code))
        duration_date_to = datetime.now() - Car.objects.get(pk=x.id).Date_To.replace(tzinfo=None)
        duration_date_to_in_s = duration_date_to.total_seconds()
        minutes_date_to = divmod(duration_date_to_in_s, 60)[0]
        minutes_date_to = int(minutes_date_to)## difference between current time and date_to

        duration_date_from = datetime.now() - Car.objects.get(pk=x.id).Date_From.replace(tzinfo=None)
        duration_date_from_in_s = duration_date_from.total_seconds()
        minutes_date_from = divmod(duration_date_from_in_s, 60)[0]
        minutes_date_from = int(minutes_date_from) ## difference between current time and date_from
        # print("minutes_date_from  :" + str(minutes_date_from))
        # print("minutes_date_to  :" + str(minutes_date_to))
        if minutes_date_from > 15:
            if Car.objects.get(pk=x.id).status == 'ACTIVE':
                Car.objects.filter(pk=x.id
                                          ).update(status='CANCELLED')
                print("Car ID:"+str(x.id)+"CHANGED STATUS FROM ACTIVE TO CANCELLED AT"+datetime.now())
        if minutes_date_to > 15:

            if Car.objects.get(pk=x.id).status == 'RESERVED':
                Car.objects.filter(pk=x.code.update(status='RESERVED_L'))
                Car.objects.filter(pk=x.code).update(Date_To=datetime.now())
                print("Car ID:" + str(x.code) + "CHANGED STATUS FROM RSERVED TO RESERVED_L AT:" + datetime.now())
                Car.objects.filter(pk=x.code).refresh_from_db()
                time1 = Car.objects.get(pk=x.code).Date_From.replace(tzinfo=None)
                time2 = Car.objects.get(pk=x.code).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60
                                               - hours))
                Cost = Booking.objects.filter(pk=x.booking.code
                                                 ).parking.HOUR_COST * HOURS \
                       * Booking.objects.filter(pk=x.booking
                                                   ).parking.number_of_cars
                Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                # print("Booking ID:" + str( x.booking) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))
            if Car.objects.get(pk=x.id).status == 'RESERVED_L':
                Car.objects.filter(pk=x.id
                                       ).update(Date_To=datetime.now())
                Car.objects.filter(pk=x.id).refresh_from_db()
                time1 = Car.objects.get(pk=x.id).Date_From.replace(tzinfo=None)
                time2 = Car.objects.get(pk=x.id).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60
                                               - hours))
                Cost = Booking.objects.filter(pk=x.booking
                                              ).parking.HOUR_COST * HOURS \
                       * Booking.objects.filter(pk=x.booking
                                                ).parking.number_of_cars
                Car.objects.filter(pk=x.code).refresh_from_db()
                Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                # print("Booking ID:" + str(x.code) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(
                #     Cost) + "AT:" + datetime.now())
            if Car.objects.get(pk=x.id).status == 'RESERVED_L':
                Car.objects.filter(pk=x.id).update(Date_To=datetime.now())
                Car.objects.filter(pk=x.id).refresh_from_db()
                time1 = Car.objects.get(pk=x.id).Date_From.replace(tzinfo=None)
                time2 = Car.objects.get(pk=x.id).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60 - hours))
                Cost = Booking.objects.filter(pk=x.booking).parking.HOUR_COST * HOURS * Booking.objects.filter(pk=x.booking).parking.number_of_cars
                Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                # print("Booking ID:" + str(x.code) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))
            if Booking.objects.get(pk=x.code).status == 'EXPIRED_E':
                Car.objects.filter(pk=x.code).update(Date_To=datetime.now())
                Car.objects.filter(pk=x.code).refresh_from_db()
                time1 = Car.objects.get(pk=x.code).Date_From.replace(tzinfo=None)
                time2 = Car.objects.get(pk=x.code).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60 - hours))
                Cost = Booking.objects.filter(pk=x.booking).parking.HOUR_COST * HOURS * Booking.objects.filter(pk=x.booking).parking.number_of_cars
                Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                # print("Booking ID:" + str(x.booking) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))

while True:
    update_parking()
    update_booking()
    time.sleep(60)



