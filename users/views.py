from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from exceptions.httpExceptionsHandler import UNAUTHORIZED
from templatetags.templatetag import has_group_v4
from django.contrib.auth.models import Group

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from users.tokens import account_activation_token
from django.core.mail import EmailMessage
from rest_framework import status
from rest_auth.registration.views import RegisterView


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(" LOGIN Condition satisfied")
            user = form.get_user()

            l = []
            for g in user.groups.all():
                l.append(g.name)

            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', { 'form': form })

def signup_view(request):

    if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
             print(" REGISTER Condition satisfied")


             user = form.save()
             user.is_active = False

             group = Group.objects.get(name='Parking_manager')
             user.groups.add(group)
             user.save()
             current_site = get_current_site(request)
             print("get_current_site(request)"+str(get_current_site(request)))
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

    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', { 'form': form })

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        print("Checking out")
        if not has_group_v4(user,"Client_mobile"):
            raise UNAUTHORIZED("Unable to log in with provided credentials.")

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CustomRegisterView(RegisterView):
        def create(self, request, *args, **kwargs):
            response = super().create(request, *args, **kwargs)
            if status.is_success(response.status_code):
                print("Request_check"+str(self.request.data['email']))
                user=str(self.request.data['email'])
                user = CustomUser.objects.get(email=user).id

                my_group = Group.objects.get(name='Client_mobile')
                my_group.user_set.add(user)
            return response
