from django.urls import path

from . import views

urlpatterns = [
	path('addLike/', views.add_like),
	path('addDislike/', views.add_dislike),
	path('addComment/', views.add_comment),
]
