from fun_auxiliar import Auxiliar
from constantes import *
import pygame

class Objeto():

    def __init__(self, x, y, path) -> None:
        self.item = Auxiliar.obtener_surface(path,1,1)
        self.frame = 0
        self.animacion = self.item
        self.image = self.animacion[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def morir(self):
        del self
    
    def draw(self, pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla, 'red', self.rect, 2, 2)
        self.image = self.animacion[self.frame]
        pantalla.blit(self.image, self.rect)