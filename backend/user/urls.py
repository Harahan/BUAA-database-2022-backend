from django.conf.urls.static import static
from django.urls import path
from backend import settings
from . import views

urlpatterns = [
	path('login/', views.login),
	path('signup/', views.signup),
	path('logout/', views.logout),
	path('follow/', views.follow),
	path('fixProfile/', views.fix_profile),
	path('getProfile/', views.get_profile),
	path('getContacts/', views.get_contacts),
]