from django.urls import path

from . import views

urlpatterns = [
	path('addOrCancelLike/', views.add_or_cancel_like),
	path('addOrCancelDislike/', views.add_or_cancel_dislike),
	path('addComment/', views.add_comment),
	path('delComment/', views.del_comment),
]
