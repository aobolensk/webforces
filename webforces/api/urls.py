import djoser.urls.authtoken
from django.urls import path

from . import index, views

urlpatterns = [
    path('', index.APIIndexView.as_view()),
    path('get_token/', djoser.urls.authtoken.views.TokenCreateView.as_view()),
    path('stats/', views.StatsView.as_view()),
]
