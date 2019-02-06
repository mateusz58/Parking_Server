from django import template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, CreateView
from django.conf.urls import url
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.conf import settings
##from snippets.models import Location
from django.contrib.auth.models import User
##from snippets.serializers import LocationSerializer,UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED
from oauth2client import client, crypt
from rest_framework import routers
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from Basic_Functions.String_processing import check_query_string
from Basic_Functions.Time_convert import convert_string_date_time
from TRIGGERS.FREE_PLACES_UPDATE import free_places_update
from customexceptions import FORBIDDEN
from decorators import group_required
from templatetags.templatetag import has_group
from .filters import UserFilter, BookingFilter
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import authentication_classes, permission_classes
#
from rest_framework import viewsets, permissions, filters, generics, authentication, status, routers
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from pages.models import Parking,Booking
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.parsers import JSONParser
from django.views.generic import TemplateView
from rest_framework.exceptions import APIException
from pages.serializers import User_Serializer, Booking_Serializer, Parking_Serializer, Parking_Serializer_Coordinates, \
    User_Serializer_Login_Email, Booking_Serializer_delete
from users.models import CustomUser
from rest_framework.decorators import api_view
from datetime import datetime

from django.db.models import Q, Sum
import re


#
# class Filter_booking_view(CreateView):
#
#     def filter_booking_view(request):
#         permission_classes = (IsAuthenticated,)
#         booking_list = Booking.objects.all()
#         booking_filter = BookingFilter(request.GET, queryset=booking_list)
#         return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})
#
# def is_member(user):
#     return user.groups.filter(name='Parking_manager').exists()
# class IsParking_Manager(permissions.BasePermission):
#
# @user_passes_test(lambda u: u.groups.filter(name='companyGroup').exists())
#
# ##SNIPPET VIEWSET
#

##HOME PAGE VIEW

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

@login_required
def filter_booking_view(request):
    user=request.user

    requested_user = user
    user_get_id = CustomUser.objects.get(email=requested_user).id
    parking_filtered = Parking.objects.get(user_parking=user_get_id).id
    booking_filtered = Booking.objects.filter(parking=parking_filtered)

    print("filter_booking_view"+str(user))
    permission_classes = (IsAuthenticated,)
    # booking_list = Booking.objects.all()
    booking_filter = BookingFilter(request.GET, queryset=booking_filtered)
    # return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})
    if   user.groups.filter(name='Parking_manager').exists():
        return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))



class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

