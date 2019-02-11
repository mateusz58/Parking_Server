import sys
import traceback
from datetime import datetime

from pages.models import Booking, Car

time1 = datetime(2019, 2, 26, 16, 0, 00).replace(tzinfo=None)
time2 = datetime(2019, 2, 28, 16, 30, 00).replace(tzinfo=None)

book = Booking.objects.get(pk=26)

new_car_Test1 = Car(
    registration_plate="regis12",
    booking=book,
    Date_From=time1,
    Date_To=time2

)
new_car_Test1 = Car(
    registration_plate="regis12",
    booking=book,
    Date_From=time1,
    Date_To=time2

)

## TRIGGER TEST

def TRIGGER_test_check_duplicate_registration_place():

def TRIGGER_test_check_if_can_reserve_in_that_period_of_time():

def TRIGGER_test_if_can_add_wrong_registration_plate():

def TRIGGER_test_if_can_reserve_on_full_parking_place():

def TRIGGER_test_if_Date_From_is_different_than_Date_From():

def TRIGGER_test_if_Date_From_is_higher_than_current_time():

def TRIGGER_test_if_can_change_state():


# HTTP RESPONSES


def HTTP_POST_LOGIN()

def HTTP_POST_REGISTER()

def HTTP_POST_BOOK()

def HTTP_PUT_BOOK()









