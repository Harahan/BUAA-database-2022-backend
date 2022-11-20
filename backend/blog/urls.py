from django.urls import path
from . import views

urlpatterns = [
	path('fetchAll/', views.fetch_all),
	path('delete/', views.delete),
	path('fetchOne/', views.fetch_one),
	path('uploadPicture/', views.upload_picture),
	path('postArticle/', views.post_article),
	path('fetchUserArticles/', views.fetch_user_articles),
	path('uploadVideo/', views.upload_video),
]