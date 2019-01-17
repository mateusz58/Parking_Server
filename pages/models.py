from django.db import models

# Create your models here.
import datetime

from django.core.exceptions import ValidationError
from django.db import models

##from park.tasks  import set_race_as_inactive
from django.db.models.signals import post_save
from django.dispatch import receiver

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
)







class Parking(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    parking_name = models.CharField(max_length=200,unique=True)
    parking_Street = models.CharField(max_length=200)
    parking_City = models.CharField(max_length=200)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    free_places = models.IntegerField(default=0)
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
    Date_From = models.DateTimeField()
    Date_To = models.DateTimeField()
    Cost = models.FloatField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='ACTIVE', editable=False)
    active = models.BooleanField(default=True, editable=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __int__(self):
         return self.code


    #
    # def save(self, *args, **kwargs):
    #     self.active = self.Date_To.strftime("%Y-%m-%d %H:%M:%S") > datetime.datetime.utcnow().strftime(
    #         "%Y-%m-%d %H:%M:%S")
    #     super().save()
    #     print(self.Date_To.strftime("%Y-%m-%d %H:%M:%S"))
    #     print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
