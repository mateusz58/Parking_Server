

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from templatetags.templatetag import has_group
# from users.forms import CustomUserCreationForm
from users.models import CustomUser as User
# from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group






