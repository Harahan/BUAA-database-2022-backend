from django.urls import path

from . import views

urlpatterns = [
	path('fetchAll/', views.fetchAll),
]
