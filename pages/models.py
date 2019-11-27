import datetime as dt
from collections import namedtuple

from crum import get_current_user
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from djangox_project import settings
from helper.String_processing import check_query_string
from helper.calculateTimeDifference import is_overlapped
from users.models import CustomUser
from validators.carValidators import isalphavalidator
import logging

logger = logging.getLogger(__name__)

def free_places_update_v2(Car_object):
    _b1 = Car.objects
    _b1 = _b1.filter(Q(Date_From__lt=dt.datetime.now()) & Q(Date_To__gt=dt.datetime.now()) & Q(
        booking__parking=Car_object.booking.parking) & (
                             Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
    free_places = Parking.objects.get(pk=Car_object.booking.parking).number_of_places - check_query_string(_b1)
    print("Booking_View free_places:" + str(free_places))
    Parking.objects.filter(pk=Car_object.booking.parking.id).save(free_places=free_places)

def free_places_update_booking(Car_object):
    _b1 = Car.objects
    count = _b1.filter(Q(Date_From__lt=dt.datetime.now()) & Q(Date_To__gt=dt.datetime.now()) & Q(
        booking=Car_object.booking) & (
                               Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count()
    free_places = Parking.objects.get(pk=Car_object.booking.parking).number_of_places - count
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

    class Meta:
        unique_together = ('parking_Street', 'parking_City',)

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
    id = models.BigAutoField(primary_key=True, editable=False)
    parking = models.ForeignKey(Parking, related_name='parking', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user', null=True, on_delete=models.CASCADE, editable=False)
    Cost = models.FloatField(editable=False, default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_cars = models.PositiveIntegerField(default=0, editable=True)
    Date_From = models.DateTimeField(default=dt.datetime.now(), editable=True)
    Date_To = models.DateTimeField(default=dt.datetime.now(), editable=True)
    active = models.BooleanField(default=True, editable=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                   default=None, on_delete=models.CASCADE, related_name='created_by', editable=False)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                    default=None, on_delete=models.CASCADE, related_name='modified_by', editable=False)

    def __init__(self, *args, **kwargs):

        super(Booking, self).__init__(*args, **kwargs)

        self.old_active = self.active

        if self.pk is not None:

            post_save.disconnect(model_add, sender=Booking)
        else:

            post_save.connect(model_add, sender=Booking)

        pass
        pass

    def get_Cost_sum(self, arg):
        print("CAR MODEL STATE TRIGGER get_Cost")
        time1 = self.Date_From.replace(tzinfo=None)
        time2 = self.Date_To.replace(tzinfo=None)
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = self.parking.HOUR_COST * HOURS
        Cost = round(Cost, 2)
        return Cost * self.number_of_cars

    def get_Cost_single(self, arg):
        print("CAR MODEL STATE TRIGGER get_Cost")
        time1 = self.Date_From.replace(tzinfo=None)
        time2 = self.Date_To.replace(tzinfo=None)
        duration = time2 - time1
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        minutes = divmod(duration_in_s, 60)[0]
        HOURS = float("{0:.2f}".format(hours + ((minutes / 60) - hours)))
        Cost = self.parking.HOUR_COST * HOURS
        Cost = round(Cost, 2)
        return Cost

    def validate_if_place_available_excluded_registration_plate_exists(self, arg):

        if not self.pk is None:
            print("MODEL BOOKING UPDATE validator validate_if_place_available_excluded_registration_plate_exists")
        if self.pk is None:
            print("MODEL BOOKING CREATE validator validate_if_place_available_excluded_registration_plate_exists")

        print("BOOKING MODEL GENERAL validator validate_if_place_available_excluded_registration_plate_exists")
        date_from = self.Date_From.replace(tzinfo=None)
        date_to = self.Date_To.replace(tzinfo=None)
        duration = self.Date_To.replace(
            tzinfo=None) - self.Date_From.replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes" + str(minutes))
        i = 0

        query = Car.objects.filter(Q(
            booking__parking=self.parking) & (
                                           Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        Range = namedtuple('Range', ['start', 'end'])
        variations = []
        for record in query:
            r1 = Range(start=date_from,
                       end=date_to)
            r2 = Range(start=record.Date_From.replace(tzinfo=None),
                       end=record.Date_To.replace(tzinfo=None))

            if is_overlapped(r1, r2):
                variations.append(record)

        sum_before_request = len(variations)
        sum_after_request = len(variations) + self.number_of_cars
        max_number_places = Parking.objects.get(id=self.parking.id).number_of_places - sum_before_request
        if max_number_places < 0:
            max_number_places = 0
        if sum_after_request > Parking.objects.get(id=self.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve in that "
                "period of time is:" + str(max_number_places))

    def validate_minutes(self, arg):
        print("CAR MODEL STATE TRIGGER validate_minutes")

        duration = self.Date_To - self.Date_From
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)

        if minutes < 30:
            raise ValidationError('You cannot register parking place for less than 30 minutes')

    def validate_current_time(self, arg):
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) < dt.datetime.now().replace(second=0,
                                                                                                          microsecond=0):
            raise ValidationError("Value of Date_To must be higher or equal to current time")

    def calculate_number_of_cars(self, arg):

        query = Car.objects.filter(booking=self.id)
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

        query = Car.objects.filter(booking=self.id)
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

    def clean(self):

        self.validate_minutes(self)
        self.validate_current_time(self)

        if self.old_active == False and self.active == True:
            raise ValidationError("You cannot change state of that booking")

        if self.pk is None:
            self.validate_if_place_available_excluded_registration_plate_exists(self)

    def save(self, **kwargs):
        print("save()TRIGGER BOOKING ACTIVATED")

        if not self.active:
            self.Cost = 0
            self.number_of_cars = 0
            Car.objects.filter(booking=self.id).update(status="CANCELLED")
            Car.objects.filter(booking=self.id).update(Cost=0)

        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user

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
        date_from = self.Date_From
        date_to = self.Date_To
        duration = self.Date_To.replace(
            tzinfo=None) - self.Date_From.replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes" + str(minutes))
        i = 0

        query = Car.objects.filter(Q(
            booking__parking=self.booking.parking) & (
                                           Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        Range = namedtuple('Range', ['start', 'end'])
        variations = []
        for record in query:
            r1 = Range(start=date_from,
                       end=date_to)
            r2 = Range(start=record.Date_From.replace(tzinfo=None),
                       end=record.Date_To.replace(tzinfo=None))

            if is_overlapped(r1, r2):
                variations.append(record)

        sum_before_request = len(variations)
        sum_after_request = len(variations) + self.number_of_cars
        max_number_places = Parking.objects.get(id=self.parking.id).number_of_places - sum_before_request
        if max_number_places < 0:
            max_number_places = 0
        if sum_after_request > Parking.objects.get(pk=self.request.data['parking']).number_of_places:
            raise ValidationError(
                "*Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    max_number_places))

    def validate_if_place_available(self, arg):

        print("CAR MODEL TRIGGER valide_if_place_available")

        if not self.pk is None:
            print("MODEL CAR UPDATE validator validate_if_place_available")
        if self.pk is None:
            print("MODEL CAR CREATE validator validate_if_place_available")

        date_from = self.Date_From
        date_to = self.Date_To
        duration = self.Date_To.replace(
            tzinfo=None) - self.Date_From.replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes" + str(minutes))
        i = 0

        query = Car.objects.filter(Q(
            booking__parking=self.booking.parking) & (
                                           Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))

        Range = namedtuple('Range', ['start', 'end'])
        variations = []
        for record in query:
            r1 = Range(start=date_from,
                       end=date_to)
            r2 = Range(start=record.Date_From.replace(tzinfo=None),
                       end=record.Date_To.replace(tzinfo=None))

            if is_overlapped(r1, r2):
                if not self.registration_plate == "Not provided":
                    if record.registration_plate == self.registration_plate:
                        raise ValidationError("Car with registration number:" + str(
                            self.registration_plate) + " have already registered parking place in that period of time")

                variations.append(record)

        sum_before_request = len(variations)
        sum_after_request = len(variations) + 1
        max_number_places = Parking.objects.get(id=self.booking.parking.id).number_of_places - sum_before_request
        if max_number_places < 0:
            max_number_places = 0
        if sum_after_request > Parking.objects.get(id=self.booking.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    max_number_places))

    def validate_if_place_available_old(self, arg):

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
            sum = sum + check_query_string(variations[i])
            i += 1
        sum_after_request = sum + 1
        max_number_places = Parking.objects.get(pk=self.booking.parking.id).number_of_places
        if max_number_places < 0:
            max_number_places = 0
        if sum_after_request > Parking.objects.get(pk=self.booking.parking.id).number_of_places:
            raise ValidationError(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    max_number_places))

    def validate_minutes_min_30(self, arg):
        print("CAR MODEL STATE TRIGGER validate_minutes_min_30")

        duration = self.Date_To - self.Date_From
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)

        if minutes < 30:
            raise ValidationError('You cannot register parking place for less than 30 minutes')

    def validate_registration_plate_signs(self, arg):
        print("CAR MODEL STATE TRIGGER validate_registration_plate_signs")

        if self.pk is None:
            if not self.registration_plate == "Not provided":
                if not str(self.registration_plate).isalnum():
                    raise ValidationError(
                        "Wrong registration number of car,car registration number can consist only of numbers and "
                        "letters characters")
                if len(self.registration_plate) < 6:
                    raise ValidationError("Wrong registration number of car:" + str(
                        self.registration_plate) + "car registration number must consist of at least 6 characters and maximum 10 characters")

                if len(self.registration_plate) > 10:
                    raise ValidationError("Wrong registration number of car:" + str(self.registration_plate
                                                                                    ) + ",car registration number must consist of at least 6 characters and maximum 10 characters")
        else:
            if not self.registration_plate == "Not provided":
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
        hours = divmod(duration_in_s, 3600)[0]
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
                self.status == "EXPIRED" or self.status == "EXPIRED_E" or self.status == "RESERVED_L"):
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

        if self.status == "RESERVED":
            if not self.Date_From.replace(tzinfo=None) <= dt.datetime.now().replace(
                    tzinfo=None) <= self.Date_To.replace(tzinfo=None):
                raise ValidationError('You cannot set state to Reserved in current condiction ')

        if self.status == "RESERVED_L":
            if self.Date_To.replace(tzinfo=None) >= dt.datetime.now().replace(tzinfo=None):
                raise ValidationError('You cannot set state to Reserved_L when Date To is higher than current time ')

        if self.status == "EXPIRED_E":
            if self.Date_To.replace(tzinfo=None) < dt.datetime.now().replace(tzinfo=None):
                raise ValidationError('You cannot set state to EXPIRED_E when Date To is lower than current time ')

    def validate_registration_plate_exists(self, arg):

        print("CAR MODEL STATE TRIGGER validate_registration_plate_exists")

    def validate_plate_booking_duplicate(self, arg):

        print("CAR MODEL STATE TRIGGER validate_plate_booking_duplicate")

        if self.pk is None:

            if not self.registration_plate == "Not provided":

                query = Car.objects.filter(booking=self.booking)
                query = query.filter(
                    Q(booking=self.booking.id) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
                if query.filter(registration_plate=self.old_registration_plate).exists():
                    raise ValidationError("Car with that reservation number:" + str(
                        self.old_registration_plate) + " is on the booking list")


        else:

            if self.registration_plate != "Not provided":

                if self.old_registration_plate != self.registration_plate:

                    query = Car.objects.filter(
                        Q(booking=self.booking.id) & (
                                    Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
                    query = query.exclude(id=self.id)
                    if query.filter(registration_plate=self.registration_plate).exists():
                        raise ValidationError(
                            "Car with that reservation number" + str(self.registration_plate) + "is on "
                                                                                                "the "
                                                                                                "booking list")

        print("clean()CAR MODEL TRIGGER validate_status_check_free_places_registration_placte_exists")

    def clean_exclude_register_plate_exist_and_validate_registration_plate_signs(self, arg):

        print("(clean_EXCLUDING) TRIGGER CAR ACTIVATED")
        from django.core.exceptions import ValidationError
        self.validate_states(self)
        self.validate_if_booking_none(self)
        self.validate_if_place_available_excluded_registration_plate_exists(self)
        self.validate_minutes_min_30(self)
        if self.Date_To.replace(tzinfo=None) <= dt.datetime.now().replace(tzinfo=None):
            raise ValidationError("Value of Date_To must be higher or equal to current time")
        if self.old_status == 'ACTIVE' and self.status == 'RESERVED_L':
            raise ValidationError('You cannot change active reservation to rerserved_L state')
        name = self.registration_plate

    def clean(self):
        from django.core.exceptions import ValidationError

        self.validate_plate_booking_duplicate(self)

        self.validate_if_booking_none(self)
        self.validate_minutes_min_30(self)
        self.validate_registration_plate_signs(self)
        if self.pk is None:
            print("(clean)TRIGGER CAR ACTIVATED CREATING OBJECT")

            self.validate_if_place_available(self)
            self.validate_plate_booking_duplicate(self)
            if self.Date_From.replace(tzinfo=None) < dt.datetime.now().replace(tzinfo=None):
                raise ValidationError('Value of Date From must be higher than current time')

        if not self.pk is None:
            self.validate_plate_booking_duplicate(self)
            self.validate_states(self)
            print("(clean)TRIGGER CAR ACTIVATED UPDATE OBJECT")

        if self.old_status == 'ACTIVE' and self.status == 'RESERVED_L':
            raise ValidationError('You cannot change active reservation to rerserved_L state')
        name = self.registration_plate

    def save(self, *args, **kwargs):

        print("(save)TRIGGER CAR ACTIVATED")

        self.old_status = self.status

        if not self.status == "CANCEL":
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
            Q(booking=Booking.objects.get(pk=self.booking.id)) & Q(status='ACTIVE') | Q(status='RESERVED') | Q(
                status='RESERVED_L'))
        if not car.exists():
            Booking.objects.filter(pk=self.booking.id).update(active=False)
            print("NO dates with that citeria")

        else:
            print("(save)TRIGGER FOR DATE FROM AND DATE TO")
            earliest = car.earliest('Date_From').Date_From
            latest = car.latest('Date_To').Date_To
            Booking.objects.filter(pk=self.booking.id).update(Date_From=earliest)
            Booking.objects.filter(pk=self.booking.id).update(Date_To=latest)

        if self.status == "CANCELLED":
            Car.objects.filter(id=self.id).update(Cost=0)
        Booking.objects.filter(pk=self.booking.id).update(number_of_cars=Car.objects.filter(
            Q(booking=self.booking) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count())

        if Car.objects.filter(
                Q(booking=self.booking) & (
                        Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L') | Q(status='EXPIRED') | Q(
                    status='EXPIRED_E'))).exists():

            Booking.objects.filter(id=self.booking.id).update(Cost=Car.objects.filter(
                Q(booking=self.booking) & (
                        Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L') | Q(status='EXPIRED') | Q(
                    status='EXPIRED_E'))).aggregate(Sum('Cost'))['Cost__sum'])

        else:
            Booking.objects.filter(id=self.booking.id).update(Cost=0)

        if not Car.objects.filter(Q(booking=self.booking) & (
                Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).exists():
            Booking.objects.filter(pk=self.booking.id).update(active=False)


@receiver(pre_delete, sender=Booking)
def model_Booking_delete(sender, instance, **kwargs):
    try:
        print("Receiver for object:" + str(instance.id))
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
    print("presave")

    if instance.pk is None:
        print("Object created")

    if not instance.pk is None:
        print("Object updated")


@receiver(post_save, sender=Booking)
def model_add(sender, instance, **kwargs):
    print("Receiver Model_add called post_save Booking")

    obj = Booking.objects.get(id=instance.id)
    obj.refresh_from_db()

    user = instance.created_by
    l = []
    for g in user.groups.all():
        l.append(g.name)

    if l.__contains__("Client_mobile"):
        return
    else:

        import sys

        for x in range(instance.number_of_cars):
            try:
                Car(registration_plate="Not provided", booking=Booking.objects.get(id=instance.id),
                    Date_From=instance.Date_From,
                    Date_To=instance.Date_To, Cost=instance.get_Cost_single(instance)).clean()

            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        for x in range(instance.number_of_cars):
            Car(registration_plate="Not provided", booking=Booking.objects.get(id=instance.id),
                Date_From=instance.Date_From,
                Date_To=instance.Date_To, Cost=instance.get_Cost_single(instance)).save()

        Booking.objects.filter(id=obj.id).update(Cost=instance.get_Cost_sum(instance))

        print("Reveiver after all")
        Booking.objects.filter(id=obj.id).update(number_of_cars=Car.objects.filter(
            Q(booking=obj) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count())

        b = 2
