from django.urls import path
from . import views

urlpatterns = [
	path('fetchAll/', views.fetchAll),
	path('delete/', views.delete),
	path('fetchOne/', views.fetchOne),
]
