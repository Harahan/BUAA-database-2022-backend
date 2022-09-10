"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('getquestion/', views.get_question),
    path('gethistory/', views.get_history),
    path('getuser/', views.get_user),
    path('deletehis/<int:table_id>', views.delete_history),
    path('addquestion/', views.add_question),
    path('adduser/', views.add_user),
    path('searchhis/', views.search_history),
    path('changeans/<int:question_id>', views.change_answer),
    path('admin/', admin.site.urls),
]
