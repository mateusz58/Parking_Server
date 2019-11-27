from django import forms
from django.contrib.auth.models import User, Group
import django_filters

from pages.models import Booking
from users.models import CustomUser


class UserFilter(django_filters.FilterSet):
    date_joined = django_filters.NumberFilter(field_name='date_joined', lookup_expr='year')
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
    id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    Cost = django_filters.NumberFilter()
    user__email = django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_name = django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_Street = django_filters.CharFilter(lookup_expr='icontains')
    parking__parking_City = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Booking
        fields = ['id', 'parking', 'user', 'Cost', ]
