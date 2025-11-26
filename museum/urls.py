from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_collection, name='car_collection'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('arenas/', views.arena_collection, name='arena_collection'),
    path('arenas/<int:arena_id>/', views.arena_detail, name='arena_detail'),
    path('history/', views.game_history, name='game_history'),
    path('history/update/<int:update_id>/', views.update_detail, name='update_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('highlights/', views.highlights, name='highlights'),
    path('highlights/<int:highlight_id>/', views.highlight_detail, name='highlight_detail'),
    path('highlights/add/', views.add_highlight, name='add_highlight'),
    path('comments/add/', views.add_comment, name='add_comment'),
    path('comments/', views.comments_list, name='comments_list'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('about/', views.about, name='about'),
]