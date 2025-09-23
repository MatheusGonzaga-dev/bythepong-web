from django.urls import path
import os

# Usar views simples na Vercel
if os.environ.get('VERCEL'):
    from . import views_simple as views
else:
    from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jogar/', views.index, name='index'),
    path('game/', views.game_view, name='game'),
    path('api/start-game/', views.start_game, name='start_game'),
    path('api/update-game/', views.update_game, name='update_game'),
    path('api/end-game/', views.end_game, name='end_game'),
    path('ranking/', views.ranking, name='ranking'),
]
