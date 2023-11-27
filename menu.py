import pygame
from constantes import *
from pygame.locals import *

pygame.init()

def mostrar_menu(ancho_alto_pantalla):

    pantalla = pygame.display.set_mode(ancho_alto_pantalla)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Fantasmin👻')

    ancho_boton = 100
    alto_boton = 30
    separacion_botones = 100
    posicion_x = (ancho_alto_pantalla[0] - ancho_boton) // 2
    posicion_1 = ((ancho_alto_pantalla[1] - (alto_boton + separacion_botones) * 3) // 2) + separacion_botones * 3
    posicion_2 = posicion_1 + separacion_botones
    posicion_3 = posicion_2 + separacion_botones

    pygame.mixer.music.load("parcial_juego\Sonidos\- Overworld Day.mp3")
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(0.05)

    fondo = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Main_Menu\BG.png')
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    correr = True
    while correr:
        
        clock.tick()
        pantalla.blit(fondo, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
                
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if jugar.collidepoint(mouse_pos):
                    return "nivel"
                if leaderboard.collidepoint(mouse_pos):
                    return "puntajes"
                if exit.collidepoint(mouse_pos):
                    return "exit"
        
        fuente = pygame.font.SysFont('Impact', 80)
        titulo = fuente.render("- Fantasmin -", True, ('white'))
        titulo_rect = titulo.get_rect(center=(ancho_alto_pantalla[0] // 2, ancho_alto_pantalla[1] // 4))
        titulo_image = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Shop\Table_01.png')
        titulo_image = pygame.transform.scale(titulo_image, (ancho_alto_pantalla[0] // 2, ancho_alto_pantalla[1] // 4 - 100))
        pantalla.blit(titulo_image, (300, 180))
        pantalla.blit(titulo, titulo_rect)
        
        jugar = pygame.Rect(posicion_x, posicion_1, ancho_boton, alto_boton)
        fuente = pygame.font.SysFont('Impact', 40)
        texto = fuente.render("Play", True, ('white'))
        text_rect = texto.get_rect(center=(ancho_alto_pantalla[0] // 2, posicion_1 + alto_boton // 2))
        play_image = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Hangar\Table_02.png')
        play_image = pygame.transform.scale(play_image, (ancho_boton + 10, alto_boton + 30))
        pantalla.blit(play_image, (posicion_x - 5, posicion_1 - 10))
        pantalla.blit(texto, text_rect)
        
        leaderboard = pygame.Rect(posicion_x - 100, posicion_2, ancho_boton * 3, alto_boton)
        fuente = pygame.font.SysFont('Impact', 40)
        texto = fuente.render("Leaderboard", True, ('white'))
        text_rect = texto.get_rect(center=(ancho_alto_pantalla[0] // 2, posicion_2 + alto_boton // 2))
        leaderboard_image = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Hangar\Table_02.png')
        leaderboard_image = pygame.transform.scale(leaderboard_image, (ancho_boton * 3, alto_boton + 30))
        pantalla.blit(leaderboard_image, (posicion_x - 100, posicion_2 - 10))
        pantalla.blit(texto, text_rect)

        exit = pygame.Rect(posicion_x, posicion_3, ancho_boton, alto_boton)
        fuente = pygame.font.SysFont('Impact', 40)
        texto = fuente.render("Exit", True, ('white'))
        text_rect = texto.get_rect(center=(ancho_alto_pantalla[0] // 2, posicion_3 + alto_boton // 2))
        exit_image = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Hangar\Table_02.png')
        exit_image = pygame.transform.scale(exit_image, (ancho_boton, alto_boton + 30))
        pantalla.blit(exit_image, (posicion_x, posicion_3 - 10))
        pantalla.blit(texto, text_rect)

        pygame.display.update()
    pygame.quit()
