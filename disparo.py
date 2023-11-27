import pygame
from constantes import *
from fun_auxiliar import Auxiliar

class Proyectil():
    def __init__(self, x, y, velocidad, direccion, frame_rate_ms, move_rate_ms, player, path, daño):
        self.disparo_r = Auxiliar.obtener_surface(path, 4, 1)
        self.disparo_l = Auxiliar.obtener_surface(path, 4, 1, True)
        self.frame = 0
        self.daño = daño
        self.animacion = self.disparo_r
        self.image = self.animacion[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.player = player
        self.velocidad = velocidad
        self.direccion = direccion
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.tiempo_transcurrido_mover = 0
        self.tiempo_transcurrido_animacion = 0
    
    def animation(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.frame_rate_ms:
            self.tiempo_transcurrido_animacion = 0

            if self.frame < len(self.animacion) - 1:
                self.frame += 1
            else:
                self.frame = 0

    def update(self, delta_ms, lista_enemigos):
        self.tiempo_transcurrido_mover += delta_ms

        if self.direccion != None:
            if self.tiempo_transcurrido_mover >= self.move_rate_ms:
                self.tiempo_transcurrido_mover = 0

                if self.player.rect.x > self.rect.x:
                    self.animacion = self.disparo_l
                elif self.player.rect.x < self.rect.x:
                    self.animacion = self.disparo_r
                
                self.rect.x += self.velocidad * self.direccion[0]
                self.rect.y += self.velocidad * self.direccion[1]
                self.animation(delta_ms)

                enemigos_alcanzados = pygame.sprite.spritecollide(self, lista_enemigos, False)

                for enemigo in enemigos_alcanzados:
                    enemigo.recibir_daño(self.daño)
                    self.mark_for_deletion = True
    
    def draw(self, pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla, 'red', self.rect, 2, 2)
        self.image = self.animacion[self.frame]
        pantalla.blit(self.image, self.rect)