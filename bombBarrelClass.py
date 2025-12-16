'''
Bomb Barrel Class

By: Nicholas Vardin

A program that contains a bomb barrel class
'''

import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pygame as p
import princeEventClasses as pEC
import bombClasses as bC
import tileClass as tlC

class bombBarrel(bFC.physicsCircle,tlC.tile):
    '''Bomb barrel class that will explode upon being destroyd'''
    def __init__(self, screen, space, oPrinceEventHandler, center, radius = bGI.basicTileWidth//2, health = 15, explosionRadius = 100):
        '''initialize object'''
        clr = (55,0,0)
        super().__init__(screen, space, clr, center, radius, collisionType = 7)
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isPlayerGroundObstacle=True) #give barrel tile attributes

        self.oPrinceEventHandler = oPrinceEventHandler

        self.innerRadius = radius//1.4
        self.innerClr = (139, 69, 19)
        self.health = health
        self.explosionRadius = explosionRadius
        self.image = p.image.load(r'images\bombBarrelIcon.png')
         
    def explode(self):
        '''spawns in an explosion and removes self from room'''
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(bC.explosion(self.screen,self.space,self.oPrinceEventHandler,self.body.position,self.explosionRadius)))
        self.oPrinceEventHandler.addEvent(pEC.removeBombBarrelFromRoomEvent(self))
    
    def draw(self):
        '''draws self to screen'''
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)