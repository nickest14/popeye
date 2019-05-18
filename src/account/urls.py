
from django.urls import path, re_path, include
from account import views as account
from rest_framework import routers

router = routers.DefaultRouter()
router.register('testview', account.TestViewSet, base_name='testview')
router.register('register', account.MemberRegistrationViewSet,
                base_name='register')
router.register('member', account.MemberViewSet,
                base_name='member')

urlpatterns = [
    re_path(r'', include(router.urls)),
    path('test3/', account.TestViewSet,  name='test3'),
    path('test2/', account.test),
    path('test/', account.test),
]
