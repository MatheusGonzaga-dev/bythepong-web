"""
Classe Ball - Representa a bola no jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

import math
import random

class Ball:
    def __init__(self, x: int, y: int, radius: int = 10, initial_speed: int = 5):
        """
        Inicializa a bola com posição e propriedades físicas
        
        Args:
            x (int): Posição X inicial
            y (int): Posição Y inicial
            radius (int): Raio da bola
            initial_speed (int): Velocidade inicial da bola
        """
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__speed = initial_speed
        self.__initial_speed = initial_speed
        self.__angle = random.uniform(-math.pi/4, math.pi/4)  # Ângulo aleatório inicial
        self.__dx = self.__speed * math.cos(self.__angle)
        self.__dy = self.__speed * math.sin(self.__angle)
    
    @property
    def x(self) -> int:
        """Retorna a posição X da bola"""
        return self.__x
    
    @x.setter
    def x(self, value: int):
        """Define a posição X da bola"""
        self.__x = value
    
    @property
    def y(self) -> int:
        """Retorna a posição Y da bola"""
        return self.__y
    
    @y.setter
    def y(self, value: int):
        """Define a posição Y da bola"""
        self.__y = value
    
    @property
    def radius(self) -> int:
        """Retorna o raio da bola"""
        return self.__radius
    
    @property
    def speed(self) -> float:
        """Retorna a velocidade da bola"""
        return self.__speed
    
    def move(self):
        """Move a bola baseado na velocidade atual"""
        self.__x += self.__dx
        self.__y += self.__dy
    
    def bounce_x(self):
        """Inverte a direção horizontal da bola"""
        self.__dx = -self.__dx
    
    def bounce_y(self):
        """Inverte a direção vertical da bola"""
        self.__dy = -self.__dy
    
    def bounce_paddle(self, paddle_y: int, paddle_height: int):
        """
        Calcula o ângulo de rebote baseado na posição da raquete
        
        Args:
            paddle_y (int): Posição Y da raquete
            paddle_height (int): Altura da raquete
        """
        # Calcula a posição relativa na raquete (0 a 1)
        relative_intersect_y = (self.__y - paddle_y) / paddle_height
        relative_intersect_y = max(0, min(1, relative_intersect_y))
        
        # Converte para ângulo (-45 a 45 graus)
        angle = (relative_intersect_y - 0.5) * math.pi / 2
        
        # Aumenta ligeiramente a velocidade
        self.__speed = min(self.__speed * 1.05, 12)
        
        # Inverte apenas a direção horizontal (sempre)
        self.__dx = -self.__dx
        self.__dy = self.__speed * math.sin(angle)
        
        # Garante velocidade mínima
        if abs(self.__dx) < 2:
            self.__dx = 2 if self.__dx > 0 else -2
    
    def reset(self, x: int, y: int):
        """
        Reseta a bola para uma nova posição
        
        Args:
            x (int): Nova posição X
            y (int): Nova posição Y
        """
        self.__x = x
        self.__y = y
        self.__speed = self.__initial_speed
        self.__angle = random.uniform(-math.pi/4, math.pi/4)
        self.__dx = self.__speed * math.cos(self.__angle)
        self.__dy = self.__speed * math.sin(self.__angle)
    
    def get_rect(self):
        """Retorna as coordenadas do retângulo da bola para colisão"""
        return (self.__x - self.__radius, self.__y - self.__radius, 
                self.__radius * 2, self.__radius * 2)
