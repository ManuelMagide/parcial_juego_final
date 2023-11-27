import pygame
import random
from constantes import *
from fun_auxiliar import Auxiliar

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

class Enemigo():

    def __init__(self, path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo) -> None:
        self.walk_r = Auxiliar.obtener_surface(path, columnas, filas)
        self.walk_l = Auxiliar.obtener_surface(path, columnas, filas,True)
        self.tipo = tipo
        self.frame = 0
        self.vida = vida
        self.daño = daño
        self.vida_actual = vida
        self.speed_walk = speed_walk
        self.animacion = self.walk_l
        self.direccion = DIRECCION_R
        self.image = self.animacion[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-40, ANCHO_VENTANA])  
        self.rect.y = random.randrange(-40, ALTO_VENTANA)
        self.bandera_lado = False
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.tiempo_transcurrido_mover = 0
        self.tiempo_transcurrido_animacion = 0

        self.hitbox = Auxiliar.obtener_rectangulos(self.rect)

        self.player = player
        self.probabilidad_movimiento = random.random()

        self.salud = 1
    
    def animation(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.frame_rate_ms:
            self.tiempo_transcurrido_animacion = 0

            if self.frame < len(self.animacion) - 1:
                self.frame += 1
            else:
                self.frame = 0
    
    def mover(self, delta_ms):
        self.tiempo_transcurrido_mover += delta_ms

        if self.tiempo_transcurrido_mover >= self.move_rate_ms:
            self.tiempo_transcurrido_mover = 0
            
            if random.random() > self.probabilidad_movimiento:
                if self.player.rect.y > self.rect.y:
                    self.add_y(self.speed_walk)
                elif self.player.rect.y < self.rect.y:
                    self.add_y(-self.speed_walk)

                if self.player.rect.x > self.rect.x:
                    self.add_x(self.speed_walk)
                    self.animacion = self.walk_l
                elif self.player.rect.x < self.rect.x:
                    self.add_x(-self.speed_walk)
                    self.animacion = self.walk_r
    
    def add_x(self, delta_x):
        self.hitbox['main'].x += delta_x
        self.hitbox['top'].x += delta_x
        self.hitbox['right'].x += delta_x 
        self.hitbox['left'].x += delta_x
        self.hitbox['bottom'].x += delta_x

    def add_y(self, delta_y):
        self.hitbox['main'].y += delta_y
        self.hitbox['top'].y += delta_y
        self.hitbox['right'].y += delta_y
        self.hitbox['left'].y += delta_y
        self.hitbox['bottom'].y += delta_y

    def update(self, delta_ms):
        self.mover(delta_ms)
        self.animation(delta_ms)
    
    def recibir_daño(self, cantidad):
        self.vida_actual -= cantidad

    def draw(self, pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla, 'red', self.rect)
            pygame.draw.rect(pantalla, 'blue', self.hitbox['top'], 2, 3)
            pygame.draw.rect(pantalla, 'blue', self.hitbox['bottom'], 2, 3)
            pygame.draw.rect(pantalla, 'blue', self.hitbox['right'], 2, 3)
            pygame.draw.rect(pantalla, 'blue', self.hitbox['left'], 2, 3)
        self.image = self.animacion[self.frame]
        pantalla.blit(self.image, self.rect)
    
    def crear_lista_enemigos(cantidad,col,fil,speed,frame,move,jugador,life, daño, bandera, tipo):
        lista_enemigos = []

        for i in range(cantidad):
            if bandera:
                diccionario = Abeja('parcial_juego\Imagenes\enemigos\caro\S_Walk.png', col, fil, speed, frame, move, jugador, life, daño, tipo)
                diccionario2 = Gato('parcial_juego\Imagenes\enemigos\gato\S_Walk.png', col, fil, speed, frame, move, jugador, life, daño, tipo)
                lista_enemigos.append(diccionario)
                lista_enemigos.append(diccionario2)
            elif bandera == False:
                diccionario3 = Boss('parcial_juego\Imagenes\soss\Pumpkin_portal2.png', col, fil, speed, frame, move, jugador, life, daño, tipo)
                lista_enemigos.append(diccionario3)
        
        return lista_enemigos

class Abeja(Enemigo):
    def __init__(self, path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo) -> None:
        super().__init__(path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo)

class Gato(Enemigo):
    def __init__(self, path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo) -> None:
        super().__init__(path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo)

class Boss(Enemigo):
    def __init__(self, path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo) -> None:
        super().__init__(path, columnas, filas, speed_walk, frame_rate_ms, move_rate_ms, player, vida, daño, tipo)