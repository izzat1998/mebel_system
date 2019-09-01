"""mebel_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from .views import ShopView, CategoryDetailView, ProfileDetailView, QuestionnaireView,MainMenuView



urlpatterns = [
    path('', MainMenuView.as_view(), name='main_menu'),
    path('shop/', ShopView.as_view(), name='index'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('questionnaire/', QuestionnaireView.as_view(), name='questionnaire'),
]
