from django.conf.urls import url
from django.shortcuts import redirect
from django.urls import path, include
from allauth.account.views import confirm_email
# from decorators import group_required
from pages import views
from pages.views_related import Car_booking_View, Update_Car_booking_View,Car_booking_View_logged
from users.email_acctivation import activate
from users.views import login_view, signup_view, CustomRegisterView
from .views import HomePageView, AboutPageView, Parking_View_Coordinates, Parking_View, Booking_View, User_View, \
    Delete_User_View, Delete_Booking_View, Parking_View_Search, User_View_Search, Booking_View_Search, \
    Delete_Parking_View, Booking_View_logged, Car_View, redirect_view, Car_View_logged, Update_Car_View

from rest_framework_nested import routers
from django.views.generic.base import RedirectView


urlpatterns = [

    # path('', lambda _: redirect('admin:index'), name="index"),
    # url(r'^$', RedirectView.as_view(url='/admin/'),name='admin-redirect'),
    path('', HomePageView.as_view(), name='home'),
    path('/about/', redirect_view, name='redirectview'),
    path('about/', AboutPageView.as_view(), name='about'),
    #### Redirect to django admin site

    # path('accounts/login/', LoginPageView.as_view(), name='login'),
    url(r'login/$',login_view, name="account_login"),
    url(r'signup/$',signup_view, name="account_signup"),
    ##aktywacja maila
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    # url(r'^booking/search/', views.filter_booking_view, name='booking'),
# group_required('Parking_manager'),
###JSON serializers
    # path('api/test/', views.test_detail,name='test'),
   # url(r'^api/snippet/', views.booking_list),

    path('api/booking/logged/<int:pk>', Delete_Booking_View.as_view()),
    path('api/booking/', Booking_View.as_view()),
    url(r'api/booking/logged/', Booking_View_logged.as_view()),

    path('api/car_booking/logged/', Car_booking_View_logged.as_view()),
    path('api/car_booking/', Car_booking_View.as_view()),
    path('api/car_booking/logged/<int:pk>', Update_Car_booking_View.as_view()),
    path('api/car/', Car_View.as_view()),
    path('api/car/logged/', Car_View_logged.as_view()),
    path('api/car/logged/<int:pk>', Update_Car_View.as_view()),
    path('api/parking/', Parking_View.as_view()),
    path('api/parking/<int:pk>', Delete_Parking_View.as_view()),
    path('api/parking_wsp/', Parking_View_Coordinates.as_view()),
    url(r'api/parking/search$', Parking_View_Search.as_view()),

    path('api/users/', User_View.as_view()),
    path('api/users/<int:pk>', Delete_User_View.as_view()),
    url(r'api/users/search$', User_View_Search.as_view()),



    ######

### AUTHENTICATION
    # path('users/', include('users.urls')),  ####Zwraca uzytkownikow
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/rest-auth/', include('rest_auth.urls')), ####


    ## REJESTRACJA STANDARDOWA
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),  ##### rejestracja

    ## REJESTRACJA CUSTOM
    url(r'api/registration_custom/', CustomRegisterView.as_view(), name='CustomRegisterView'),

    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),

    # url(r'^accounts-rest/registration/account-confirm-email-v2-custom/(?P<key>.+)/$', CustomVerifyEmailView.as_view(), name='account_confirm_email_custom')

    # 'api/registration_custom/'    REJESTRACJA
    # 'api/rest-auth/password/reset/' RESET HASLA
    # 'api/rest-auth/password/change/'ZMIANA HASLA
    #  'api-token-auth/'              LOGOWANIE
    #   api/rest-auth/logout/
########
## PARKINGER VIEW

]
  ##path(r'parking/(?P<parking>\w+)/$', Parking_View_Search.as_view(),name='parking_name')
    # url(r'^parking/(?P.+)/$', Parking_View_Search.as_view()
# r'parking/(?P<parking>\w+)/$','yourviewname',name='parking_search'


####Query for searching parking name :http://127.0.0.1:8000/api/parking/search?parking_name=Parking1
##http://127.0.0.1:8000/hello/?format=json

##Query for searching username
##http://127.0.0.1:8000/api/users/search?email=matp321@gmail.com


##Query for searching username http://192.168.8.106:8000/api/booking/search?user=cxbvwdd5rakc@10minutemail.pl

##Query for login username http://192.168.8.106:8000/api/booking/login?user=cxbvwdd5rakc@10minutemail.pl

