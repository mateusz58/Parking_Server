from django.contrib import admin
##from .router import router

from django.urls import path, include

from rest_framework.authtoken import views

urlpatterns = [

    # path('api/', include(router.urls)),
    # path('api-token-auth/',views.obtain_auth_token,name='api-token auth')

    # path('snippets/',include('snippets.urls',namespace='snippets')),
    path('api-token-auth/',views.obtain_auth_token,name='api-token auth'),
    path('admin/', admin.site.urls),
   path('users/', include('django.contrib.auth.urls')),
  path('accounts/', include('allauth.urls')),
  path('', include('pages.urls'))
]
