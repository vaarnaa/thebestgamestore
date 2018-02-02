from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


import core.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', core.views.index, name='index'),
    #url(r'^login', core.views.login, name='login'),
    #url(r'^login/$', auth_views.login, {'template_name': 'core/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name="logout"),
    url(r'^games', core.views.games, name='games'),
    url(r'^highscores', core.views.highscores, name='highscores'),
    path('signup/', core.views.signup, name='signup'),
    #path('signup/player', core.views.PlayerSignUp.as_view(), name='player_signup'),
    path('signup/player', core.views.player_signup, name='player_signup'),
    #path('signup/developer', core.views.DeveloperSignUp.as_view(), name='developer_signup'),
    path('signup/developer', core.views.developer_signup, name='developer_signup'),
    url(r'^activate/player/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core.views.player_activate, name='player_activate'),
    url(r'^activate/developer/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core.views.developer_activate, name='developer_activate'),
    url(r'^db', core.views.db, name='db'),
    path('admin/', admin.site.urls),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^', include('core.urls', namespace='core')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
