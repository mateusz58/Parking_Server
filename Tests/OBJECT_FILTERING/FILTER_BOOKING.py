from datetime import datetime,tzinfo

from django.db.models import Q, Sum

from Basic_Functions.Time_difference import time_difference_minutes
from TRIGGERS.CALCULATE_COST import calculate_cost
from templatetags.templatetag import has_group
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.db import connection
#CHANGES
from pages.models import Parking, Booking, CustomUser, Car
from django.utils import timezone
import re

## Wyswietlanie wszystkich

# Booking.objects.all()
#
# Parking.objects.all()

# queryset =  Booking.objects.all()

#
# print("FILTERED FIELD NAME OF FOREIGN KEY")
# # Booking.objects.get(user=1).code
# print("FILTERED FIELD EXISTS")
# userfilter(name=group_name).exists()
#
# user.groups.filter(name=group_name).exists()

# CustomUser.objects.filter(email='o8922871@nwytg.net').exists()
# print("ID")
# CustomUser.objects.get(email='o8922871@nwytg.net').id


# Booking.objects.all()
#
# time1 = datetime(2019, 2, 28, 10, 0, 00)
# time2 = datetime(2019, 2, 28, 16, 0, 00)
#
# time3 = datetime(2018, 2, 28, 16, 0, 00)
#
#
# parking1=1


# Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])


### RAW QUERIES ##########################

# print("RAW QUERIES FULL")
# for p in Booking.objects.raw('SELECT pages_booking.code,pages_booking.Date_From,pages_booking.Date_To,pages_booking.number_of_cars FROM pages_booking'):
#     print(p.code)
#
# print("RAW QUERIES FILTER")
# for p in Booking.objects.raw('SELECT pages_booking.code,pages_booking.Date_From,pages_booking.Date_To,pages_booking.number_of_cars FROM pages_booking WHERE pages_booking.Date_From>%s ',[time1]):
#     print(p.code)
#
# print("RAW QUERIES SUM AGGREGATION")
# for p in Booking.objects.raw('SELECT *,SUM (pages_booking.number_of_cars) AS sum FROM pages_booking WHERE pages_booking.Date_From>%s ',[time1]):
#     print(p.sum)
#
# print("RAW QUERIES SUM AGGREGATION")
# for p in Booking.objects.raw('SELECT *,SUM (pages_booking.number_of_cars) AS sum FROM pages_booking WHERE pages_booking.Date_From>=%s AND pages_booking.Date_To<=%s ',[time1,time2]):
#     print(p.sum),
#
#
# print("ORM QUERIES SUM AGGREGATION")


### RAW QUERIES ##########################
# Q=Booking.objects.filter(Date_To__lte=time2).filter(Date_From__gte= time1).aggregate(
#     Sum('number_of_cars')).first()
#
#
# print(Q)


#
# print("Date_time:"+str(datetime.now()))
#
# print(datetime.now()<time1)
#
# print(datetime.now()<time3)


# print("BEFORE Parking.objects.get(pk=1).free_places:"+str(Parking.objects.get(pk=1).free_places))
#
# _b1 = Booking.objects
# _b1 = _b1.filter(Q(Date_From__lt=datetime.now()) & Q(Date_To__gt=datetime.now()) & Q(parking=1) & (
#     Q(status='ACTIVE') | Q(status='RESERVED')))
# _b1 = (_b1.all().aggregate(Sum('number_of_cars')))
# _b1 = re.sub("\D", "", str(_b1))
# _b1 = int(_b1)
# parking_free_places = Parking.objects.get(id=1).number_of_places - _b1
# Parking.objects.filter(pk=1).update(free_places=parking_free_places)
#
# print("AFTER Parking.objects.get(pk=1).free_places:"+str(Parking.objects.get(pk=1).free_places))


# for p in Parking.objects.raw('SELECT pages_parking.id FROM pages_parking'):
#     print(p.id)
#

# for x in Booking.objects.raw('SELECT pages_booking.code,pages_booking.Date_From FROM pages_booking'):
#     print("Booking ID :" + str(x.code))
#     duration_date_to = datetime.now() - Booking.objects.get(pk=x.code).Date_To.replace(tzinfo=None)
#     duration_date_to_in_s = duration_date_to.total_seconds()
#     minutes_date_to = divmod(duration_date_to_in_s, 60)[0]
#     minutes_date_to = int(minutes_date_to)
#     duration_date_from =datetime.now()- Booking.objects.get(pk=x.code).Date_From.replace(tzinfo=None)
#                            # For build-in functions
#     duration_date_from_in_s = duration_date_from.total_seconds()
#     minutes_date_from = divmod(duration_date_from_in_s, 60)[0]
#     minutes_date_from = int(minutes_date_from)
#     print("minutes_date_from  :" + str(minutes_date_from))
#     print("minutes_date_to  :" + str(minutes_date_to))

