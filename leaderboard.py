import pygame
from base_sqlite import *

pygame.init()

def leaderbord(PANTALLA):
    fuente = pygame.font.SysFont('Impact', 30)
    pantalla = pygame.display.set_mode(PANTALLA)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Fantasmin👻')

    fondo = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Main_Menu\BG.png')
    fondo = pygame.transform.scale(fondo, (PANTALLA))

    puntajes = saber_top10()

    ancho_boton = 500
    alto_boton = 60
    posicion_x = PANTALLA[0] // 2 - ancho_boton // 2
    posicion_1 = PANTALLA[1] - alto_boton - 80
    
    correr = True
    while correr:
        clock.tick(60)
        
        pantalla.blit(fondo,(0,0))
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_volver.collidepoint(event.pos):
                    return 'menu_principal'
        x = PANTALLA[0] // 2 - 200
        x_puntaje = x + 225
        y = 100
        texto = fuente.render(f'  Nombre -- Puntaje ', True, 'White')
        pantalla.blit(texto, (x+60, y -60))
        if not puntajes:
            texto = fuente.render('Todavia no se cargo ningun dato.', True, 'White')
            pantalla.blit(texto, (x - 110 , y + 100))
        else:
            a=1
            for nombre, puntuacion in puntajes:
                if puntuacion is not None:
                    texto = fuente.render(f'{a}. {nombre}', True, 'White')
                    pantalla.blit(texto, (x+50, y))
                    texto = fuente.render(f'-- {puntuacion}', True, 'White')
                    pantalla.blit(texto, (x_puntaje, y))
                y += 60
                a += 1
        
        boton_volver = pygame.Rect(posicion_x, posicion_1, ancho_boton, alto_boton)
        texto = fuente.render('Volver al menu principal', True, 'White')
        text_rect = texto.get_rect(center=(PANTALLA[0] // 2, posicion_1 + alto_boton // 2))
        pantalla.blit(texto, text_rect)         

        pygame.display.update()

    pygame.quit()