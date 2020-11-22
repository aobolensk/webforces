import djoser.urls.authtoken
from django.urls import path

from . import views

urlpatterns = [
    path('get_token/', djoser.urls.authtoken.views.TokenCreateView.as_view()),
    path('stats/', views.StatsView.as_view()),
    path('users/', views.UsersView.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
]
