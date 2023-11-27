import pygame
from constantes import *
from fun_auxiliar import Auxiliar
import math

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

class Jugador:

    def __init__(self, x, y, speed_walk, frame_rate_ms, move_rate_ms, lista_estructuras) -> None:
        self.walk_r = Auxiliar.obtener_surface('parcial_juego\Imagenes\personaje\Owlet_Monster\Owlet_Monster_Walk_6.png', 6, 1)
        self.walk_l = Auxiliar.obtener_surface('parcial_juego\Imagenes\personaje\Owlet_Monster\Owlet_Monster_Walk_6.png', 6, 1,True)
        self.stay_r = Auxiliar.obtener_surface('parcial_juego\Imagenes\personaje\Owlet_Monster\Owlet_Monster_Idle_4.png', 4, 1)
        self.stay_l = Auxiliar.obtener_surface('parcial_juego\Imagenes\personaje\Owlet_Monster\Owlet_Monster_Idle_4.png', 4, 1, True)
        self.barra_vida = Auxiliar.obtener_surface_alreves('parcial_juego\Imagenes\imagen_2023-11-26_001341241 (3) (1) (1).png',2,3)
        self.animacion_barra = self.barra_vida
        self.image_vida = self.animacion_barra[0]
        self.rect_vida = self.image_vida.get_rect()
        self.invulnerable = False  
        self.tiempo_invulnerable = 1000000
        self.tiempo_transcurrido_invulnerable = 0
        self.frame = 0
        self.vida = 1000
        self.vida_actual = self.vida
        self.score = 0
        self.mover_x = 0
        self.mover_y = 0
        self.puntaje = 0
        self.speed_walk = speed_walk
        self.animacion = self.stay_r
        self.direccion = DIRECCION_R
        self.image = self.animacion[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bandera_lado = False
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.tiempo_transcurrido_mover = 0
        self.tiempo_transcurrido_animacion = 0
        self.tiempo_transcurrido_disparo = 0
        self.tiempo_entre_disparos = 5000
        self.lista_estructuras = lista_estructuras

        self.hitbox = Auxiliar.obtener_rectangulos(self.rect)
    
    def walk(self, direccion):
        if self.direccion != direccion or (self.animacion != self.walk_r and self.animacion != self.walk_l):
            self.frame = 0
            self.direccion = direccion

            if direccion == DIRECCION_R:
                self.bandera_lado = True
                self.mover_x = self.speed_walk 
                self.animacion = self.walk_r
            elif direccion == DIRECCION_L:
                self.bandera_lado = False
                self.mover_x = -self.speed_walk 
                self.animacion = self.walk_l
            
            elif direccion == DIRECCION_U:
                if self.bandera_lado == True:
                    self.mover_y = -self.speed_walk 
                    self.animacion = self.walk_r
                else:
                    self.mover_y = -self.speed_walk 
                    self.animacion = self.walk_l
            elif direccion == DIRECCION_D:
                if self.bandera_lado == True:
                    self.mover_y = self.speed_walk 
                    self.animacion = self.walk_r
                else:
                    self.mover_y = self.speed_walk 
                    self.animacion = self.walk_l
    
    def stay(self):
        if self.animacion != self.stay_l and self.animacion != self.stay_r:
            if self.direccion == DIRECCION_U:
                if self.bandera_lado == True:
                    self.animacion = self.stay_r
                else:
                    self.animacion = self.stay_l
            
            elif self.direccion == DIRECCION_D:
                if self.bandera_lado == True:
                    self.animacion = self.stay_r
                else:
                    self.animacion = self.stay_l
            
            elif self.direccion == DIRECCION_R:
                self.animacion = self.stay_r
            else:
                self.animacion = self.stay_l
            
            self.mover_y = 0 
            self.mover_x = 0 
            self.frame = 0

    def animation(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.frame_rate_ms:
            self.tiempo_transcurrido_animacion = 0

            if self.frame < len(self.animacion) - 1:
                self.frame += 1
            else:
                self.frame = 0

    def mover(self, delta_ms, lista_estructuras, lista_objetos):
        self.tiempo_transcurrido_mover += delta_ms

        if self.tiempo_transcurrido_mover >= self.move_rate_ms:
            self.tiempo_transcurrido_mover = 0
            
            self.add_x(self.mover_x)
            self.add_y(self.mover_y)
            self.colisionar(lista_estructuras)
            self.chocar_bordes()
            self.agarrar_item(lista_objetos)
    
    def chocar_bordes(self):
        if self.rect.right >= pantalla.get_width():
            self.rect.right = pantalla.get_width()
            self.hitbox['left'].left = self.hitbox['main'].left
            self.hitbox['right'].right = pantalla.get_width()
            self.hitbox['top'].right = pantalla.get_width()
            self.hitbox['bottom'].right = pantalla.get_width()
        if self.rect.left <= 0:
            self.rect.left = 0
            self.hitbox['left'].left = 0
            self.hitbox['right'].right = self.hitbox['main'].right
            self.hitbox['top'].left = 0
            self.hitbox['bottom'].left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.hitbox['left'].top = 0
            self.hitbox['right'].top = 0
            self.hitbox['top'].top = 0
            self.hitbox['bottom'].bottom = self.hitbox['main'].bottom
        if self.rect.bottom >= pantalla.get_height():
            self.rect.bottom = pantalla.get_height()
            self.hitbox['left'].bottom = pantalla.get_height()
            self.hitbox['right'].bottom = pantalla.get_height()
            self.hitbox['top'].top = self.hitbox['main'].top
            self.hitbox['bottom'].bottom = pantalla.get_height()


    def colisionar(self, lista_estructuras):
        for estructura in lista_estructuras:
            if self.hitbox['main'].colliderect(estructura.hitbox['bottom']):
                self.hitbox['main'].top = estructura.hitbox['bottom'].bottom
                self.hitbox['left'].top = estructura.hitbox['bottom'].bottom
                self.hitbox['top'].top = estructura.hitbox['bottom'].bottom
                self.hitbox['right'].top = estructura.hitbox['bottom'].bottom
                self.hitbox['bottom'].bottom = self.hitbox['main'].bottom
                
            if self.hitbox['main'].colliderect(estructura.hitbox['left']):
                self.hitbox['main'].right = estructura.hitbox['left'].left
                self.hitbox['left'].left = self.hitbox['main'].left
                self.hitbox['top'].right = estructura.hitbox['left'].left
                self.hitbox['right'].right = estructura.hitbox['left'].left
                self.hitbox['bottom'].right = estructura.hitbox['left'].left
                
            if self.hitbox['main'].colliderect(estructura.hitbox['top']):
                self.hitbox['main'].bottom = estructura.hitbox['top'].top
                self.hitbox['left'].bottom = estructura.hitbox['top'].top
                self.hitbox['top'].top = self.hitbox['main'].top
                self.hitbox['right'].bottom = estructura.hitbox['top'].top
                self.hitbox['bottom'].bottom = estructura.hitbox['top'].top
                
            if self.hitbox['main'].colliderect(estructura.hitbox['right']):
                self.hitbox['main'].left = estructura.hitbox['right'].right
                self.hitbox['left'].left = estructura.hitbox['right'].right
                self.hitbox['top'].left = estructura.hitbox['right'].right
                self.hitbox['right'].right = self.hitbox['main'].right
                self.hitbox['bottom'].left = estructura.hitbox['right'].right
    
    def agarrar_item(self, lista_objetos):
        for objeto in lista_objetos:
            if self.hitbox['main'].colliderect(objeto.rect):
                sfx_channel = pygame.mixer.Channel(7)
                sfx_channel.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                self.puntaje += 150
                lista_objetos.remove(objeto)

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
    
    def disparar(self, lista_enemigos, delta_ms):
        self.tiempo_transcurrido_disparo += delta_ms

        if self.tiempo_transcurrido_disparo >= self.tiempo_entre_disparos:
            enemigo_cercano = self.obtener_enemigo_cercano(lista_enemigos)

            if enemigo_cercano is not None:
                dx = enemigo_cercano.rect.x - self.rect.x
                dy = enemigo_cercano.rect.y - self.rect.y
                distancia = math.sqrt(dx**2 + dy**2)

                if distancia != 0:
                    direccion_disparo = (dx / distancia, dy / distancia)
                    self.tiempo_transcurrido_disparo = 0
                    return direccion_disparo
        return None
    
    def obtener_enemigo_cercano(self, lista_enemigos):
        distancia_minima = float('inf')
        enemigo_cercano = None

        for enemigo in lista_enemigos:
            distancia = math.sqrt((self.rect.x - enemigo.rect.x)**2 + (self.rect.y - enemigo.rect.y)**2)

            if distancia < distancia_minima:
                distancia_minima = distancia
                enemigo_cercano = enemigo

        return enemigo_cercano
    
    def chocar_enemigo(self, lista_enemigos):
        for enemigo in lista_enemigos:
            if self.hitbox['main'].colliderect(enemigo.hitbox['main']):
                self.recibir_daño(enemigo.daño)
    
    def recibir_daño(self, cantidad):
        sfx_channel_6 = pygame.mixer.Channel(6)
        if not self.invulnerable:
            self.vida_actual -= cantidad
            if self.vida_actual <= 1000 and self.vida_actual > 800:
                self.image_vida = self.animacion_barra[0]
            elif self.vida_actual <= 800 and self.vida_actual > 600:
                self.image_vida = self.animacion_barra[1]
            elif self.vida_actual <= 600 and self.vida_actual > 400:
                self.image_vida = self.animacion_barra[2]
            elif self.vida_actual <= 400 and self.vida_actual > 200:
                self.image_vida = self.animacion_barra[3]
            elif self.vida_actual <= 200 and self.vida_actual > 0:
                self.image_vida = self.animacion_barra[4]
            elif self.vida_actual <= 0:
                self.vida_actual = 0
                self.image_vida = self.animacion_barra[5]
            
            self.invulnerable = True
            self.tiempo_invulnerable = 0
        if self.vida_actual <= 0:
            sfx_channel_6.play(pygame.mixer.Sound("parcial_juego\Sonidos\muerte (mp3cut.net).mp3"))

    def morir(self):
        del self

    def update(self, delta_ms, lista_estructuras, lista_objetos, lista_enemigos):
        self.rect_vida.x = self.hitbox['top'].left - 10
        self.rect_vida.y = self.hitbox['top'].top - 10
        self.mover(delta_ms, lista_estructuras, lista_objetos)
        self.animation(delta_ms)
        self.chocar_enemigo(lista_enemigos)
        
        if self.invulnerable:
            self.tiempo_transcurrido_invulnerable += delta_ms
            if self.tiempo_transcurrido_invulnerable >= self.tiempo_invulnerable:
                self.invulnerable = False

    def draw(self, pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla, 'red', self.rect)
            pygame.draw.rect(pantalla, 'green', self.hitbox['top'], 2, 3)
            pygame.draw.rect(pantalla, 'green', self.hitbox['bottom'], 2, 3)
            pygame.draw.rect(pantalla, 'green', self.hitbox['right'], 2, 3)
            pygame.draw.rect(pantalla, 'green', self.hitbox['left'], 2, 3)
        
        pantalla.blit(self.image_vida, self.rect_vida)
        self.image = self.animacion[self.frame]
        pantalla.blit(self.image, self.rect)