# print("\n")
# print("\n")
# print("\n")
#
#
# print("TEST User matp321@mail.com belongs to group parking_manager :"+str(has_group(CustomUser.objects.get(email='matp321@mail.com'),"Parking_manager")))
# print("TEST User user1@mail.com belongs to group Client_mobile :"+str(has_group(CustomUser.objects.get(email='user1@mail.com'),"Client_mobile")))
#
# print("User_email"+CustomUser.objects.get(pk=1).email)


# my_group = Group.objects.get(name='Client_mobile')
# my_group.user_set.add(user)
# CustomUser.objects.filter(email="user44@mail.com").update(is_active=False)
#
# user=CustomUser.objects.get(email="user44@mail.com").id
#
# CustomUser.objects.get(email="user44@mail.com")
#
# print("TEST group"+str(has_group(CustomUser.objects.get(email="user44@mail.com"),"Client_mobile")))
#
# print("TEST active"+str(CustomUser.objects.get(email="user44@mail.com").is_active))


# for p in Booking.objects.raw('SELECT * FROM pages_booking'):
#     SELECT
#     classes._id, students.studentname, classes.classname, classes.attend, classes.late, classes.dtime
#     FROM
#     students, classes
#     WHERE
#     students._id = classes.student
# requested_user="matp321@mail.com"
# user_converse=CustomUser.objects.get(email=requested_user).id
# parking_filtered=Parking.objects.get(user_parking=user_converse).id
# booking_filtered=Booking.objects.filter(parking=parking_filtered)
## pobrany uzytkownik
# print("Booking objects: "+str(Booking.objects.values_list("registration_plate")))

# print("booking filtered: "+str(booking_filtered))

# print("Booking filtered filtered"+str(Booking.objects.filter(parking=parking_filtered.id)))



# Car.objects.all().delete()

# _b1 = Car.objects
# print("\n")
# _b1 = _b1.all().aggregate(Sum('booking__number_of_cars'))
#
# print(_b1)
#



#
#
#
#
#
# # 15800
#
# self=Car.objects.get(pk=15800)
# print(self.id)


def get_foreign(self):
    print(self.booking.parking.id)

# _b1 = Car.objects
# w5 = _b1.filter(Q(Date_From=convert_string_date_time(self.Date_From)) & Q(
#     Date_To=convert_string_date_time(self.Date_To)) & Q(
#     booking__parking=self.booking.parking) & (
#                     Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
#
#

# self1=Booking.objects.get(pk=75)
# time1 = datetime(2019, 2, 28, 10, 0, 00)
# time2 = datetime(2019, 2, 28, 16, 0, 00)
#
#
# book=Booking.objects.get(pk=16)
#
#
# #
# new_car=Car(
#     registration_plate="regis12",
#     booking=book,
#     Date_From=time1,
#     Date_To=time2
#
# )
#
# new_car.save()
# #
# print("WORKING")
# print("\n\n\n\n")
# #
# # for x in Car.objects.raw('SELECT * FROM pages_car'):
# #     print("DATE:"+str(x.id))
# print("BLABLA")
# for x in Car.objects.raw('SELECT * FROM pages_car'):
#     print("ID:"+x.status)
#     x.status="ACTIVE"
#     x.save()
#     x.refresh_from_db()
#
#
# time1 = datetime(2019, 2, 28, 16, 0, 00).replace(tzinfo=None)
# time2 = datetime(2019, 2, 28, 16, 30, 00).replace(tzinfo=None)
#
#
# print(time_difference_minutes(time2,time1))
#
#
# Car.objects.filter(pk=36).update(status='RESERVED')



print(Parking.objects.filter(user_parking__email='user1@mail.com').exists())

query=Parking.objects.filter(user_parking__email='user1@mail.com')

print(query.exists())

try:
    query_user_parking = Parking.objects.filter(user_parking__email="dsf@sdf.com")
except query_user_parking.DoesNotExist:
    query_user_parking = None
    print("WRONG")


print("FURTHER")
x=2
if query_user_parking is None:
    print("NONE")


# user_get_id = CustomUser.objects.get(email=requested_user).id
# try:
#     parking_filtered = Parking.objects.get(user_parking=user_get_id).id
# except parking_filtered.DoesNotExist:
#     parking_filtered = None
# try:
#     booking_filtered = Booking.objects.filter(parking=parking_filtered)
# except booking_filtered.DoesNotExist:
#     booking_filtered = None
# try:
#     group_user = user.groups.filter(name='Parking_manager')
# except group_user.DoesNotExist:
#     group_user = None
#

user="user1@mail.com"

# try:
#     group_user=user.groups.filter(name='Parking_manager')
# except group_user.DoesNotExist:
#     group_user = "Empty"
# try:
#     query_user_parking = Parking.objects.filter(user_parking__email=user)
# except query_user_parking.DoesNotExist:
#     query_user_parking = "Empty"
#
# # booking_list = Booking.objects.all()
# if group_user=="Empty":
#     print("Empty1")
# if query_user_parking=="Empty":
#     print("Empty2")
# else:
#     print("Empty3")
#
#
#
#


comment = Car.objects.filter(pk=100)


comment.old

comment.exists()





