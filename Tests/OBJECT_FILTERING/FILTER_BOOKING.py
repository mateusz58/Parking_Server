from datetime import datetime

from users.models import CustomUser

from django.db import connection

from pages.models import Parking, Booking, CustomUser
from django.utils import timezone


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


print("RAW QUERIES FOREIGN KEY")

cursor = connection.cursor()
cursor.execute("SELECT * FROM Parking")
result = cursor.fetchall()

print("RAW QUERIES SUM AGGREGATION WITH FILTERING")
for p in Booking.objects.raw('SELECT *,SUM (pages_booking.number_of_cars) AS sum FROM pages_booking WHERE pages_booking.Date_From>=%s AND pages_booking.Date_To<=%s AND pages_booking.parking=1 ',[time1,time2]):
    print(p.sum),

print("ASSERT TEST")

assert (p.sum==6)






# for p in Booking.objects.raw('SELECT * FROM pages_booking'):
#     SELECT
#     classes._id, students.studentname, classes.classname, classes.attend, classes.late, classes.dtime
#     FROM
#     students, classes
#     WHERE
#     students._id = classes.student


