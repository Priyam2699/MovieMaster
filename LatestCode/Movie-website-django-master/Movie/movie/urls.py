from django.urls import path, re_path
from . import views
from . import models

urlpatterns = [
    path('movie_detail/<str:id>', views.detail, {'model': models.Movie}, name='movie_detail'),
    path('actor_detail/<str:id>', views.detail, {'model': models.Actor}, name='actor_detail'),
    path('actor_all/<int:page>', views.whole_list, name='whole_list'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('seen/', views.seen, name='seen'),
    path('add_seen/<str:movie_id>', views.add_seen, name='seen'),
    path('order/', views.order, name='order'),
    path('add_order/<str:movie_id>', views.add_order, name='order'),
]
