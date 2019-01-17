from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
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
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import authentication_classes, permission_classes
#
from rest_framework import viewsets, permissions, filters, generics, authentication, status, routers
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from pages.models import Parking,Booking


from django.views.generic import TemplateView

from pages.serializers import User_Serializer, Booking_Serializer, Parking_Serializer, Parking_Serializer_Coordinates, \
    User_Serializer_Login_Email
from users.models import CustomUser



###SNIPPET VIEWSET

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = User_Serializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('created').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)



##HOME PAGE VIEW

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

def filter_user_view(request):
        permission_classes = (IsAuthenticated,)
        user_list = CustomUser.objects.all()
        user_filter = UserFilter(request.GET, queryset=user_list)
        return render(request, 'filter/user_list_v2.html', {'filter': user_filter})


# class Filter_booking_view(CreateView):
#
#     def filter_booking_view(request):
#         permission_classes = (IsAuthenticated,)
#         booking_list = Booking.objects.all()
#         booking_filter = BookingFilter(request.GET, queryset=booking_list)
#         return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})
#


@login_required
def filter_booking_view(request):
    permission_classes = (IsAuthenticated,)
    booking_list = Booking.objects.all()
    booking_filter = BookingFilter(request.GET, queryset=booking_list)
    return render(request, 'filter/booking_list_v2.html', {'filter': booking_filter})


### FUNCTION THAT RETURNS LOGIN
# @login_required
# def index_view(request):
#    p = Model.objects.filter(user=request.user)
#    return render(request, 'app/index.html', {'objects': p})


### Custom search view

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

## JSON VIEWS

class User_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = User_Serializer
    def get_queryset(self):
        queryset =  CustomUser.objects.all()
        parking_name_v = self.request.query_params.get('email', None)

        if parking_name_v is not None:
            queryset = queryset.filter(login=parking_name_v)
        return queryset

class Parking_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer

class Parking_View_Search(generics.ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = Parking_Serializer
    def get_queryset(self):
        queryset =  Parking.objects.all()
        parking_name_v = self.request.query_params.get('parking_name', None)

        if parking_name_v is not None:
            queryset = queryset.filter(parking_name=parking_name_v)
        return queryset
class Parking_View_Coordinates(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = Parking.objects.all()
    serializer_class = Parking_Serializer_Coordinates



class Delete_Parking_View(RetrieveUpdateDestroyAPIView):
        permission_classes = (IsAuthenticated | ReadOnly,)
        queryset = Parking.objects.all()
        serializer_class = Parking_Serializer


class Booking_View(CreateAPIView, ListAPIView):
    permission_classes = (IsAuthenticated,)
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


class Booking_View_Search(generics.ListAPIView):
    serializer_class = Booking_Serializer
    def get_queryset(self):
        queryset =  Booking.objects.all()
        code_v = self.request.query_params.get('code', None)

        if code_v is not None:
            queryset = queryset.filter(code=code_v)
        return queryset




