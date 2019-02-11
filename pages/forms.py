from django import forms
from django.contrib import admin

from pages.models import Car


class Car_Form(forms.ModelForm):


    class Meta:
        model = Car
        exclude = ['registration_plate']




