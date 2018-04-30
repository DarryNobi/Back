"""Back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import  url
from myweb import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^account_inquiry/', views.account_inquiry),
    url(r'^account_Inquiry/', views.account_Inquiry),
    url(r'^upload_map/', views.upload_map),
    url(r'^_upload_map/', views._upload_map),
    url(r'^add_Account/', views.add_Account),
    url(r'^add_usr/', views.add_usr),
    url(r'^deliver_map/', views.deliver_map),

]
