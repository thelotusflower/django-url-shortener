from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'shortener'
urlpatterns = [
	path('', views.home, name='home'),
    path('login/', views.index, name='index'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('shortener/', views.shortenLink, name='short'),
    path('<str:query>/', views.redirectShort, name='redirect'),
]
