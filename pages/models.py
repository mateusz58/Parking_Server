import re
from django.db import models

# Create your models here.
import datetime as dt
import pytz
from django.core.exceptions import ValidationError
from django.db import models

##from park.tasks  import set_race_as_inactive
from django.db.models import Q, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from Basic_Functions.String_processing import check_query_string
from Validators.Booking_validator import validate_range_min_max
from Validators.Car_validators import isalphavalidator
from users.models import CustomUser


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core import validators
from django.utils import timezone

STATUS_CHOICES = (
    ('ACTIVE', 'active'),
    ('EXPIRED', 'expired'),
    ('RESERVED', 'reserved'),
    ('CANCELLED', 'cancelled'),
    ('RESERVED_L', 'reserved_l'),
    ('EXPIRED_E', 'expired_e')
)



class Parking(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    parking_name = models.CharField(max_length=200,unique=True)
    parking_Street = models.CharField(max_length=200)
    parking_City = models.CharField(max_length=200)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    number_of_places=models.PositiveIntegerField(default=1)
    free_places = models.PositiveIntegerField(default=number_of_places)
    HOUR_COST = models.FloatField(default=2.0)
    user_parking = models.ForeignKey(CustomUser, related_name='user_parking', on_delete=models.CASCADE,default=5)
    class Meta:
        unique_together = ('parking_Street', 'parking_City',)
    ##pub_date = models.DateTimeField('date published')

    def save(self, *args, **kwargs):
        super(Parking, self).save(*args, **kwargs)

    def __str__(self):
        return self.parking_name

class Booking(models.Model):

    code = models.BigAutoField(primary_key=True, editable=False)
    parking = models.ForeignKey(Parking, related_name='parking', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE,null=True,default=1,editable=False)
    ##choice_text = models.CharField(max_length=200)
    ##votes = models.IntegerField(default=0)
    registration_plate = models.CharField(max_length=20)
    Date_From = models.DateTimeField(default=dt.datetime.now())
    Date_To = models.DateTimeField(default=dt.datetime.now())
    Cost = models.FloatField(editable=False,default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', editable=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_cars = models.PositiveIntegerField(default=1,editable=False)
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.number_of_cars < 1:
             raise ValidationError('You cannot register register parking place for less than one car')


    def __int__(self):
         return self.registration_plate

    def save(self, *args, **kwargs):

            self.number_of_cars=str(self.calculate_number_of_cars())
            super().save(*args, **kwargs)

class Car(models.Model):


    id = models.BigAutoField(primary_key=True, editable=False)
    Date_From = models.DateTimeField(default=dt.datetime.now())
    Date_To = models.DateTimeField(default=dt.datetime.now())
    booking = models.ForeignKey(Booking, related_name='booking', on_delete=models.CASCADE, blank=True, null=True)
    registration_plate = models.CharField(max_length=10,validators=[isalphavalidator], null=False, blank=False,default='default')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', editable=True)
    Cost = models.FloatField(editable=False, default=0)


    def validate_if_place_available(self):


        duration = self.Date_To.replace(tzinfo=None) - self.Date_From.replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes" + str(minutes))

        _b1 = Car.objects
        w1 = _b1.filter(Q(Date_From__lt=self.Date_From) & Q(
            Date_To__gt=self.Date_From) & Q(
            booking__parking=self.booking.parking) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w2 = _b1.filter(Q(Date_From__gt=self.Date_From) & Q(
            Date_To__lt=self.Date_To) & Q(
            booking__parking=self.booking.parking) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w3 = _b1.filter(Q(Date_From__lt=self.Date_To) & Q(
            Date_To__gt=self.Date_To) & Q(
            booking__parking=self.booking.parking) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w4 = _b1.filter(Q(Date_From__lt=self.Date_From) & Q(
            Date_To__gt=self.Date_To) & Q(
            booking__parking=self.booking.parking) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w5 = _b1.filter(Q(Date_From=self.Date_From) & Q(
            Date_To=self.Date_To) & Q(
            booking__parking=self.booking.parking) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        variations = [w1, w2, w3, w4, w5]

        if w1.filter(registration_plate=str(self.registration_plate)).exists():
            raise ValidationError("Car with registration number:" + str(
                self.registration_plate) + " have already registered parking place in that period of time")

        if w2.filter(registration_plate=str(self.registration_plate)).exists():
            raise ValidationError("Car with registration number:" + str(
                self.registration_plate) + " have already registered parking place in that period of time")

        if w3.filter(registration_plate=str(self.registration_plate)).exists():
            raise ValidationError("Car with registration number:" + str(
                self.registration_plate) + " have already registered parking place in that period of time")

        if w4.filter(registration_plate=str(self.registration_plate)).exists():
            raise ValidationError("Car with registration number:" + str(
                self.registration_plate) + " have already registered parking place in that period of time")

        if w5.filter(registration_plate=str(self.registration_plate)).exists():
            raise ValidationError("Car with registration number:" + str(
                self.registration_plate) + " have already registered parking place in that period of time")

        i = 0
        sum = 0
        while i < len(variations):
            # print("Variation:" + str(variations))
            sum = sum + check_query_string(variations[i])
            i += 1

        sum_after_request = sum + 1

        if sum_after_request > Parking.objects.get(pk=self.booking.parking).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    self.booking.parking.number_of_places - sum))

    def validate_minutes(self):
        duration = self.Date_To - self.Date_From
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        return minutes

    def validate_registration_plate_signs(self):
        if not str(self.registration_plate).isalnum():
            raise ValidationError(
                "Wrong registration number of car,car registration number can consist only of numbers and letters characters")
        if len(self.registration_plate) < 6:
            raise ValidationError("Wrong registration number of car:" + str(self.registration_plate_list
                                                                            ) + ",car registration number must consist of at least 6 characters and maximum 10 characters")
        if len(self.registration_plate) > 10:
            raise ValidationError("Wrong registration number of car:" + str(self.registration_plate
                                                                            ) + ",car registration number must consist of at least 6 characters and maximum 10 characters")

    def validate_registration_plate_exists(self):

        query = Car.objects.filter(booking=self.booking)
        if query.filter(registration_plate=self.registration_plate).exists():
            return True
        else:
            return False

    def get_Cost(self):
        print("TRIGGER CAR COST")
        time1 = self.Date_From
        time2 = self.Date_To
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = self.booking.parking.HOUR_COST * HOURS
        Cost=round(Cost, 2)
        return Cost

    def calculate_number_of_cars(self):

        query = Car.objects.filter(booking=self.booking)
        count = 0
        for record in query:
            if record.status == 'ACTIVE':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1

        return count

    def calculate_cost_booking(self):

        query = Car.objects.filter(booking=self.booking)
        sum=0
        for record in query:
            if record.status == 'ACTIVE':
                sum=record.Cost+sum
            if record.status == 'RESERVED_L':
                sum = record.Cost + sum
            if record.status == 'RESERVED':
                sum = record.Cost + sum

        return sum+self.get_Cost(self)

    def __init__(self, *args, **kwargs):
        super(Car, self).__init__(*args, **kwargs)
        self.old_state = self.status

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.validate_registration_plate_exists(self):
            raise ValidationError('Car with registration number'+str(self.registration_plate)+"is on the booking list")
        self.validate_registration_plate_signs(self)
        if self.validate_minutes(self)<30:
                raise ValidationError('You cannot register parking place for less than 30 minutes')
        if self.Date_From.replace(tzinfo=None) < dt.datetime.now():
            raise ValidationError("Value of Date_From must be higher than current time")
        if self.old_state == 'ACTIVE' and self.status == 'RESERVED_L':
            raise ValidationError('You cannot change active reservation to rerserved_L state')
        self.validate_if_place_available(self)

    def save(self, *args, **kwargs):

        super(Car, self).save(force_insert=True, force_update=True)
        self.old_state = self.status
        self.Cost = str(self.get_Cost())
        Booking.objects.filter(pk=self.booking.code).update(number_of_cars=self.calculate_number_of_cars(self))
        Booking.objects.filter(pk=self.booking.code).update(Cost=self.calculate_cost_booking(self))



