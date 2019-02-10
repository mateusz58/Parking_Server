from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite, ModelAdmin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy

from pages.models import Parking, Booking, Car
from users.models import CustomUser
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

#
class Parking_managemnt(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Parking management system')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Parking management system')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Parking management system')


class Parking_Admin(admin.ModelAdmin):


    list_display = ['parking_name', 'parking_Street', 'parking_City', 'free_places','number_of_places','HOUR_COST']
    ordering = ['parking_name']
    search_fields = ('parking_name', 'parking_Street','parking_City')
    list_filter = ('parking_name', 'parking_Street', 'parking_City')

    def Parking_city_order(modeladmin, request, queryset):
        Parking.ordering = ['parking_City']
        modeladmin.Parking_city_order.short_description = "Order by city name"

class Booking_admin(admin.ModelAdmin):
        # list_display = ['code', 'parking','Date_From','Date_To','Cost','registration_plate','status']
        list_display = ['code','user','parking', 'Cost','number_of_cars']
        # search_fields = ('code','user__email','parking__parking_name','registration_plate','status')
        list_filter = ('user','parking__parking_name',)

        def get_readonly_fields(self, request, obj=None):
            if obj:
                return ['number_of_cars', 'parking']
            else:
                return []

class Car_admin(admin.ModelAdmin):

    list_display = ['get_id','get_booking','Cost','get_Cost','get_number','get_user','Date_From', 'Date_To','registration_plate', 'status',]
    ordering = ['Date_From']
    search_fields = ('Date_From', 'Date_To', 'booking', 'registration_plate')
    list_filter = ('status',)

    list_totals = [('Cost', lambda field: Coalesce(Sum(field), 0)), ]

    list_filter = (
        ('Date_From', DateTimeRangeFilter), ('Date_To', DateTimeRangeFilter),
    )


    # list_display = ['Cost','Date_From', 'Date_To',
    #                 'registration_plate', 'status', ]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['booking','Date_To','Date_From']
        else:
            return []
    def get_booking(self,obj):
        return obj.booking.code
    def get_id(self, obj):
        return obj.id

    def get_Cost(self, obj):
        return obj.booking.Cost

    def get_number(self, obj):
        return obj.booking.number_of_cars

    def get_user(self, obj):
        return obj.booking.user
    get_booking.short_description='Kod'
    get_Cost.admin_order_field = 'Cost'  # Allows column order sorting
    get_Cost.short_description = 'Cost booking'  # Renames column head
    get_user.short_description='User'
    get_id.short_description='Car id'
    get_number.short_description='Number of Cars'

    def Date_order(modeladmin, request, queryset):
        Car.ordering = ['Date_From']
        modeladmin.Parking_city_order.short_description = "Order by Date From"

from django.contrib import admin
from .models import SaleSummary

admin.site.register(Parking,Parking_Admin)
admin.site.register(Booking,Booking_admin)
admin.site.register(Car,Car_admin)


# admin.site.site_header = "'Parking management system'"
# admin.site.site_title = "'Parking management system'"
# admin.site.index_title = "'Parking management system'"





