from datetime import datetime

import re

from background_task import background
from django.db.models import Q, Sum

from pages.models import Booking, Parking, Car

import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

from os.path import expanduser, join, dirname, abspath

home = expanduser("~")
curdir = dirname(abspath(__file__))
filepath = join(curdir, 'filename.txt')


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def update_parking():
    for x in Parking.objects.raw('SELECT pages_parking.id FROM pages_parking'):
        try:
            _b1 = Car.objects
            _b1 = _b1.filter(Q(Date_From__lt=datetime.now())
                             & Q(Date_To__gt=datetime.now()) & Q(booking__parking=x.id
                                                                 ) & (Q(status='ACTIVE')
                                                                      | Q(status='RESERVED') | Q(
                        status='RESERVED_L'
                    )))
            if not hasNumbers(str(_b1)): continue
            _b1 = _b1.count()
            _b1 = re.sub("\D", '', str(_b1))
            _b1 = int(_b1)
            parking_free_places = Parking.objects.get(pk=x.id).number_of_places - _b1
            print("UPDATE PARKING:UPDATED FREE PLACES FROM" + str(
                Parking.objects.get(pk=x.id).number_of_places) + "To:" + str(parking_free_places))
            if (parking_free_places < 0):
                Parking.objects.filter(pk=x.id).update(free_places=0)
            else:
                Parking.objects.filter(pk=x.id).update(free_places=parking_free_places)
        except Exception as e:
            print("Exception get_max_num:" + str(e))
            continue


def update_booking():
    for x in Car.objects.raw('SELECT * FROM pages_car'):

        try:
            duration_date_to = datetime.now() - x.Date_To.replace(tzinfo=None)
            duration_date_to_in_s = duration_date_to.total_seconds()
            minutes_date_to = divmod(duration_date_to_in_s, 60)[0]
            minutes_date_to = int(minutes_date_to)
            duration_date_from = datetime.now() - x.Date_From.replace(tzinfo=None)
            duration_date_from_in_s = duration_date_from.total_seconds()
            minutes_date_from = divmod(duration_date_from_in_s, 60)[0]
            minutes_date_from = int(minutes_date_from)
            if minutes_date_from > 15 and Car.objects.get(id=x.id).status == 'ACTIVE':
                x.status = "CANCELLED"
                x.Cost = 0

                x.save()
                print("Car ID:" + str(x.id) + "CHANGED STATUS FROM ACTIVE TO CANCELLED AT" + str(datetime.now()))
            if minutes_date_to > 15:
                if Car.objects.get(id=x.id).status == 'RESERVED':
                    x.status = 'RESERVED_L'
                    x.clean()
                    x.save()
                    print("Car ID:" + str(x.id) + "CHANGED STATUS FROM RSERVED TO RESERVED_L AT:" + str(datetime.now()))
                    x.refresh_from_db()
                if Car.objects.get(id=x.id).status == 'RESERVED_L':
                    x.save()
                    print("Car ID:" + str(x.id) + "WITH STATUS RESERVED_L CHANGED DATE TO:" + str(datetime.now()))
                    x.refresh_from_db()
                if Car.objects.get(id=x.id).status == 'EXPIRED_E':
                    x.save()
                    x.refresh_from_db()
                    print("Car ID:" + str(x.id) + " WITH STATE EXPIRED_E CHANGED DATE TO:" + str(datetime.now()))
        except Exception as e:
            print("Exception get_max_num:" + str(e))
            continue


@background(schedule=1)
def main_updater():
    update_parking()
    update_booking()


main_updater(repeat=5, repeat_until=None)
