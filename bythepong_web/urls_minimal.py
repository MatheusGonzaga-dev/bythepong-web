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
        theme = data.get('theme', 'classic')
        
        if not player_name:
            return HttpResponse(json.dumps({'error': 'Nome obrigatório'}), 
                              content_type='application/json', status=400)
        
        # Configurações baseadas na dificuldade - DIFERENÇAS EXTREMAS
        difficulty_config = {
            'fácil': {
                'ball_speed': 3,        # BOLA MUITO LENTA
                'ai_speed': 2,          # IA MUITO LENTA
                'ai_reaction': 200,     # IA COM MUITO DELAY
                'paddle_size': 150,     # RAQUETE GIGANTE
                'player_speed': 12,     # JOGADOR SUPER RÁPIDO
                'ai_accuracy': 0.5      # IA MUITO IMPRECISA
            },
            'normal': {
                'ball_speed': 5,
                'ai_speed': 4,
                'ai_reaction': 80,
                'paddle_size': 100,
                'player_speed': 8,
                'ai_accuracy': 0.75
            },
            'difícil': {
                'ball_speed': 8,
                'ai_speed': 8,
                'ai_reaction': 20,
                'paddle_size': 70,
                'player_speed': 5,
                'ai_accuracy': 0.9
            },
            'expert': {
                'ball_speed': 12,       # BOLA ULTRA RÁPIDA
                'ai_speed': 15,         # IA ULTRA RÁPIDA
                'ai_reaction': 0,       # IA SEM DELAY
                'paddle_size': 40,      # RAQUETE MINÚSCULA
                'player_speed': 3,      # JOGADOR MUITO LENTO
                'ai_accuracy': 0.99     # IA QUASE PERFEITA
            }
        }
        
        config = difficulty_config.get(difficulty, difficulty_config['normal'])
        
        # Criar estado do jogo com configurações de dificuldade
        game_state = {
            'canvas_width': 800,
            'canvas_height': 600,
            'theme': theme,
            'left_paddle': {
                'x': 50, 
                'y': 300 - config['paddle_size'] // 2, 
                'width': 15, 
                'height': config['paddle_size']
            },
            'right_paddle': {
                'x': 735, 
                'y': 300 - config['paddle_size'] // 2, 
                'width': 15, 
                'height': config['paddle_size']
            },
            'ball': {
                'x': 400, 
                'y': 300, 
                'radius': 10, 
                'dx': config['ball_speed'], 
                'dy': random.choice([-config['ball_speed']//2, config['ball_speed']//2])
            },
            'player_score': 0,
            'bot_score': 0,
            'game_over': False,
            'winner': None,
            'remaining_time': 120,
            'difficulty': difficulty,
            'config': config,
            'start_time': time.time(),
            'ai_last_move': 0  # Para controlar reação da IA
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
        
        config = game_state['config']
        
        # Mover jogador com velocidade baseada na dificuldade
        if direction == 'up':
            game_state['left_paddle']['y'] = max(0, game_state['left_paddle']['y'] - config['player_speed'])
        elif direction == 'down':
            game_state['left_paddle']['y'] = min(600 - config['paddle_size'], game_state['left_paddle']['y'] + config['player_speed'])
        
        # IA DRAMATICAMENTE DIFERENTE por dificuldade
        current_time = time.time() * 1000  # em milissegundos
        if current_time - game_state['ai_last_move'] > config['ai_reaction']:
            ball_y = game_state['ball']['y']
            paddle_center = game_state['right_paddle']['y'] + config['paddle_size'] // 2
            
            if game_state['difficulty'] == 'fácil':
                # FÁCIL: IA muito burra e lenta
                if random.random() < 0.3:  # Só se move 30% das vezes
                    if ball_y < paddle_center - 30:  # Margem grande
                        game_state['right_paddle']['y'] = max(0, game_state['right_paddle']['y'] - config['ai_speed'])
                    elif ball_y > paddle_center + 30:
                        game_state['right_paddle']['y'] = min(600 - config['paddle_size'], game_state['right_paddle']['y'] + config['ai_speed'])
                        
            elif game_state['difficulty'] == 'normal':
                # NORMAL: IA equilibrada
                if random.random() < config['ai_accuracy']:
                    if ball_y < paddle_center - 15:
                        game_state['right_paddle']['y'] = max(0, game_state['right_paddle']['y'] - config['ai_speed'])
                    elif ball_y > paddle_center + 15:
                        game_state['right_paddle']['y'] = min(600 - config['paddle_size'], game_state['right_paddle']['y'] + config['ai_speed'])
                        
            elif game_state['difficulty'] == 'difícil':
                # DIFÍCIL: IA rápida e precisa
                if ball_y < paddle_center - 10:
                    game_state['right_paddle']['y'] = max(0, game_state['right_paddle']['y'] - config['ai_speed'])
                elif ball_y > paddle_center + 10:
                    game_state['right_paddle']['y'] = min(600 - config['paddle_size'], game_state['right_paddle']['y'] + config['ai_speed'])
                    
            elif game_state['difficulty'] == 'expert':
                # EXPERT: IA PERFEITA com previsão
                # Prever onde a bola vai estar
                ball_x = game_state['ball']['x']
                ball_dx = game_state['ball']['dx']
                if ball_dx > 0:  # Bola indo para direita
                    # Calcular onde a bola vai estar quando chegar na raquete
                    time_to_reach = (735 - ball_x) / ball_dx
                    predicted_y = ball_y + (game_state['ball']['dy'] * time_to_reach)
                    
                    # Ajustar para margens do canvas
                    if predicted_y < 0:
                        predicted_y = -predicted_y
                    elif predicted_y > 600:
                        predicted_y = 1200 - predicted_y
                    
                    # IA vai para a posição predita
                    if predicted_y < paddle_center - 5:
                        game_state['right_paddle']['y'] = max(0, game_state['right_paddle']['y'] - config['ai_speed'])
                    elif predicted_y > paddle_center + 5:
                        game_state['right_paddle']['y'] = min(600 - config['paddle_size'], game_state['right_paddle']['y'] + config['ai_speed'])
            
            game_state['ai_last_move'] = current_time
        
        # Mover bola
        game_state['ball']['x'] += game_state['ball']['dx']
        game_state['ball']['y'] += game_state['ball']['dy']
        
        # Verificação de segurança: se a bola ficar presa, forçar movimento
        if abs(game_state['ball']['dx']) < 0.1:
            game_state['ball']['dx'] = config['ball_speed'] if game_state['ball']['dx'] >= 0 else -config['ball_speed']
        
        # Colisões com topo/fundo
        if game_state['ball']['y'] <= 10 or game_state['ball']['y'] >= 590:
            game_state['ball']['dy'] = -game_state['ball']['dy']
        
        # Colisão com raquete do jogador (esquerda) - CORRIGIDA
        if (game_state['ball']['x'] - game_state['ball']['radius'] <= game_state['left_paddle']['x'] + game_state['left_paddle']['width'] and
            game_state['ball']['x'] + game_state['ball']['radius'] >= game_state['left_paddle']['x'] and
            game_state['ball']['y'] >= game_state['left_paddle']['y'] and 
            game_state['ball']['y'] <= game_state['left_paddle']['y'] + config['paddle_size'] and
            game_state['ball']['dx'] < 0):  # Só colide se estiver indo para a esquerda
            
            # Efeito de spin baseado na dificuldade
            ball_center = game_state['ball']['y']
            paddle_center = game_state['left_paddle']['y'] + config['paddle_size'] // 2
            relative_intersect_y = (ball_center - paddle_center) / (config['paddle_size'] // 2)
            
            # Ajustar velocidade baseado na dificuldade
            game_state['ball']['dx'] = abs(game_state['ball']['dx'])  # Mudar direção
            game_state['ball']['dy'] = relative_intersect_y * config['ball_speed']
            
            # Garantir que a bola não fique presa
            game_state['ball']['x'] = game_state['left_paddle']['x'] + game_state['left_paddle']['width'] + game_state['ball']['radius']
            
        # Colisão com raquete da IA (direita) - CORRIGIDA
        if (game_state['ball']['x'] + game_state['ball']['radius'] >= game_state['right_paddle']['x'] and
            game_state['ball']['x'] - game_state['ball']['radius'] <= game_state['right_paddle']['x'] + game_state['right_paddle']['width'] and
            game_state['ball']['y'] >= game_state['right_paddle']['y'] and 
            game_state['ball']['y'] <= game_state['right_paddle']['y'] + config['paddle_size'] and
            game_state['ball']['dx'] > 0):  # Só colide se estiver indo para a direita
            
            # Efeito de spin baseado na dificuldade
            ball_center = game_state['ball']['y']
            paddle_center = game_state['right_paddle']['y'] + config['paddle_size'] // 2
            relative_intersect_y = (ball_center - paddle_center) / (config['paddle_size'] // 2)
            
            # Ajustar velocidade baseado na dificuldade
            game_state['ball']['dx'] = -abs(game_state['ball']['dx'])  # Mudar direção
            game_state['ball']['dy'] = relative_intersect_y * config['ball_speed']
            
            # Garantir que a bola não fique presa
            game_state['ball']['x'] = game_state['right_paddle']['x'] - game_state['ball']['radius']
        
        # Pontuação
        if game_state['ball']['x'] < -50:  # Margem maior para evitar travamento
            game_state['bot_score'] += 1
            # Reset da bola com velocidade baseada na dificuldade
            game_state['ball']['x'] = 400
            game_state['ball']['y'] = 300
            game_state['ball']['dx'] = random.choice([-config['ball_speed'], config['ball_speed']])
            game_state['ball']['dy'] = random.choice([-config['ball_speed']//2, config['ball_speed']//2])
        elif game_state['ball']['x'] > 850:  # Margem maior para evitar travamento
            game_state['player_score'] += 1
            # Reset da bola com velocidade baseada na dificuldade
            game_state['ball']['x'] = 400
            game_state['ball']['y'] = 300
            game_state['ball']['dx'] = random.choice([-config['ball_speed'], config['ball_speed']])
            game_state['ball']['dy'] = random.choice([-config['ball_speed']//2, config['ball_speed']//2])
        
        # Correção de emergência: se a bola ficar muito tempo atrás das raquetes
        if (game_state['ball']['x'] < 0 or game_state['ball']['x'] > 800):
            # Forçar reset da posição
            game_state['ball']['x'] = 400
            game_state['ball']['y'] = 300
            game_state['ball']['dx'] = random.choice([-config['ball_speed'], config['ball_speed']])
            game_state['ball']['dy'] = random.choice([-config['ball_speed']//2, config['ball_speed']//2])
        
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
