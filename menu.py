"""
Classe Menu - Interface de menu e entrada de nome do jogador
Implementa encapsulamento e gerencia as telas do jogo
"""

import pygame
import sys
from typing import Optional, Callable
from score_manager import ScoreManager
from responsive_utils import ResponsiveManager

class Menu:
    def __init__(self, width: int = None, height: int = None):
        """
        Inicializa o menu com dimensões da tela
        
        Args:
            width (int): Largura da tela (None para tela cheia)
            height (int): Altura da tela (None para tela cheia)
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
        
        pygame.display.set_caption("ByThePong - Menu")
        
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
        self.__LIGHT_BLUE = (100, 150, 255)
        self.__DARK_BLUE = (0, 50, 150)
        self.__GOLD = (255, 215, 0)
        
        # Fontes responsivas
        self.__font_title = pygame.font.Font(None, self.__responsive.scale_font_size(72))
        self.__font_large = pygame.font.Font(None, self.__responsive.scale_font_size(48))
        self.__font_medium = pygame.font.Font(None, self.__responsive.scale_font_size(36))
        self.__font_small = pygame.font.Font(None, self.__responsive.scale_font_size(24))
        
        # Estado do menu
        self.__current_screen = "main"  # main, name_input, difficulty, ranking
        self.__player_name = ""
        self.__input_active = False
        self.__selected_difficulty = "normal"
        self.__difficulties = ["fácil", "normal", "difícil", "expert"]
        self.__difficulty_index = 1  # Começa com "normal"
        self.__clock = pygame.time.Clock()
        self.__fps = 60
        
        # Gerenciador de pontuação
        self.__score_manager = ScoreManager()
        
        # Callback para iniciar o jogo
        self.__start_game_callback: Optional[Callable[[str, str], None]] = None
    
    def set_start_game_callback(self, callback: Callable[[str, str], None]):
        """
        Define a função callback para iniciar o jogo
        
        Args:
            callback: Função que recebe o nome do jogador e dificuldade e inicia o jogo
        """
        self.__start_game_callback = callback
    
    def __draw_title(self):
        """Desenha o título do jogo com efeitos visuais"""
        # Efeito de gradiente no título
        title_text = self.__font_title.render("ByThePong", True, self.__BLUE)
        title_rect = title_text.get_rect(center=(self.__width // 2, 100))
        
        # Sombra do título
        shadow_text = self.__font_title.render("ByThePong", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.__width // 2 + 3, 103))
        self.__screen.blit(shadow_text, shadow_rect)
        
        # Título principal
        self.__screen.blit(title_text, title_rect)
        
        # Linha decorativa
        pygame.draw.line(self.__screen, self.__BLUE, 
                        (self.__width // 2 - 150, 130), (self.__width // 2 + 150, 130), 3)
        
        subtitle_text = self.__font_medium.render("Jogo Pong em Python", True, self.__GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(self.__width // 2, 150))
        self.__screen.blit(subtitle_text, subtitle_rect)
    
    def __draw_gradient_button(self, rect, color1, color2, text, text_color):
        """Desenha um botão com gradiente e efeitos visuais"""
        # Sombra do botão
        shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(self.__screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        # Gradiente do botão
        for i in range(rect.height):
            ratio = i / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(self.__screen, (r, g, b), 
                           (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))
        
        # Borda do botão
        pygame.draw.rect(self.__screen, self.__WHITE, rect, 3, border_radius=10)
        
        # Texto do botão
        button_text = self.__font_large.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        self.__screen.blit(button_text, text_rect)
    
    def __draw_background_pattern(self):
        """Desenha um padrão decorativo de fundo adaptado para tela cheia"""
        # Gradiente de fundo sutil
        for y in range(0, self.__height, 2):
            # Gradiente vertical do preto para um cinza muito escuro
            intensity = int(10 + (y / self.__height) * 5)
            color = (intensity, intensity, intensity)
            pygame.draw.line(self.__screen, color, (0, y), (self.__width, y))
        
        # Linhas diagonais sutis mais espaçadas
        spacing = max(80, self.__width // 20)  # Espaçamento adaptativo
        for i in range(0, self.__width + self.__height, spacing):
            # Linha diagonal da esquerda para direita
            start_x = max(0, i - self.__height)
            end_x = min(self.__width, i)
            start_y = max(0, self.__height - i)
            end_y = min(self.__height, self.__width + self.__height - i)
            
            if start_x < end_x and start_y < end_y:
                pygame.draw.line(self.__screen, (25, 25, 25), 
                               (start_x, start_y), (end_x, end_y), 1)
        
        # Pontos decorativos mais sutis e espaçados
        dot_spacing = max(120, self.__width // 15)  # Espaçamento adaptativo
        for x in range(dot_spacing, self.__width, dot_spacing):
            for y in range(dot_spacing, self.__height, dot_spacing):
                pygame.draw.circle(self.__screen, (35, 35, 35), (x, y), 1)
        
        # Bordas sutis
        pygame.draw.rect(self.__screen, (40, 40, 40), 
                        (0, 0, self.__width, self.__height), 2)
    
    def __draw_main_menu(self):
        """Desenha o menu principal com estilização melhorada"""
        self.__draw_title()
        
        # Botão Jogar com gradiente
        play_rect = pygame.Rect(self.__width // 2 - 120, 200, 240, 70)
        self.__draw_gradient_button(play_rect, self.__GREEN, (0, 200, 0), "JOGAR", self.__BLACK)
        
        # Botão Dificuldade com gradiente
        difficulty_rect = pygame.Rect(self.__width // 2 - 120, 290, 240, 70)
        self.__draw_gradient_button(difficulty_rect, self.__LIGHT_BLUE, (50, 100, 200), "DIFICULDADE", self.__WHITE)
        
        # Botão Ranking com gradiente
        ranking_rect = pygame.Rect(self.__width // 2 - 120, 380, 240, 70)
        self.__draw_gradient_button(ranking_rect, self.__BLUE, (0, 50, 150), "RANKING", self.__WHITE)
        
        # Botão Sair com gradiente
        quit_rect = pygame.Rect(self.__width // 2 - 120, 470, 240, 70)
        self.__draw_gradient_button(quit_rect, self.__RED, (150, 0, 0), "SAIR", self.__WHITE)
        
        # Fundo decorativo
        self.__draw_background_pattern()
        
        # Instruções com estilo melhorado
        instructions = [
            "Use as setas ou clique nos botões para navegar",
            "Pressione ESC para voltar ao menu anterior"
        ]
        for i, instruction in enumerate(instructions):
            # Sombra do texto
            shadow_text = self.__font_small.render(instruction, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(self.__width // 2 + 1, 560 + i * 25 + 1))
            self.__screen.blit(shadow_text, shadow_rect)
            
            # Texto principal
            text = self.__font_small.render(instruction, True, self.__GRAY)
            text_rect = text.get_rect(center=(self.__width // 2, 560 + i * 25))
            self.__screen.blit(text, text_rect)
    
    def __draw_difficulty_menu(self):
        """Desenha a tela de seleção de dificuldade com estilização melhorada"""
        self.__draw_title()
        
        # Título da seção com efeitos
        title_text = self.__font_large.render("Escolha a Dificuldade:", True, self.__WHITE)
        title_rect = title_text.get_rect(center=(self.__width // 2, 200))
        
        # Sombra do título
        shadow_text = self.__font_large.render("Escolha a Dificuldade:", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.__width // 2 + 2, 202))
        self.__screen.blit(shadow_text, shadow_rect)
        
        # Título principal
        self.__screen.blit(title_text, title_rect)
        
        # Linha decorativa
        pygame.draw.line(self.__screen, self.__WHITE, 
                        (self.__width // 2 - 200, 230), (self.__width // 2 + 200, 230), 2)
        
        # Opções de dificuldade
        difficulties_info = {
            "fácil": "Perfeito para iniciantes",
            "normal": "Equilibrado e divertido", 
            "difícil": "Para jogadores experientes",
            "expert": "Apenas para os melhores!"
        }
        
        # Cores para cada dificuldade
        difficulty_colors = {
            "fácil": (self.__GREEN, (0, 150, 0)),
            "normal": (self.__LIGHT_BLUE, (50, 100, 200)),
            "difícil": (self.__BLUE, (0, 50, 150)),
            "expert": (self.__RED, (150, 0, 0))
        }
        
        for i, difficulty in enumerate(self.__difficulties):
            y_pos = 260 + i * 80
            
            # Cores baseadas na seleção
            if difficulty == self.__selected_difficulty:
                color1, color2 = difficulty_colors[difficulty]
                text_color = self.__WHITE
                border_color = self.__WHITE
            else:
                color1 = self.__GRAY
                color2 = (60, 60, 60)
                text_color = self.__WHITE
                border_color = (100, 100, 100)
            
            # Botão de dificuldade com gradiente
            diff_rect = pygame.Rect(self.__width // 2 - 180, y_pos, 360, 60)
            self.__draw_gradient_button(diff_rect, color1, color2, difficulty.title(), text_color)
            
            # Descrição da dificuldade
            desc_text = self.__font_small.render(difficulties_info[difficulty], True, self.__GRAY)
            desc_rect = desc_text.get_rect(center=(self.__width // 2, y_pos + 40))
            self.__screen.blit(desc_text, desc_rect)
        
        # Botão Confirmar com gradiente
        confirm_rect = pygame.Rect(self.__width // 2 - 120, 580, 240, 60)
        self.__draw_gradient_button(confirm_rect, self.__BLUE, (0, 50, 150), "CONFIRMAR", self.__WHITE)
        
        # Fundo decorativo
        self.__draw_background_pattern()
        
        # Instruções com estilo melhorado
        instructions = [
            "Use as setas para navegar entre as opções",
            "Pressione ENTER ou clique em CONFIRMAR",
            "Pressione ESC para voltar ao menu"
        ]
        for i, instruction in enumerate(instructions):
            # Sombra do texto
            shadow_text = self.__font_small.render(instruction, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(self.__width // 2 + 1, 660 + i * 20 + 1))
            self.__screen.blit(shadow_text, shadow_rect)
            
            # Texto principal
            text = self.__font_small.render(instruction, True, self.__GRAY)
            text_rect = text.get_rect(center=(self.__width // 2, 660 + i * 20))
            self.__screen.blit(text, text_rect)
    
    def __draw_name_input(self):
        """Desenha a tela de entrada do nome"""
        self.__draw_title()
        
        # Título da seção
        title_text = self.__font_large.render("Digite seu nome:", True, self.__WHITE)
        title_rect = title_text.get_rect(center=(self.__width // 2, 250))
        self.__screen.blit(title_text, title_rect)
        
        # Campo de entrada
        input_rect = pygame.Rect(self.__width // 2 - 150, 300, 300, 50)
        color = self.__LIGHT_BLUE if self.__input_active else self.__GRAY
        pygame.draw.rect(self.__screen, color, input_rect)
        pygame.draw.rect(self.__screen, self.__WHITE, input_rect, 3)
        
        # Texto do nome
        name_text = self.__font_medium.render(self.__player_name, True, self.__BLACK)
        name_rect = name_text.get_rect(center=input_rect.center)
        self.__screen.blit(name_text, name_rect)
        
        # Cursor piscante
        if self.__input_active:
            cursor_x = name_rect.right + 5
            cursor_rect = pygame.Rect(cursor_x, input_rect.y + 10, 2, 30)
            pygame.draw.rect(self.__screen, self.__BLACK, cursor_rect)
        
        # Botão Confirmar
        confirm_rect = pygame.Rect(self.__width // 2 - 100, 380, 200, 50)
        pygame.draw.rect(self.__screen, self.__GREEN, confirm_rect)
        pygame.draw.rect(self.__screen, self.__WHITE, confirm_rect, 3)
        
        confirm_text = self.__font_medium.render("CONFIRMAR", True, self.__BLACK)
        confirm_text_rect = confirm_text.get_rect(center=confirm_rect.center)
        self.__screen.blit(confirm_text, confirm_text_rect)
        
        # Instruções
        instructions = [
            "Digite seu nome e pressione ENTER ou clique em CONFIRMAR",
            "Pressione ESC para voltar ao menu"
        ]
        for i, instruction in enumerate(instructions):
            text = self.__font_small.render(instruction, True, self.__GRAY)
            text_rect = text.get_rect(center=(self.__width // 2, 450 + i * 25))
            self.__screen.blit(text, text_rect)
    
    def __draw_ranking(self):
        """Desenha a tela de ranking"""
        self.__draw_title()
        
        # Título da seção
        title_text = self.__font_large.render("🏆 RANKING TOP 10 🏆", True, self.__GOLD)
        title_rect = title_text.get_rect(center=(self.__width // 2, 200))
        self.__screen.blit(title_text, title_rect)
        
        # Ranking
        ranking = self.__score_manager.get_ranking()
        if ranking:
            for i, entry in enumerate(ranking):
                y_pos = 250 + i * 30
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}º"
                
                rank_text = f"{medal} {entry['name']}: {entry['score']} pontos"
                text = self.__font_medium.render(rank_text, True, self.__WHITE)
                text_rect = text.get_rect(center=(self.__width // 2, y_pos))
                self.__screen.blit(text, text_rect)
        else:
            no_scores_text = self.__font_medium.render("Nenhuma pontuação registrada ainda!", True, self.__GRAY)
            no_scores_rect = no_scores_text.get_rect(center=(self.__width // 2, 300))
            self.__screen.blit(no_scores_text, no_scores_rect)
        
        # Botão Voltar
        back_rect = pygame.Rect(self.__width // 2 - 100, 500, 200, 50)
        pygame.draw.rect(self.__screen, self.__BLUE, back_rect)
        pygame.draw.rect(self.__screen, self.__WHITE, back_rect, 3)
        
        back_text = self.__font_medium.render("VOLTAR", True, self.__WHITE)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.__screen.blit(back_text, back_text_rect)
    
    def __handle_main_menu_click(self, pos):
        """Processa cliques no menu principal"""
        x, y = pos
        
        # Coordenadas dos botões baseadas no tamanho da tela
        button_width = 240
        button_height = 70
        button_x = self.__width // 2 - button_width // 2
        
        # Botão Jogar
        if (button_x <= x <= button_x + button_width and 
            200 <= y <= 200 + button_height):
            self.__current_screen = "name_input"
            self.__input_active = True
        
        # Botão Dificuldade
        elif (button_x <= x <= button_x + button_width and 
              290 <= y <= 290 + button_height):
            self.__current_screen = "difficulty"
        
        # Botão Ranking
        elif (button_x <= x <= button_x + button_width and 
              380 <= y <= 380 + button_height):
            self.__current_screen = "ranking"
        
        # Botão Sair
        elif (button_x <= x <= button_x + button_width and 
              470 <= y <= 470 + button_height):
            return False
        
        return True
    
    def __handle_name_input_click(self, pos):
        """Processa cliques na tela de entrada do nome"""
        x, y = pos
        
        # Campo de entrada (centralizado)
        input_width = 300
        input_height = 50
        input_x = self.__width // 2 - input_width // 2
        if (input_x <= x <= input_x + input_width and 
            300 <= y <= 300 + input_height):
            self.__input_active = True
        
        # Botão Confirmar (centralizado)
        confirm_width = 200
        confirm_height = 50
        confirm_x = self.__width // 2 - confirm_width // 2
        if (confirm_x <= x <= confirm_x + confirm_width and 
            380 <= y <= 380 + confirm_height):
            if self.__player_name.strip():
                self.__start_game()
        
        return True
    
    def __handle_difficulty_click(self, pos):
        """Processa cliques na tela de seleção de dificuldade"""
        x, y = pos
        
        # Botões de dificuldade (360x60, centralizados)
        diff_button_width = 360
        diff_button_height = 60
        diff_button_x = self.__width // 2 - diff_button_width // 2
        
        for i, difficulty in enumerate(self.__difficulties):
            y_pos = 260 + i * 80
            if (diff_button_x <= x <= diff_button_x + diff_button_width and 
                y_pos <= y <= y_pos + diff_button_height):
                self.__selected_difficulty = difficulty
                self.__difficulty_index = i
        
        # Botão Confirmar (240x60, centralizado)
        confirm_width = 240
        confirm_height = 60
        confirm_x = self.__width // 2 - confirm_width // 2
        if (confirm_x <= x <= confirm_x + confirm_width and 
            580 <= y <= 580 + confirm_height):
            self.__current_screen = "main"
        
        return True
    
    def __handle_ranking_click(self, pos):
        """Processa cliques na tela de ranking"""
        x, y = pos
        
        # Botão Voltar (centralizado)
        back_width = 200
        back_height = 50
        back_x = self.__width // 2 - back_width // 2
        if (back_x <= x <= back_x + back_width and 
            500 <= y <= 500 + back_height):
            self.__current_screen = "main"
        
        return True
    
    def __start_game(self):
        """Inicia o jogo com o nome do jogador e dificuldade"""
        if self.__start_game_callback and self.__player_name.strip():
            self.__start_game_callback(self.__player_name.strip(), self.__selected_difficulty)
    
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
    
    def __handle_keyboard_input(self, event):
        """Processa entrada do teclado"""
        if self.__current_screen == "name_input" and self.__input_active:
            if event.key == pygame.K_BACKSPACE:
                self.__player_name = self.__player_name[:-1]
            elif event.key == pygame.K_RETURN:
                if self.__player_name.strip():
                    self.__start_game()
            elif event.unicode.isprintable() and len(self.__player_name) < 20:
                self.__player_name += event.unicode
        elif self.__current_screen == "difficulty":
            if event.key == pygame.K_UP:
                self.__difficulty_index = (self.__difficulty_index - 1) % len(self.__difficulties)
                self.__selected_difficulty = self.__difficulties[self.__difficulty_index]
            elif event.key == pygame.K_DOWN:
                self.__difficulty_index = (self.__difficulty_index + 1) % len(self.__difficulties)
                self.__selected_difficulty = self.__difficulties[self.__difficulty_index]
            elif event.key == pygame.K_RETURN:
                self.__current_screen = "main"
    
    def update(self):
        """Atualiza o menu"""
        self.__screen.fill(self.__BLACK)
        
        if self.__current_screen == "main":
            self.__draw_main_menu()
        elif self.__current_screen == "name_input":
            self.__draw_name_input()
        elif self.__current_screen == "difficulty":
            self.__draw_difficulty_menu()
        elif self.__current_screen == "ranking":
            self.__draw_ranking()
        
        pygame.display.flip()
        self.__clock.tick(self.__fps)
    
    def handle_events(self) -> bool:
        """
        Processa eventos do pygame
        
        Returns:
            bool: True se o menu deve continuar, False para sair
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.__current_screen == "name_input":
                        self.__current_screen = "main"
                        self.__input_active = False
                    elif self.__current_screen == "difficulty":
                        self.__current_screen = "main"
                    elif self.__current_screen == "ranking":
                        self.__current_screen = "main"
                    else:
                        return False
                elif event.key == pygame.K_F11:
                    # Alternar entre tela cheia e janela
                    self.__toggle_fullscreen()
                else:
                    self.__handle_keyboard_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    if self.__current_screen == "main":
                        return self.__handle_main_menu_click(event.pos)
                    elif self.__current_screen == "name_input":
                        return self.__handle_name_input_click(event.pos)
                    elif self.__current_screen == "difficulty":
                        return self.__handle_difficulty_click(event.pos)
                    elif self.__current_screen == "ranking":
                        return self.__handle_ranking_click(event.pos)
        
        return True
    
    def quit(self):
        """Finaliza o menu e limpa recursos"""
        pygame.quit()
        sys.exit()
