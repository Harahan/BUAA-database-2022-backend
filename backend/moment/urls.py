from django.urls import path
from . import views

urlpatterns = [
	path('sendMoment/', views.send_moment),
	path('getMoment/', views.get_moment),
	path('delMoment/', views.del_moment),
]