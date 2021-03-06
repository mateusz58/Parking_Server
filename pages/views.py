from collections import namedtuple

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from helper.String_processing import is_all_items_unique
from helper.timeConvert import convert_string_date_time
from helper.calculateTimeDifference import is_overlapped
from exceptions.httpExceptionsHandler import FORBIDDEN, STATUS_CHANGE
from templatetags.templatetag import has_group, has_group_v2
from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pages.models import Parking, Booking, Car
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from pages.serializers import User_Serializer, Booking_Serializer, Parking_Serializer, Parking_Serializer_Coordinates, \
    User_Serializer_Login_Email, Booking_Serializer_delete, Car_Serializer, Car_Serializer_update
from users.models import CustomUser
from datetime import datetime

from django.db.models import Q

import logging

log = logging.getLogger(__name__)

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


@login_required
def redirect_view(request):
    user = request.user
    requested_user = user
    l = []
    for g in user.groups.all():
        l.append(g.name)
    query_user_parking = Parking.objects.filter(user_parking__username=user)
    print(query_user_parking.exists())
    permission_classes = (IsAuthenticated,)

    if not l.__contains__("Parking_manager"):
        from django.contrib import messages
        messages.info(request,
                      'You are not authorized to access this section. Contact the administrator to access this section!')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))
    if not query_user_parking.exists():
        from django.contrib import messages
        messages.info(request,
                      'You are not authorized to access this section. Contact the administrator to access this section!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))

    else:
        from django.contrib import messages
        booking_filtered = Booking.objects.filter(parking=query_user_parking)

        response = redirect('/admin/')
        return response


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class User_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer_Login_Email

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Delete_User_View(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer

class User_View_Email_login(CreateAPIView, ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class User_View_Search(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = User_Serializer_Login_Email

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        parking_name_v = self.request.query_params.get('email', None)

        if parking_name_v is not None:
            queryset = queryset.filter(email=parking_name_v)
        return queryset


class Parking_View(CreateAPIView, ListAPIView):
    permission_classes = (ReadOnly,)
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer


class Parking_View_Search(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = Parking_Serializer

    def get_queryset(self):
        queryset = Parking.objects.all()
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
    permission_classes = (ReadOnly,)
    serializer_class = Parking_Serializer

    def get_queryset(self):
        queryset = Parking.objects.all()
        parking_name_v = self.request.query_params.get('parking_name', None)

        if parking_name_v is not None:
            queryset = queryset.filter(parking_name=parking_name_v)
        return queryset

    def test_func(self):
        user = self.request.user
        print("Delete_Parking_View" + str(user))

        return has_group(user, "Parking_manager")


class Booking_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = Booking.objects.all()
    serializer_class = Booking_Serializer

    def perform_create(self, serializer):

        registration_plate_list = str(self.request.META['HTTP_REGISTRATION_PLATE'])
        registration_plate_list = list(registration_plate_list.split(","))

        if int(self.request.data['number_of_cars']) != len(registration_plate_list):
            raise FORBIDDEN("Numbers of cars and registration number must be equal")

        if len(registration_plate_list) > 1:
            if is_all_items_unique(registration_plate_list):
                raise FORBIDDEN("All registration numbers must be different")

        date_from = str(self.request.META['HTTP_DATE_FROM'])
        date_to = str(self.request.META['HTTP_DATE_TO'])
        date_from = convert_string_date_time(date_from)
        date_to = convert_string_date_time(date_to)
        duration = convert_string_date_time(str(self.request.META['HTTP_DATE_TO'])).replace(
            tzinfo=None) - convert_string_date_time(str(self.request.META['HTTP_DATE_FROM'])).replace(tzinfo=None)
        duration_s = duration.total_seconds()
        minutes = divmod(duration_s, 60)[0]
        minutes = int(minutes)
        i = 0
        while i < len(registration_plate_list):
            if not str(registration_plate_list[i]).isalnum():
                raise FORBIDDEN(
                    "Wrong registration number of car,car registration number can consist only of numbers and letters characters")
            if len(registration_plate_list[i]) < 6 or len(registration_plate_list[i]) > 10:
                raise FORBIDDEN("Wrong registration number of car:" + str(registration_plate_list[
                                                                              i]) + ",car registration number must consist of at least 6 characters and maximum 10 characters")
            i = i + 1
        i = 0
        if len(registration_plate_list) < 1:
            log.error("You cannot register register parking place for less than one car")
            raise FORBIDDEN("You cannot register register parking place for less than one car")
        if minutes < 30:
            log.error("You cannot register parking place for less than 30 minutes")
            raise FORBIDDEN("You cannot register parking place for less than 30 minutes")
        if convert_string_date_time(self.request.META['HTTP_DATE_TO']).replace(tzinfo=None) < convert_string_date_time(
                self.request.META['HTTP_DATE_FROM']).replace(tzinfo=None):
            log.error("Value of Date_From must be higher than Date_To")
            raise FORBIDDEN("Value of Date_From must be higher than Date_To")
        if convert_string_date_time(self.request.META['HTTP_DATE_FROM']).replace(tzinfo=None) < datetime.now():
            raise FORBIDDEN("Value of Date_From must be higher than current time")
        if minutes < 30:
            log.error("Value of Date_From must be higher than Date_To")
            raise FORBIDDEN("You cannot register parking place for less than 30 minutes")
        _b1 = Car.objects

        query = _b1.filter(Q(
            booking__parking=self.request.data['parking']) & (
                                   Q(status='ACTIVE') | Q(status='RESERVED') | Q(status='RESERVED_L')))

        Range = namedtuple('Range', ['start', 'end'])
        variations = []
        for record in query:
            r1 = Range(start=date_from,
                       end=date_to)
            r2 = Range(start=record.Date_From.replace(tzinfo=None),
                       end=record.Date_To.replace(tzinfo=None))

            if is_overlapped(r1, r2):
                variations.append(record)

        while i < int(self.request.data['number_of_cars']):

            for x in variations:

                if (x.registration_plate == str(registration_plate_list[i])):
                    log.error("Car with registration number:" + str(
                        registration_plate_list[i]) + " have already registered parking place in that period of time")
                    raise FORBIDDEN("Car with registration number:" + str(
                        registration_plate_list[i]) + " have already registered parking place in that period of time")

            i = i + 1
        i = 0
        sum_after_request = len(variations) + int(self.request.data['number_of_cars'])
        if sum_after_request > Parking.objects.get(id=int(self.request.data['parking'])).number_of_places:
            max_number_places = Parking.objects.get(pk=self.request.data['parking']).number_of_places
            if max_number_places < 0:
                max_number_places = 0
            log.error((
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    max_number_places)))
            raise FORBIDDEN(
                "Not enough free places in that period of time,maximum number of places you can reserve is:" + str(
                    max_number_places))

        modify = serializer.save()

        user_id = CustomUser.objects.get(email=str(self.request.user))
        book = Booking.objects.filter(id=modify.id).update(user=user_id)
        booking_instance = Booking.objects.get(pk=modify.id)
        booking_instance.refresh_from_db()

        Booking.objects.filter(pk=modify.id).update(user=user_id)
        if not int(self.request.data['number_of_cars']) == len(registration_plate_list):
            log.error("Number of provided registration numbers are not equal to number of parking places you want to register ")
            raise FORBIDDEN(
                "Number of provided registration numbers are not equal to number of parking places you want to register ")
        i = 0
        while i < int(self.request.data['number_of_cars']):
            new_car = Car(
                registration_plate=registration_plate_list[i],
                booking=booking_instance,
                Date_From=date_from,
                Date_To=date_to
            )
            new_car.save()
            new_car.refresh_from_db()
            i = i + 1
            user_id = CustomUser.objects.get(email=str(self.request.user))
            user_id.refresh_from_db()
            Booking.objects.filter(id=modify.id).update(user=user_id)
            Booking.objects.filter(id=modify.id).update(active=True)


class Delete_Booking_View(LoginRequiredMixin, UserPassesTestMixin, RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = Booking_Serializer_delete
    model = Booking
    queryset = Booking.objects.all()

    def test_func(self):
        obj = self.get_object()
        if has_group_v2(self.request.user, "Client_mobile"):
            user = self.request.user
            if obj.user == user:

                return True
            else:
                log.error("You do not have permission to view that")
                raise FORBIDDEN("You do not have permission to view that")

        else:
            log.error("You do not have permission to view that")
            raise FORBIDDEN("You do not have permission to view that")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        if not self.request.data['active']:
            count_query_active_cancelled = Car.objects.filter(
                Q(booking=obj) & (Q(status='ACTIVE') | Q(status='CANCELLED'))).count()
            count_query_all = Car.objects.filter(booking=obj).count()
            if count_query_active_cancelled == count_query_all:

                serializer.is_valid(raise_exception=True)
                obj = Booking.objects.get(id=obj.id)
                obj.active = False
                obj.save()
                return Response(serializer.data)

            else:
                log.error("You do not have permission to cancel that bookings")
                raise FORBIDDEN("You do not have permission to cancel that bookings")

        else:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)


class Booking_View_Search(generics.ListAPIView):
    serializer_class = Booking_Serializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        user_v = self.request.query_params.get('user', None)
        if user_v is not None:
            queryset = queryset.filter(user__email=user_v)
        return queryset


class Booking_View_logged(generics.ListAPIView):
    serializer_class = Booking_Serializer
    model = Booking

    def get_queryset(self):
        user = self.request.user
        if has_group(user, "Client_mobile"):
            queryset = Booking.objects.all()
            return queryset.filter(user__email=self.request.user)


class Car_View(generics.ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = Car_Serializer
    model = Car

    def get_queryset(self):
        queryset = Car.objects.all()
        return queryset


class Car_View_logged(generics.ListAPIView):
    serializer_class = Car_Serializer
    model = Car

    def get_queryset(self):
        user = self.request.user
        if has_group(user, "Client_mobile"):

            try:
                car_id = self.request.META['HTTP_CAR_ID']
                id = self.request.META['HTTP_CAR_ID']
                id_booking = self.request.META['HTTP_BOOKING_ID']
                car = Car.objects.get(pk=id)
                car.status = "CANCELLED"
                car.Cost = 0
                car.save()
                raise STATUS_CHANGE("Status has been changed")
            except:
                pass
            finally:
                queryset = Car.objects.all()
                return queryset.filter(booking__user__email=self.request.user)

        queryset = Car.objects.all()
        return queryset.filter(booking__user__email=self.request.user)


class Update_Car_View(LoginRequiredMixin, UserPassesTestMixin, RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Car_Serializer_update
    model = Car
    queryset = Car.objects.all()

    def test_func(self):

        if self.request.method == 'GET':
            print('GET CALLED')

        obj = self.get_object()

        if has_group_v2(self.request.user, "Client_mobile"):
            user = self.request.user
            if obj.booking.user == user:

                return True
            else:
                log.error("You do not have permission to view that")
                raise FORBIDDEN("You do not have permission to view that")

        else:
            log.error("You do not have permission to view that")
            raise FORBIDDEN("You do not have permission to view that")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        if str(self.request.data['status']).__contains__('CANCELLED'):

            try:
                serializer.is_valid(raise_exception=True)
                obj = Car.objects.get(id=obj.id)
                obj.status = 'CANCELLED'
                obj.clean()
                obj.save()
            except:
                log.error("You do not have permission to cancel that bookings")
                raise FORBIDDEN("You do not have permission to cancel that bookings")

            return Response(serializer.data)

        else:
            log.error("Valid operation you can only change status to cancelled")
            raise FORBIDDEN("Valid operation you can only change status to cancelled")
