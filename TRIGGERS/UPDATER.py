#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

import time

import re
from django.db.models import Q, Sum

from pages.models import Booking, Parking



import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)




def update_parking():
    for x in Parking.objects.raw('SELECT pages_parking.id FROM pages_parking'):
        _b1 = Booking.objects
        _b1 = _b1.filter(Q(Date_From__lt=datetime.now())
                         & Q(Date_To__gt=datetime.now()) & Q(parking=x.id
                                                                     ) & (Q(status='ACTIVE')
                                                                             | Q(status='RESERVED') | Q(
            status='RESERVED_L'
            )))
        _b1 = _b1.all().aggregate(Sum('number_of_cars'))
        _b1 = re.sub("\D", '', str(_b1))
        _b1 = int(_b1)
        parking_free_places = Parking.objects.get(pk=x.id).number_of_places - _b1
        Parking.objects.filter(pk=x.id).update(free_places=parking_free_places)



def update_booking():
    for x in Booking.objects.raw('SELECT pages_booking.code FROM pages_booking'):
        duration_date_to = Booking.objects.get(pk=x.code).Date_To.replace(tzinfo=None) - datetime.now()
        duration_date_to_in_s = duration_date_to.total_seconds()
        minutes_date_to = divmod(duration_date_to_in_s, 60)[0]
        minutes_date_to = int(minutes_date_to)
        duration_date_from = Booking.objects.get(pk=x.code).Date_From.replace(tzinfo=None) \
                             - datetime.now()  # For build-in functions
        duration_date_from_in_s = duration_date_from.total_seconds()
        minutes_date_from = divmod(duration_date_from_in_s, 60)[0]
        minutes_date_from = int(minutes_date_from)
        if minutes_date_from > 15:
            if Booking.objects.get(pk=x.code).status == 'ACTIVE':
                Booking.objects.filter(pk=x.code
                                          ).update(status='CANCELLED')
        if minutes_date_to > 15:

            if Booking.objects.get(pk=x.code).status == 'RESERVED':
                Booking.objects.filter(pk=x.code
                                          ).update(status='RESERVED_L')
                Booking.objects.filter(pk=x.code
                                          ).update(Date_To=datetime.now())
                Booking.objects.filter(pk=x.code).refresh_from_db()
                time1 = Booking.objects.get(pk=x.code).Date_From.replace(tzinfo=None)
                time2 = Booking.objects.get(pk=x.code).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60
                                               - hours))
                Cost = Booking.objects.filter(pk=x.code
                                                 ).parking.HOUR_COST * HOURS \
                       * Booking.objects.filter(pk=x.code
                                                   ).parking.number_of_cars
                Booking.objects.filter(pk=x.code).update(Cost=Cost)
            if Booking.objects.get(pk=x.code).status == 'RESERVED_L':
                Booking.objects.filter(pk=x.code
                                          ).update(Date_To=datetime.now())
                Booking.objects.filter(pk=x.code).refresh_from_db()
                time1 = Booking.objects.get(pk=x.code).Date_From.replace(tzinfo=None)
                time2 = Booking.objects.get(pk=x.code).Date_To.replace(tzinfo=None)
                duration = time2 - time1
                duration_in_s = duration.total_seconds()
                hours = divmod(duration_in_s, 3600)[0]  # # HOURS DURATION
                minutes = divmod(duration_in_s, 60)[0]
                HOURS = float('{0:.2f}'.format(hours + minutes / 60
                                               - hours))
                Cost = Booking.objects.filter(pk=x.code
                                                 ).parking.HOUR_COST * HOURS \
                       * Booking.objects.filter(pk=x.code
                                                   ).parking.number_of_cars
                Booking.objects.filter(pk=x.code).update(Cost=Cost)





update_parking()
update_booking()

