'''
Trap door class

By Nicholas Vardin

This file contains the trap door class that is used to travel through floors
'''


import pygame as p
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import pymunk as pk
import tileClass as tlC


class trapDoor(bFC.physicsRect,tlC.tile):
    '''Trap door class that can be open or closed and lets the player travel to the next floor'''
    def __init__(self, screen, space,oPlayer, center,width = bGI.basicTileWidth, height = bGI.basicTileHeight):
        '''Initializes object'''
        clr = (100,100,20) #green colour
        super().__init__(screen, space, clr, center, width, height, collisionType= 19)
        self.instantiateTileAttributes() #gives tile attributes
        
        self.oPlayer = oPlayer #keeps track of player
    
        distToPlayer = bFC.getDistanceBetween2RectsEdges(self.getLPoints(),self.oPlayer.getLPoints())
        #if player is too close it will spawn closed
        if distToPlayer > 50:
            self.open = True
        else:
            self.open = False 
            
        self.closedClr = clr = (100,100,0)
        self.openClr = clr = (0,0,0)
        
    def update(self):
        '''Updates the trap door'''
        if not self.open: #if player is too close it will remain closed to avoid the player accidentally going to the next floor
            distToPlayer = bFC.getDistanceBetween2RectsEdges(self.getLPoints(),self.oPlayer.getLPoints())
            if distToPlayer > 50:
                self.open = True
    
    def draw(self):
        '''Draws the trap door to screen'''
        if self.open: #determines the clr based on if the trapdoor is open or closed
            clr = self.openClr
        else:
            clr = self.closedClr
        p.draw.rect(self.screen,clr,(self.body.position[0]-self.width/2,self.body.position[1]-self.height/2,self.width,self.height))

    
    
        
    