import os
from django.db import models
from django.contrib.auth.models import AbstractUser


def avatar_dir_path(instance, filename):
    return os.path.join('user', instance.username, filename)


class User(AbstractUser):

    ROLE_ADMIN = 'admin'
    ROLE_STAFF = 'staff'
    ROLE_CUSTOMER = 'customer'
    ROLE_STORE = 'store'
    ROLE_OPTIONS = (
        (ROLE_ADMIN, 'admin'),
        (ROLE_STAFF, 'staff'),
        (ROLE_CUSTOMER, 'customer'),
        (ROLE_STORE, 'store'),
    )

    nickname = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    line = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    register_ip = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True,
                               upload_to=avatar_dir_path)
    role = models.CharField(max_length=30, default=ROLE_STAFF,
                            choices=ROLE_OPTIONS)