## JSON VIEWS
# @permission_required('GET_Users_API', raise_exception=True)
class User_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer_Login_Email
    def get(self, request, *args, **kwargs):
     return self.list(request, *args, *kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
# @permission_required('Update_Users_API', raise_exception=True)
class Delete_User_View(RetrieveUpdateDestroyAPIView):
        queryset = CustomUser.objects.all()
        serializer_class = User_Serializer
# @permission_required('GET_Users_API', raise_exception=True)
class User_View_Email_login(CreateAPIView, ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# @permission_required('GET_Users_API', raise_exception=True)
class User_View_Search(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = User_Serializer_Login_Email
    def get_queryset(self):
        queryset =  CustomUser.objects.all()
        parking_name_v = self.request.query_params.get('email', None)

        if parking_name_v is not None:
            queryset = queryset.filter(email=parking_name_v)
        return queryset

# @permission_required('GET_Parking_API', raise_exception=True)
class Parking_View(CreateAPIView, ListAPIView):
    permission_classes = (ReadOnly,)
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer

# @permission_required('GET_Parking_API', raise_exception=True)
class Parking_View_Search(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = Parking_Serializer
    def get_queryset(self):
        queryset =  Parking.objects.all()
        parking_name_v = self.request.query_params.get('parking_name', None)

        if parking_name_v is not None:
            queryset = queryset.filter(parking_name=parking_name_v)
        return queryset


class Parking_View_Coordinates(CreateAPIView, ListAPIView):
    permission_classes = (ReadOnly,)
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer_Coordinates
    def get(self, request, *args, **kwargs):
     return self.list(request, *args, *kwargs)

class Delete_Parking_View(RetrieveUpdateAPIView):
        permission_classes = (IsAuthenticated,)
        queryset = Parking.objects.all()
        serializer_class = Parking_Serializer
        def test_func(self):
            user=self.request.user
            print("Delete_Parking_View"+str(user))
            return has_group(user, "Parking_manager")

class Booking_View(CreateAPIView,ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = Booking.objects.all()
    serializer_class = Booking_Serializer
    def perform_create(self, serializer):
        duration =convert_string_date_time(self.request.data['Date_To']).replace(tzinfo=None)-convert_string_date_time(self.request.data['Date_From']).replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        print("Minutes"+str(minutes))
        if not str(self.request.data['registration_plate']).isalnum():
            raise FORBIDDEN("Wrong registration number of car,car registration number can consist only of numbers and letters characters")
        if len(str(self.request.data['registration_plate']))<6:
            raise FORBIDDEN("Wrong registration number of car,car registration number must consist of at least 6 characters and maximum 10 characters")
        if len(str(self.request.data['registration_plate']))>10:
            raise FORBIDDEN("Wrong registration number of car,car registration number must consist of at least 6 characters and maximum 10 characters")
        if self.request.data['number_of_cars'] < 1:
            raise FORBIDDEN("You cannot register register parking place for less than one car")
        if minutes < 30:
            raise FORBIDDEN("You cannot register parking place for less than 30 minutes")
        if convert_string_date_time(self.request.data['Date_To']).replace(tzinfo=None)<convert_string_date_time(self.request.data['Date_From']).replace(tzinfo=None):
            raise FORBIDDEN("Value of Date_From must be higher than Date_To")
        if convert_string_date_time(self.request.data['Date_From']).replace(tzinfo=None)<datetime.now():
            raise FORBIDDEN("Value of Date_From must be higher than current time")
        if minutes < 30:
            raise FORBIDDEN("You cannot register parking place for less than 30 minutes")
        _b1 = Booking.objects
        w1 = _b1.filter(Q(Date_From__lt=convert_string_date_time(self.request.data['Date_From'])) & Q(Date_To__gt=convert_string_date_time(self.request.data['Date_From'])) & Q(parking=self.request.data['parking']) & (
            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w2= _b1.filter(Q(Date_From__gt=convert_string_date_time(self.request.data['Date_From'])) & Q(Date_To__lt=convert_string_date_time(self.request.data['Date_To'])) & Q(parking=self.request.data['parking']) & (
            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w3=_b1.filter(Q(Date_From__lt=convert_string_date_time(self.request.data['Date_To'])) & Q(Date_To__gt=convert_string_date_time(self.request.data['Date_To'])) & Q(parking=self.request.data['parking']) & (
            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        w4 = _b1.filter(Q(Date_From__lt=convert_string_date_time(self.request.data['Date_From'])) & Q(Date_To__gt=convert_string_date_time(self.request.data['Date_To'])) & Q(
            parking=self.request.data['parking']) & (
                            Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))
        variations = [w1, w2, w3, w4]
        i=0

        if w1.filter(registration_plate=self.request.data['registration_plate']).exists():
            raise FORBIDDEN("Car with registration number:"+str(self.request.data['registration_plate'])+" have already registered parking place in that period of time")

        if w2.filter(registration_plate=self.request.data['registration_plate']).exists():
            raise FORBIDDEN("Car with registration number:"+str(self.request.data['registration_plate'])+" have already registered parking place in that period of time")

        if w3.filter(registration_plate=self.request.data['registration_plate']).exists():
            raise FORBIDDEN("Car with registration number:"+str(self.request.data['registration_plate'])+" have already registered parking place in that period of time")

        if w4.filter(registration_plate=self.request.data['registration_plate']).exists():
            raise FORBIDDEN("Car with registration number:"+str(self.request.data['registration_plate'])+" have already registered parking place in that period of time")

        sum=0
        while i < len(variations):
             sum=sum+check_query_string(variations[i])
             i += 1
        sum_after_request=sum+self.request.data['number_of_cars']

        if sum_after_request>Parking.objects.get(pk=self.request.data['parking']).number_of_places:
            raise FORBIDDEN("Not enough free places in that period of time,maximum number of places you can reserve is:"+str(Parking.objects.get(pk=self.request.data['parking']).number_of_places-sum))
        ### FREE PLACES  ALGORITHM NOW
        modify = serializer.save()

        print("MODIFY"+modify)



class Delete_Booking_View(LoginRequiredMixin, UserPassesTestMixin,RetrieveUpdateAPIView):

        permission_classes = (IsAuthenticated | ReadOnly,)
        serializer_class = Booking_Serializer_delete
        model = Booking
        fields = ['code']
        queryset = Booking.objects.all()
        def test_func(self):
            obj = self.get_object()
            print("obj.user  VALUE:"+str(obj.user)+"CustomUser.objects.get(email=self.request.user).id VALUE"+str(CustomUser.objects.get(email=self.request.user).email))
            print("obj.status  VALUE:" + str(obj.status))
            return str(obj.user) == str(CustomUser.objects.get(email=self.request.user).email)
        def perform_update(self, serializer):
            obj = self.get_object()
            #### FREE PLACES UPDATE ALGORITHM NOW
            if has_group(CustomUser.objects.get(pk=self.request.data['user']).email, "Parking_manager"):
                if str(self.request.data['status']) == "CANCELLED":
                    if str(obj.status) == "CANCELLED":
                        raise FORBIDDEN("Error cannot cancel that reservation ")
                    if str(obj.status) == "EXPIRED":
                        raise FORBIDDEN("Error cannot cancel that reservation ")
                    if str(obj.status) == "RESERVED":
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                    if str(obj.status) == "EXPIRED_E":
                        raise FORBIDDEN("Error cannot cancel that reservation ")
                    if str(obj.status) == "RESERVED_L":
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                    else:
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()

                if str(self.request.data['status']) == "RESERVED":
                    if str(obj.status) == "ACTIVE":
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                    else:
                        raise FORBIDDEN("Error cannot change state to RESERVED")

                if str(self.request.data['status']) == "EXPIRED_E":
                    if str(obj.status) == "RESERVED":
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                    else:
                        raise FORBIDDEN("Error cannot change state to EXPIRED_E")

                if str(self.request.data['status']) == "RESERVED_L":
                    if str(obj.status) == "RESERVED":
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                    else:
                        raise FORBIDDEN("Error cannot change state to RESERVED_L")

            if has_group(CustomUser.objects.get(pk=self.request.data['user']).email, "Client_mobile"):
                if str(self.request.data['status']) == "CANCELLED":
                    if str(obj.status) == "ACTIVE":
                        free_places_update(self.request.data['parking'])
                        serializer.save()
                    else:
                        free_places_update(self.request.data['parking'])
                        print("UPDATE status:" + str(self.request.data['status']))
                        raise FORBIDDEN("Error cannot cancel that reservation ")
                        ## FREE PLACES ALGORIITHM
                        serializer.save()
                else:
                    raise FORBIDDEN("Internal error: wrong body request  ")


# @permission_required('GET_booking_API', raise_exception=True)
class Booking_View_Search(generics.ListAPIView):
    serializer_class = Booking_Serializer
    def get_queryset(self):
        queryset =  Booking.objects.all()
        user_v = self.request.query_params.get('user', None)
        if user_v is not None:
            queryset = queryset.filter(user__email=user_v)
        return queryset

class Booking_View_logged(generics.ListAPIView):
        serializer_class = Booking_Serializer
        model = Booking
        def get_queryset(self):
            user=self.request.user
            if has_group(self.request.user, "Client_mobile"):
                queryset = Booking.objects.all()
                return queryset.filter(user__email=self.request.user)





#





