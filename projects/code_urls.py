from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.proj_page, {'type': '','cat': 'code'}, name='code'),
    url(r'^(?P<type>[A-Za-z]{3,})/$', views.proj_page, {'cat': 'code'}, name='code_focus'),
]
