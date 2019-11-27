from admin_totals.admin import ModelAdminTotals
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db.models import Q
from rangefilter.filter import DateTimeRangeFilter

from pages.adminActions import make_active, make_cancelled, make_expired, make_reserved, make_expired_e, \
    make_reserved_l
from pages.models import Parking, Booking, Car
from users.models import CustomUser


class Tabular_Cars(admin.TabularInline):
    model = Car
    extra = 5

    list_display = ['Cost', 'Date_From', 'Date_To',
                    'registration_plate', 'status', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'booking', 'Cost']
        else:
            return []

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'Car id'
    proxy = False

    def get_formset(self, request, obj=None, **kwargs):

        if obj is None:
            print("Tabular cars initiate")
            Tabular_Cars.proxy = True
            obj = 0
            return super(Tabular_Cars, self).get_formset(request, obj, **kwargs)
        else:
            print("Tabular cars else")
            self.booking = obj
            self.temp = self.booking

            Tabular_Cars.proxy = False
            return super(Tabular_Cars, self).get_formset(request, obj, **kwargs)

    def get_max_num(self, request, obj=None, **kwargs):

        if obj == 0:
            return 0
        if obj is None:
            return 0
        else:
            try:
                print("Tabular get_max_num cars Called when adding:" + str(self.temp))
                self.max_num = Booking.objects.get(pk=self.temp).number_of_cars
                return self.max_num
            except Exception as e:
                print("Exception get_max_num:" + str(e))
                return 0

    def get_extra(self, request, obj=None, **kwargs):

        if obj:
            return 0
        return self.extra


class Parking_Admin(admin.ModelAdmin):
    list_display = ['id', 'parking_name', 'parking_Street', 'parking_City', 'free_places', 'number_of_places',
                    'HOUR_COST']
    ordering = ['parking_name']
    search_fields = ('parking_name', 'parking_Street', 'Tabular cars obj:parking_City')
    list_filter = ('parking_name', 'parking_Street', 'parking_City')

    def get_queryset(self, request):

        user = request.user

        query = CustomUser.objects.filter(username=user).get().username

        l = []

        for g in request.user.groups.all():
            l.append(g.name)

        if l.__contains__("Parking_manager"):

            return Parking.objects.filter(user_parking=user)

        else:
            return Parking.objects.all()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['parking_Street', 'parking_City', 'parking_name', 'number_of_places', 'x', 'y', 'user_parking', ]
        else:
            return []

    def Parking_city_order(modeladmin, request, queryset):
        Parking.ordering = ['parking_City']
        modeladmin.Parking_city_order.short_description = "Order by city name"


class Booking_admin(AdminAdvancedFiltersMixin, ModelAdminTotals, admin.ModelAdmin):
    model = Booking
    inlines = [Tabular_Cars]
    list_totals = [('Cost', lambda field: Coalesce(Sum(field), 0)), ]
    list_display = ['Cost']

    list_display = ['id', 'user', 'parking', 'Cost', 'number_of_cars', 'active', 'Date_From', 'Date_To', ]
    search_fields = ('id', 'user__email',)
    list_filter = (
        ('Date_From', DateTimeRangeFilter), ('Date_To', DateTimeRangeFilter), ('active')
    )

    advanced_filter_fields = (
        'Cost',
        'active',
        'number_of_cars',
        'user__email',

    )

    def save_formset(self, request, form, formset, change=True):
        change = True
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

    def after_saving_model_and_related_inlines(self, obj):
        car_count = Car.objects.filter(
            Q(booking=obj.id) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count()

        if Booking.objects.filter(id=obj.id).exists():
            Booking.objects.filter(id=obj.id).update(number_of_cars=car_count)
            return obj
        else:
            return obj

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        Booking.objects.filter(id=obj.id).update(number_of_cars=Car.objects.filter(
            Q(booking=obj) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count())
        return super(Booking_admin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        Booking.objects.filter(id=obj.id).update(number_of_cars=Car.objects.filter(
            Q(booking=obj) & (Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L'))).count())
        return super(Booking_admin, self).response_change(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        name = Parking.objects.get(user_parking=request.user).parking_name
        if db_field.name == "parking":
            kwargs["queryset"] = Parking.objects.filter(parking_name__exact=str(name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):

        user = request.user

        query = CustomUser.objects.filter(username=user).get().username

        l = []

        for g in request.user.groups.all():
            l.append(g.name)

        if l.__contains__("Parking_manager"):

            return Booking.objects.filter(parking__user_parking=user)

        else:
            return Booking.objects.all()

    def get_id(self, obj):
        return obj.id

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['parking', 'number_of_cars', 'Date_From', 'Date_To']
        else:
            return []


class Car_admin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    actions = [make_active, make_cancelled, make_expired, make_reserved, make_expired_e, make_reserved_l]
    list_display = ['get_id', 'get_booking', 'Cost', 'get_Cost', 'get_number', 'get_user',
                    'registration_plate', 'status', 'Date_From', 'Date_To', ]
    ordering = ['Date_From']
    search_fields = ('id', 'registration_plate',)
    list_filter = ('status',)
    list_totals = [('Cost', lambda field: Coalesce(Sum(field), 0)), ]
    list_filter = (
        ('Date_From', DateTimeRangeFilter), ('Date_To', DateTimeRangeFilter), ('status'),
    )

    advanced_filter_fields = (
        'Cost',
        'status',
        'registration_plate',
    )

    def get_queryset(self, request):

        user = request.user

        query = CustomUser.objects.filter(username=user).get().username

        l = []

        for g in request.user.groups.all():
            l.append(g.name)

        if l.__contains__("Parking_manager"):

            return Car.objects.filter(booking__parking__user_parking=user)

        else:
            return Car.objects.all()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['booking', 'Date_To', 'Date_From', ]
        else:
            return ['status']

    def get_booking(self, obj):
        return obj.booking.id

    def get_id(self, obj):
        return obj.id

    def get_Cost(self, obj):
        return obj.booking.Cost

    def get_number(self, obj):
        return obj.booking.number_of_cars

    def get_user(self, obj):
        return obj.booking.user

    get_booking.short_description = 'Kod'
    get_Cost.admin_order_field = 'Cost'
    get_Cost.short_description = 'Cost booking'
    get_user.short_description = 'User'
    get_id.short_description = 'Car id'
    get_number.short_description = 'Number of Cars'

    def Date_order(modeladmin, request, queryset):
        Car.ordering = ['Date_From']
        modeladmin.Parking_city_order.short_description = "Order by Date From"


from django.db.models import Sum
from django.db.models.functions import Coalesce

from django.contrib import admin

admin.site.register(Parking, Parking_Admin)
admin.site.register(Booking, Booking_admin)
admin.site.register(Car, Car_admin)

admin.site.disable_action('delete_selected')

admin.sites.AdminSite.site_header = 'Parking management system'
admin.sites.AdminSite.site_title = 'Parking management system'
admin.sites.AdminSite.index_title = 'Parking management system'
