'''
Rock Class

By Nicholas Vardin

This file contains different rock objects
'''


import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pymunk as pk
import pygameBasic as pb
import tileClass as tlC
import pygame as p
import bombClasses as bC
import princeEventClasses as pEC

class rock(bFC.physicsRect,tlC.tile):
    '''Rock class that acts as an obstacle to entities on the ground'''
    def __init__(self, screen, space, center, width = bGI.basicTileWidth, height = bGI.basicTileHeight):
        '''initializes the rock'''
        clr = (160,150,170)
        super().__init__(screen, space, clr, center, width, height, collisionType= 3)
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isPlayerGroundObstacle=True)
        self.image = p.image.load(r'images\rockIcon.png')

    def draw(self):
        '''draws the rock to the screen'''
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)
        
class bombRock(bFC.physicsRect,tlC.tile):
    '''BombRock class that acts as an obstacle and can explode'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width = bGI.basicTileWidth, height=bGI.basicTileHeight):
        '''initializes the bomb rock'''
        collisionType = 9
        clr = (160,150,170)
        super().__init__(screen, space, clr, center, width, height, collisionType)
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isPlayerGroundObstacle=True)
        self.oPrinceEventHandler = oPrinceEventHandler
        self.image = p.image.load(r'images\bombRockIcon.png')

    def explode(self):
        '''handles the explosion of the bomb rock'''
        oExplosion = bC.explosion(self.screen,self.space,self.oPrinceEventHandler,self.body.position)
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))
        self.oPrinceEventHandler.addEvent(pEC.removeBombRockFromRoomEvent(self))
        

    def draw(self):
        '''draws the bomb rock to the screen'''
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)

#testing code
class test:
    def __init__(self):
        self.screen,self.clock = pb.setup(800,600)
        self.space = pk.Space()
        self.space.gravity = (0,0)
        self.rock = rock(self.screen,self.space,np.array([100,100]))
        
        
    def update(self):
        self.space.step(1/60)
        self.clock.tick(60)
    def draw(self):
        self.rock.draw()
        
def main():
    oTest = test()
    pb.run(oTest)

if __name__ == '__main__':
    main()

