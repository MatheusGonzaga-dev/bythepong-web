import random
import time
from typing import Tuple, Dict, Any

class Ball:
    """Classe para a bola do jogo com encapsulamento"""
    
    def __init__(self, x: int, y: int, radius: int = 10):
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__dx = 0
        self.__dy = 0
        self.__speed = 5
    
    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y
    
    @property
    def radius(self) -> int:
        return self.__radius
    
    @property
    def dx(self) -> int:
        return self.__dx
    
    @property
    def dy(self) -> int:
        return self.__dy
    
    def set_position(self, x: int, y: int):
        """Define posição da bola"""
        self.__x = x
        self.__y = y
    
    def set_velocity(self, dx: int, dy: int):
        """Define velocidade da bola"""
        self.__dx = dx
        self.__dy = dy
    
    def move(self):
        """Move a bola"""
        self.__x += self.__dx
        self.__y += self.__dy
    
    def bounce_wall(self):
        """Inverte direção vertical ao bater na parede"""
        self.__dy = -self.__dy
    
    def bounce_paddle(self):
        """Inverte direção horizontal ao bater na raquete"""
        self.__dx = -self.__dx
    
    def reset(self, center_x: int, center_y: int):
        """Reseta a bola para o centro"""
        self.__x = center_x
        self.__y = center_y
        self.__dx = random.choice([-self.__speed, self.__speed])
        self.__dy = random.choice([-self.__speed, self.__speed])
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'x': self.__x,
            'y': self.__y,
            'radius': self.__radius,
            'dx': self.__dx,
            'dy': self.__dy
        }

class Paddle:
    """Classe para a raquete com encapsulamento"""
    
    def __init__(self, x: int, y: int, width: int = 15, height: int = 100):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__speed = 5
    
    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y
    
    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height
    
    def move_up(self):
        """Move a raquete para cima"""
        self.__y = max(0, self.__y - self.__speed)
    
    def move_down(self, max_height: int):
        """Move a raquete para baixo"""
        self.__y = min(max_height - self.__height, self.__y + self.__speed)
    
    def set_position(self, y: int, max_height: int):
        """Define posição da raquete"""
        self.__y = max(0, min(max_height - self.__height, y))
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'x': self.__x,
            'y': self.__y,
            'width': self.__width,
            'height': self.__height
        }

