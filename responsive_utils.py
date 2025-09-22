"""
ByThePong - Utilitários de Responsividade
Sistema para adaptação automática de elementos do jogo a diferentes resoluções
"""

class ResponsiveManager:
    """
    Gerenciador de responsividade para adaptar elementos do jogo
    Mantém encapsulamento e proporcionalidade em diferentes resoluções
    """
    
    def __init__(self):
        # Dimensões base (referência para cálculos)
        self.__base_width = 800
        self.__base_height = 600
        
        # Dimensões atuais
        self.__current_width = 800
        self.__current_height = 600
        
        # Fatores de escala
        self.__scale_x = 1.0
        self.__scale_y = 1.0
        self.__scale_factor = 1.0
    
    def update_screen_size(self, width: int, height: int):
        """
        Atualiza as dimensões da tela e recalcula fatores de escala
        
        Args:
            width (int): Nova largura da tela
            height (int): Nova altura da tela
        """
        self.__current_width = width
        self.__current_height = height
        
        # Calcula fatores de escala
        self.__scale_x = width / self.__base_width
        self.__scale_y = height / self.__base_height
        
        # Usa o menor fator para manter proporção
        self.__scale_factor = min(self.__scale_x, self.__scale_y)
    
    @property
    def scale_factor(self) -> float:
        """Retorna o fator de escala principal"""
        return self.__scale_factor
    
    @property
    def scale_x(self) -> float:
        """Retorna o fator de escala horizontal"""
        return self.__scale_x
    
    @property
    def scale_y(self) -> float:
        """Retorna o fator de escala vertical"""
        return self.__scale_y
    
    def scale_width(self, width: int) -> int:
        """
        Escala uma largura baseada na resolução atual
        
        Args:
            width (int): Largura base
            
        Returns:
            int: Largura escalada
        """
        return int(width * self.__scale_factor)
    
    def scale_height(self, height: int) -> int:
        """
        Escala uma altura baseada na resolução atual
        
        Args:
            height (int): Altura base
            
        Returns:
            int: Altura escalada
        """
        return int(height * self.__scale_factor)
    
    def scale_font_size(self, size: int) -> int:
        """
        Escala tamanho de fonte baseado na resolução
        
        Args:
            size (int): Tamanho base da fonte
            
        Returns:
            int: Tamanho escalado da fonte
        """
        scaled = int(size * self.__scale_factor)
        return max(12, scaled)  # Tamanho mínimo
    
    @property
    def paddle_props(self) -> dict:
        """
        Retorna propriedades escaladas das raquetes
        
        Returns:
            dict: Propriedades das raquetes
        """
        base_width = 15
        base_height = 100
        base_speed = 7
        
        return {
            'width': self.scale_width(base_width),
            'height': self.scale_height(base_height),
            'speed': max(3, int(base_speed * self.__scale_factor)),
            'speed_multiplier': self.__scale_factor
        }
    
    @property
    def ball_props(self) -> dict:
        """
        Retorna propriedades escaladas da bola
        
        Returns:
            dict: Propriedades da bola
        """
        base_radius = 10
        
        return {
            'radius': max(5, self.scale_width(base_radius)),
            'speed_multiplier': self.__scale_factor
        }
    
    @property
    def margins(self) -> dict:
        """
        Retorna margens escaladas para diferentes elementos
        
        Returns:
            dict: Margens responsivas
        """
        return {
            'small': self.scale_width(10),
            'medium': self.scale_width(20),
            'large': self.scale_width(40),
            'paddle_offset': self.scale_width(50)
        }
    
    def get_responsive_position(self, x: int, y: int) -> tuple:
        """
        Converte posição base para posição responsiva
        
        Args:
            x (int): Posição X base
            y (int): Posição Y base
            
        Returns:
            tuple: (x_escalado, y_escalado)
        """
        return (
            int(x * self.__scale_x),
            int(y * self.__scale_y)
        )
    
    def get_base_position(self, x: int, y: int) -> tuple:
        """
        Converte posição responsiva para posição base
        
        Args:
            x (int): Posição X responsiva
            y (int): Posição Y responsiva
            
        Returns:
            tuple: (x_base, y_base)
        """
        return (
            int(x / self.__scale_x),
            int(y / self.__scale_y)
        )
    
    def is_mobile_size(self) -> bool:
        """
        Verifica se a tela atual é de tamanho mobile
        
        Returns:
            bool: True se for mobile
        """
        return self.__current_width < 768 or self.__current_height < 600
    
    def is_tablet_size(self) -> bool:
        """
        Verifica se a tela atual é de tamanho tablet
        
        Returns:
            bool: True se for tablet
        """
        return (768 <= self.__current_width < 1024 or 
                600 <= self.__current_height < 800)
    
    def is_desktop_size(self) -> bool:
        """
        Verifica se a tela atual é de tamanho desktop
        
        Returns:
            bool: True se for desktop
        """
        return self.__current_width >= 1024 and self.__current_height >= 800
    
    def get_device_type(self) -> str:
        """
        Retorna o tipo de dispositivo baseado na resolução
        
        Returns:
            str: 'mobile', 'tablet' ou 'desktop'
        """
        if self.is_mobile_size():
            return 'mobile'
        elif self.is_tablet_size():
            return 'tablet'
        else:
            return 'desktop'