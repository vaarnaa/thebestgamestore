from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

import core.views

urlpatterns = [
    url(r'^$', core.views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name="logout"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^games', core.views.games, name='games'),
    url(r'^add_games', core.views.add_games, name='add_games'),
    url(r'^added', core.views.add_game, name='add_game'),
    url(r'^remove_game', core.views.remove_game, name='remove_game'),
    url(r'^update_price', core.views.update_price, name='update_price'),
    url(r'^highscores', core.views.highscores, name='highscores'),
    url(r'^player_highscores', core.views.player_highscores, name='player_highscores'),
    path('signup/', core.views.signup, name='signup'),
    path('signup/select_user_type/', core.views.get_user_type, name='usertype'),
    path('signup/player', core.views.player_signup, name='player_signup'),
    path('signup/developer', core.views.developer_signup, name='developer_signup'),
    url(r'^activate/player/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core.views.player_activate, name='player_activate'),
    url(r'^activate/developer/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core.views.developer_activate, name='developer_activate'),
    path('admin/', admin.site.urls),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^', include('core.urls', namespace='core')),
    url(r'^', include('gameService.urls', namespace='gameService')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
