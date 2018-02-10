from django.conf.urls import url
from . import views

app_name = 'gameService'

urlpatterns = [
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.game, name='game'),
]
