
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated

from exceptions.httpExceptionsHandler import FORBIDDEN
from pages.models import Booking
from pages.serializers import Car_booking_Serializer
from pages.views import ReadOnly
from templatetags.templatetag import has_group, has_group_v2


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
