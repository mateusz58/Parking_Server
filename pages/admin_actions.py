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


def sum_all(modeladmin, request, queryset):
    sum=0
    for book in queryset:
        sum=book.Cost+sum
        book.save()
sum_all.short_description = 'Sum Cost of selected bookings'


# def export_csv(modeladmin, request, queryset):
#
#
#     def get_booking(self,obj):
#         return obj.booking.code
#     def get_id(self, obj):
#         return obj.id
#
#     def get_Cost(self, obj):
#         return obj.booking.Cost
#
#     def get_number(self, obj):
#         return obj.booking.number_of_cars
#
#     def get_user(self, obj):
#         return obj.booking.user
#
#
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="books.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Id', 'Booking id', 'Cost', 'Price', 'Pages', 'Book Type'])
#     books = queryset.values_list = ('get_id','get_booking','Cost','get_Cost','get_number','get_user','Date_From', 'Date_To','registration_plate', 'status')
#
#
#
#     for book in books:
#         writer.writerow(book)
#     return response
# export_csv.short_description = 'Export to csv'