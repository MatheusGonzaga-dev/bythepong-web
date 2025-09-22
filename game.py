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
        
        self.__ball = Ball(
            self.__width // 2, 
            self.__height // 2, 
            ball_props['radius'], 
            int(self.__difficulty_settings["ball_speed"] * ball_props['speed_multiplier'])
        )
        
        self.__left_paddle = Paddle(
            margins['paddle_offset'], 
            self.__height // 2 - paddle_props['height'] // 2, 
            paddle_props['width'], 
            paddle_props['height'], 
            paddle_props['speed']
        )
        
        self.__right_paddle = Paddle(
            self.__width - margins['paddle_offset'] - paddle_props['width'], 
            self.__height // 2 - paddle_props['height'] // 2, 
            paddle_props['width'], 
            paddle_props['height'], 
            int(self.__difficulty_settings["ai_speed"] * ball_props['speed_multiplier'])
        )
        self.__score_manager = ScoreManager()
        
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
    
    def __get_difficulty_settings(self) -> dict:
        """
        Retorna as configurações baseadas na dificuldade escolhida
        
        Returns:
            dict: Configurações de dificuldade
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
        
        # Reposiciona paddles com dimensões responsivas
        paddle_props = self.__responsive.paddle_props
        margins = self.__responsive.margins
        
        self.__left_paddle.set_position(
            margins['paddle_offset'], 
            self.__height // 2 - paddle_props['height'] // 2
        )
        self.__right_paddle.set_position(
            self.__width - margins['paddle_offset'] - paddle_props['width'], 
            self.__height // 2 - paddle_props['height'] // 2
        )
    
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
        """Verifica colisões entre bola e raquetes/paredes"""
        ball_x = self.__ball.x
        ball_y = self.__ball.y
        ball_radius = self.__ball.radius
        
        # Debug: mostra posição da bola
        if ball_x < 0 or ball_x > self.__width:
            print(f"Bola saiu da tela! X: {ball_x}, Y: {ball_y}, Width: {self.__width}")
        
        # Primeiro verifica colisões com paredes (mais simples)
        # Colisão com parede superior
        if ball_y <= ball_radius:
            self.__ball.bounce_y()
            self.__ball.y = ball_radius + 1  # Força sair da parede
        
        # Colisão com parede inferior  
        if ball_y >= self.__height - ball_radius:
            self.__ball.bounce_y()
            self.__ball.y = self.__height - ball_radius - 1  # Força sair da parede
        
        # Verifica colisões com raquetes
        # Colisão com raquete esquerda (jogador)
        left_paddle = self.__left_paddle
        if (ball_x - ball_radius <= left_paddle.x + left_paddle.width and
            ball_x + ball_radius >= left_paddle.x and
            ball_y + ball_radius >= left_paddle.y and
            ball_y - ball_radius <= left_paddle.y + left_paddle.height and
            self.__ball.x < left_paddle.x + left_paddle.width):  # Só rebata se estiver se aproximando
            
            # Rebate e reposiciona
            self.__ball.bounce_paddle(left_paddle.y, left_paddle.height)
            self.__ball.x = left_paddle.x + left_paddle.width + ball_radius + 2
        
        # Colisão com raquete direita (bot)
        right_paddle = self.__right_paddle
        if (ball_x + ball_radius >= right_paddle.x and
            ball_x - ball_radius <= right_paddle.x + right_paddle.width and
            ball_y + ball_radius >= right_paddle.y and
            ball_y - ball_radius <= right_paddle.y + right_paddle.height and
            self.__ball.x > right_paddle.x):  # Só rebata se estiver se aproximando
            
            # Rebate e reposiciona
            self.__ball.bounce_paddle(right_paddle.y, right_paddle.height)
            self.__ball.x = right_paddle.x - ball_radius - 2
        
        # Pontuação - bola saiu da tela
        if ball_x < 0:
            # Bot ganhou ponto (bola passou pela raquete esquerda do jogador)
            self.__bot.add_point()
            print(f"Bot ganhou ponto! Jogador: {self.__player.score} x Bot: {self.__bot.score}")
            self.__ball.reset(self.__width // 2, self.__height // 2)
        elif ball_x > self.__width:
            # Jogador ganhou ponto (bola passou pela raquete direita do bot)
            self.__player.add_point()
            print(f"Jogador ganhou ponto! Jogador: {self.__player.score} x Bot: {self.__bot.score}")
            self.__ball.reset(self.__width // 2, self.__height // 2)
        
        # Verifica se alguém ganhou (3 pontos)
        if self.__player.score >= 3 or self.__bot.score >= 3:
            winner = "Jogador" if self.__player.score >= 3 else "Bot"
            print(f"{winner} ganhou o jogo! Placar final: {self.__player.score} x {self.__bot.score}")
            self.__score_manager.add_score(self.__player.name, self.__player.score)
            self.__game_running = False
            self.__show_game_over_screen(winner)
        
        # Verifica tempo limite (2 minutos)
        current_time = pygame.time.get_ticks() // 1000
        elapsed_time = current_time - self.__game_start_time
        if elapsed_time >= self.__game_duration:
            # Tempo esgotado - quem tem mais pontos ganha
            if self.__player.score > self.__bot.score:
                winner = "Jogador"
            elif self.__bot.score > self.__player.score:
                winner = "Bot"
            else:
                winner = "Empate"
            
            print(f"Tempo esgotado! {winner} ganhou! Placar final: {self.__player.score} x {self.__bot.score}")
            self.__score_manager.add_score(self.__player.name, self.__player.score)
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
                        # Reinicia o jogo
                        self.start_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        # Volta ao menu
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
            self.__ball.move()
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
        
        return True
    
    def __toggle_fullscreen(self):
        """Alterna entre tela cheia e modo janela"""
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
    
    def quit(self):
        """Finaliza o jogo e limpa recursos"""
        pygame.quit()
        sys.exit()
