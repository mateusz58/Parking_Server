from datetime import datetime

from django.db.models import Q, Sum

from users.models import CustomUser

from django.db import connection

from pages.models import Parking, Booking, CustomUser
from django.utils import timezone
import re

## Wyswietlanie wszystkich

Booking.objects.all()

Parking.objects.all()

# queryset =  Booking.objects.all()


print("FILTERED FIELD NAME OF FOREIGN KEY")
# Booking.objects.get(user=1).code
print("FILTERED FIELD EXISTS")
# userfilter(name=group_name).exists()
#
# user.groups.filter(name=group_name).exists()

# CustomUser.objects.filter(email='o8922871@nwytg.net').exists()
print("ID")
CustomUser.objects.get(email='o8922871@nwytg.net').id


Booking.objects.all()

time1 = datetime(2019, 2, 28, 10, 0, 00)
time2 = datetime(2019, 2, 28, 16, 0, 00)

time3 = datetime(2018, 2, 28, 16, 0, 00)


parking1=1


# Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])

print("RAW QUERIES FULL")
for p in Booking.objects.raw('SELECT pages_booking.code,pages_booking.Date_From,pages_booking.Date_To,pages_booking.number_of_cars FROM pages_booking'):
    print(p.code)

print("RAW QUERIES FILTER")
for p in Booking.objects.raw('SELECT pages_booking.code,pages_booking.Date_From,pages_booking.Date_To,pages_booking.number_of_cars FROM pages_booking WHERE pages_booking.Date_From>%s ',[time1]):
    print(p.code)

print("RAW QUERIES SUM AGGREGATION")
for p in Booking.objects.raw('SELECT *,SUM (pages_booking.number_of_cars) AS sum FROM pages_booking WHERE pages_booking.Date_From>%s ',[time1]):
    print(p.sum)

print("RAW QUERIES SUM AGGREGATION")
for p in Booking.objects.raw('SELECT *,SUM (pages_booking.number_of_cars) AS sum FROM pages_booking WHERE pages_booking.Date_From>=%s AND pages_booking.Date_To<=%s ',[time1,time2]):
    print(p.sum),


print("ORM QUERIES SUM AGGREGATION")

# Q=Booking.objects.filter(Date_To__lte=time2).filter(Date_From__gte= time1).aggregate(
#     Sum('number_of_cars')).first()
#
#
# print(Q)

_q = Booking.objects
_q = _q.filter(Q(Date_From__gte=time1)&Q(Date_To__lte=time2)&Q(Date_To__lte=time2)&Q(parking=1)&(Q(status='ACTIVE')|Q(status='RESERVED')))
_q=(_q.all().aggregate(Sum('number_of_cars')))
_q=re.sub("\D", "", str(_q))

print(_q)

print("Date_time:"+str(datetime.now()))

print(datetime.now()<time1)

print(datetime.now()<time3)

print("ORM QUERIES SUM AGGREGATION ACTIVE AND RESERVED")
_b = Booking.objects
_b = _b.filter(Q(Date_From__lt=datetime.now()) & Q(Date_To__gt=datetime.now()) & Q(parking=1) & (Q(status='ACTIVE') | Q(status='RESERVED')))
_b = (_b.all().aggregate(Sum('number_of_cars')))
_b = re.sub("\D", "", str(_b))
_b=int(_b)

parking_free_places=Parking.objects.get(id=1).free_places-_b
Parking.objects.filter(pk=1).update(free_places=parking_free_places)



Parking.objects.filter(pk=1).update(free_places=98)



# _p = Parking.objects
# _p = _p.filter(Q(id=1))
# _p =_p.update(Q(free_places=_p_free_places-int(_b)))
# _p = re.sub("\D", "", str(_b))






print(_q)





print("ASSERT TEST")







# for p in Booking.objects.raw('SELECT * FROM pages_booking'):
#     SELECT
#     classes._id, students.studentname, classes.classname, classes.attend, classes.late, classes.dtime
#     FROM
#     students, classes
#     WHERE
#     students._id = classes.student


