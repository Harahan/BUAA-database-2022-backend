from django.urls import path

from . import views

urlpatterns = [
	path('getChats/', views.get_chats),
	path('findUser/', views.find_user),
	path('getRecords/', views.get_records),
	path('sendRecord/', views.send_record),
]
