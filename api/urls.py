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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mebel_system import settings
from api.views import GetCustomerInformationApiView, GetCountCategoryApiView, GetCategoryCount, GetWhileCategoryCount, \
    getDateCount, GetCustomerDetail, TenDaysGetCount, PostCustomerInformationApi, GetCustomerDetailUpdate

urlpatterns = [
    path('customer/<int:pk>/update', GetCustomerDetailUpdate.as_view(), name='customer-info'),
    path('customer/post', PostCustomerInformationApi.as_view(), name='customer-post'),
    path('customer/<int:pk>', GetCustomerDetail.as_view(), name='customer-info'),
    path('customer/', GetCustomerInformationApiView.as_view(), name='customer-info'),
    path('ten_day_count/', TenDaysGetCount.as_view(), name='ten-day-count'),
    path('count/', GetCategoryCount.as_view(), name='product_amounts'),
    path('test/', GetWhileCategoryCount.as_view(), name='range'),
    path('customercount/', getDateCount.as_view(), name='getCount'),
]
