"""
Classe Ball - Representa a bola no jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

import math
import random

class Ball:
    def __init__(self, x: int, y: int, radius: int = 10, initial_speed: int = 5, max_speed: int = 12, speed_increase_factor: float = 1.05, initial_angle_range: float = math.pi/4):
        """
        Inicializa a bola com posição e propriedades físicas
        
        Args:
            x (int): Posição X inicial
            y (int): Posição Y inicial
            radius (int): Raio da bola
            initial_speed (int): Velocidade inicial da bola
            max_speed (int): Velocidade máxima permitida
            speed_increase_factor (float): Fator de aumento de velocidade por rebote
            initial_angle_range (float): amplitude do ângulo inicial (em radianos)
        """
        self.__x = x
        self.__y = y
        # posição anterior para detecção contínua de colisão (swept)
        self.__prev_x = x
        self.__prev_y = y
        self.__radius = radius
        self.__speed = initial_speed
        self.__initial_speed = initial_speed
        self.__max_speed = max_speed
        self.__speed_increase_factor = speed_increase_factor
        self.__initial_angle_range = max(0.05, min(initial_angle_range, math.pi/2))
        self.__angle = random.uniform(-self.__initial_angle_range, self.__initial_angle_range)
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
        # armazena posição anterior antes de mover
        self.__prev_x = self.__x
        self.__prev_y = self.__y
        self.__x += self.__dx
        self.__y += self.__dy
    
    def bounce_x(self):
        """Inverte a direção horizontal da bola"""
        self.__dx = -self.__dx
    
    def force_direction_right(self):
        """Força a direção horizontal para a direita (positiva)"""
        if self.__dx < 0:
            self.__dx = -self.__dx
    
    def force_direction_left(self):
        """Força a direção horizontal para a esquerda (negativa)"""
        if self.__dx > 0:
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
        
        # Aumenta velocidade dentro do limite
        self.__speed = min(self.__speed * self.__speed_increase_factor, self.__max_speed)
        
        # Define direção horizontal após o rebote (inverte)
        horizontal_direction = -1 if self.__dx > 0 else 1
        
        # Recalcula componentes dx/dy mantendo o novo módulo de velocidade
        self.__dx = horizontal_direction * max(3.0, abs(self.__speed * math.cos(angle)))
        self.__dy = self.__speed * math.sin(angle)
        
    def accelerate(self, factor: float):
        """
        Acelera a bola multiplicando sua velocidade e clampando ao máximo.
        Args:
            factor (float): fator > 1.0 para acelerar levemente por frame
        """
        if factor <= 1.0:
            return
        # Escala componentes
        new_dx = self.__dx * factor
        new_dy = self.__dy * factor
        # Calcula nova velocidade e aplica teto
        new_speed = (new_dx ** 2 + new_dy ** 2) ** 0.5
        if new_speed > self.__max_speed:
            # Normaliza para max_speed
            if new_speed > 0:
                scale = self.__max_speed / new_speed
                new_dx *= scale
                new_dy *= scale
                new_speed = self.__max_speed
        self.__dx = new_dx
        self.__dy = new_dy
        self.__speed = new_speed
        
    def reset(self, x: int, y: int):
        """
        Reseta a bola para uma nova posição
        
        Args:
            x (int): Nova posição X
            y (int): Nova posição Y
        """
        self.__x = x
        self.__y = y
        self.__prev_x = x
        self.__prev_y = y
        self.__speed = self.__initial_speed
        self.__angle = random.uniform(-self.__initial_angle_range, self.__initial_angle_range)
        # Sorteia direção horizontal inicial para evitar previsibilidade
        direction = random.choice([-1, 1])
        # Garante componente horizontal mínima
        base_dx = abs(self.__speed * math.cos(self.__angle))
        self.__dx = direction * max(3.0, base_dx)
        self.__dy = self.__speed * math.sin(self.__angle)
    
    def get_rect(self):
        """Retorna as coordenadas do retângulo da bola para colisão"""
        return (self.__x - self.__radius, self.__y - self.__radius, 
                self.__radius * 2, self.__radius * 2)

    # --- propriedades apenas leitura das posições anteriores ---
    @property
    def prev_x(self) -> int:
        return self.__prev_x

    @property
    def prev_y(self) -> int:
        return self.__prev_y
