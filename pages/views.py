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
from decorators import group_required
from pages.api_group_permission import HasGroupPermission
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

from django.views.generic import TemplateView

from pages.serializers import User_Serializer, Booking_Serializer, Parking_Serializer, Parking_Serializer_Coordinates, \
    User_Serializer_Login_Email
from users.models import CustomUser
from rest_framework.decorators import api_view
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

# @user_passes_test(lambda u: u.groups.filter(name='companyGroup').exists())

###SNIPPET VIEWSET


##HOME PAGE VIEW

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

@login_required
def filter_booking_view(request):
    user=request.user
    permission_classes = (IsAuthenticated,)
    booking_list = Booking.objects.all()
    booking_filter = BookingFilter(request.GET, queryset=booking_list)
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
    permission_classes = (IsAuthenticated | ReadOnly,)
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
    permission_classes = (IsAuthenticated | ReadOnly,)
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
            print("Delete_Parking_View"+user)
            return has_group(user, "Parking_manager")




class Booking_View(CreateAPIView,ListAPIView):

    permission_classes = (IsAuthenticated | ReadOnly,)
    queryset = Booking.objects.all()
    serializer_class = Booking_Serializer









class Delete_Booking_View(LoginRequiredMixin, UserPassesTestMixin,RetrieveUpdateAPIView):


        permission_classes = (IsAuthenticated | ReadOnly,)
        serializer_class = Booking_Serializer
        model = Booking
        fields = ['code']
        queryset = Booking.objects.all()
        def test_func(self):
            obj = self.get_object()
            print("obj.user  VALUE:"+str(obj.user)+"CustomUser.objects.get(email=self.request.user).id VALUE"+str(CustomUser.objects.get(email=self.request.user).email))
            return str(obj.user) == str(CustomUser.objects.get(email=self.request.user).email)

# @permission_required('GET_booking_API', raise_exception=True)
class Booking_View_Search(generics.ListAPIView):
    serializer_class = Booking_Serializer
    def get_queryset(self):
        queryset =  Booking.objects.all()
        user_v = self.request.query_params.get('user', None)
        if user_v is not None:
            queryset = queryset.filter(user__email=user_v)
        return queryset

class Booking_View_logged(generics.CreateAPIView,generics.ListAPIView):
        serializer_class = Booking_Serializer
        model = Booking
        def get_queryset(self):
            user=self.request.user
            queryset = Booking.objects.all()
            return queryset.filter(user__email=self.request.user)

#





