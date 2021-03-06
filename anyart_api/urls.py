"""anyart_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

detail_dict = {
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
    'patch': 'partial_update'
}

list_dict = {
    'get': 'list',
    'post': 'create'
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.HelloView.as_view(), name='hello'),
    path('authorization/', include('authorization.urls')),
    path('workload/', include('workload.urls')),
    path('approval/', include('approval.urls'))
]
