#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

import time

import re
from django.db.models import Q, Sum

from pages.models import Booking, Parking, Car


import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

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
        print("UPDATE PARKING:UPDATED FREE PLACES FROM"+str(Parking.objects.get(pk=x.id).number_of_places)+"To:"+str(parking_free_places))
        if(parking_free_places<0):
            Parking.objects.filter(pk=x.id).update(free_places=0)
        else:
            Parking.objects.filter(pk=x.id).update(free_places=parking_free_places)


def update_booking():
    print("UPDATE BOOKING" + str(datetime.now()))
    for x in Car.objects.raw('SELECT * FROM pages_car'):

        duration_date_to = datetime.now() - x.Date_To.replace(tzinfo=None)
        duration_date_to_in_s = duration_date_to.total_seconds()
        minutes_date_to = divmod(duration_date_to_in_s, 60)[0]
        minutes_date_to = int(minutes_date_to)  ## difference between current time and date_to
        duration_date_from = datetime.now() - x.Date_From.replace(tzinfo=None)
        duration_date_from_in_s = duration_date_from.total_seconds()
        minutes_date_from = divmod(duration_date_from_in_s, 60)[0]
        minutes_date_from = int(minutes_date_from)
        if minutes_date_from > 15 and Car.objects.get(pk=x.id).status == 'ACTIVE':
            x.status = "CANCELLED"
            x.clean()
            x.save()
            print("Car ID:" + str(x.id) + "CHANGED STATUS FROM ACTIVE TO CANCELLED AT" + str(datetime.now()))
        if minutes_date_to > 15:
                if Car.objects.get(pk=x.id).status == 'RESERVED':
                    x.status = 'RESERVED_L'
                    x.clean()
                    x.save()
                    print("Car ID:" + str(x.id) + "CHANGED STATUS FROM RSERVED TO RESERVED_L AT:" + str(datetime.now()))
                    x.refresh_from_db()
                if Car.objects.get(pk=x.id).status == 'RESERVED_L':
                        x.clean()
                        x.save()
                        print("Car ID:" + str(x.id) + "WITH STATUS RESERVED_L CHANGED DATE TO:" + str(datetime.now()))
                        x.refresh_from_db()
                if Car.objects.get(pk=x.id).status == 'EXPIRED_E':
                                x.clean()
                                x.save()
                                x.refresh_from_db()
                                print("Car ID:" + str(x.id) + " WITH STATE EXPIRED_E CHANGED DATE TO:" + str(datetime.now()))

    # print("Booking ID :" + str(x.code))

     ## difference between current time and date_from
            # print("minutes_date_from  :" + str(minutes_date_from))
            # print("minutes_date_to  :" + str(minutes_date_to))



                    # duration = x.Date_To - x.Date_From
                    # duration_in_s = duration.total_seconds()
                    # hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                    # minutes = divmod(duration_in_s, 60)[0]
                    # HOURS = float('{0:.2f}'.format(hours + minutes / 60
                    #                                - hours))
                    # Cost = Booking.objects.filter(pk=x.booking.code
                    #                                  ).parking.HOUR_COST * HOURS \
                    #        * Booking.objects.filter(pk=x.booking
                    #                                    ).parking.number_of_cars
                    # Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                    # print("Booking ID:" + str( x.booking) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))

                    # time1 = Car.objects.get(pk=x.id).Date_From.replace(tzinfo=None)
                    # time2 = Car.objects.get(pk=x.id).Date_To.replace(tzinfo=None)
                    # duration = time2 - time1
                    # duration_in_s = duration.total_seconds()
                    # hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                    # minutes = divmod(duration_in_s, 60)[0]
                    # # HOURS = float('{0:.2f}'.format(hours + minutes / 60
                    # #                                - hours))
                    # # Cost = Booking.objects.filter(pk=x.booking
                    # #                               ).parking.HOUR_COST * HOURS \
                    # #        * Booking.objects.filter(pk=x.booking
                    # #                                 ).parking.number_of_cars
                    # Car.objects.filter(pk=x.code).refresh_from_db()
                    # Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                    # print("Booking ID:" + str(x.code) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(
                    #     Cost) + "AT:" + datetime.now())


                    # print("Booking ID:" + str(x.code) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))

                    # time1 = Car.objects.get(pk=x.id).Date_From.replace(tzinfo=None)
                    # time2 = Car.objects.get(pk=x.id).Date_To.replace(tzinfo=None)
                    # duration = time2 - time1
                    # duration_in_s = duration.total_seconds()
                    # hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                    # minutes = divmod(duration_in_s, 60)[0]
                    # HOURS = float('{0:.2f}'.format(hours + minutes / 60 - hours))
                    # Cost = Booking.objects.filter(pk=x.booking).parking.HOUR_COST * HOURS * Booking.objects.filter(pk=x.booking).parking.number_of_cars
                    # Booking.objects.filter(pk=x.booking).update(Cost=Cost)
                    # print("Booking ID:" + str(x.booking) + "CHANGED COST FROM:" + str(x.Cost) + "To:" + str(Cost) + "AT:" + str(datetime.now()))

def main():
    while True:
        print("LOOP2")
        update_parking()
        update_booking()
        time.sleep(5)


main()



