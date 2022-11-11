from django.contrib import admin

# Register your models here.
from .models import Article, Area, AreaWithArticle


@admin.register(AreaWithArticle)
@admin.register(Area)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	pass

