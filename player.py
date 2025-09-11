"""
Classe Player - Representa um jogador no jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

class Player:
    def __init__(self, name: str = "Jogador"):
        """
        Inicializa um jogador com nome e pontuação
        
        Args:
            name (str): Nome do jogador
        """
        self.__name = name
        self.__score = 0
    
    @property
    def name(self) -> str:
        """Retorna o nome do jogador"""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """Define o nome do jogador"""
        if isinstance(value, str) and len(value.strip()) > 0:
            self.__name = value.strip()
        else:
            raise ValueError("Nome deve ser uma string não vazia")
    
    @property
    def score(self) -> int:
        """Retorna a pontuação atual do jogador"""
        return self.__score
    
    def add_point(self):
        """Adiciona um ponto ao jogador"""
        self.__score += 1
    
    def reset_score(self):
        """Reseta a pontuação do jogador para zero"""
        self.__score = 0
    
    def __str__(self) -> str:
        """Representação string do jogador"""
        return f"{self.__name}: {self.__score} pontos"
    
    def __repr__(self) -> str:
        """Representação para debug"""
        return f"Player(name='{self.__name}', score={self.__score})"
