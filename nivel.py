import pygame
import sys
from constantes import *
from jugador import Jugador
from estructuras_mapa import *
from enemigo import *
from disparo import Proyectil
from items import Objeto
from pygame.locals import *
from puntajes import *

def nivel():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Fantasmin👻')

    lapida = pygame.image.load('parcial_juego\Imagenes\soss\Tombstone1.png')
    header = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Window.png')
    win = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Win\Header.png')
    lose = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Header.png')
    stars = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Star_01.png')
    score = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Score.png')
    play_again = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Replay_BTN.png')
    volver_menu = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Level_Menu\Hangar_BTN.png')
    stars_win = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\You_Lose\Star_03.png')
    guardar_puntos = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Rating\Ok_BTN.png')

    lose = pygame.transform.scale(lose, (175, 50))
    win = pygame.transform.scale(win, (175, 50))
    header = pygame.transform.scale(header, (PANTALLA[0] // 2, PANTALLA[1] // 2))
    stars = pygame.transform.scale(stars, (75, 75))
    stars_win = pygame.transform.scale(stars_win, (75, 75))
    score = pygame.transform.scale(score, (100, 50))
    play_again = pygame.transform.scale(play_again, (75, 75))
    volver_menu = pygame.transform.scale(volver_menu, (75, 75))
    guardar_puntos = pygame.transform.scale(guardar_puntos, (75, 75))

    bandera_tiempo = True
    aux_tiempo = 1
    tiempo_regresivo = 100 
    bandera_disparo_2 = False
    bandera_disparo_3 = False
    dejar_item_1 = False
    dejar_item_2 = False
    dejar_disparo_2 = False
    dejar_disparo_3 = False
    dejar_curacion = False
    bandera_boss = True
    bandera_win = False
    bandera_lose = False

    pygame.mixer.music.load("parcial_juego\Sonidos\- Overworld Day.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    sfx_channel = pygame.mixer.Channel(1)
    sfx_channel_2 = pygame.mixer.Channel(2)
    sfx_channel_4 = pygame.mixer.Channel(4)
    sfx_channel_5 = pygame.mixer.Channel(5)

    fuente = pygame.font.SysFont('Impact', 30)

    fondo = pygame.image.load('parcial_juego\Imagenes\Fondo.jpg')
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    lista_estructuras = []
    proyectiles = []
    lista_objetos = []
    dic_puntaje = {}

    lista_estructuras.append(Estructura(x=425, y=240, ancho=280, alto=160, pantalla=pantalla))
    lista_estructuras.append(Estructura(x=355, y=305, ancho=210, alto=160, pantalla=pantalla))
    lista_estructuras.append(Estructura(x=777, y=205, ancho=210, alto=160, pantalla=pantalla))

    personaje_princ = Jugador(x=600, y=500, speed_walk=5, frame_rate_ms=100, move_rate_ms=60, lista_estructuras=lista_estructuras)

    enemigos = Enemigo.crear_lista_enemigos(cantidad=2, col=6, fil=1, speed=1, frame=50, move=20, jugador=personaje_princ, life=200, daño=3, bandera=True, tipo='normal')

    while True:

        mouse_pos = pygame.mouse.get_pos()

        tiempo = int(pygame.time.get_ticks()/1000)
        if bandera_tiempo:
            tiempo_regresivo = 100
            bandera_tiempo = False
        else:
            if aux_tiempo != tiempo and tiempo_regresivo > 0:
                aux_tiempo = tiempo
                tiempo_regresivo -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if bandera_win == True or bandera_lose == True:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if volver.collidepoint(mouse_pos):
                        return "menu_principal", dic_puntaje
                    if replay.collidepoint(mouse_pos):
                        return "nivel", dic_puntaje
                    if guardar.collidepoint(mouse_pos):
                        if len(dic_puntaje) <= 0:
                            dic_puntaje['puntaje'] = 0
                            return 'guardar_puntaje',dic_puntaje
                        else:
                            return 'guardar_puntaje',dic_puntaje
        
        delta_ms = clock.tick(FPS)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            personaje_princ.walk(DIRECCION_L)
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            personaje_princ.walk(DIRECCION_R)
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            personaje_princ.walk(DIRECCION_U)
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            personaje_princ.walk(DIRECCION_D)
        
        if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            personaje_princ.stay()
        if keys[pygame.K_a] and keys[pygame.K_d]:
            personaje_princ.stay()
        if keys[pygame.K_s] and keys[pygame.K_w]:
            personaje_princ.stay()
        
        cronometro = fuente.render('Tiempo restante: '+str(tiempo_regresivo), True, 'white')
        puntaje = personaje_princ.puntaje
        dic_puntaje['puntaje'] = puntaje
        puntos_final = fuente.render(str(puntaje), True, 'white')
        puntaje = fuente.render('Puntos: '+str(puntaje), True, 'black')

        pantalla.blit(fondo, fondo.get_rect())
        pantalla.blit(cronometro, (900,5))
        pantalla.blit(puntaje, (10, 10))

        #Creacion de items y utilizacion de listas
        disparo_2 = Objeto(x=700, y=250, path='parcial_juego\Imagenes\items\PNG\Transperent\Icon36.png')
        disparo_3 = Objeto(x=200, y=150, path='parcial_juego\Imagenes\items\PNG\Transperent\Icon37.png')
        item_especial_1 = Objeto(x=300, y=700, path='parcial_juego\Imagenes\items\PNG\Transperent\Icon45.png')
        item_especial_2 = Objeto(x=800, y=700, path='parcial_juego\Imagenes\items\PNG\Transperent\Icon46.png')
        curacion = Objeto(x=600, y=500, path='parcial_juego\Imagenes\items\PNG\Transperent\Icon12.png')

        for proyectil in proyectiles:
            proyectil.update(delta_ms, enemigos)
            proyectil.draw(pantalla)
        
        proyectiles = [proyectil for proyectil in proyectiles if not hasattr(proyectil, 'mark_for_deletion') or not proyectil.mark_for_deletion]

        for objeto in lista_objetos:
            objeto.draw(pantalla)

        for estructura in lista_estructuras:
            estructura.draw(pantalla)

        for enemigo in enemigos:
            enemigo.update(delta_ms)
            enemigo.draw(pantalla)
        #Manejar todo lo de los enemigos
            if enemigo.tipo == 'normal' and enemigo.vida_actual <= 0:
                sfx_channel_5.play(pygame.mixer.Sound("parcial_juego\Sonidos\muerte (mp3cut.net).mp3"))
                lista_objetos.append(Objeto(x=enemigo.rect.x, y=enemigo.rect.y, path='parcial_juego\Imagenes\Icon29 (2).png'))
                enemigos.remove(enemigo)
                personaje_princ.puntaje += 100
            elif enemigo.tipo == 'boss' and enemigo.vida_actual <= 0:
                sfx_channel_5.play(pygame.mixer.Sound("parcial_juego\Sonidos\muerte (mp3cut.net).mp3"))
                lista_objetos.append(Objeto(x=enemigo.rect.x, y=enemigo.rect.y, path='parcial_juego\Imagenes\Icon1.png'))
                enemigos.remove(enemigo)
                personaje_princ.puntaje += 3000
                bandera_win = True
        
        if len(enemigos) <= 0 and tiempo_regresivo > 1 and tiempo_regresivo <= 50:
            enemigos = Enemigo.crear_lista_enemigos(cantidad=7, col=6, fil=1, speed=1, frame=50, move=20, jugador=personaje_princ, life=200, daño=3, bandera=True, tipo='normal')
        elif len(enemigos) <= 0 and tiempo_regresivo == 0 and bandera_boss == True:
            sfx_channel_2.play(pygame.mixer.Sound("parcial_juego\Sonidos\jefe (mp3cut.net).mp3"))
            enemigos = Enemigo.crear_lista_enemigos(cantidad=1, col=4, fil=1, speed=3, frame=100, move=30, jugador=personaje_princ, life=3000, daño=5, bandera=False, tipo='boss')
            bandera_boss = False

        #Manejar todo lo del personaje en cuanto su vida disparos etc
        if personaje_princ.vida_actual <= 0:
            personaje_princ.morir()
            bandera_lose = True
            pantalla.blit(lapida, (personaje_princ.rect.x, personaje_princ.rect.y))
            pantalla.blit(header, (300, 250))
            pantalla.blit(puntos_final, (575, 525))
            pantalla.blit(lose, (510, 260))
            pantalla.blit(stars, (565, 335))
            pantalla.blit(stars, (490, 365))
            pantalla.blit(stars, (640, 365))
            pantalla.blit(score, (550, 450))
            replay = pygame.Rect(710, 600, 75, 75)
            pantalla.blit(play_again, replay)
            volver = pygame.Rect(410, 600, 75, 75)
            pantalla.blit(volver_menu, volver)
            guardar = pygame.Rect(560, 600, 75, 75)
            pantalla.blit(guardar_puntos, guardar)
        else:
            personaje_princ.update(delta_ms, lista_estructuras, lista_objetos, enemigos)
            personaje_princ.draw(pantalla)

            direccion_disparo = personaje_princ.disparar(enemigos, delta_ms)

            if tiempo_regresivo == 80:
                dejar_disparo_2 = True
            if tiempo_regresivo == 60:
                dejar_curacion = True
                dejar_item_2 = True
            if tiempo_regresivo == 40:
                dejar_disparo_3 = True
            if tiempo_regresivo == 20:
                dejar_curacion = True
                dejar_item_1 = True
            
            if dejar_item_1 == True:
                item_especial_1.draw(pantalla)
                if personaje_princ.hitbox['main'].colliderect(item_especial_1.rect):
                    sfx_channel_4.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                    dejar_item_1 = False
                    item_especial_1.morir()
                    personaje_princ.tiempo_entre_disparos = 3500
            if dejar_item_2 == True:
                item_especial_2.draw(pantalla)
                if personaje_princ.hitbox['main'].colliderect(item_especial_2.rect):
                    sfx_channel_4.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                    dejar_item_2 = False
                    item_especial_2.morir()
                    personaje_princ.speed_walk = 6
            
            if dejar_curacion == True:
                curacion.draw(pantalla)
                if personaje_princ.hitbox['main'].colliderect(curacion.rect):
                    sfx_channel_4.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                    dejar_curacion = False
                    curacion.morir()
                    personaje_princ.vida_actual += 400
                    personaje_princ.recibir_daño(0)
            
            if dejar_disparo_2 == True:
                disparo_2.draw(pantalla)
                if personaje_princ.hitbox['main'].colliderect(disparo_2.rect):
                    sfx_channel_4.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                    bandera_disparo_2 = True
                    dejar_disparo_2 = False
                    disparo_2.morir()
            if dejar_disparo_3 == True:
                disparo_3.draw(pantalla)
                if personaje_princ.hitbox['main'].colliderect(disparo_3.rect):
                    sfx_channel_4.play(pygame.mixer.Sound("parcial_juego\Sonidos\item_4 (mp3cut.net).mp3"))
                    bandera_disparo_3 = True
                    dejar_disparo_3 = False
                    disparo_3.morir()

            if direccion_disparo is not None:
                proyectil_nuevo = Proyectil(x=personaje_princ.rect.centerx, y=personaje_princ.rect.centery, velocidad=2, direccion=direccion_disparo, frame_rate_ms=50, move_rate_ms=40, player=personaje_princ, path='parcial_juego\Imagenes\Ship1_normal_flight_001.png', daño=100)
                proyectiles.append(proyectil_nuevo)
                sfx_channel.play(pygame.mixer.Sound("parcial_juego\Sonidos\laser-rifle_uvJVY5a (mp3cut.net).mp3"))
                if bandera_disparo_2 == True:
                    proyectil_nuevo_dos = Proyectil(x=personaje_princ.rect.centerx - 5, y=personaje_princ.rect.centery - 5, velocidad=3, direccion=direccion_disparo, frame_rate_ms=50, move_rate_ms=40, player=personaje_princ, path='parcial_juego\Imagenes\Ship3_normal_flight_001.png', daño=50)
                    proyectiles.append(proyectil_nuevo_dos)
                    sfx_channel.play(pygame.mixer.Sound("parcial_juego\Sonidos\laser-rifle_uvJVY5a (mp3cut.net).mp3"))
                if bandera_disparo_3 == True:
                    proyectil_nuevo_tres = Proyectil(x=personaje_princ.rect.centerx + 5, y=personaje_princ.rect.centery + 5, velocidad=1, direccion=direccion_disparo, frame_rate_ms=50, move_rate_ms=40, player=personaje_princ, path='parcial_juego\Imagenes\Ship5_normal_flight_002.png', daño=150)
                    proyectiles.append(proyectil_nuevo_tres)
                    sfx_channel.play(pygame.mixer.Sound("parcial_juego\Sonidos\laser-rifle_uvJVY5a (mp3cut.net).mp3"))

        if bandera_win == True:
            pantalla.blit(header, (300, 250))
            pantalla.blit(puntos_final, (575, 525))
            pantalla.blit(win, (510, 260))
            pantalla.blit(stars_win, (565, 335))
            pantalla.blit(stars_win, (490, 365))
            pantalla.blit(stars_win, (640, 365))
            pantalla.blit(score, (550, 450))
            replay = pygame.Rect(710, 600, 75, 75)
            pantalla.blit(play_again, replay)
            volver = pygame.Rect(410, 600, 75, 75)
            pantalla.blit(volver_menu, volver)
            guardar = pygame.Rect(560, 600, 75, 75)
            pantalla.blit(guardar_puntos, guardar)

        pygame.display.flip()