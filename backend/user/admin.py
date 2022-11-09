from django.contrib import admin

# Register your models here.
from .models import User, Follow


@admin.register(User)
@admin.register(Follow)
class UserAdmin(admin.ModelAdmin):
	pass
