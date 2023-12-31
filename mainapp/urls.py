from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('updateDetails', views.updateDetails),
    path('profile/<str:username>', views.profile),
    path('sendRequest', views.sendMatchRequest),
    path('matches', views.matches),
]