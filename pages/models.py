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

from Validators.Booking_validator import validate_range_min_max
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
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    ##choice_text = models.CharField(max_length=200)
    ##votes = models.IntegerField(default=0)
    registration_plate = models.CharField(max_length=20)
    Date_From = models.DateTimeField(default=dt.datetime.now())
    Date_To = models.DateTimeField(default=dt.datetime.now())
    Cost = models.FloatField(editable=False,default=-0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', editable=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_cars = models.PositiveIntegerField(default=1)

    def get_Cost_Custom(self):


        print("TRIGGER BOOKING COST")
        time1 = self.Date_From
        time2 = self.Date_To
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = self.parking.HOUR_COST * HOURS*self.number_of_cars
        return Cost



    def __int__(self):
         return self.registration_plate



    def save(self, *args, **kwargs):


            # date_to=self.Date_To.strftime("%Y-%m-%d %H:%M:%S")
            # date_from = self.Date_From.strftime("%Y-%m-%d %H:%M:%S")
            # self.Date_From = dt.datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
            # self.Date_To = dt.datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')
            #
            # self.Date_From=self.Date_From.replace(tzinfo=None)
            # self.Date_To=self.Date_To.replace(tzinfo=None)


            self.Cost = str(self.get_Cost_Custom())
            super().save(*args, **kwargs)
