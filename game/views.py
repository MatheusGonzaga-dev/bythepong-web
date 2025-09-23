from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import os

# Importar models apenas se o banco estiver disponível
DB_AVAILABLE = False
try:
    from .models import Player, GameSession
    DB_AVAILABLE = True
except Exception as e:
    print(f"Models não disponíveis: {e}")

# Importar game_logic com fallback
try:
    from .game_logic import Game
    GAME_LOGIC_AVAILABLE = True
except Exception as e:
    print(f"Game logic não disponível: {e}")
    GAME_LOGIC_AVAILABLE = False

# Importar versão simples como fallback
try:
    from .simple_game import SimpleGame
    SIMPLE_GAME_AVAILABLE = True
except Exception as e:
    print(f"Simple game não disponível: {e}")
    SIMPLE_GAME_AVAILABLE = False

# Instância global do jogo (em produção, usar Redis ou banco)
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
        
        # Criar nova instância do jogo
        if GAME_LOGIC_AVAILABLE:
            current_game = Game(difficulty=difficulty)
        elif SIMPLE_GAME_AVAILABLE:
            current_game = SimpleGame(difficulty=difficulty)
        else:
            return JsonResponse({'error': 'Sistema de jogo não disponível'}, status=500)
            
        current_game.start_game()
        
        return JsonResponse({
            'success': True,
            'player_name': player_name,
            'difficulty': difficulty,
            'game_state': current_game.to_dict()
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
        player_direction = data.get('direction')  # 'up', 'down', ou None
        
        current_game.update(player_direction)
        
        return JsonResponse({
            'success': True,
            'game_state': current_game.to_dict()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def end_game(request):
    """Finaliza o jogo e salva resultado"""
    global current_game
    
    if not current_game:
        return JsonResponse({'error': 'Nenhum jogo ativo'}, status=400)
    
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()
        
        if not player_name:
            return JsonResponse({'error': 'Nome do jogador é obrigatório'}, status=400)
        
        # Determinar vencedor
        won = current_game.winner == 'player'
        
        result = {
            'success': True,
            'final_score': {
                'player': current_game.player_score,
                'bot': current_game.bot_score
            },
            'winner': current_game.winner,
            'won': won
        }
        
        # Limpar jogo atual
        current_game = None
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ranking(request):
    """Página de ranking"""
    if not DB_AVAILABLE:
        # Dados mockados quando o banco não está disponível
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
    
    try:
        # Buscar jogadores e ordenar por best_score (a propriedade win_rate será calculada no template)
        players = Player.objects.all().order_by('-best_score', '-total_wins')
        
        # Ordenar por win_rate usando Python (já que é uma propriedade)
        players_list = list(players)
        players_list.sort(key=lambda p: p.win_rate, reverse=True)
        
        recent_games = GameSession.objects.select_related('player').order_by('-created_at')[:10]
        
        # Estatísticas por dificuldade
        easy_games = GameSession.objects.filter(difficulty='fácil').count()
        normal_games = GameSession.objects.filter(difficulty='normal').count()
        hard_games = GameSession.objects.filter(difficulty='difícil').count()
        expert_games = GameSession.objects.filter(difficulty='expert').count()
        
        # Total de partidas
        total_games = GameSession.objects.count()
        
        context = {
            'players': players_list,
            'recent_games': recent_games,
            'easy_games': easy_games,
            'normal_games': normal_games,
            'hard_games': hard_games,
            'expert_games': expert_games,
            'total_games': total_games
        }
        
        return render(request, 'game/ranking.html', context)
        
    except Exception as e:
        # Fallback em caso de erro
        context = {
            'players': [],
            'recent_games': [],
            'easy_games': 0,
            'normal_games': 0,
            'hard_games': 0,
            'expert_games': 0,
            'total_games': 0,
            'db_error': str(e)
        }
        return render(request, 'game/ranking.html', context)
