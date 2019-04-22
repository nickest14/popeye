from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at', 'role')
    list_filter = ('role', )


admin.site.register(User, UserAdmin)