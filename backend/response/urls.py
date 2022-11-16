from django.urls import path

from . import views

urlpatterns = [
	path('takeStance/', views.take_stance),
]
