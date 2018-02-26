from django.conf.urls import url
from . import views

app_name = 'gameService'

urlpatterns = [
    url(r'^play/(?P<id>\d+)/$', views.play, name='play'),
    url(r'^play/savescore/(?P<id>\d+)/$', views.savescore, name='savescore'),
]
