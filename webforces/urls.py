"""webforces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.log_in, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign_up/', views.sign_up),
    path('api/', include('webforces.api.urls')),
    path('users/<str:user>/', views.UserView.as_view()),
    path('users/<str:user>/update/', views.UpdUserView.as_view()),
    path('store/<int:alg_id>/alg/', views.AlgView.as_view()),
    path('store/<int:alg_id>/download/', views.DownloadAlgView.as_view()),
    path('store/<int:alg_id>/add_test/', views.AddTestView.as_view()),
    path('store/<int:alg_id>/buy/', views.BuyAlgView.as_view()),
    path('stats/', views.StatsView.as_view()),
    path('store/', views.StoreView.as_view()),
    path('add_alg/', views.AddAlgView.as_view()),
    path('run/<int:alg_id>/', views.RunTaskView.as_view()),
    path('Error403/', views.Error403View.as_view())
]
