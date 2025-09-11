"""
Classe Paddle - Representa uma raquete no jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

class Paddle:
    def __init__(self, x: int, y: int, width: int = 15, height: int = 100, speed: int = 7):
        """
        Inicializa uma raquete com posição e dimensões
        
        Args:
            x (int): Posição X inicial
            y (int): Posição Y inicial
            width (int): Largura da raquete
            height (int): Altura da raquete
            speed (int): Velocidade da raquete
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__speed = speed
    
    @property
    def x(self) -> int:
        """Retorna a posição X da raquete"""
        return self.__x
    
    @property
    def y(self) -> int:
        """Retorna a posição Y da raquete"""
        return self.__y
    
    @property
    def width(self) -> int:
        """Retorna a largura da raquete"""
        return self.__width
    
    @property
    def height(self) -> int:
        """Retorna a altura da raquete"""
        return self.__height
    
    @property
    def speed(self) -> int:
        """Retorna a velocidade da raquete"""
        return self.__speed
    
    def move_up(self, screen_height: int):
        """
        Move a raquete para cima
        
        Args:
            screen_height (int): Altura da tela para limitar movimento
        """
        if self.__y > 0:
            self.__y -= self.__speed
            if self.__y < 0:
                self.__y = 0
    
    def move_down(self, screen_height: int):
        """
        Move a raquete para baixo
        
        Args:
            screen_height (int): Altura da tela para limitar movimento
        """
        if self.__y < screen_height - self.__height:
            self.__y += self.__speed
            if self.__y > screen_height - self.__height:
                self.__y = screen_height - self.__height
    
    def set_position(self, x: int, y: int):
        """
        Define a posição da raquete
        
        Args:
            x (int): Nova posição X
            y (int): Nova posição Y
        """
        self.__x = x
        self.__y = y
    
    def get_rect(self):
        """Retorna as coordenadas do retângulo da raquete para colisão"""
        return (self.__x, self.__y, self.__width, self.__height)
    
    def center_y(self) -> int:
        """Retorna a posição Y central da raquete"""
        return self.__y + self.__height // 2
