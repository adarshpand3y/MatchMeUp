from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('updateDetails', views.updateDetails),
    path('profile', views.profile),
]