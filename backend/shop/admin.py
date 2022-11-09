from django.contrib import admin

# Register your models here.
from .models import Merchandise


@admin.register(Merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
	pass
