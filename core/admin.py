from django.contrib import admin
from .models import Game, Category, Player, Developer, User, Highscore


class PlayerAdmin(admin.ModelAdmin):

    list_display = ["username"]


admin.site.register(Player, PlayerAdmin)


class DeveloperAdmin(admin.ModelAdmin):

    list_display = ["username"]


admin.site.register(Developer, DeveloperAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class GameAdmin(admin.ModelAdmin):

    list_display = ['name', 'url', 'slug', 'price', 'image', 'description']
    list_display_links = None
    list_editable = ['url', 'name', 'slug', 'price', 'image', 'description']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Game, GameAdmin)


class UserAdmin(admin.ModelAdmin):

    list_display = ["username", "email"]


admin.site.register(User, UserAdmin)


class HighscoreAdmin(admin.ModelAdmin):

    list_display = ["game", "player", "score"]


admin.site.register(Highscore, HighscoreAdmin)
