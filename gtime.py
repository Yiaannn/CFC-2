import pygame.time

RESOLUTION= 1*60*60*24 #*1 #intervalo de tempo, em segundos, em que cada ponto é calculado
tick= 0
sleep= pygame.time.wait
current= pygame.time.get_ticks

def update():
    global tick
    tick+= 1