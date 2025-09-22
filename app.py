"""
ByThePong Web - Aplicação Flask Principal
Backend web mantendo POO e encapsulamento
"""

from flask import Flask, render_template, request, jsonify, session
# from flask_socketio import SocketIO, emit
import uuid
import json
from datetime import datetime
import os

# Importa as classes existentes do jogo
from player import Player
from ball import Ball
from paddle import Paddle
from score_manager import ScoreManager

class WebGameManager:
    """
    Gerenciador de jogos web - mantém encapsulamento e coordena sessões
    """
    
    def __init__(self):
        self.__active_games = {}  # Dicionário de jogos ativos
        self.__score_manager = ScoreManager()
    
    def create_game_session(self, player_name: str, difficulty: str = "normal") -> str:
        """
        Cria uma nova sessão de jogo
        
        Args:
            player_name (str): Nome do jogador
            difficulty (str): Nível de dificuldade
            
        Returns:
            str: ID da sessão do jogo
        """
        game_id = str(uuid.uuid4())
        
        # Cria objetos do jogo com encapsulamento
        player = Player(player_name)
        bot = Player("Bot")
        
        # Configurações de dificuldade (mantém lógica original)
        difficulty_settings = self.__get_difficulty_settings(difficulty)
        
        # Inicializa objetos com dimensões web padrão
        ball = Ball(400, 300, 10, difficulty_settings["ball_speed"])
        left_paddle = Paddle(50, 250, 15, 100, 7)
        right_paddle = Paddle(735, 250, 15, 100, difficulty_settings["ai_speed"])
        
        game_session = {
            'id': game_id,
            'player': player,
            'bot': bot,
            'ball': ball,
            'left_paddle': left_paddle,
            'right_paddle': right_paddle,
            'difficulty': difficulty,
            'difficulty_settings': difficulty_settings,
            'game_running': False,
            'game_start_time': 0,
            'game_duration': 120,  # 2 minutos
            'created_at': datetime.now(),
            'width': 800,
            'height': 600
        }
        
        self.__active_games[game_id] = game_session
        return game_id
    
    def __get_difficulty_settings(self, difficulty: str) -> dict:
        """
        Retorna configurações de dificuldade (mesmo do jogo original)
        
        Args:
            difficulty (str): Nível de dificuldade
            
        Returns:
            dict: Configurações
        """
        settings = {
            "fácil": {
                "ai_difficulty": 0.3,
                "ball_speed": 3,
                "ai_speed": 4,
                "description": "Perfeito para iniciantes"
            },
            "normal": {
                "ai_difficulty": 0.6,
                "ball_speed": 5,
                "ai_speed": 6,
                "description": "Equilibrado e divertido"
            },
            "difícil": {
                "ai_difficulty": 0.8,
                "ball_speed": 7,
                "ai_speed": 8,
                "description": "Para jogadores experientes"
            },
            "expert": {
                "ai_difficulty": 0.95,
                "ball_speed": 9,
                "ai_speed": 10,
                "description": "Apenas para os melhores!"
            }
        }
        return settings.get(difficulty, settings["normal"])
    
    def get_game_session(self, game_id: str) -> dict:
        """
        Retorna sessão de jogo específica
        
        Args:
            game_id (str): ID da sessão
            
        Returns:
            dict: Dados da sessão ou None
        """
        return self.__active_games.get(game_id)
    
    def get_game_state(self, game_id: str) -> dict:
        """
        Retorna estado atual do jogo para envio ao frontend
        
        Args:
            game_id (str): ID da sessão
            
        Returns:
            dict: Estado serializado do jogo
        """
        game = self.get_game_session(game_id)
        if not game:
            return None
        
        return {
            'game_id': game_id,
            'player': {
                'name': game['player'].name,
                'score': game['player'].score
            },
            'bot': {
                'name': game['bot'].name,
                'score': game['bot'].score
            },
            'ball': {
                'x': game['ball'].x,
                'y': game['ball'].y,
                'radius': game['ball'].radius
            },
            'left_paddle': {
                'x': game['left_paddle'].x,
                'y': game['left_paddle'].y,
                'width': game['left_paddle'].width,
                'height': game['left_paddle'].height
            },
            'right_paddle': {
                'x': game['right_paddle'].x,
                'y': game['right_paddle'].y,
                'width': game['right_paddle'].width,
                'height': game['right_paddle'].height
            },
            'difficulty': game['difficulty'],
            'game_running': game['game_running'],
            'width': game['width'],
            'height': game['height']
        }
    
    def start_game(self, game_id: str) -> bool:
        """
        Inicia o jogo
        
        Args:
            game_id (str): ID da sessão
            
        Returns:
            bool: Sucesso da operação
        """
        game = self.get_game_session(game_id)
        if not game:
            return False
        
        game['game_running'] = True
        game['game_start_time'] = datetime.now().timestamp()
        game['player'].reset_score()
        game['bot'].reset_score()
        game['ball'].reset(game['width'] // 2, game['height'] // 2)
        
        return True
    
    def update_paddle_position(self, game_id: str, direction: str) -> bool:
        """
        Atualiza posição da raquete do jogador
        
        Args:
            game_id (str): ID da sessão
            direction (str): "up" ou "down"
            
        Returns:
            bool: Sucesso da operação
        """
        game = self.get_game_session(game_id)
        if not game or not game['game_running']:
            return False
        
        if direction == "up":
            game['left_paddle'].move_up(game['height'])
        elif direction == "down":
            game['left_paddle'].move_down(game['height'])
        
        return True
    
    def remove_game_session(self, game_id: str):
        """
        Remove sessão de jogo
        
        Args:
            game_id (str): ID da sessão
        """
        if game_id in self.__active_games:
            del self.__active_games[game_id]
    
    @property
    def score_manager(self) -> ScoreManager:
        """Retorna gerenciador de pontuação"""
        return self.__score_manager

# Inicializa Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bythepong_secret_key_2024'
# socketio = SocketIO(app, cors_allowed_origins="*")

# Gerenciador global de jogos
game_manager = WebGameManager()

@app.route('/')
def index():
    """Página principal do jogo"""
    return render_template('index.html')

@app.route('/game')
def game():
    """Página do jogo"""
    return render_template('game.html')

@app.route('/api/create_game', methods=['POST'])
def create_game():
    """
    API para criar nova sessão de jogo
    """
    data = request.json
    player_name = data.get('player_name', 'Jogador')
    difficulty = data.get('difficulty', 'normal')
    
    if not player_name.strip():
        return jsonify({'error': 'Nome do jogador é obrigatório'}), 400
    
    try:
        game_id = game_manager.create_game_session(player_name, difficulty)
        session['game_id'] = game_id
        
        return jsonify({
            'success': True,
            'game_id': game_id,
            'message': 'Jogo criado com sucesso'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/game_state/<game_id>')
def get_game_state(game_id):
    """
    API para obter estado atual do jogo
    """
    state = game_manager.get_game_state(game_id)
    if not state:
        return jsonify({'error': 'Jogo não encontrado'}), 404
    
    return jsonify(state)

@app.route('/api/start_game/<game_id>', methods=['POST'])
def start_game(game_id):
    """
    API para iniciar o jogo
    """
    if game_manager.start_game(game_id):
        return jsonify({'success': True, 'message': 'Jogo iniciado'})
    else:
        return jsonify({'error': 'Erro ao iniciar jogo'}), 400

@app.route('/api/ranking')
def get_ranking():
    """
    API para obter ranking
    """
    try:
        ranking = game_manager.score_manager.get_ranking()
        return jsonify({
            'success': True,
            'ranking': ranking
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/paddle_move/<game_id>', methods=['POST'])
def move_paddle(game_id):
    """
    API para mover raquete do jogador
    """
    data = request.json
    direction = data.get('direction')
    
    if direction not in ['up', 'down']:
        return jsonify({'error': 'Direção inválida'}), 400
    
    if game_manager.update_paddle_position(game_id, direction):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Erro ao mover raquete'}), 400

# WebSocket Events
# @socketio.on('connect')
# def handle_connect():
#     """Usuário conectou"""
#     emit('connected', {'message': 'Conectado ao ByThePong!'})

# @socketio.on('disconnect')
# def handle_disconnect():
#     """Usuário desconectou"""
#     game_id = session.get('game_id')
#     if game_id:
#         game_manager.remove_game_session(game_id)

# @socketio.on('join_game')
# def handle_join_game(data):
#     """Usuário entrou no jogo"""
#     game_id = data.get('game_id')
#     if game_id:
#         session['game_id'] = game_id
#         emit('game_joined', {'game_id': game_id})

# @socketio.on('paddle_move')
# def handle_paddle_move(data):
#     """Movimento da raquete via WebSocket"""
#     game_id = session.get('game_id')
#     direction = data.get('direction')
    
#     if game_id and game_manager.update_paddle_position(game_id, direction):
#         # Emite estado atualizado para todos os clientes do jogo
#         state = game_manager.get_game_state(game_id)
#         emit('game_update', state, broadcast=True)

if __name__ == '__main__':
    # Cria diretório de templates se não existir
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Iniciando ByThePong Web...")
    print("📱 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

