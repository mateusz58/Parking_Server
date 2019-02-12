import random

from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite, ModelAdmin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import forms
from django.urls import resolve
from django.utils.translation import ugettext_lazy

from djangox_project.logger import logger
from pages.admin_actions import make_active, make_cancelled, make_expired, make_reserved, make_expired_e, \
    make_reserved_l, Booking_set_inactive
from pages.forms import Booking_Form
from pages.models import Parking, Booking, Car
from users.models import CustomUser
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

#

from merged_inlines.admin import MergedInlineAdmin


class Tabular_Cars(admin.TabularInline):
    model = Car
    extra = 8

    list_display = ['get_id','Cost', 'Date_From', 'Date_To',
                    'registration_plate', 'status','get_number', ]

    # list_display = ['Cost','Date_From', 'Date_To',
    #                 'registration_plate', 'status', ]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['booking', 'Date_To', 'Date_From']
        else:
            return []

    def get_number(self, obj):
        return obj.booking.number_of_cars

    get_number.short_description = 'Number of Cars'

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ['parking', 'number_of_cars', 'Date_From', 'Date_To']
    #     else:
    #         return []



    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'Car id'



    def get_formset(self, request, obj=None, **kwargs):
        print("obj value:" + str(obj))
        Tabular_Cars.obj = obj
        print("Tabular cars obj:" + str(Tabular_Cars.obj))
        if obj is None:
            obj = 0
            return super(Tabular_Cars, self).get_formset(request, obj, **kwargs)
        else:
            self.booking = obj
            return super(Tabular_Cars, self).get_formset(request, obj, **kwargs)

    def get_max_num(self, request, obj=None, **kwargs):

        if obj == 0:
            return 0
        else:
            self.max_num = self.booking.number_of_cars
            return self.max_num

    def get_min_num(self, request, obj=None, **kwargs):
        if obj == 0:
            return 0
        else:
            # print("PARENT min_num" + str(self.booking.number_of_cars))
            self.min_num = self.booking.number_of_cars
            return self.min_num



class Parking_managemnt(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Parking management system')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Parking management system')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Parking management system')


class Parking_Admin(admin.ModelAdmin):
    list_display = ['id','parking_name', 'parking_Street', 'parking_City', 'free_places', 'number_of_places', 'HOUR_COST']
    ordering = ['parking_name']
    search_fields = ('parking_name', 'parking_Street', 'parking_City')
    list_filter = ('parking_name', 'parking_Street', 'parking_City')



    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['parking_Street', 'parking_City', 'parking_name', 'number_of_places', 'x', 'y', 'user_parking', ]
        else:
            return []

    def Parking_city_order(modeladmin, request, queryset):
        Parking.ordering = ['parking_City']
        modeladmin.Parking_city_order.short_description = "Order by city name"


class Booking_admin(admin.ModelAdmin):
    model = Booking
    inlines = [Tabular_Cars]
    actions = [Booking_set_inactive]
    # list_display = ['code', 'parking','Date_From','Date_To','Cost','registration_plate','status']
    list_display = ['code', 'Date_From', 'Date_To', 'user', 'parking', 'Cost', 'number_of_cars', 'active', ]
    search_fields = ('code', 'user__email',)
    list_filter = (
        ('Date_From', DateTimeRangeFilter), ('Date_To', DateTimeRangeFilter), ('active')
    )



    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['parking', 'number_of_cars', 'Date_From', 'Date_To']
        else:
            return []


class Car_admin(admin.ModelAdmin):
    actions = [make_active, make_cancelled, make_expired, make_reserved, make_expired_e, make_reserved_l]
    list_display = ['get_id', 'get_booking', 'Cost', 'get_Cost', 'get_number', 'get_user', 'Date_From', 'Date_To',
                    'registration_plate', 'status', ]
    ordering = ['Date_From']
    search_fields = ('registration_plate',)
    list_filter = ('status',)
    list_totals = [('Cost', lambda field: Coalesce(Sum(field), 0)), ]
    list_filter = (
        ('Date_From', DateTimeRangeFilter), ('Date_To', DateTimeRangeFilter), ('status'),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # list_display = ['Cost','Date_From', 'Date_To',
    #                 'registration_plate', 'status', ]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['booking', 'Date_To', 'Date_From','registration_plate',]
        else:
            return ['status']

    def get_booking(self, obj):
        return obj.booking.code

    def get_id(self, obj):
        return obj.id

    def get_Cost(self, obj):
        return obj.booking.Cost

    def get_number(self, obj):
        return obj.booking.number_of_cars

    def get_user(self, obj):
        return obj.booking.user

    get_booking.short_description = 'Kod'
    get_Cost.admin_order_field = 'Cost'  # Allows column order sorting
    get_Cost.short_description = 'Cost booking'  # Renames column head
    get_user.short_description = 'User'
    get_id.short_description = 'Car id'
    get_number.short_description = 'Number of Cars'

    def Date_order(modeladmin, request, queryset):
        Car.ordering = ['Date_From']
        modeladmin.Parking_city_order.short_description = "Order by Date From"


from django.contrib import admin

admin.site.register(Parking, Parking_Admin)
admin.site.register(Booking, Booking_admin)
admin.site.register(Car, Car_admin)

admin.sites.AdminSite.site_header = 'Parking management system'
admin.sites.AdminSite.site_title = 'Parking management system'
admin.sites.AdminSite.index_title = 'Parking management system'

# admin.site.site_header = "'Parking management system'"
# admin.site.site_title = "'Parking management system'"
# admin.site.index_title = "'Parking management system'"
