from django.urls import path
from . import views

urlpatterns = [
	path('sendMoment/', views.sendMoment),
]