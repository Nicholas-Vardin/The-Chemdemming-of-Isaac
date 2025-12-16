'''A program containing the bomb and explosion classes:
By: Nicholas Vardin'''

import princeEventClasses as pEC
import pygame as p
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import pymunk as pk
import math

class bomb(bFC.physicsCircle):
    '''A bomb class that will explode after a certain amount of time'''
    def __init__(self, screen,space:pk.Space,oPrinceEventHandler:pEC.princeEventHandler, center, radius = 15,enemyDamage = 50,explosionRadius = 100,framesTilExplosion = bGI.fps*2):
        '''Initializes object'''
        clr = (0,0,0)
        super().__init__(screen,space,clr,center,radius,collisionType=6,bodyType=pk.Body.DYNAMIC)
        
        
        self.enemyDamage = enemyDamage
        
        self.framesTilExplosion = framesTilExplosion
        self.oPrinceEventHandler = oPrinceEventHandler
        self.explosionRadius = explosionRadius
        
         
    def update(self):
        '''updates the bomb every frame it is in the room'''
        if self.framesTilExplosion <= 0: #explodes bomb when it is time to explode
            self.explode()
        else:
            self.framesTilExplosion -=1
    
    def explode(self):
        '''Method to explode bomb, spawns explosion and removes self from room'''
        oExplosion = explosion(self.screen,self.space,self.oPrinceEventHandler,self.body.position,self.explosionRadius,enemyDamage = self.enemyDamage)
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))
        self.oPrinceEventHandler.addEvent(pEC.removeBombFromRoomEvent(self))
    
    def draw(self):
        '''draws self to screen'''
        clr = self.getClr()
        p.draw.circle(self.screen,clr,self.body.position,self.radius)

    def getClr(self):
        '''Returns black or red as a colour depending on how much time the bomb has left before exploding,
        rapidly changes colours as it gets closer to exploding'''
        #checks if value on sin function is greater or less than 0
        value = math.sin(1500/(self.framesTilExplosion+1))
        if value > 0:
            return (0,0,0)
        else:
            return (255,0,0)
            

class explosion(bFC.physicsCircle):
    '''explosion class that breaks other objects in the room'''
    def __init__(self, screen, space, oPrinceEventHandler, center, radius = 100, enemyDamage = 50,framesTilGone = bGI.fps//3, playerDamage = 1):
        '''initialize object'''
        clr = (255,0,0)
        super().__init__(screen, space, clr, center, radius, collisionType = 16, bodyType= pk.Body.KINEMATIC)
        self.framesTilGone = framesTilGone
        self.numDamageFrames = 1
        self.canDamageEntities = True
        self.oPrinceEventHandler = oPrinceEventHandler
        self.playerDamage = playerDamage
        self.enemyDamage = enemyDamage
        
    def update(self):
        '''updates explosion every frame'''
        #only damages things during 1st frame
        if self.numDamageFrames >0:
            self.numDamageFrames -=1
        else:
            self.canDamageEntities = False
        #removes self when it has exploded for long enough
        if self.framesTilGone <= 0:
            self.oPrinceEventHandler.addEvent(pEC.removeExplosionFromRoomEvent(self))
        else:
            self.framesTilGone -=1
        
