from django.core.exceptions import ValidationError


def validate_if_booking_none(self, arg):
    print("CAR MODEL STATE TRIGGER validate_if_booking_none")

    if self.booking is None:
        raise ValidationError("You must assign Booking value")

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
    if sum_after_request > Parking.objects.get(pk=self.booking.parking.id).number_of_places
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

def validate_registration_plate_exists(self, arg):
    print("CAR MODEL STATE TRIGGER validate_registration_plate_exists")

    query = Car.objects.filter(booking=self.booking)

    query = query.filter(
        Q(booking=self.booking.id) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
    if query.filter(registration_plate=self.registration_plate).exists():
        return True
    else:
        return False

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
            self.status == "EXPIRED" or self.status == "EXPIRED_E" or self.status == "RESERVED_L" or self.status == "RESERVED"):
        raise ValidationError("You cannot change state CANCELLED to: " + str(self.status))

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

    if self.status == "RESERVED_L":
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) >= dt.datetime.now().replace(second=0,
                                                                                                           microsecond=0):
            raise ValidationError('You cannot set state to Reserved_L when Date To is higher than current time ')

    if self.status == "EXPIRED_E":
        if self.Date_To.replace(tzinfo=None).replace(second=0, microsecond=0) < dt.datetime.now().replace(second=0,
                                                                                                          microsecond=0):
            raise ValidationError('You cannot set state to EXPIRED_E when Date To is lower than current time ')

def validate_status_check_free_places_registration_placte_exists(self, arg):
    print("clean()CAR MODEL TRIGGER validate_status_check_free_places_registration_placte_exists")

    qs = Car.objects.filter(pk=self.id)
    if self.pk is not None:
        qs = qs.exclude(pk=self.pk)
    if qs.exists():
        if (self.old_status == "CANCELLED" or self.old_status == "EXPIRED_E" or self.old_status == "EXPIRED") and (
                self.state == "ACTIVE" or self.state == "RESERVED" or self.state == "RESERVED_L"):
            if self.validate_registration_plate_exists(self):
                raise ValidationError(
                    'Car with registration number: ' + str(self.registration_plate) + "is already on that booking")
            self.validate_if_place_available(self)



