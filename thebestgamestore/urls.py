from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import core.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', core.views.index, name='index'),
    url(r'^login', core.views.login, name='login'),
    url(r'^games', core.views.games, name='games'),
    url(r'^highscores', core.views.highscores, name='highscores'),
    url(r'^signup', core.views.signup, name='signup'),
    url(r'^db', core.views.db, name='db'),
    path('admin/', admin.site.urls),
]
