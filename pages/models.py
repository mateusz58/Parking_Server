from django.db import models

# Create your models here.
import datetime as dt
import pytz
from django.core.exceptions import ValidationError
from django.db import models

##from park.tasks  import set_race_as_inactive
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
    Cost = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', editable=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_cars = models.PositiveIntegerField(default=1)
    def __int__(self):
         return self.registration_plate
    def save(self, *args, **kwargs):


            date_to=self.Date_To.strftime("%Y-%m-%d %H:%M:%S")
            date_from = self.Date_From.strftime("%Y-%m-%d %H:%M:%S")
            self.Date_From = dt.datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
            self.Date_To = dt.datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')

            self.Date_From=self.Date_From.replace(tzinfo=None)
            self.Date_To=self.Date_To.replace(tzinfo=None)


            # self.Date_To=self.Date_To.replace('Z','')
            # self.Date_From=self.Date_From.replace('Z', '')


            # /self.Date_To = self.Date_To.toISOString().replace('Z', '').replace('T', '');
            # updated=self.updated.strftime("%Y-%m-%d %H:%M:%S")
            # Date_From1= self.Date_From.strftime("%Y-%m-%d %H:%M:%S")
            # added1 =self.added.strftime("%Y-%m-%d %H:%M:%S")
            # updated1 = self.updated.strftime("%Y-%m-%d %H:%M:%S")

            # updated=self.updated.strftime("%Y-%m-%d %H:%M:%S")
            # Date_From1= self.Date_From.strftime("%Y-%m-%d %H:%M:%S")
            # added1 =self.added.strftime("%Y-%m-%d %H:%M:%S")
            # updated1 = self.updated.strftime("%Y-%m-%d %H:%M:%S")
            super(Booking, self).save(*args, **kwargs)
