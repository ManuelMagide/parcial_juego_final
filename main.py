import pygame
from menu import *
from nivel import *
from puntajes import *
from leaderboard import *

def main():
    pygame.init()

    estado = "menu_principal"
    puntaje = {}
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if estado == "menu_principal":
            estado = mostrar_menu(PANTALLA)
        elif estado == "nivel":
            estado, puntaje = nivel()
        elif estado == 'guardar_puntaje':
            estado = mostrar_puntajes(puntaje, PANTALLA)
        elif estado == "puntajes":
            estado = leaderbord(PANTALLA)
        elif estado == "exit":
            running = False
            break
    pygame.quit()

main()