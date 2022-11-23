from django.contrib import admin

# Register your models here.
from .models import Like, Dislike, Comment


@admin.register(Like)
@admin.register(Dislike)
@admin.register(Comment)
class ResponseAdmin(admin.ModelAdmin):
	pass
