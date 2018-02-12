from django.conf.urls import url, include
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='game_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.game_detail, name='game_detail'),


]
