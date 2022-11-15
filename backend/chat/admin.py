from django.contrib import admin
from .models import Chat, Record


# Register your models here.
class ChatsAdmin(admin.ModelAdmin):
	filter_horizontal = ('member',)


@admin.register(Record)
class ChatAdmin(admin.ModelAdmin):
	pass


admin.site.register(Chat, ChatsAdmin)
