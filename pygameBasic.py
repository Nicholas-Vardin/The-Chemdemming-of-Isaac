'''
pygameBasic

By Nicholas Vardin

This file is a basic file meant to easily run pygame programs

'''


import pygame
import numpy as np

#easy colour access
colours = {'white':(255,255,255), 'red':(255,0,0),'green':(0,255,0),
           'blue':(0,0,255),'black':(0,0,0)}

def run(program):
    '''Runs the program updating it every frame, handles exiting the program with escape'''
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        program.update()
        program.draw()
        pygame.display.update()

def setup(width,height):
    '''Allows easy setup for pygame programs, takes in the width and height of the screen'''
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    return screen,clock

    