from django.urls import path

from . import views

urlpatterns = [
	path('fetchAll/', views.fetch_all),
	path('fetchUserMerchandises/', views.fetch_user_merchandises),
]
