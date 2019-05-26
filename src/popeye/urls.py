from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token
from account.views import test

urlpatterns = [
    path('account/', include('account.urls')),

    path('popeyeadmin/', admin.site.urls),
    path('login/', obtain_jwt_token),
    path('test/', test),
    path('test3/', test),
]
