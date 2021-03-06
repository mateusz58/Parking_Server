from django.conf.urls import url
from django.urls import path, include
from allauth.account.views import confirm_email
from pages.views_related import Car_booking_View, Update_Car_booking_View, Car_booking_View_logged
from users.emailActivation import activate
from users.views import login_view, signup_view, CustomRegisterView
from .views import HomePageView, AboutPageView, Parking_View_Coordinates, Parking_View, Booking_View, User_View, \
    Delete_User_View, Delete_Booking_View, Parking_View_Search, User_View_Search, Booking_View_Search, \
    Delete_Parking_View, Booking_View_logged, Car_View, redirect_view, Car_View_logged, Update_Car_View

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', redirect_view, name='redirectview'),
    path('about/', AboutPageView.as_view(), name='about'),
    url(r'login/$', login_view, name="account_login"),
    url(r'signup/$', signup_view, name="account_signup"),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

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

    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/rest-auth/', include('rest_auth.urls')),

    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'api/registration_custom/', CustomRegisterView.as_view(), name='CustomRegisterView'),

    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email,
        name='account_confirm_email')]
