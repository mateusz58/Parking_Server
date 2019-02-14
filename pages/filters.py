from django import forms
from django.contrib.auth.models import User,Group
import django_filters

from pages.models import Booking
from users.models import CustomUser


# class UserFilter(django_filters.FilterSet):
#     # username = django_filters.CharFilter(lookup_expr='icontains')
#     # date_joined = django_filters.NumberFilter(lookup_expr='year')
#     # date_joined = django_filters.NumberFilter(lookup_expr='month')
#     # # date_joined = django_filters.NumberFilter(lookup_expr='time')
#     # ##year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
#     # # year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__gt')
#     # # year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__lt')
#     class Meta:
#         model = CustomUser
#         fields = {
#             'username': ['icontains', ],
#             'date_joined': ['year', 'year__gt', 'year__lt', ],
#             'date_joined': ['month', 'month__gt', 'month__lt', ],
#             'date_joined': ['day', 'day__gt', 'day__lt', ],
#         }
class UserFilter(django_filters.FilterSet):
    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    ##year_joined = django_filters.NumberFilter(lookup_expr='year')
    date_joined = django_filters.NumberFilter(field_name='date_joined',lookup_expr='year')
    groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = {
            'username': ['exact', ],
            'first_name': ['exact', ],
            'last_name': ['exact', ],
            'date_joined': ['exact', ],
        }




class BookingFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id',lookup_expr='icontains')
    # registration_plate = django_filters.CharFilter(field_name='registration_plate',lookup_expr='icontains')
    Cost=django_filters.NumberFilter()
    # release_year_From = django_filters.NumberFilter(field_name='Date_From', lookup_expr='year')
    # release_year__gt_From = django_filters.NumberFilter(field_name='Date_From', lookup_expr='year__gt')
    # release_year__lt_From = django_filters.NumberFilter(field_name='Date_From', lookup_expr='year__lt')

    # release_year_To = django_filters.NumberFilter(field_name='Date_To', lookup_expr='year')
    # release_year__gt_To = django_filters.NumberFilter(field_name='Date_To', lookup_expr='year__gt')
    # release_year__lt_To = django_filters.NumberFilter(field_name='Date_To', lookup_expr='year__lt')

    user__email = django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_name= django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_Street=django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_City=django_filters.CharFilter(lookup_expr='icontains')



    class Meta:

        model = Booking



        fields = ['id', 'parking','user','Cost',]
        # fields = {
        #     'code': ['exact',],
        #     'parking': ['icontains',],
        #     'user': ['icontains',],
        #     'Date_From': ['exact',],
        #     'Date_To': ['exact',],
        #     'Cost': ['exact',],
        #     'registration_plate': ['icontains',],
        #     'status': ['exact',],
        #
        # }


        # class BookingFilter(django_filters.FilterSet):
#         class Meta:
#             model = Booking
#             fields = ['code', 'parking', 'parking__parking_Street', 'parking__parking_City',
#                       'parking__free_places' 'user', 'Date_From', 'Date_To', 'Cost', 'registration_plate']