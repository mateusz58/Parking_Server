from django.shortcuts import render, HttpResponse
from django.utils.http import urlsafe_base64_decode


from django.contrib.auth import login
from users.tokens import account_activation_token

from users.models import CustomUser


def index(request):
    return render(request, 'register/index.html')













































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

