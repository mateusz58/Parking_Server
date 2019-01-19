from django.conf.urls import url
from django.urls import path, include

from decorators import group_required
from pages import views
from users.email_acctivation import activate
from users.views import login_view, signup_view
from .views import HomePageView, AboutPageView, Parking_View_Coordinates, Parking_View, Booking_View, User_View, \
    Delete_User_View, Delete_Booking_View, Parking_View_Search, User_View_Search, Booking_View_Search,  \
    Delete_Parking_View

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    # path('accounts/login/', LoginPageView.as_view(), name='login'),
    url(r'login/$',login_view, name="account_login"),
    url(r'signup/$',signup_view, name="account_signup"),

    ##aktywacja maila
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),


    url(r'^booking/search/', views.filter_booking_view, name='booking'),

# group_required('Parking_manager'),
###JSON serializers

    # path('api/test/', views.test_detail,name='test'),
   # url(r'^api/snippet/', views.booking_list),

    path('api/parking/', Parking_View.as_view()),
    path('api/parking/<int:pk>', Delete_Parking_View.as_view()),
    path('api/parking_wsp/', Parking_View_Coordinates.as_view()),
    path('api/booking/', Booking_View.as_view()),
    path('api/users/', User_View.as_view()),
    path('api/users/<int:pk>', Delete_User_View.as_view()),
    url(r'api/users/search$', User_View_Search.as_view()),
    path('api/booking/<int:pk>', Delete_Booking_View.as_view()),
    url(r'api/parking/search$', Parking_View_Search.as_view()),
    url(r'api/booking/search$', Booking_View_Search.as_view()),
    ######
    # path('test/', views.HelloView.as_view(), name='hello'),
    ##Users system
### AUTHENTICATION
    ##path('users/', include('users.urls')),  ####Zwraca uzytkownikow
    path('api/rest-auth/', include('rest_auth.urls')),  ##Zwraca wartosc Hasz
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),  ##### rejestracja
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
########

## PARKINGER VIEW



]
  ##path(r'parking/(?P<parking>\w+)/$', Parking_View_Search.as_view(),name='parking_name')
    # url(r'^parking/(?P.+)/$', Parking_View_Search.as_view()
# r'parking/(?P<parking>\w+)/$','yourviewname',name='parking_search'
####Query for searching parking name :http://127.0.0.1:8000/api/parking/search?parking_name=Parking1
##http://127.0.0.1:8000/hello/?format=json

