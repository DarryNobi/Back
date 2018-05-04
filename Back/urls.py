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

    url(r'^index/', views.index),
    url(r'^add_usr/', views.add_usr),
    url(r'^account_show/', views.account_show),
    url(r'^_account_show/', views._account_show),
    url(r'^account_inquiry/', views.account_inquiry),
    url(r'^add_Account/', views.add_Account),
    url(r'^info_revise/', views.info_revise),
    url(r'^_info_revise/', views._info_revise),
    url(r'^deliver_map/', views.deliver_map),
    url(r'^upload_map/', views.upload_map),
    url(r'^query_map/', views.query_map),
    url(r'^_download_map/', views._download_map),
    url(r'^_upload_map/', views._upload_map),
    url(r'^status_revise/', views.status_revise),
    url(r'^permission_revise/', views.permission_revise),
    url(r'^password_revise/', views.password_revise),
    url(r'^_password_revise/', views.password_reset),
    url(r'^sinfo_revise/', views.sinfo_revise),
    url(r'^_sinfo_revise/', views._sinfo_revise),
    url(r'^_download_map/', views._download_map),
    url(r'^_delete_map/', views._delete_map),
    url(r'^_delete_module/', views._delete_module),
    url(r'^add_module/', views.add_module),
    url(r'^_add_module/', views._add_module),
    url(r'^login/', views.login),
    url(r'^query_module/', views.query_module),

]
