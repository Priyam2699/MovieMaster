from django.contrib import admin
from movie.models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'movieid', 'rate')

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'actorid')

class PopularityAdmin(admin.ModelAdmin):
    list_display = ('movieid', 'weight')


class SeenAdmin(admin.ModelAdmin):
    list_display = ('username', 'movieid')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('username', 'movieid')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Popularity, PopularityAdmin)
admin.site.register(Seen, SeenAdmin)
admin.site.register(Order, OrderAdmin)