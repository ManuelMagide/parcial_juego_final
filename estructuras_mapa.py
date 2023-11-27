import pygame
from constantes import *
from fun_auxiliar import Auxiliar

class Estructura:
    def __init__(self, x, y, ancho, alto, pantalla) -> None:
        self.pantalla = pantalla
        self.rect = pygame.Rect(x, y, ancho, alto) #LEFT, TOP, ANCHO Y ALTO
        self.rect.x = x
        self.rect.y = y
        self.hitbox = Auxiliar.obtener_rectangulos(self.rect)
    
    def draw(self, pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla, 'blue', self.hitbox['main'], 3, 3)
            pygame.draw.rect(pantalla, 'green', self.hitbox['top'], 3, 3) 
            pygame.draw.rect(pantalla, 'red', self.hitbox['bottom'], 3, 3) 
            pygame.draw.rect(pantalla, 'yellow', self.hitbox['left'], 3, 3)
            pygame.draw.rect(pantalla, 'white', self.hitbox['right'], 3, 3) 