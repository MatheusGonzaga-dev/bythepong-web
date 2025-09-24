import random
import time

class SimpleGame:
    """Versão simplificada do jogo para funcionar na Vercel"""
    
    def __init__(self, difficulty='normal'):
        self.difficulty = difficulty
        self.canvas_width = 800
        self.canvas_height = 600
        self.ball_radius = 10
        
        # Dimensões de raquete por dificuldade
        if difficulty == 'fácil':
            self.paddle_width_l, self.paddle_height_l = 15, 100
            self.paddle_width_r, self.paddle_height_r = 15, 100
        elif difficulty == 'normal':
            self.paddle_width_l, self.paddle_height_l = 15, 100
            self.paddle_width_r, self.paddle_height_r = 15, 100
        elif difficulty == 'difícil':
            self.paddle_width_l, self.paddle_height_l = 12, 60
            self.paddle_width_r, self.paddle_height_r = 12, 60
        else:  # expert -> jogador pequeno, bot grande
            self.paddle_width_l, self.paddle_height_l = 10, self.ball_radius * 2
            self.paddle_width_r, self.paddle_height_r = 16, 120
        
        # Posições iniciais
        self.left_paddle = {
            'x': 50,
            'y': self.canvas_height // 2 - self.paddle_height_l // 2,
            'width': self.paddle_width_l,
            'height': self.paddle_height_l
        }
        
        self.right_paddle = {
            'x': self.canvas_width - 50 - self.paddle_width_r,
            'y': self.canvas_height // 2 - self.paddle_height_r // 2,
            'width': self.paddle_width_r,
            'height': self.paddle_height_r
        }
        
        self.ball = {
            'x': self.canvas_width // 2,
            'y': self.canvas_height // 2,
            'radius': self.ball_radius,
            'dx': 5 if difficulty == 'fácil' else 7 if difficulty == 'normal' else 9 if difficulty == 'difícil' else 11,
            'dy': random.choice([-3, -2, 2, 3])
        }
        
        # Scores
        self.player_score = 0
        self.bot_score = 0
        self.game_over = False
        self.winner = None
        self.remaining_time = 120  # 2 minutos
        self.start_time = time.time()
        
    def start_game(self):
        """Inicia o jogo"""
        self.start_time = time.time()
        self.game_over = False
        self.winner = None
        
    def update(self, player_direction=None):
        """Atualiza o estado do jogo"""
        if self.game_over:
            return
            
        # Atualizar tempo
        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, 120 - int(elapsed))
        
        # Mover raquete do jogador
        if player_direction == 'up':
            self.left_paddle['y'] = max(0, self.left_paddle['y'] - 8)
        elif player_direction == 'down':
            self.left_paddle['y'] = min(self.canvas_height - self.paddle_height_l, 
                                      self.left_paddle['y'] + 8)
        
        # IA da raquete direita
        ball_center_y = self.ball['y']
        paddle_center_y = self.right_paddle['y'] + self.paddle_height_r // 2
        
        speed = 4 if self.difficulty == 'fácil' else 6 if self.difficulty == 'normal' else 8 if self.difficulty == 'difícil' else 10
        
        if ball_center_y < paddle_center_y - 10:
            self.right_paddle['y'] = max(0, self.right_paddle['y'] - speed)
        elif ball_center_y > paddle_center_y + 10:
            self.right_paddle['y'] = min(self.canvas_height - self.paddle_height_r,
                                       self.right_paddle['y'] + speed)
        
        # Mover bola
        self.ball['x'] += self.ball['dx']
        self.ball['y'] += self.ball['dy']
        
        # Colisão com topo/fundo
        if self.ball['y'] <= self.ball_radius or self.ball['y'] >= self.canvas_height - self.ball_radius:
            self.ball['dy'] = -self.ball['dy']
        
        # Colisão com raquete esquerda (jogador)
        if (self.ball['x'] - self.ball_radius <= self.left_paddle['x'] + self.paddle_width_l and
            self.ball['x'] + self.ball_radius >= self.left_paddle['x'] and
            self.ball['y'] + self.ball_radius >= self.left_paddle['y'] and
            self.ball['y'] - self.ball_radius <= self.left_paddle['y'] + self.paddle_height_l):
            self.ball['dx'] = abs(self.ball['dx'])
        
        # Colisão com raquete direita (bot)
        if (self.ball['x'] + self.ball_radius >= self.right_paddle['x'] and
            self.ball['x'] - self.ball_radius <= self.right_paddle['x'] + self.paddle_width_r and
            self.ball['y'] + self.ball_radius >= self.right_paddle['y'] and
            self.ball['y'] - self.ball_radius <= self.right_paddle['y'] + self.paddle_height_r):
            self.ball['dx'] = -abs(self.ball['dx'])
        
        # Pontuação
        if self.ball['x'] < 0:
            self.bot_score += 1
            self.reset_ball()
        elif self.ball['x'] > self.canvas_width:
            self.player_score += 1
            self.reset_ball()
        
        # Verificar fim do jogo
        if self.player_score >= 3 or self.bot_score >= 3 or self.remaining_time <= 0:
            self.game_over = True
            if self.player_score > self.bot_score:
                self.winner = 'player'
            elif self.bot_score > self.player_score:
                self.winner = 'bot'
            else:
                self.winner = 'tie'
    
    def reset_ball(self):
        """Reseta a posição da bola"""
        self.ball['x'] = self.canvas_width // 2
        self.ball['y'] = self.canvas_height // 2
        self.ball['dx'] = random.choice([-abs(self.ball['dx']), abs(self.ball['dx'])])
        self.ball['dy'] = random.choice([-3, -2, 2, 3])
    
    def to_dict(self):
        """Converte o estado do jogo para dicionário"""
        return {
            'left_paddle': self.left_paddle,
            'right_paddle': self.right_paddle,
            'ball': self.ball,
            'player_score': self.player_score,
            'bot_score': self.bot_score,
            'game_over': self.game_over,
            'winner': self.winner,
            'remaining_time': self.remaining_time,
            'difficulty': self.difficulty,
            'canvas_width': self.canvas_width,
            'canvas_height': self.canvas_height
        }
    
    def get_remaining_time(self):
        """Retorna o tempo restante"""
        return self.remaining_time
