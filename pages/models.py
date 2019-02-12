# Create your models here.
import datetime as dt

from django.core.exceptions import ValidationError
from django.db import models
##from park.tasks  import set_race_as_inactive
from django.db.models import Q, Sum
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver

from Basic_Functions.SQL_FUNCTIONS import sum_field_from_query
from Basic_Functions.String_processing import check_query_string
from Basic_Functions.Time_difference import time_difference_minutes
from Validators.Car_validators import isalphavalidator
# from djangox_project.get_username import get_request

from users.models import CustomUser


def free_places_update_v2(Car_object):
    _b1 = Car.objects
    _b1 = _b1.filter(Q(Date_From__lt=dt.datetime.now()) & Q(Date_To__gt=dt.datetime.now()) & Q(
        booking__parking=Car_object.booking.parking) & (
                             Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
    free_places = Parking.objects.get(pk=Car_object.booking.parking.id).number_of_places - check_query_string(_b1)
    print("Booking_View free_places:" + str(free_places))
    Parking.objects.filter(pk=Car_object.booking.parking.id).save(free_places=free_places)


STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('EXPIRED', 'Expired'),
    ('RESERVED', 'Reserved'),
    ('CANCELLED', 'Cancelled'),
    ('RESERVED_L', 'Reserved Late'),
    ('EXPIRED_E', 'Expired early')
)


class Parking(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    parking_name = models.CharField(max_length=30, unique=True)
    parking_Street = models.CharField(max_length=20)
    parking_City = models.CharField(max_length=20)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    number_of_places = models.PositiveIntegerField(default=1)
    free_places = models.PositiveIntegerField(default=0, editable=False)
    HOUR_COST = models.FloatField(default=2.0)
    user_parking = models.ForeignKey(CustomUser, related_name='user_parking', null=True, on_delete=models.CASCADE,
                                     default=0)

    def clean(self):
        from django.core.exceptions import ValidationError

        i = "asdasd"

        if not all(x.isalpha() or x.isspace() for x in str(self.parking_name)):
            raise ValidationError("Parking name can contain only letters")

        if not all(x.isalnum() or x.isspace() for x in str(self.parking_Street)):
            raise ValidationError("Parking street name can contain only letters and numbers")

        if not all(x.isalpha() or x.isspace() for x in str(self.parking_City)):
            raise ValidationError("Parking city name can contain only letters")
        if self.HOUR_COST < 0:
            raise ValidationError("Hour cost cannot be lower than zero")
        if self.y < -90:
            raise ValidationError("Latitude value is too small")
        if self.y > 90:
            raise ValidationError("Latitude value is too big")
        if self.x < -180:
            raise ValidationError("Longitude value is too small")
        if self.x > 180:
            raise ValidationError("Longitude value is too big")

        # self.UPDATE_STATUS_TRIGGER(self)

    class Meta:
        unique_together = ('parking_Street', 'parking_City',)

    ##pub_date = models.DateTimeField('date published')

    def save(self, *args, **kwargs):
        print("ACTIVATED ONLY ONCE DURING CREATION")
        if self.free_places < 0:
            Parking.objects.filter(pk=self.id).update(free_places=0)
        if not self.free_places:
            self.free_places = self.number_of_places
        super(Parking, self).save(*args, **kwargs)
        Parking.objects.filter(pk=self.id).update(HOUR_COST=round(self.HOUR_COST, 2))

    def __str__(self):
        return self.parking_name


class Booking(models.Model):
    code = models.BigAutoField(primary_key=True, editable=False)
    parking = models.ForeignKey(Parking, related_name='parking', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user', null=True, on_delete=models.CASCADE, editable=False)
    Cost = models.FloatField(editable=False, default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_cars = models.PositiveIntegerField(default=0, editable=True)
    Date_From = models.DateTimeField(default=dt.datetime.now(), editable=True)
    Date_To = models.DateTimeField(default=dt.datetime.now(), editable=True)
    active = models.BooleanField(default=True, editable=False)

    def validate_if_place_available_excluded_registration_plate_exists(self, arg):
        print("CAR MODEL STATE TRIGGER validate_if_place_available")
        duration = self.Date_To.replace(tzinfo=None) - self.Date_From.replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes" + str(minutes))

        _b1 = Car.objects
        w1 = _b1.filter(Q(Date_From__lt=self.Date_From) & Q(
            Date_To__gt=self.Date_From) & Q(
            booking__parking=self.parking) & (
                                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w2 = _b1.filter(Q(Date_From__gt=self.Date_From) & Q(
            Date_To__lt=self.Date_To) & Q(
            booking__parking=self.parking) & (
                                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w3 = _b1.filter(Q(Date_From__lt=self.Date_To) & Q(
            Date_To__gt=self.Date_To) & Q(
            booking__parking=self.parking) & (
                                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w4 = _b1.filter(Q(Date_From__lt=self.Date_From) & Q(
            Date_To__gt=self.Date_To) & Q(
            booking__parking=self.parking) & (
                                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w5 = _b1.filter(Q(Date_From=self.Date_From) & Q(
            Date_To=self.Date_To) & Q(
            booking__parking=self.parking) & (
                                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        variations = [w1, w2, w3, w4, w5]

        i = 0
        sum = 0
        while i < len(variations):
            # print("Variation:" + str(variations))
            sum = sum + check_query_string(variations[i])
            i += 1
        sum_after_request = sum + self.number_of_cars
        if sum_after_request > Parking.objects.get(pk=self.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    self.parking.number_of_places - sum))

    def validate_minutes(self, arg):
        print("CAR MODEL STATE TRIGGER validate_minutes")

        duration = self.Date_To - self.Date_From
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)

        if minutes < 30:
            raise ValidationError('You cannot register parking place for less than 30 minutes')

    def validate_current_time(self, arg):
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) <= dt.datetime.now().replace(second=0,
                                                                                                           microsecond=0):
            raise ValidationError("Value of Date_To must be higher or equal to current time")

    def calculate_number_of_cars(self, arg):

        query = Car.objects.filter(booking=self.code)
        count = 0
        for record in query:
            if record.status == 'ACTIVE':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1

        print("CAR MODEL ID:" + str(self.id) + "STATE TRIGGER calculate_number_of_cars:" + str(count))
        return count

    def calculate_cost_booking(self, arg):

        query = Car.objects.filter(booking=self.code)
        sum = 0
        for record in query:
            if record.status == 'ACTIVE':
                sum = record.Cost + sum
            if record.status == 'RESERVED_L':
                sum = record.Cost + sum
            if record.status == 'RESERVED':
                sum = record.Cost + sum
            if record.status == 'EXPIRED':
                sum = record.Cost + sum
            if record.status == 'EXPIRED_E':
                sum = record.Cost + sum

        print("CAR MODEL ID:" + str(self.id) + "STATE TRIGGER calculate_cost_booking for value:" + str(round(sum, 2)))
        return round(sum, 2)

    def __int__(self):
        return self.code

    def clean(self):

        self.validate_minutes(self)
        self.validate_current_time(self)

        self.validate_if_place_available_excluded_registration_plate_exists(self)

        # count = 0
        # for x in range(self.number_of_cars):
        #     try:
        #         car = Car(registration_plate="", booking=Booking.objects.get(code=self.code), Date_From=self.Date_From,
        #                   Date_To=self.Date_To).full_clean()
        #         car = Car(registration_plate="", booking=Booking.objects.get(code=self.code), Date_From=self.Date_From,
        #                   Date_To=self.Date_To).save()
        #         count = count + 1
        #
        #     except Exception as e:
        #         print("BOOKING EXCEPTION")
        #         continue
        # if (count == 0):
        #     raise ValidationError("Not enough free places in that period of time:")

    def cancel_all(self, arg):
        if self.active == False:
            try:
                Car.objects.filter(booking=self.code).update(state="CANCELLED")
                Booking.objects.filter(code=self.code).update(Cost=0)
                Booking.objects.filter(code=self.code).update(number_of_cars=0)
            except:
                pass

    def save(self, **kwargs):
        print("save()TRIGGER BOOKING ACTIVATED")

        return super(Booking, self).save(**kwargs)


class Car(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    Date_From = models.DateTimeField(default=dt.datetime.now())
    Date_To = models.DateTimeField(default=dt.datetime.now())
    booking = models.ForeignKey(Booking, related_name='booking', on_delete=models.CASCADE, blank=True, null=True,
                                default=0)
    registration_plate = models.CharField(max_length=10, validators=[isalphavalidator], null=False, blank=False,
                                          default='default')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', editable=True)
    Cost = models.FloatField(editable=False, default=0)

    def __init__(self, *args, **kwargs):
        super(Car, self).__init__(*args, **kwargs)
        self.old_status = self.status
        self.old_date_to = self.Date_To
        self.old_date_from = self.Date_From
        self.old_registration_plate = self.registration_plate

    def validate_if_booking_none(self, arg):

        print("CAR MODEL STATE TRIGGER validate_if_booking_none")

        if self.booking is None:
            raise ValidationError("You must assign Booking value")

    def validate_if_place_available_excluded_registration_plate_exists(self, arg):
        print("CAR MODEL STATE TRIGGER validate_if_place_available")
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

        i = 0
        sum = 0
        while i < len(variations):
            # print("Variation:" + str(variations))
            sum = sum + check_query_string(variations[i])
            i += 1
        sum_after_request = sum + 1
        if sum_after_request > Parking.objects.get(pk=self.booking.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    self.booking.parking.number_of_places - sum))

    def validate_if_place_available(self, arg):

        print("CAR MODEL STATE TRIGGER validate_if_place_available")

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
        if sum_after_request > Parking.objects.get(pk=self.booking.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    self.booking.parking.number_of_places - sum))

    def validate_minutes(self, arg):
        print("CAR MODEL STATE TRIGGER validate_minutes")

        duration = self.Date_To - self.Date_From
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)

        if minutes < 30:
            raise ValidationError('You cannot register parking place for less than 30 minutes')

    def validate_current_time(self, arg):
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) <= dt.datetime.now().replace(second=0,
                                                                                                           microsecond=0):
            raise ValidationError("Value of Date_To must be higher or equal to current time")

    def validate_registration_plate_signs(self, arg):
        print("CAR MODEL STATE TRIGGER validate_registration_plate_signs")

        if not str(self.registration_plate).isalnum():
            raise ValidationError(
                "Wrong registration number of car,car registration number can consist only of numbers and letters characters")
        if len(self.registration_plate) < 6:
            raise ValidationError("Wrong registration number of car:" + str(
                self.registration_plate) + "car registration number must consist of at least 6 characters and maximum 10 characters")

        if len(self.registration_plate) > 10:
            raise ValidationError("Wrong registration number of car:" + str(self.registration_plate
                                                                            ) + ",car registration number must consist of at least 6 characters and maximum 10 characters")

    def get_Cost(self, arg):
        print("CAR MODEL STATE TRIGGER get_Cost")
        time1 = self.Date_From.replace(tzinfo=None)
        time2 = self.Date_To.replace(tzinfo=None)
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]  ## HOURS DURATION
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = self.booking.parking.HOUR_COST * HOURS
        Cost = round(Cost, 2)
        return Cost

    def calculate_number_of_cars(self, arg):

        query = Car.objects.filter(booking=self.booking)
        count = 0
        for record in query:
            if record.status == 'ACTIVE':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1
            if record.status == 'RESERVED_L':
                count = count + 1

        print("CAR MODEL ID:" + str(self.id) + "STATE TRIGGER calculate_number_of_cars:" + str(count))
        return count

    def calculate_cost_booking(self, arg):

        query = Car.objects.filter(booking=self.booking)
        sum = 0
        for record in query:
            if record.status == 'ACTIVE':
                sum = record.Cost + sum
            if record.status == 'RESERVED_L':
                sum = record.Cost + sum
            if record.status == 'RESERVED':
                sum = record.Cost + sum
            if record.status == 'EXPIRED':
                sum = record.Cost + sum
            if record.status == 'EXPIRED_E':
                sum = record.Cost + sum

        print("CAR MODEL ID:" + str(self.id) + "STATE TRIGGER calculate_cost_booking for value:" + str(round(sum, 2)))
        return round(sum, 2)

    def validate_states(self, arg):

        print("clean()CAR MODEL TRIGGER validate_states")

        if self.old_status == "ACTIVE" and (
                self.status == "EXPIRED" or self.status == "EXPIRED_E" or self.status == "RESERVED_L"):  ###
            raise ValidationError("You cannot change state ACTIVE to: " + str(self.status))

        if self.old_status == "CANCELLED" and (
                self.status == "EXPIRED" or self.status == "EXPIRED_E" or self.status == "RESERVED_L" or self.status == "RESERVED" or self.status == "ACTIVE"):
            raise ValidationError("You cannot change state CANCELLED")

        if self.old_status == "EXPIRED" and (
                self.status == "ACTIVE" or self.status == "EXPIRED_E" or self.status == "RESERVED_L" or self.status == "RESERVED" or self.status == "CANCELLED"):
            raise ValidationError("You cannot change state EXPIRED to: " + str(self.status))

        if self.old_status == "EXPIRED_E" and (
                self.status == "ACTIVE" or self.status == "EXPIRED" or self.status == "RESERVED_L" or self.status == "RESERVED" or self.status == "CANCELLED"):
            raise ValidationError("You cannot change state EXPIRED_E to" + str(self.status))

        if self.old_status == "RESERVED" and (self.status == "ACTIVE" or self.status == "CANCELLED"):
            raise ValidationError("You cannot change state RESERVED to: " + str(self.status))

        if self.old_status == "RESERVED_L" and (
                self.status == "ACTIVE" or self.status == "CANCELLED" or self.status == "RESERVED"):
            raise ValidationError("You cannot change state RESERVED_L to: " + str(self.status))

        ## TIME VALIDATION

        if self.status == "RESERVED":
            if not self.Date_From.replace(tzinfo=None).replace(second=0, microsecond=0) <= dt.datetime.now().replace(
                    second=0, microsecond=0) <= self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0):
                raise ValidationError('You cannot set state to Reserved in current condiction ')

        if self.status == "RESERVED_L":
            if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) >= dt.datetime.now().replace(second=0,
                                                                                                               microsecond=0):
                raise ValidationError('You cannot set state to Reserved_L when Date To is higher than current time ')

        if self.status == "EXPIRED_E":
            if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) < dt.datetime.now().replace(second=0,
                                                                                                              microsecond=0):
                raise ValidationError('You cannot set state to EXPIRED_E when Date To is lower than current time ')

    def validate_registration_plate_exists(self, arg):

        print("CAR MODEL STATE TRIGGER validate_registration_plate_exists")

    def validate_status_check_free_places_registration_placte_exists(self, arg):

        # self.state == "ACTIVE" or self.state == "RESERVED" or self.state == "RESERVED_L"):

        print("clean()CAR MODEL TRIGGER validate_status_check_free_places_registration_placte_exists")

        if not self.pk is None:  ### EXECUTED WHEN UPDATING OBJECT
            print("CHECKING NOT NONE")  ##
        if self.pk is None:  ### EXECUTED WHEN CREATING NEW OBJECT
            print("CHECKING NONE")
            if self.status == "ACTIVE":
                print("EXECUTED")
                query = Car.objects.filter(booking=self.booking)
                query = query.filter(
                    Q(booking=self.booking.code) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
                if query.filter(registration_plate=self.registration_plate).exists():
                    raise ValidationError('Car with that reservation number is on the booking list')
                else:
                    return False
                self.validate_if_place_available(self)

    def clean_exclude_register_plate_exist_and_validate_registration_plate_signs(self, arg):

        print("(clean_EXCLUDING) TRIGGER CAR ACTIVATED")
        from django.core.exceptions import ValidationError
        self.validate_states(self)
        self.validate_if_booking_none(self)
        self.validate_if_place_available_excluded_registration_plate_exists(self)
        self.validate_minutes(self)
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) <= dt.datetime.now().replace(second=0,
                                                                                                           microsecond=0):
            raise ValidationError("Value of Date_To must be higher or equal to current time")
        if self.old_status == 'ACTIVE' and self.status == 'RESERVED_L':
            raise ValidationError('You cannot change active reservation to rerserved_L state')
        name = self.registration_plate

    def clean(self):

        print("(clean)TRIGGER CAR ACTIVATED")
        from django.core.exceptions import ValidationError
        self.validate_status_check_free_places_registration_placte_exists(self)
        self.validate_current_time(self)
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) <= dt.datetime.now().replace(second=0,
                                                                                                           microsecond=0):
            raise ValidationError("Value of Date_To must be higher or equal to current time")
        self.validate_states(self)
        self.validate_if_booking_none(self)
        self.validate_registration_plate_signs(self)
        self.validate_minutes(self)
        if self.old_status == 'ACTIVE' and self.status == 'RESERVED_L':
            raise ValidationError('You cannot change active reservation to rerserved_L state')
        name = self.registration_plate

    def save(self, *args, **kwargs):

        print("(save)TRIGGER CAR ACTIVATED")

        self.old_status = self.status
        Car.objects.filter(pk=self.id).update(Cost=self.get_Cost(self))

        self.Cost = self.get_Cost(self)

        super(Car, self).save()

        if self.status == "RESERVED_L":
            Car.objects.filter(id=self.id).update(Date_To=dt.datetime.now())
            Cost = self.get_Cost(self)
            self.Cost = Cost
            self.Date_To = dt.datetime.now()
            Car.objects.filter(pk=self.id).update(Cost=Cost)

        if self.status == "EXPIRED_E":
            Car.objects.filter(id=self.id).update(Date_To=dt.datetime.now())
            Cost = self.get_Cost(self)
            Car.objects.filter(pk=self.id).update(Cost=Cost)

        car = Car.objects.filter(
            Q(booking=Booking.objects.get(pk=self.booking.code)) & Q(status='ACTIVE') | Q(status='RESERVED') | Q(
                status='RESERVED_L'))
        if not car.exists():
            Booking.objects.filter(pk=self.booking.code).update(active=False)
            print("NO dates with that citeria")

        else:
            print("(save)TRIGGER FOR DATE FROM AND DATE TO")
            earliest = car.earliest('Date_From').Date_From
            latest = car.latest('Date_To').Date_To
            Booking.objects.filter(pk=self.booking.code).update(Date_From=earliest)
            Booking.objects.filter(pk=self.booking.code).update(Date_To=latest)

        if self.status == "CANCELLED":
            Car.objects.filter(id=self.id).update(Cost=0)
        Booking.objects.filter(pk=self.booking.code).update(number_of_cars=Car.objects.filter(
            Q(booking=self.booking) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count())
        Booking.objects.filter(code=self.booking.code).update(Cost=Car.objects.filter(
            Q(booking=self.booking) & (
                    Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L') | Q(status='EXPIRED') | Q(
                status='EXPIRED_E'))).aggregate(Sum('Cost'))['Cost__sum'])

        if not Car.objects.filter(Q(booking=self.booking) & (
                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).exists():
            Booking.objects.filter(pk=self.booking.code).update(active=False)


@receiver(pre_delete, sender=Booking)
def model_Booking_delete(sender, instance, **kwargs):
    try:
        print("Receiver for object:" + str(instance.code))
        Car.objects.filter(booking=instance).delete()
    except Exception as e:
        print(str(e))


@receiver(pre_delete, sender=Parking)
def model_Parking_delete(sender, instance, **kwargs):
    try:
        print("Receiver for object:" + str(instance.id))
        Booking.objects.filter(parking=instance).delete()
    except Exception as e:
        print(str(e))


@receiver(pre_save, sender=Booking)
def model_add(sender, instance, **kwargs):
    print("Receiver for object:" + str(instance.code))
    print("Pre save save signal Booking count value:" + str(instance.number_of_cars))
    # count = Car.objects.filter(booking=instance).count()
    # if count==0:
    #     raise ValidationError(
    #         "Not enough free places in that period of time:")
    # else:
    #     Booking.objects.filter(code=instance.code).update(number_of_cars=count)
