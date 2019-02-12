from django import forms
from django.contrib import admin

from pages.models import Car


class Car_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Car_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Car
        exclude = ['registration_plate']
