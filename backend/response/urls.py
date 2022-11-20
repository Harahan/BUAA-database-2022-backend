from django.urls import path

from . import views

urlpatterns = [
	path('takeStance/', views.take_stance),
	path('addComment/', views.add_comment),
	path('delComment/', views.del_comment),
	path('findComment/', views.find_comment),
]
