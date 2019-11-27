from datetime import datetime

from django.db.models import Q

from helper.String_processing import check_query_string
from pages.models import Car, Parking


def free_places_update(parking):
    _b1 = Car.objects
    _b1 = _b1.filter(Q(Date_From__lt=datetime.now()) & Q(Date_To__gt=datetime.now()) & Q(
        booking__parking=parking) & (
                             Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))

    free_places = Parking.objects.get(pk=parking).number_of_places - check_query_string(_b1)
    print("Booking_View free_places:" + str(free_places))
    Parking.objects.filter(pk=parking).update(free_places=free_places)
