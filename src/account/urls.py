
from django.urls import path
from account import views as account

urlpatterns = [
    path('register/', account.MemberRegistrationViewSet),
    path('account/test/', account.test),
]
