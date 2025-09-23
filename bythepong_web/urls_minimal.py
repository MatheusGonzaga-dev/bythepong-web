from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import random
import time

# Estado global do jogo
game_state = None

def home(request):
    """Página inicial"""
    return render(request, 'game/home.html')

def jogar(request):
    """Página do jogo"""
    return render(request, 'game/index.html')

def game(request):
    """Página do canvas do jogo"""
    return render(request, 'game/game.html')

def ranking(request):
    """Página de ranking"""
    context = {
        'players': [],
        'recent_games': [],
        'easy_games': 0,
        'normal_games': 0,
        'hard_games': 0,
        'expert_games': 0,
        'total_games': 0,
        'db_unavailable': True
    }
    return render(request, 'game/ranking.html', context)

@csrf_exempt
def start_game(request):
    """API para iniciar jogo"""
    global game_state
    
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()
        difficulty = data.get('difficulty', 'normal')
        
        if not player_name:
            return HttpResponse(json.dumps({'error': 'Nome obrigatório'}), 
                              content_type='application/json', status=400)
        
        # Criar estado do jogo
        game_state = {
            'canvas_width': 800,
            'canvas_height': 600,
            'left_paddle': {'x': 50, 'y': 250, 'width': 15, 'height': 100},
            'right_paddle': {'x': 735, 'y': 250, 'width': 15, 'height': 100},
            'ball': {'x': 400, 'y': 300, 'radius': 10, 'dx': 7, 'dy': 3},
            'player_score': 0,
            'bot_score': 0,
            'game_over': False,
            'winner': None,
            'remaining_time': 120,
            'difficulty': difficulty,
            'start_time': time.time()
        }
        
        result = {
            'success': True,
            'player_name': player_name,
            'difficulty': difficulty,
            'game_state': game_state
        }
        
        return HttpResponse(json.dumps(result), content_type='application/json')
        
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}), 
                          content_type='application/json', status=500)

@csrf_exempt
def update_game(request):
    """API para atualizar jogo"""
    global game_state
    
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    
    if not game_state:
        return HttpResponse(json.dumps({'error': 'Nenhum jogo ativo'}), 
                          content_type='application/json', status=400)
    
    try:
        data = json.loads(request.body)
        direction = data.get('direction')
        
        # Atualizar tempo
        elapsed = time.time() - game_state['start_time']
        game_state['remaining_time'] = max(0, 120 - int(elapsed))
        
        # Mover jogador
        if direction == 'up':
            game_state['left_paddle']['y'] = max(0, game_state['left_paddle']['y'] - 8)
        elif direction == 'down':
            game_state['left_paddle']['y'] = min(500, game_state['left_paddle']['y'] + 8)
        
        # IA
        ball_y = game_state['ball']['y']
        paddle_center = game_state['right_paddle']['y'] + 50
        speed = 6
        
        if ball_y < paddle_center - 10:
            game_state['right_paddle']['y'] = max(0, game_state['right_paddle']['y'] - speed)
        elif ball_y > paddle_center + 10:
            game_state['right_paddle']['y'] = min(500, game_state['right_paddle']['y'] + speed)
        
        # Mover bola
        game_state['ball']['x'] += game_state['ball']['dx']
        game_state['ball']['y'] += game_state['ball']['dy']
        
        # Colisões
        if game_state['ball']['y'] <= 10 or game_state['ball']['y'] >= 590:
            game_state['ball']['dy'] = -game_state['ball']['dy']
        
        if (game_state['ball']['x'] <= 65 and 
            game_state['left_paddle']['y'] <= game_state['ball']['y'] <= game_state['left_paddle']['y'] + 100):
            game_state['ball']['dx'] = abs(game_state['ball']['dx'])
            
        if (game_state['ball']['x'] >= 735 and 
            game_state['right_paddle']['y'] <= game_state['ball']['y'] <= game_state['right_paddle']['y'] + 100):
            game_state['ball']['dx'] = -abs(game_state['ball']['dx'])
        
        # Pontuação
        if game_state['ball']['x'] < 0:
            game_state['bot_score'] += 1
            game_state['ball']['x'] = 400
            game_state['ball']['y'] = 300
            game_state['ball']['dx'] = random.choice([-7, 7])
        elif game_state['ball']['x'] > 800:
            game_state['player_score'] += 1
            game_state['ball']['x'] = 400
            game_state['ball']['y'] = 300
            game_state['ball']['dx'] = random.choice([-7, 7])
        
        # Fim do jogo
        if game_state['player_score'] >= 3 or game_state['bot_score'] >= 3 or game_state['remaining_time'] <= 0:
            game_state['game_over'] = True
            if game_state['player_score'] > game_state['bot_score']:
                game_state['winner'] = 'player'
            elif game_state['bot_score'] > game_state['player_score']:
                game_state['winner'] = 'bot'
            else:
                game_state['winner'] = 'tie'
        
        return HttpResponse(json.dumps({'success': True, 'game_state': game_state}), 
                          content_type='application/json')
        
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}), 
                          content_type='application/json', status=500)

@csrf_exempt
def end_game(request):
    """API para finalizar jogo"""
    global game_state
    
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    
    if not game_state:
        return HttpResponse(json.dumps({'error': 'Nenhum jogo ativo'}), 
                          content_type='application/json', status=400)
    
    try:
        result = {
            'success': True,
            'final_score': {
                'player': game_state['player_score'],
                'bot': game_state['bot_score']
            },
            'winner': game_state['winner'],
            'won': game_state['winner'] == 'player'
        }
        
        game_state = None
        
        return HttpResponse(json.dumps(result), content_type='application/json')
        
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}), 
                          content_type='application/json', status=500)

urlpatterns = [
    path('', home, name='home'),
    path('jogar/', jogar, name='index'),
    path('game/', game, name='game'),
    path('ranking/', ranking, name='ranking'),
    path('api/start-game/', start_game, name='start_game'),
    path('api/update-game/', update_game, name='update_game'),
    path('api/end-game/', end_game, name='end_game'),
]
