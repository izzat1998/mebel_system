from django.contrib import admin
from django.urls import path, include

from CallCenter.views import GetCustomerInfo, PostCallContent, UpdateCallContent

urlpatterns = [
    path('call_center/', GetCustomerInfo.as_view(), name='call_center'),
    path('call_content/', PostCallContent.as_view(), name='post_call_content'),
    path('call_content/<int:id>/update/', UpdateCallContent.as_view(), name='post_call_content'),

    # path('call_center/edit/<int:id>/')

]

