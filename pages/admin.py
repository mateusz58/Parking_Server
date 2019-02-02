from django.contrib import admin

# Register your models here.
from pages.models import Parking, Booking
from users.models import CustomUser


class Parking_Admin(admin.ModelAdmin):
    list_display = ['parking_name', 'parking_Street', 'parking_City', 'free_places','HOUR_COST']
    ordering = ['parking_name']
    search_fields = ('parking_name', 'parking_Street','parking_City')
    list_filter = ('parking_name', 'parking_Street', 'parking_City')

    def Parking_city_order(modeladmin, request, queryset):
        Parking.ordering = ['parking_City']
        modeladmin.Parking_city_order.short_description = "Order by city name"

class Booking_admin(admin.ModelAdmin):
        list_display = ['code', 'parking', 'user', 'Date_From','Date_To','Cost','registration_plate','status']
        ordering = ['Date_From']
        search_fields = ('code','user__email','parking__parking_name','registration_plate','status')
        list_filter = ('user','parking__parking_name','status')


admin.site.register(Parking,Parking_Admin)
admin.site.register(Booking,Booking_admin)
