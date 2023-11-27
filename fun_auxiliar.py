import pygame
from constantes import *

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

class Auxiliar:
    @staticmethod
    def obtener_surface(path, columnas, filas, flip=False):
        lista = []

        surface_imagen = pygame.image.load(path)
        fotograma_ancho = int(surface_imagen.get_width()/columnas)
        fotograma_alto = int(surface_imagen.get_height()/filas)

        x = 0
        y = 0
        
        for fila in range(filas):
            for columna in range(columnas):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(x,y,fotograma_ancho,fotograma_alto)
                if (flip):
                    surface_fotograma = pygame.transform.flip(surface_fotograma, True, False)
                lista.append(surface_fotograma)

        return lista
    
    def obtener_surface_alreves(path, columnas, filas, flip=False):
        lista = []

        surface_imagen = pygame.image.load(path)
        fotograma_ancho = int(surface_imagen.get_width()/columnas)
        fotograma_alto = int(surface_imagen.get_height()/filas)

        x = 0
        y = 0
        
        for columna in range(columnas):
            for fila in range(filas):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(x,y,fotograma_ancho,fotograma_alto)
                if (flip):
                    surface_fotograma = pygame.transform.flip(surface_fotograma, True, False)
                lista.append(surface_fotograma)

        return lista

    def obtener_rectangulos(principal)->dict:
        diccionario = {}
        diccionario["main"] = principal
        diccionario["bottom"] = pygame.Rect(principal.left, principal.bottom - 10, principal.width, 10)
        diccionario["right"] = pygame.Rect(principal.right -10, principal.top, 10, principal.height)
        diccionario["left"] = pygame.Rect(principal.left, principal.top, 10, principal.height)
        diccionario["top"] = pygame.Rect(principal.left,principal.top, principal.width, 10)
        return diccionario
