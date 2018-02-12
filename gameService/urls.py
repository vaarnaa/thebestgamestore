from django.conf.urls import url
from . import views

app_name = 'gameService'

urlpatterns = [
    url(r'^play/(?P<id>\d+)/$', views.play, name='play'),
]
