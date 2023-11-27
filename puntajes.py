import pygame
from pygame.locals import *
from base_sqlite import *
from constantes import *
from nivel import *

pygame.init()

def mostrar_puntajes(puntaje_final, PANTALLA):

    fuente = pygame.font.SysFont('Impact', 30)
    pantalla = pygame.display.set_mode(PANTALLA)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Fantasmin👻')

    fondo = pygame.image.load('parcial_juego\Imagenes\menu sprites\PNG\Main_Menu\BG.png')
    fondo = pygame.transform.scale(fondo, (PANTALLA))

    ancho_boton = 300
    alto_boton = 30
    separacion_botones = 50
    posicion_x = (PANTALLA[0] - ancho_boton) // 2
    posicion = ((PANTALLA[1] - (alto_boton + separacion_botones) * 3) // 2) + separacion_botones * 3
    posicion_1 = posicion + alto_boton + separacion_botones

    letra_1 = None
    letra_2 = None
    letra_3 = None

    puede_guardar = False
    boton_apretado = False
    carga = False
    volvio_a_cargar =False

    correr = True

    while correr:

        clock.tick(60)

        pantalla.blit(fondo, (0,0))

        if letra_1 != None and letra_2 != None and letra_3 != None:
            puede_guardar = True

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if boton.collidepoint(mouse_pos) and not volvio_a_cargar:
                    boton_apretado = True
            elif event.type == pygame.KEYDOWN:
                for tecla, letra in teclas_letras.items():
                    if event.key == tecla:
                        if letra_1 == None:
                            letra_1 = letra
                        elif letra_2 == None:
                            letra_2 = letra
                        elif letra_3 == None:
                            letra_3 = letra
                    elif event.key == pygame.K_BACKSPACE:
                        if letra_3 is not None:
                            letra_3 = None
                            puede_guardar = False
                        elif letra_2 is not None:
                            letra_2 = None
                        elif letra_1 is not None:
                            letra_1 = None
        
        puntaje = puntaje_final['puntaje']
        texto_puntaje = fuente.render(f'Puntaje del juego: {puntaje}', True, ('white'))
        pantalla.blit(texto_puntaje, ((PANTALLA[0] / 2) - 150, 100))
        
        texto_ingresar_nombre = fuente.render('Ingrese nombre:', True, ('white'))
        pantalla.blit(texto_ingresar_nombre, ((PANTALLA[0] // 2) - 100, 300))

        texto_letras = fuente.render(f'{letra_1 or "_"} {letra_2 or "_"} {letra_3 or "_"}', True, ('red'))
        pantalla.blit(texto_letras, ((PANTALLA[0] // 2) - 30, 450))

        boton = pygame.Rect(posicion_x, posicion_1, ancho_boton, alto_boton)
        texto = fuente.render('Guardar puntaje', True, ('white'))
        text_rect = texto.get_rect(center=(PANTALLA[0] // 2, posicion_1 + alto_boton // 2))
        pantalla.blit(texto, text_rect)

        if boton_apretado:
            if puede_guardar:
                nombre = letra_1 + letra_2 + letra_3
                carga = cargar_campo(nombre, puntaje)
                boton_apretado = False
            else:
                boton_apretado = False
        
        if carga:
            texto = fuente.render('Se cargo correctamente', True, ('white'))
            pantalla.blit(texto, ((PANTALLA[0] // 2) - 160, 750))
            volvio_a_cargar = True
            return 'menu_principal'
        else:
            texto = fuente.render('Se deben ingresar las 3 letras para poder guardar.', True, ('white'))
            pantalla.blit(texto, ((PANTALLA[0] // 2) - 300, 750))

        pygame.display.update()

    pygame.quit()