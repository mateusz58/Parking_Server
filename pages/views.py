from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf.urls import url
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse
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
from .filters import UserFilter, BookingFilter

#
from rest_framework import viewsets, permissions, filters, generics, authentication, status, routers
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView

from pages.models import Parking,Booking


from django.views.generic import TemplateView

from pages.serializers import User_Serializer, Booking_Serializer, Parking_Serializer, Parking_Serializer_Coordinates, \
    User_Serializer_Login_Email
from users.models import CustomUser


##HOME PAGE VIEW

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

def filter_user_view(request):
    user_list = CustomUser.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'filter/user_list_v2.html', {'filter': user_filter})



def filter_booking_view(request):
    booking_list = Booking.objects.all()
    booking_filter = BookingFilter(request.GET, queryset=booking_list)
    return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})


### FUNCTION THAT RETURNS LOGIN
# @login_required
# def index_view(request):
#    p = Model.objects.filter(user=request.user)
#    return render(request, 'app/index.html', {'objects': p})


### Custom search view



## JSON VIEWS

class User_View(CreateAPIView, ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer_Login_Email

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
    serializer_class = User_Serializer
    def get_queryset(self):
        queryset =  CustomUser.objects.all()
        parking_name_v = self.request.query_params.get('email', None)

        if parking_name_v is not None:
            queryset = queryset.filter(login=parking_name_v)
        return queryset
class Booking_View_Search(generics.ListAPIView):
    serializer_class = Booking_Serializer
    def get_queryset(self):
        queryset =  Booking.objects.all()
        code_v = self.request.query_params.get('code', None)

        if code_v is not None:
            queryset = queryset.filter(code=code_v)
        return queryset
class Parking_View_Search(generics.ListAPIView):
    serializer_class = Parking_Serializer

    def get_queryset(self):
        queryset =  Parking.objects.all()
        parking_name_v = self.request.query_params.get('parking_name', None)

        if parking_name_v is not None:
            queryset = queryset.filter(parking_name=parking_name_v)
        return queryset
class Parking_View_Coordinates(CreateAPIView, ListAPIView):
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer_Coordinates

class Parking_View(CreateAPIView, ListAPIView):
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer

class Delete_Parking_View(RetrieveUpdateDestroyAPIView):
        queryset = Parking.objects.all()
        serializer_class = Parking_Serializer



class Booking_View(CreateAPIView, ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = Booking_Serializer


class Delete_Booking_View(LoginRequiredMixin, UserPassesTestMixin,RetrieveUpdateDestroyAPIView):
        queryset = Booking.objects.all()
        serializer_class = Booking_Serializer
        model = Booking
        fields = ['code']

        def test_func(self):
            obj = self.get_object()
            return obj.code == self.request.user

