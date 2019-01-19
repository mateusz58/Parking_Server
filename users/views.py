from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model

# Create your views here.
from templatetags.templatetag import has_group
from django.contrib.auth.models import Group

from users.forms import CustomUserCreationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        user=request.user
        # print(user)
        if form.is_valid() and has_group(form.get_user(), "Parking_manager"):
            print(" LOGIN Condition satisfied")
            # log the user in
            # has_group(request.user, "Parking_manager")
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', { 'form': form })
 # and has_group(request.user, "Parking_manager"):


def signup_view(request):

    if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
             print(" REGISTER Condition satisfied")
             user = form.save()
             group = Group.objects.get(name='Parking_manager')
             user.groups.add(group)
             ## log the user in
             login(request, user)
             return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', { 'form': form })
