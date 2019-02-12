from django import forms
from django.contrib import admin

from pages.models import Booking


class Booking_Form(forms.ModelForm):


    class Meta:
        model = Booking
        exclude = ['registration_plate']
        fields = ('Date_From','Date_To')
