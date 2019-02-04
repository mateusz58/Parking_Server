from datetime import datetime

from django.db.models import Q, Sum

from users.models import CustomUser

from django.db import connection

from pages.models import Parking, Booking, CustomUser
from django.utils import timezone
import re

print("BEFORE Parking.objects.get(pk=1).free_places:"+str(Parking.objects.get(pk=1).free_places))


for x in range(Parking.objects.count()):
    _b1 = Booking.objects
    _b1 = _b1.filter(Q(Date_From__lt=datetime.now()) & Q(Date_To__gt=datetime.now()) & Q(parking=x+1) & (
        Q(status='ACTIVE') | Q(status='RESERVED')))
    _b1 = (_b1.all().aggregate(Sum('number_of_cars')))
    _b1 = re.sub("\D", "", str(_b1))
    _b1 = int(_b1)
    parking_free_places = Parking.objects.get(pk=x+1).number_of_places - _b1
    Parking.objects.filter(pk=x+1).update(free_places=parking_free_places)

print("AFTER Parking.objects.get(pk=1).free_places:"+str(Parking.objects.get(pk=1).free_places))

