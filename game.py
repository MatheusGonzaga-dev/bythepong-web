"""
Classe Game - Classe principal do jogo ByThePong
Implementa encapsulamento e coordena todas as outras classes
"""

import pygame
import sys
import math
import random
from typing import Tuple, Optional
from player import Player
from ball import Ball
from paddle import Paddle
from score_manager import ScoreManager
from responsive_utils import ResponsiveManager

class Game:
    def __init__(self, width: int = None, height: int = None, difficulty: str = "normal"):
        """
        Inicializa o jogo com dimensões da tela e dificuldade
        
        Args:
            width (int): Largura da tela (None para tela cheia)
            height (int): Altura da tela (None para tela cheia)
            difficulty (str): Nível de dificuldade ("fácil", "normal", "difícil", "expert")
        """
        pygame.init()
        
        # Configurações da tela - tela cheia se não especificado
        if width is None or height is None:
            info = pygame.display.Info()
            self.__width = info.current_w
            self.__height = info.current_h
            self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.FULLSCREEN)
        else:
            self.__width = width
            self.__height = height
            self.__screen = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption("ByThePong - Jogo Pong em Python")
        
        # Inicializa o gerenciador de responsividade
        self.__responsive = ResponsiveManager()
        self.__responsive.update_screen_size(self.__width, self.__height)
        
        # Cores
        self.__BLACK = (0, 0, 0)
        self.__WHITE = (255, 255, 255)
        self.__BLUE = (0, 100, 255)
        self.__RED = (255, 50, 50)
        self.__GREEN = (50, 255, 50)
        self.__GRAY = (128, 128, 128)
        self.__OBSTACLE = (80, 80, 200)
        self.__BUTTON_BG = (40, 40, 40)
        self.__BUTTON_BORDER = (200, 200, 200)
        
        # Configuração de dificuldade
        self.__difficulty = difficulty
        self.__difficulty_settings = self.__get_difficulty_settings()
        
        # Objetos do jogo com dimensões responsivas
        self.__player = Player()
        self.__bot = Player("Bot")
        
        # Propriedades responsivas
        paddle_props = self.__responsive.paddle_props
        ball_props = self.__responsive.ball_props
        margins = self.__responsive.margins
        
        # Dimensões das raquetes (reduzidas no expert)
        paddle_width = paddle_props['width']
        paddle_height = paddle_props['height']
        if self.__difficulty == "expert":
            paddle_height = max(ball_props['radius'] * 2, 6)
            paddle_width = max(self.__responsive.scale_width(10), 6)
        
        self.__ball = Ball(
            self.__width // 2, 
            self.__height // 2, 
            ball_props['radius'], 
            int(self.__difficulty_settings["ball_speed"] * ball_props['speed_multiplier']),
            max_speed=self.__difficulty_settings["ball_max_speed"],
            speed_increase_factor=self.__difficulty_settings["ball_speed_increase"],
            initial_angle_range=self.__difficulty_settings.get("initial_angle_range", math.pi/4)
        )
        
        self.__left_paddle = Paddle(
            margins['paddle_offset'], 
            self.__height // 2 - paddle_height // 2, 
            paddle_width, 
            paddle_height, 
            paddle_props['speed']
        )
        
        self.__right_paddle = Paddle(
            self.__width - margins['paddle_offset'] - paddle_width, 
            self.__height // 2 - paddle_height // 2, 
            paddle_width, 
            paddle_height, 
            int(self.__difficulty_settings["ai_speed"] * ball_props['speed_multiplier'])
        )
        self.__score_manager = ScoreManager()
        
        # Obstáculos (ativados para dificuldades elevadas)
        self.__obstacles = []  # lista de dicts: {rect: pygame.Rect, vx: int, vy: int}
        if self.__difficulty_settings["obstacles_enabled"]:
            self.__create_obstacles(self.__difficulty_settings["obstacles_count"], 
                                    self.__difficulty_settings["obstacles_speed"])
        
        # Estado do jogo
        self.__game_running = False
        self.__clock = pygame.time.Clock()
        self.__fps = 60
        self.__game_start_time = 0
        self.__game_duration = 120  # 2 minutos em segundos
        
        # Fontes responsivas
        self.__font_large = pygame.font.Font(None, self.__responsive.scale_font_size(74))
        self.__font_medium = pygame.font.Font(None, self.__responsive.scale_font_size(36))
        self.__font_small = pygame.font.Font(None, self.__responsive.scale_font_size(24))
        
        # Controle de IA para paddle direito
        self.__ai_difficulty = self.__difficulty_settings["ai_difficulty"]

        # Área do botão de tela cheia (definida no draw)
        self.__fullscreen_button_rect = None
    
    def __get_difficulty_settings(self) -> dict:
        """
        Retorna as configurações baseadas na dificuldade escolhida
        
        Returns:
            dict: Configurações de dificuldade
        """
        settings = {
            "fácil": {
                "ai_difficulty": 0.3,
                "ball_speed": 2,
                "ai_speed": 4,
                "ball_max_speed": 8,
                "ball_speed_increase": 1.02,
                "acceleration_factor": 1.0,  # sem aceleração contínua
                "initial_angle_range": math.pi/3,
                "obstacles_enabled": False,
                "obstacles_count": 0,
                "obstacles_speed": 0,
                "description": "Perfeito para iniciantes"
            },
            "normal": {
                "ai_difficulty": 0.6,
                "ball_speed": 5,
                "ai_speed": 6,
                "ball_max_speed": 12,
                "ball_speed_increase": 1.05,
                "acceleration_factor": 1.002,  # aceleração muito leve
                "initial_angle_range": math.pi/4,
                "obstacles_enabled": False,
                "obstacles_count": 0,
                "obstacles_speed": 0,
                "description": "Equilibrado e divertido"
            },
            "difícil": {
                "ai_difficulty": 0.92,
                "ball_speed": 10,
                "ai_speed": 10,
                "ball_max_speed": 60,
                "ball_speed_increase": 1.16,
                "acceleration_factor": 1.02,  # aceleração forte
                "initial_angle_range": math.pi/6,
                "obstacles_enabled": True,
                "obstacles_count": 1,
                "obstacles_speed": 7,
                "description": "Para jogadores experientes"
            },
            "expert": {
                "ai_difficulty": 0.99,
                "ball_speed": 12,
                "ai_speed": 14,
                "ball_max_speed": 90,
                "ball_speed_increase": 1.20,
                "acceleration_factor": 1.03,  # aceleração muito forte
                "initial_angle_range": math.pi/8,
                "obstacles_enabled": True,
                "obstacles_count": 2,
                "obstacles_speed": 9,
                "description": "Apenas para os melhores!"
            }
        }
        
        return settings.get(self.__difficulty, settings["normal"])
    
    @property
    def width(self) -> int:
        """Retorna a largura da tela"""
        return self.__width
    
    @property
    def height(self) -> int:
        """Retorna a altura da tela"""
        return self.__height
    
    @property
    def player(self) -> Player:
        """Retorna o objeto do jogador"""
        return self.__player
    
    @property
    def score_manager(self) -> ScoreManager:
        """Retorna o gerenciador de pontuação"""
        return self.__score_manager
    
    def set_player_name(self, name: str):
        """
        Define o nome do jogador
        
        Args:
            name (str): Nome do jogador
        """
        self.__player.name = name
    
    def start_game(self):
        """Inicia o jogo"""
        self.__game_running = True
        self.__game_start_time = pygame.time.get_ticks() // 1000  # Tempo em segundos
        self.__player.reset_score()
        self.__bot.reset_score()
        self.__ball.reset(self.__width // 2, self.__height // 2)
        
        margins = self.__responsive.margins
        
        # Reposiciona paddles usando dimensões atuais das raquetes
        self.__left_paddle.set_position(
            margins['paddle_offset'], 
            self.__height // 2 - self.__left_paddle.height // 2
        )
        self.__right_paddle.set_position(
            self.__width - margins['paddle_offset'] - self.__right_paddle.width, 
            self.__height // 2 - self.__right_paddle.height // 2
        )
        
        # Recria obstáculos a cada início
        self.__obstacles.clear()
        if self.__difficulty_settings["obstacles_enabled"]:
            self.__create_obstacles(self.__difficulty_settings["obstacles_count"], 
                                    self.__difficulty_settings["obstacles_speed"])
    
    def stop_game(self):
        """Para o jogo"""
        self.__game_running = False
    
    def __handle_input(self):
        """Processa entrada do usuário"""
        keys = pygame.key.get_pressed()
        
        # Movimento da raquete esquerda (jogador)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.__left_paddle.move_up(self.__height)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.__left_paddle.move_down(self.__height)
    
    def __update_ai(self):
        """Atualiza a IA da raquete direita"""
        ball_y = self.__ball.y
        paddle_center = self.__right_paddle.center_y()
        
        # Calcula a diferença entre a bola e o centro da raquete
        diff = ball_y - paddle_center
        
        # Move a raquete baseado na dificuldade
        if abs(diff) > 5:  # Só move se a diferença for significativa
            if diff > 0:
                # Bola está abaixo, move para baixo
                if random.random() < self.__ai_difficulty:
                    self.__right_paddle.move_down(self.__height)
            else:
                # Bola está acima, move para cima
                if random.random() < self.__ai_difficulty:
                    self.__right_paddle.move_up(self.__height)
    
    def __check_collisions(self):
        """Verifica colisões entre bola e raquetes/paredes/obstáculos"""
        ball_x = self.__ball.x
        ball_y = self.__ball.y
        ball_radius = self.__ball.radius
        prev_x = self.__ball.prev_x
        prev_y = self.__ball.prev_y
        
        # Debug: mostra posição da bola
        if ball_x < 0 or ball_x > self.__width:
            print(f"Bola saiu da tela! X: {ball_x}, Y: {ball_y}, Width: {self.__width}")
        
        # Colisões com paredes
        if ball_y <= ball_radius:
            self.__ball.bounce_y()
            self.__ball.y = ball_radius + 1
        if ball_y >= self.__height - ball_radius:
            self.__ball.bounce_y()
            self.__ball.y = self.__height - ball_radius - 1
        
        # Colisões com raquetes - Abordagem simplificada e robusta
        epsilon = 5.0  # Espaço garantido entre bola e raquete
        
        # --- Raquete esquerda ---
        left_paddle = self.__left_paddle
        left_edge_right = left_paddle.x + left_paddle.width
        
        # Verifica sobreposição Y
        overlaps_y_left = (ball_y + ball_radius >= left_paddle.y and 
                          ball_y - ball_radius <= left_paddle.y + left_paddle.height)
        
        # ANTI-STUCK: Se a bola está atrás ou muito próxima da raquete esquerda
        # Verifica também se estava se movendo em direção à raquete (vindo do centro)
        if ball_x < left_edge_right + epsilon and overlaps_y_left:
            # Verifica se a bola acabou de ser resetada (prev_x == ball_x) ou está muito próxima
            is_recently_reset = (abs(prev_x - ball_x) < 1.0)
            # Se foi resetada recentemente ou está atrás da raquete, corrige
            if is_recently_reset or ball_x < left_edge_right:
                # Reposiciona a bola para a frente da raquete
                self.__ball.x = left_edge_right + ball_radius + epsilon
                # Aplica bounce_paddle que recalcula a direção
                self.__ball.bounce_paddle(left_paddle.y, left_paddle.height)
                # FORÇA direção para DIREITA (sempre afasta da raquete esquerda)
                self.__ball.force_direction_right()
                # Garante que a posição não está atrás
                if self.__ball.x < left_edge_right:
                    self.__ball.x = left_edge_right + ball_radius + epsilon
        
        # Colisão normal - bola está na frente ou colidindo com a face da raquete
        elif overlaps_y_left and ball_x >= left_paddle.x and ball_x <= left_edge_right + ball_radius * 2:
            # Colisão detectada - aplica rebote
            self.__ball.bounce_paddle(left_paddle.y, left_paddle.height)
            # Garante posição correta
            self.__ball.x = left_edge_right + ball_radius + epsilon

        # --- Raquete direita ---
        right_paddle = self.__right_paddle
        right_edge_left = right_paddle.x
        
        # Verifica sobreposição Y
        overlaps_y_right = (ball_y + ball_radius >= right_paddle.y and 
                           ball_y - ball_radius <= right_paddle.y + right_paddle.height)
        
        # ANTI-STUCK: Se a bola está atrás ou muito próxima da raquete direita
        # Verifica também se estava se movendo em direção à raquete (vindo do centro)
        if ball_x > right_edge_left - epsilon and overlaps_y_right:
            # Verifica se a bola acabou de ser resetada (prev_x == ball_x) ou está muito próxima
            is_recently_reset = (abs(prev_x - ball_x) < 1.0)
            # Se foi resetada recentemente ou está atrás da raquete, corrige
            if is_recently_reset or ball_x > right_edge_left:
                # Reposiciona a bola para a frente da raquete
                self.__ball.x = right_edge_left - ball_radius - epsilon
                # Aplica bounce_paddle que recalcula a direção
                self.__ball.bounce_paddle(right_paddle.y, right_paddle.height)
                # FORÇA direção para ESQUERDA (sempre afasta da raquete direita)
                self.__ball.force_direction_left()
                # Garante que a posição não está atrás
                if self.__ball.x > right_edge_left:
                    self.__ball.x = right_edge_left - ball_radius - epsilon
        
        # Colisão normal - bola está na frente ou colidindo com a face da raquete
        elif overlaps_y_right and ball_x <= right_paddle.x + right_paddle.width and ball_x >= right_edge_left - ball_radius * 2:
            # Colisão detectada - aplica rebote
            self.__ball.bounce_paddle(right_paddle.y, right_paddle.height)
            # Garante posição correta
            self.__ball.x = right_edge_left - ball_radius - epsilon
        
        # Colisões com obstáculos
        if self.__obstacles:
            self.__check_obstacle_collisions()
        
        # Pontuação - bola saiu da tela
        if ball_x < 0:
            self.__bot.add_point()
            print(f"Bot ganhou ponto! Jogador: {self.__player.score} x Bot: {self.__bot.score}")
            self.__ball.reset(self.__width // 2, self.__height // 2)
        elif ball_x > self.__width:
            self.__player.add_point()
            print(f"Jogador ganhou ponto! Jogador: {self.__player.score} x Bot: {self.__bot.score}")
            self.__ball.reset(self.__width // 2, self.__height // 2)
        
        # Verifica se alguém ganhou (3 pontos)
        if self.__player.score >= 3 or self.__bot.score >= 3:
            winner = "Jogador" if self.__player.score >= 3 else "Bot"
            player_won = (winner == "Jogador")
            print(f"{winner} ganhou o jogo! Placar final: {self.__player.score} x {self.__bot.score}")
            self.__score_manager.add_score(self.__player.name, self.__player.score, won=player_won)
            self.__game_running = False
            self.__show_game_over_screen(winner)
        
        # Verifica tempo limite (2 minutos)
        current_time = pygame.time.get_ticks() // 1000
        elapsed_time = current_time - self.__game_start_time
        if elapsed_time >= self.__game_duration:
            if self.__player.score > self.__bot.score:
                winner = "Jogador"
                player_won = True
            elif self.__bot.score > self.__player.score:
                winner = "Bot"
                player_won = False
            else:
                winner = "Empate"
                player_won = False
            
            print(f"Tempo esgotado! {winner} ganhou! Placar final: {self.__player.score} x {self.__bot.score}")
            self.__score_manager.add_score(self.__player.name, self.__player.score, won=player_won)
            self.__game_running = False
            self.__show_game_over_screen(winner)
    
    def __show_game_over_screen(self, winner: str):
        """Mostra a tela de fim de jogo"""
        self.__screen.fill(self.__BLACK)
        
        # Título do fim de jogo
        if winner == "Jogador":
            title_text = self.__font_large.render("VITÓRIA!", True, self.__GREEN)
        else:
            title_text = self.__font_large.render("DERROTA!", True, self.__RED)
        
        title_rect = title_text.get_rect(center=(self.__width // 2, 150))
        self.__screen.blit(title_text, title_rect)
        
        # Placar final
        score_text = self.__font_medium.render(f"Placar Final: {self.__player.score} x {self.__bot.score}", True, self.__WHITE)
        score_rect = score_text.get_rect(center=(self.__width // 2, 220))
        self.__screen.blit(score_text, score_rect)
        
        # Mensagem de vitória/derrota
        if winner == "Jogador":
            message = f"Parabéns {self.__player.name}! Você venceu!"
            color = self.__GREEN
        else:
            message = f"Que pena {self.__player.name}! O Bot venceu!"
            color = self.__RED
        
        message_text = self.__font_medium.render(message, True, color)
        message_rect = message_text.get_rect(center=(self.__width // 2, 280))
        self.__screen.blit(message_text, message_rect)
        
        # Instruções
        instructions = [
            "Pressione ESPAÇO para jogar novamente",
            "Pressione ESC para voltar ao menu"
        ]
        for i, instruction in enumerate(instructions):
            text = self.__font_small.render(instruction, True, self.__GRAY)
            text_rect = text.get_rect(center=(self.__width // 2, 350 + i * 30))
            self.__screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        # Aguarda input do usuário
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.__game_running = False
    
    def __draw(self):
        """Desenha todos os elementos na tela"""
        self.__screen.fill(self.__BLACK)
        
        # Desenha linha central
        pygame.draw.line(self.__screen, self.__GRAY, 
                        (self.__width // 2, 0), (self.__width // 2, self.__height), 2)
        
        # Desenha raquetes
        pygame.draw.rect(self.__screen, self.__WHITE, self.__left_paddle.get_rect())
        pygame.draw.rect(self.__screen, self.__WHITE, self.__right_paddle.get_rect())
        
        # Desenha obstáculos
        if self.__obstacles:
            self.__draw_obstacles()
        
        # Desenha bola
        pygame.draw.circle(self.__screen, self.__WHITE, 
                          (int(self.__ball.x), int(self.__ball.y)), self.__ball.radius)
        
        # Desenha placar com posicionamento responsivo
        margins = self.__responsive.margins
        score_y = margins['large']
        
        # Pontuação do jogador (esquerda)
        player_score_text = self.__font_large.render(str(self.__player.score), True, self.__GREEN)
        player_score_x = self.__width // 2 - self.__responsive.scale_width(80)
        self.__screen.blit(player_score_text, (player_score_x, score_y))
        
        # Separador do placar
        separator_text = self.__font_large.render("x", True, self.__WHITE)
        separator_x = self.__width // 2 - self.__responsive.scale_width(15)
        self.__screen.blit(separator_text, (separator_x, score_y))
        
        # Pontuação do bot (direita)
        bot_score_text = self.__font_large.render(str(self.__bot.score), True, self.__RED)
        bot_score_x = self.__width // 2 + self.__responsive.scale_width(30)
        self.__screen.blit(bot_score_text, (bot_score_x, score_y))
        
        # Desenha nomes e informações com posicionamento responsivo
        top_margin = margins['small']
        
        # Desenha nome do jogador
        name_text = self.__font_medium.render(f"Jogador: {self.__player.name}", True, self.__GREEN)
        self.__screen.blit(name_text, (margins['small'], top_margin))
        
        # Desenha nome do bot
        bot_name_text = self.__font_medium.render("Bot", True, self.__RED)
        bot_name_width = bot_name_text.get_width()
        self.__screen.blit(bot_name_text, (self.__width - bot_name_width - margins['small'], top_margin))
        
        # Desenha dificuldade atual
        difficulty_text = self.__font_small.render(f"Dificuldade: {self.__difficulty.title()}", True, self.__BLUE)
        difficulty_y = top_margin + self.__responsive.scale_height(30)
        self.__screen.blit(difficulty_text, (margins['small'], difficulty_y))
        
        # Botão Tela Cheia (topo direito)
        button_padding = self.__responsive.scale_width(10)
        button_w = self.__responsive.scale_width(150)
        button_h = self.__responsive.scale_height(36)
        button_x = self.__width - button_w - margins['small']
        button_y = margins['small']
        self.__fullscreen_button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        pygame.draw.rect(self.__screen, self.__BUTTON_BG, self.__fullscreen_button_rect)
        pygame.draw.rect(self.__screen, self.__BUTTON_BORDER, self.__fullscreen_button_rect, 2)
        label = "Tela Cheia" if not (self.__screen.get_flags() & pygame.FULLSCREEN) else "Janela"
        label_text = self.__font_small.render(label, True, self.__WHITE)
        label_rect = label_text.get_rect(center=self.__fullscreen_button_rect.center)
        self.__screen.blit(label_text, label_rect)
        
        # Desenha tempo restante
        if self.__game_running:
            current_time = pygame.time.get_ticks() // 1000
            elapsed_time = current_time - self.__game_start_time
            remaining_time = max(0, self.__game_duration - elapsed_time)
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            time_text = self.__font_small.render(f"Tempo: {minutes:02d}:{seconds:02d}", True, self.__WHITE)
            time_width = time_text.get_width()
            time_y = difficulty_y
            self.__screen.blit(time_text, (self.__width - time_width - margins['small'], time_y))
    
        # Desenha instruções com posicionamento responsivo
        if not self.__game_running:
            instructions = [
                "Pressione ESPAÇO para começar",
                "Use W/S ou ↑/↓ para mover a raquete",
                "Pressione ESC para sair"
            ]
            instruction_spacing = self.__responsive.scale_height(25)
            instruction_start_y = self.__height - self.__responsive.scale_height(80)
            
            for i, instruction in enumerate(instructions):
                text = self.__font_small.render(instruction, True, self.__GRAY)
                y_pos = instruction_start_y + i * instruction_spacing
                self.__screen.blit(text, (margins['small'], y_pos))
    
    def update(self):
        """Atualiza o estado do jogo"""
        if self.__game_running:
            self.__handle_input()
            self.__update_ai()
            # Aceleração diferenciada por nível
            acceleration_factor = self.__difficulty_settings["acceleration_factor"]
            if acceleration_factor > 1.0:
                self.__ball.accelerate(acceleration_factor)
            self.__ball.move()
            if self.__obstacles:
                self.__update_obstacles()
            self.__check_collisions()
        
        self.__draw()
        pygame.display.flip()
        self.__clock.tick(self.__fps)
    
    def handle_events(self) -> bool:
        """
        Processa eventos do pygame
        
        Returns:
            bool: True se o jogo deve continuar, False para sair
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F11:
                    # Alternar entre tela cheia e janela
                    self.__toggle_fullscreen()
                elif event.key == pygame.K_SPACE and not self.__game_running:
                    self.start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.__fullscreen_button_rect and self.__fullscreen_button_rect.collidepoint(event.pos):
                    self.__toggle_fullscreen()
        
        return True
    
    def __toggle_fullscreen(self):
        """Alterna entre tela cheia e modo janela e atualiza responsividade"""
        if self.__screen.get_flags() & pygame.FULLSCREEN:
            # Sai da tela cheia
            self.__screen = pygame.display.set_mode((800, 600))
            self.__width = 800
            self.__height = 600
        else:
            # Entra em tela cheia
            info = pygame.display.Info()
            self.__width = info.current_w
            self.__height = info.current_h
            self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.FULLSCREEN)
        
        # Atualiza responsividade e fontes após alternar
        self.__responsive.update_screen_size(self.__width, self.__height)
        self.__font_large = pygame.font.Font(None, self.__responsive.scale_font_size(74))
        self.__font_medium = pygame.font.Font(None, self.__responsive.scale_font_size(36))
        self.__font_small = pygame.font.Font(None, self.__responsive.scale_font_size(24))
    
    def quit(self):
        """Finaliza o jogo e limpa recursos"""
        pygame.quit()
        sys.exit()

    # ---------------------- Obstáculos ----------------------
    def __create_obstacles(self, count: int, speed: int):
        """Cria obstáculos retangulares móveis no centro da arena"""
        width = self.__responsive.scale_width(20)
        height = self.__responsive.scale_height(120)
        gap = self.__responsive.scale_width(80)
        center_x = self.__width // 2
        start_y = self.__height // 4
        for i in range(count):
            x = center_x - width // 2 + (i * (gap if i % 2 == 0 else -gap))
            y = start_y if i % 2 == 0 else self.__height - start_y - height
            rect = pygame.Rect(x, y, width, height)
            vx = 0
            vy = speed if i % 2 == 0 else -speed
            self.__obstacles.append({"rect": rect, "vx": vx, "vy": vy})
    
    def __update_obstacles(self):
        """Atualiza a posição dos obstáculos e rebate nas bordas"""
        for obs in self.__obstacles:
            rect = obs["rect"]
            rect.x += obs["vx"]
            rect.y += obs["vy"]
            if rect.top <= 0 or rect.bottom >= self.__height:
                obs["vy"] = -obs["vy"]
                # leve aleatoriedade
                if random.random() < 0.2:
                    obs["vy"] += 1 if obs["vy"] > 0 else -1
    
    def __draw_obstacles(self):
        for obs in self.__obstacles:
            pygame.draw.rect(self.__screen, self.__OBSTACLE, obs["rect"])
    
    def __check_obstacle_collisions(self):
        """Detecta colisões da bola com obstáculos e ajusta direção/velocidade"""
        bx, by, bw, bh = self.__ball.get_rect()
        ball_rect = pygame.Rect(bx, by, bw, bh)
        for obs in self.__obstacles:
            rect = obs["rect"]
            if ball_rect.colliderect(rect):
                # Decide eixo do rebote pela menor penetração
                overlap_left = ball_rect.right - rect.left
                overlap_right = rect.right - ball_rect.left
                overlap_top = ball_rect.bottom - rect.top
                overlap_bottom = rect.bottom - ball_rect.top
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                if min_overlap in (overlap_left, overlap_right):
                    self.__ball.bounce_x()
                    if ball_rect.centerx < rect.centerx:
                        self.__ball.x = rect.left - self.__ball.radius - 2
                    else:
                        self.__ball.x = rect.right + self.__ball.radius + 2
                else:
                    self.__ball.bounce_y()
                    if ball_rect.centery < rect.centery:
                        self.__ball.y = rect.top - self.__ball.radius - 2
                    else:
                        self.__ball.y = rect.bottom + self.__ball.radius + 2
                break
