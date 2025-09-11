"""
ByThePong - Jogo Pong em Python
Programa principal que coordena menu e jogo
"""

import pygame
import sys
from game import Game
from menu import Menu

def start_game_with_name(player_name: str, difficulty: str = "normal"):
    """
    Inicia o jogo com o nome do jogador e dificuldade
    
    Args:
        player_name (str): Nome do jogador
        difficulty (str): Nível de dificuldade
    """
    try:
        # Cria e configura o jogo
        game = Game(difficulty=difficulty)
        game.set_player_name(player_name)
        
        # Loop principal do jogo
        while True:
            if not game.handle_events():
                break
            
            game.update()
        
        # Volta ao menu após o jogo
        game.quit()
        
    except Exception as e:
        print(f"Erro durante o jogo: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        # Configura o callback para iniciar o jogo
        menu = Menu()
        menu.set_start_game_callback(start_game_with_name)
        
        # Loop principal do menu
        while True:
            if not menu.handle_events():
                break
            
            menu.update()
        
        # Finaliza o programa
        menu.quit()
        
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário.")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        pygame.quit()
        sys.exit()
