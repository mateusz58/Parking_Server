
from rest_framework import viewsets, permissions, filters, generics, authentication, status, routers
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED

from customexceptions import FORBIDDEN
from pages.models import Booking, Car, free_places_update_v2
from pages.serializers import Car_booking_Serializer, Car_Serializer
from pages.views import ReadOnly
from templatetags.templatetag import has_group, has_group_v2
from users.models import CustomUser







class Car_booking_View(generics.ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = Car_booking_Serializer
    model = Booking
    queryset=Booking.objects.all()


class Update_Car_booking_View(LoginRequiredMixin, UserPassesTestMixin,RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Car_booking_Serializer
    model = Booking
    queryset = Booking.objects.all()
    def test_func(self):
        obj = self.get_object()
        # print("obj.user  VALUE:"+str(obj.user)+"CustomUser.objects.get(email=self.request.user).id VALUE"+str(CustomUser.objects.get(email=self.request.user).email))
        if has_group_v2(self.request.user, "Client_mobile"):
            user=self.request.user
            if obj.user == user:

                return True
            else:
                raise FORBIDDEN("You do not have permission to view that")

        else:
            raise FORBIDDEN("You do not have permission to view that")


class Car_booking_View_logged(generics.ListAPIView):
    serializer_class = Car_booking_Serializer
    model = Booking
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if has_group(self.request.user, "Client_mobile"):
            queryset = Booking.objects.all()
            return queryset.filter(user__email=self.request.user)


