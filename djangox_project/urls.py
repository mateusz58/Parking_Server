from django.conf.urls import url
from django.contrib import admin


from django.urls import path, include

from rest_framework.authtoken import views

from users.views import CustomAuthToken

urlpatterns = [
    path('api-token-auth/',CustomAuthToken.as_view(), name='api-token auth'),
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('pages.urls')),
    url(r'^advanced_filters/', include('advanced_filters.urls'))
]
