from django.contrib import admin

# Register your models here.
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	pass

