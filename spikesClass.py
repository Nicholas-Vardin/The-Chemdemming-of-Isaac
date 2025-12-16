'''
SpikesClass

By Nicholas Vardin

This file contains the spikes tile class that damages entities that walk on it
'''


import numpy
import pygame as p
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import pymunk as pk
import tileClass as tlC
import numpy as np

class spikes(bFC.physicsRect,tlC.tile):
    '''Tile that damages anything that walks on it'''
    def __init__(self, screen, space,center, width = bGI.basicTileWidth, height = bGI.basicTileHeight,playerDamage = 1,enemyDamage = .5):
        '''intializes spikes'''
        clr = (200,200,200) #light grey
        super().__init__(screen, space, clr, center, width, height, collisionType = 18, bodyType = pk.Body.STATIC)
        self.instantiateTileAttributes()
        self.playerDamage = playerDamage
        self.enemyDamage = enemyDamage
        self.numSpikesPerRow = 4 #num spikes per row and column
        self.spikeWidth = self.width/self.numSpikesPerRow
        self.tlPos = np.array([self.body.position[0]-self.width/2,self.body.position[1]-self.height/2])
    
    def draw(self):
        '''draws spikes to screen'''
        for row in range(self.numSpikesPerRow): #draws triangles in a grid
            for col in range(self.numSpikesPerRow):
                y = self.tlPos[1] + (row+1)*self.spikeWidth
                x = self.tlPos[0] + col*self.spikeWidth
                p.draw.polygon(self.screen,self.clr,[(x,y),(x+self.spikeWidth/2,y-self.spikeWidth+3),(x+self.spikeWidth,y)])