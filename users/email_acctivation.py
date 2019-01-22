from django.contrib.sites.shortcuts import get_current_site
from django.db.migrations import serializer
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# import bcrypt
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from pipenv.vendor.vistir.termcolors import colored

from django.contrib.auth import login, logout, get_user_model
from users.tokens import account_activation_token
from django.core.mail import EmailMessage
import sys, traceback

from users.models import CustomUser


def index(request):
    return render(request, 'register/index.html')


# def register(request):
#     errors = CustomUser.objects.validator(request.POST)
#     if len(errors):
#         for tag, error in errors.iteritems():
#             messages.error(request, error, extra_tags=tag)
#         return redirect('/')
#     hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
#     user = user.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
#     user.is_active = False
#     user.save()
#     current_site = get_current_site(request)
#     message = render_to_string('register/acc_active_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#         'token': account_activation_token.make_token(user),
#     })
#     mail_subject = 'Activate your blog account.'
#     to_email = user.email
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#
#     email.send()
#     request.session['id'] = user.id
#     ##return redirect('/success')
#     return HttpResponse('Please confirm your email address to complete the registration')
#
# def login(request):
#     if (User.objects.filter(email=request.POST['login_email']).exists()):
#         user = User.objects.filter(email=request.POST['login_email'])[0]
#         if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):
#             request.session['id'] = user.id
#             return redirect('/success')
#     return redirect('/')
#
# def success(request):
#     user = User.objects.get(id=request.session['id'])
#     context = {
#         "user": user
#     }
#     return render(request, 'register/success.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        print(uid)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Dziekujemy za potwierdzenie maila konto zostało aktywowane.')
    else:
        return HttpResponse('Link aktywacyjny jest nie poprawny!')

