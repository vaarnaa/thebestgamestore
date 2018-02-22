from django.contrib import admin
from .models import Game, Category, Player, Developer, User, Highscore, Payment, Order, OrderItem



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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['game']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payment_id", 'order']


admin.site.register(Payment,PaymentAdmin)
