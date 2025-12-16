'''
Door Classes

By: Nicholas Vardin

A program that contains a door class and different types of door classes that act as children
'''

import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pygame as p
import tileClass as tlC

lockImage = p.image.load(r'images\lockIcon.png')

class door(bFC.physicsRect,tlC.tile):
    '''Parent and basic door class, can be entered and leads to a new room'''
    def __init__(self, screen, space, leadToIndex,unlockedClr, center, width = bGI.basicTileWidth, 
                height = bGI.basicTileHeight,keyLocked= False,explosionLocked= False,roomClearLocked = False,
                lockedClr = (0,0,0)):
        '''Initalizes object'''
        super().__init__(screen, space,unlockedClr, center, width, height, collisionType = 5)
        #locked variabled
        self.keyLocked = keyLocked
        self.explosionLocked = explosionLocked
        self.roomClearLocked = roomClearLocked
        self.locked = self.keyLocked or self.explosionLocked or self.roomClearLocked

        self.leadToIndex = leadToIndex #where the door leads
        self.unlockedClr = unlockedClr
        self.lockedClr = lockedClr
        
        #gives door tile attributes
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isEnemyAirObstacle=True,
                                       isPlayerGroundObstacle=self.locked,isPlayerAirObstacle=self.locked)
    
    def updateLockedStatus(self):
        '''updates the locked status when called to handle when a single locked attribute is changed'''
        self.locked = self.keyLocked or self.explosionLocked or self.roomClearLocked 
        self.isPlayerAirObstacle = self.locked
        self.isPlayerGroundObstacle = self.locked
        
    
    def draw(self):
        '''draws self to screen'''
        if self.locked: #determine door colour 
            self.clr = self.lockedClr
        else:
            self.clr = self.unlockedClr
        p.draw.rect(self.screen,self.clr,(self.body.position[0]-self.width/2,self.body.position[1]-self.height/2,self.width,self.height)) 
        if self.keyLocked: #draw padlock icon if door is key locked
            drawPos = np.array([self.body.position[0]-lockImage.get_width()/2,self.body.position[1]-lockImage.get_height()/2])
            self.screen.blit(lockImage,drawPos)  

class itemRoomDoor(door):
    '''Child class of door class,
    is key locked and acts as a door in or out of an item room'''
    def __init__(self, screen, space, leadToIndex,center, width = bGI.basicTileWidth, 
                height = bGI.basicTileHeight, startKeyLocked = True):
        unlockedClr = (225,215,0)
        lockedClr = (50,50,0)
        super().__init__(screen, space, leadToIndex,unlockedClr, center, width, height,keyLocked = startKeyLocked,
                         lockedClr=lockedClr)
    
        
class shopRoomDoor(door):
    '''Child class of door class,
    is key locked and acts as a door in or out of a shop room'''
    def __init__(self, screen, space, leadToIndex,center, width = bGI.basicTileWidth, 
                height = bGI.basicTileHeight, startKeyLocked = True):
        unlockedClr = (204,102,0)
        lockedClr = (51,25,0)
        super().__init__(screen, space, leadToIndex,unlockedClr, center, width, height,keyLocked = startKeyLocked,
                         lockedClr=lockedClr)

class bossRoomDoor(door):
    '''Child class of door class,
    is key locked and acts as a door in or out of a boss room'''
    def __init__(self, screen, space, leadToIndex,center, width = bGI.basicTileWidth, 
                height = bGI.basicTileHeight):
        unlockedClr = (200,0,0)
        lockedClr = (50,0,0)
        super().__init__(screen, space, leadToIndex,unlockedClr, center, width, height,lockedClr=lockedClr)

class secretRoomDoor(door):
    '''Child class of door class,
    is key locked and acts as a door in or out of a secret room'''
    def __init__(self, screen, space, leadToIndex,lockedClr,center, width = bGI.basicTileWidth, 
                height = bGI.basicTileHeight, startExplosionLocked = True):
        unlockedClr = (0,200,0)
        super().__init__(screen, space, leadToIndex,unlockedClr, center, width, height,
                         explosionLocked=startExplosionLocked,lockedClr=lockedClr)