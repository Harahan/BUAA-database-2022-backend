from django.contrib import admin

# Register your models here.
from .models import Moment


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
	pass
