from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from account.views import test

urlpatterns = [
    path('', include('account.urls')),

    path('popeyeadmin/', admin.site.urls),

    path('login/', obtain_jwt_token),
    path('test/', test),
]
