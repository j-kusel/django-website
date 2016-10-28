from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.proj_page, {'type': ''}, name='sound'),
    url(r'^(?P<type>[A-Za-z]{4,})/$', views.proj_page, name='sound_focus'),
]
