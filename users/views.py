from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from templatetags.templatetag import has_group
from django.contrib.auth.models import Group

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from users.tokens import account_activation_token
from django.core.mail import EmailMessage

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
             # hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
             # print("Primary key of user"+str(pk))
             user = form.save()
             user.is_active = False



             # print("USER ACTIVE"+user.is_active)
             group = Group.objects.get(name='Parking_manager')
             user.groups.add(group)
             user.save()
             current_site = get_current_site(request)
             message = render_to_string('account/email/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                      })
             mail_subject = 'Aktywacja konta.'
             to_email = user.email
             email = EmailMessage(
                         mail_subject, message, to=[to_email]
                      )
             email.send()
             request.session['id'] = user.id
             user.is_active = False
             print("Primary key of user" + str(user.id))
             return HttpResponse('Please confirm your email address to complete the registration')
             ## log the user in
             # login(request, user)
             # return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', { 'form': form })
