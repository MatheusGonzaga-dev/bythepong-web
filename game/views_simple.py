from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import time

# Instância global do jogo simples
current_game = None


def home(request):
    """Página inicial com informações sobre o jogo"""
    return render(request, 'game/home.html')


def index(request):
    """Página de configuração do jogo"""
    return render(request, 'game/index.html')


def game_view(request):
    """Página do jogo"""
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
@require_http_methods(["POST"])
def start_game(request):
    """Inicia uma nova partida"""
    global current_game

    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()
        difficulty = data.get('difficulty', 'normal')

        if not player_name:
            return JsonResponse({'error': 'Nome do jogador é obrigatório'}, status=400)

        # Canvas e bola
        canvas_width = 800
        canvas_height = 600
        ball_radius = 10

        # Dimensões das raquetes por dificuldade
        if difficulty == 'fácil':
            paddle_width_l, paddle_height_l = 15, 100
            paddle_width_r, paddle_height_r = 15, 100
        elif difficulty == 'normal':
            paddle_width_l, paddle_height_l = 15, 100
            paddle_width_r, paddle_height_r = 15, 100
        elif difficulty == 'difícil':
            paddle_width_l, paddle_height_l = 12, 60
            paddle_width_r, paddle_height_r = 12, 60
        else:  # expert -> jogador pequeno, bot grande
            paddle_width_l, paddle_height_l = 10, ball_radius * 2
            paddle_width_r, paddle_height_r = 16, 120

        # Posições iniciais centralizadas verticalmente
        left_y = canvas_height // 2 - paddle_height_l // 2
        right_y = canvas_height // 2 - paddle_height_r // 2

        # Criar jogo simples inline
        current_game = {
            'canvas_width': canvas_width,
            'canvas_height': canvas_height,
            'paddle_width': paddle_width_l,
            'paddle_height': paddle_height_l,
            'ball_radius': ball_radius,
            'left_paddle': {
                'x': 50,
                'y': left_y,
                'width': paddle_width_l,
                'height': paddle_height_l
            },
            'right_paddle': {
                'x': canvas_width - 50 - paddle_width_r,
                'y': right_y,
                'width': paddle_width_r,
                'height': paddle_height_r
            },
            'ball': {
                'x': canvas_width // 2,
                'y': canvas_height // 2,
                'radius': ball_radius,
                'dx': 7,
                'dy': 3
            },
            'player_score': 0,
            'bot_score': 0,
            'game_over': False,
            'winner': None,
            'remaining_time': 120,
            'difficulty': difficulty,
            'start_time': time.time()
        }

        return JsonResponse({
            'success': True,
            'player_name': player_name,
            'difficulty': difficulty,
            'game_state': current_game
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_game(request):
    """Atualiza o estado do jogo"""
    global current_game

    if not current_game:
        return JsonResponse({'error': 'Nenhum jogo ativo'}, status=400)

    try:
        data = json.loads(request.body)
        player_direction = data.get('direction')

        canvas_height = current_game['canvas_height']
        ball_r = current_game['ball_radius']
        lp = current_game['left_paddle']
        rp = current_game['right_paddle']

        # Atualizar tempo
        elapsed = time.time() - current_game['start_time']
        current_game['remaining_time'] = max(0, 120 - int(elapsed))

        # Mover raquete do jogador
        if player_direction == 'up':
            lp['y'] = max(0, lp['y'] - 8)
        elif player_direction == 'down':
            lp['y'] = min(canvas_height - lp['height'], lp['y'] + 8)

        # IA da raquete direita
        ball_center_y = current_game['ball']['y']
        paddle_center_y = rp['y'] + rp['height'] // 2

        speed = 4 if current_game['difficulty'] == 'fácil' else 6 if current_game['difficulty'] == 'normal' else 8 if current_game['difficulty'] == 'difícil' else 10

        if ball_center_y < paddle_center_y - 10:
            rp['y'] = max(0, rp['y'] - speed)
        elif ball_center_y > paddle_center_y + 10:
            rp['y'] = min(canvas_height - rp['height'], rp['y'] + speed)

        # Mover bola
        current_game['ball']['x'] += current_game['ball']['dx']
        current_game['ball']['y'] += current_game['ball']['dy']

        # Colisão com topo/fundo
        if current_game['ball']['y'] <= ball_r or current_game['ball']['y'] >= canvas_height - ball_r:
            current_game['ball']['dy'] = -current_game['ball']['dy']

        # Colisão com raquete esquerda
        if (current_game['ball']['x'] - ball_r <= lp['x'] + lp['width'] and
            current_game['ball']['x'] + ball_r >= lp['x'] and
            current_game['ball']['y'] + ball_r >= lp['y'] and
            current_game['ball']['y'] - ball_r <= lp['y'] + lp['height']):
            current_game['ball']['dx'] = abs(current_game['ball']['dx'])

        # Colisão com raquete direita
        if (current_game['ball']['x'] + ball_r >= rp['x'] and
            current_game['ball']['x'] - ball_r <= rp['x'] + rp['width'] and
            current_game['ball']['y'] + ball_r >= rp['y'] and
            current_game['ball']['y'] - ball_r <= rp['y'] + rp['height']):
            current_game['ball']['dx'] = -abs(current_game['ball']['dx'])

        # Pontuação
        if current_game['ball']['x'] < 0:
            current_game['bot_score'] += 1
            current_game['ball']['x'] = current_game['canvas_width'] // 2
            current_game['ball']['y'] = current_game['canvas_height'] // 2
            current_game['ball']['dx'] = random.choice([-7, 7])
            current_game['ball']['dy'] = random.choice([-3, 3])
        elif current_game['ball']['x'] > current_game['canvas_width']:
            current_game['player_score'] += 1
            current_game['ball']['x'] = current_game['canvas_width'] // 2
            current_game['ball']['y'] = current_game['canvas_height'] // 2
            current_game['ball']['dx'] = random.choice([-7, 7])
            current_game['ball']['dy'] = random.choice([-3, 3])

        # Verificar fim do jogo
        if current_game['player_score'] >= 3 or current_game['bot_score'] >= 3 or current_game['remaining_time'] <= 0:
            current_game['game_over'] = True
            if current_game['player_score'] > current_game['bot_score']:
                current_game['winner'] = 'player'
            elif current_game['bot_score'] > current_game['player_score']:
                current_game['winner'] = 'bot'
            else:
                current_game['winner'] = 'tie'

        return JsonResponse({
            'success': True,
            'game_state': current_game
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def end_game(request):
    """Finaliza o jogo"""
    global current_game

    if not current_game:
        return JsonResponse({'error': 'Nenhum jogo ativo'}, status=400)

    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()

        if not player_name:
            return JsonResponse({'error': 'Nome do jogador é obrigatório'}, status=400)

        # Determinar vencedor
        won = current_game['winner'] == 'player'

        result = {
            'success': True,
            'final_score': {
                'player': current_game['player_score'],
                'bot': current_game['bot_score']
            },
            'winner': current_game['winner'],
            'won': won
        }

        # Limpar jogo atual
        current_game = None

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
