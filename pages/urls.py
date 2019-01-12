from django.conf.urls import url
from django.urls import path, include

from .views import HomePageView, AboutPageView, Parking_View_Coordinates, Parking_View, Booking_View, User_View, \
    Delete_User_View, Delete_Booking_View, Parking_View_Search, User_View_Search, Booking_View_Search

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),

    path('parking/', Parking_View.as_view()),
    path('parking_wsp/', Parking_View_Coordinates.as_view()),
    path('booking/', Booking_View.as_view()),
    path('user_clients/', User_View.as_view()),
    path('user_clients/<int:pk>', Delete_User_View.as_view()),
    path('booking/<int:pk>', Delete_Booking_View.as_view()),
    url(r'parking/search$', Parking_View_Search.as_view()),
    url(r'user_clients/search$', User_View_Search.as_view()),
    url(r'booking/search$', Booking_View_Search.as_view()),

    # path('test/', views.HelloView.as_view(), name='hello'),
    ##Users system

    ##path('users/', include('users.urls')),  ####Zwraca uzytkownikow
    path('rest-auth/', include('rest_auth.urls')),  ##Zwraca wartosc Hasz
    path('rest-auth/registration/', include('rest_auth.registration.urls')),  ##### rejestracja
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

]