class Game:
    """Classe principal do jogo com encapsulamento"""
    
    def __init__(self, width: int = 800, height: int = 600, difficulty: str = 'normal'):
        self.__width = width
        self.__height = height
        self.__difficulty = difficulty
        self.__player_score = 0
        self.__bot_score = 0
        self.__game_start_time = None
        self.__game_duration = 120  # 2 minutos
        self.__game_over = False
        self.__winner = None
        
        # Configurações baseadas na dificuldade
        self.__difficulty_settings = self.__get_difficulty_settings()
        
        # Inicializar objetos do jogo
        self.__ball = Ball(width // 2, height // 2)
        self.__left_paddle = Paddle(50, height // 2 - 50)
        self.__right_paddle = Paddle(width - 65, height // 2 - 50)
        
        # Configurar velocidade baseada na dificuldade
        self.__ball.set_velocity(
            self.__difficulty_settings['ball_speed'],
            self.__difficulty_settings['ball_speed']
        )
    
    def __get_difficulty_settings(self) -> Dict[str, int]:
        """Retorna configurações baseadas na dificuldade"""
        settings = {
            'fácil': {'ball_speed': 3, 'bot_speed': 2},
            'normal': {'ball_speed': 5, 'bot_speed': 4},
            'difícil': {'ball_speed': 7, 'bot_speed': 6},
            'expert': {'ball_speed': 9, 'bot_speed': 8}
        }
        return settings.get(self.__difficulty, settings['normal'])
    
    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height
    
    @property
    def player_score(self) -> int:
        return self.__player_score
    
    @property
    def bot_score(self) -> int:
        return self.__bot_score
    
    @property
    def game_over(self) -> bool:
        return self.__game_over
    
    @property
    def winner(self) -> str:
        return self.__winner
    
    @property
    def difficulty(self) -> str:
        return self.__difficulty
    
    def start_game(self):
        """Inicia o jogo"""
        self.__game_start_time = time.time()
        self.__game_over = False
        self.__winner = None
        self.__player_score = 0
        self.__bot_score = 0
        self.__ball.reset(self.__width // 2, self.__height // 2)
    
    def update(self, player_direction: str = None):
        """Atualiza o estado do jogo"""
        if self.__game_over:
            return
        
        # Mover jogador
        if player_direction == 'up':
            self.__left_paddle.move_up()
        elif player_direction == 'down':
            self.__left_paddle.move_down(self.__height)
        
        # IA do bot
        self.__update_bot()
        
        # Mover bola
        self.__ball.move()
        
        # Verificar colisões
        self.__check_collisions()
        
        # Verificar pontuação
        self.__check_scoring()
        
        # Verificar fim do jogo
        self.__check_game_over()
    
    def __update_bot(self):
        """Atualiza a IA do bot"""
        bot_center = self.__right_paddle.y + self.__right_paddle.height // 2
        ball_y = self.__ball.y
        
        if ball_y < bot_center - 10:
            self.__right_paddle.move_up()
        elif ball_y > bot_center + 10:
            self.__right_paddle.move_down(self.__height)
    
    def __check_collisions(self):
        """Verifica colisões da bola"""
        # Colisão com paredes superior/inferior
        if self.__ball.y <= 0 or self.__ball.y >= self.__height - self.__ball.radius:
            self.__ball.bounce_wall()
        
        # Colisão com raquete esquerda (jogador)
        if (self.__ball.x <= self.__left_paddle.x + self.__left_paddle.width and
            self.__ball.y >= self.__left_paddle.y and
            self.__ball.y <= self.__left_paddle.y + self.__left_paddle.height):
            self.__ball.bounce_paddle()
        
        # Colisão com raquete direita (bot)
        if (self.__ball.x >= self.__right_paddle.x - self.__ball.radius and
            self.__ball.y >= self.__right_paddle.y and
            self.__ball.y <= self.__right_paddle.y + self.__right_paddle.height):
            self.__ball.bounce_paddle()
    
    def __check_scoring(self):
        """Verifica pontuação"""
        # Ponto do bot (bola passou pela esquerda)
        if self.__ball.x <= 0:
            self.__bot_score += 1
            self.__ball.reset(self.__width // 2, self.__height // 2)
        
        # Ponto do jogador (bola passou pela direita)
        elif self.__ball.x >= self.__width:
            self.__player_score += 1
            self.__ball.reset(self.__width // 2, self.__height // 2)
    
    def __check_game_over(self):
        """Verifica condições de fim de jogo"""
        # Primeiro a 3 pontos
        if self.__player_score >= 3:
            self.__game_over = True
            self.__winner = 'player'
        elif self.__bot_score >= 3:
            self.__game_over = True
            self.__winner = 'bot'
        
        # Tempo limite (2 minutos)
        elif self.__game_start_time and time.time() - self.__game_start_time >= self.__game_duration:
            self.__game_over = True
            if self.__player_score > self.__bot_score:
                self.__winner = 'player'
            elif self.__bot_score > self.__player_score:
                self.__winner = 'bot'
            else:
                self.__winner = 'draw'
    
    def get_remaining_time(self) -> int:
        """Retorna tempo restante em segundos"""
        if not self.__game_start_time:
            return self.__game_duration
        
        elapsed = time.time() - self.__game_start_time
        remaining = max(0, self.__game_duration - elapsed)
        return int(remaining)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte estado do jogo para dicionário"""
        return {
            'width': self.__width,
            'height': self.__height,
            'player_score': self.__player_score,
            'bot_score': self.__bot_score,
            'game_over': self.__game_over,
            'winner': self.__winner,
            'difficulty': self.__difficulty,
            'remaining_time': self.get_remaining_time(),
            'ball': self.__ball.to_dict(),
            'left_paddle': self.__left_paddle.to_dict(),
            'right_paddle': self.__right_paddle.to_dict()
        }

