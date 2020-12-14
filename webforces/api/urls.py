from django.urls import path

from . import index, views

urlpatterns = [
    path('', index.APIIndexView.as_view()),
    path('get_token/', views.GetTokenView.as_view()),
    path('stats/', views.StatsView.as_view()),
    path('users/', views.UsersView.as_view()),
    path('users/<int:pk>/', views.UserViewID.as_view()),
    path('users/<str:login>/', views.UserViewLogin.as_view()),
    path('algs/', views.AlgsView.as_view()),
]
