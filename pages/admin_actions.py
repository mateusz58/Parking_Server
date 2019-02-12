import csv
import decimal

from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy
from django.db.models import F
from pages.models import Parking, Booking, Car
from users.models import CustomUser


# def sum_all(modeladmin, request, queryset):
#     sum=0
#     for book in queryset:
#         sum=book.Cost+sum
#         book.save()
# sum_all.short_description = 'Sum Cost of selected bookings'
#
#

def make_active(Car_admin, request, queryset):

    # queryset.update(status='ACTIVE')
    make_active.short_description = "Mark selected reservations as ACTIVE"


def make_cancelled(Car_admin, request, queryset):
    # queryset.update(status='CANCELLED')
    make_active.short_description = "Mark selected reservations as CANCELLED"

def make_expired(Car_admin, request, queryset):

    queryset.update(status='EXPIRED')
    make_active.short_description = "Mark selected reservations as EXPIRED"


def make_reserved(Car_admin, request, queryset):
    # queryset.update(status='EXPIRED_E')
    make_active.short_description = "Mark selected reservations as RESERVED"



def make_expired_e(Car_admin, request, queryset):
    # queryset.update(status='RESERVED_L')
    make_active.short_description = "Mark selected reservations as EXPIRED_E"

def make_reserved_l(Car_admin, request, queryset):
    # queryset.update(status='RESERVED')
    print(str(request))
    make_active.short_description = "Mark selected reservations as RESERVED_L"


def Booking_set_inactive(Car_admin, request, queryset):
    # queryset.update(status='RESERVED')
    queryset.update(active=False)










