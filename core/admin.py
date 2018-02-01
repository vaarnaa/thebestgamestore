from django.contrib import admin
from .models import Game, Category, Player


class PlayerAdmin(admin.ModelAdmin):
    list_display =["username"]
admin.site.register(Player, PlayerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'url', 'slug', 'price', 'image', 'description']
    list_display_links = None
    list_editable = ['url', 'name', 'slug', 'price', 'image', 'description']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Game, GameAdmin)
# Register your models here.
