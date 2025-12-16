'''
Tear classes

By Nicholas Vardin

This file contains the basic projectiles (tears) that are used by the player and enemies
'''

import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import npVectorMath as npVM
import princeEventClasses as pEC
import pymunk as pk
import math
import bombClasses as bC

class tear(bFC.physicsCircle):
    '''Tear object that is used as a projectile'''
    def __init__(self, screen, space,oPrinceEventHandler:pEC.princeEventHandler, center, radius, velo, tearRange, damage,clr = (40,40,255),
                  canHitPlayer = False,canHitEnemy = True,trackingLevel = 0,phaseThroughObstacles =False,splitBehaviours =[],doExplode = False):
        '''Initializes the tear'''
        
        # Call the parent class constructor
        super().__init__(screen, space, clr, center, radius, collisionType = 15, bodyType = pk.Body.KINEMATIC)
        
        # Initialize attributes
        self.oPrinceEventHandler = oPrinceEventHandler
        self.velo = velo
        self.tearRange = tearRange
        self.damage = damage
        self.numIterationsBeforeFall = self.tearRange*bGI.basicTileWidth/npVM.absValue(self.velo)
        self.canHitPlayer = canHitPlayer
        self.canHitEnemy = canHitEnemy
        self.trackingLevel =trackingLevel
        self.doExplode = doExplode


    def update(self,oLoop):
        '''Updates the position and behavior of the tear'''
        
        # Update position based on velocity
        self.body.position += pk.Vec2d(*self.velo)
        
        # Perform tracking if applicable
        if self.trackingLevel == 1:
            self.doTracking(oLoop)

        # Check if the tear has exceeded its range
        self.doRange()
    

    def doTracking(self,oLoop):
        '''Handles tracking behavior for the tear'''
        
        # If the tear can hit enemies, adjust its velocity to track the nearest enemy
        if self.canHitEnemy:
            direction = self.getDirectionToNearestEnemy(oLoop)
            if direction != None:
                self.velo = npVM.scaleVector(direction,npVM.absValue(self.velo))

    def getDirectionToNearestEnemy(self,oLoop):
        '''Finds the direction to the nearest enemy'''
        
        enemyWithMinDistance = None
        minDistance = 100000000  # Initialize with a large value
        
        # Iterate through enemies in the current room
        for oEnemy in oLoop.currentFloor.currentRoom.lEnemies:
            dist = math.dist(oEnemy.body.position,self.body.position)
            if dist< minDistance:
                enemyWithMinDistance = oEnemy
                minDistance = dist
        
        # Return the direction to the nearest enemy, or None if no enemies are found
        if enemyWithMinDistance != None:
            return enemyWithMinDistance.body.position - self.body.position
        return None

    def doRange(self):
        '''Handles the range behavior of the tear'''
        
        # Decrease the remaining iterations before the tear falls
        self.numIterationsBeforeFall -= 1
        
        # If the tear has exceeded its range, remove it or trigger an explosion
        if self.numIterationsBeforeFall <=0:
            if self.doExplode:
                self.explode()
            self.oPrinceEventHandler.addEvent(pEC.removeTearEvent(self))
    
    def explode(self):
        '''Triggers an explosion at the tear's position'''
        
        # Create an explosion object and add it to the event handler
        oExplosion = bC.explosion(self.screen,self.space,self.oPrinceEventHandler,self.body.position,radius = 75)
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))

class enemyTear(tear):
    '''Enemy tear object that inherits from the tear class'''
    def __init__(self, screen, space, oPrinceEventHandler, center, radius, velo, tearRange, damage=1,clr =  (150,10, 10),doExplode = False):
        '''Initializes the enemy tear'''
        
        # Call the parent class constructor with specific attributes for enemy tears
        super().__init__(screen, space, oPrinceEventHandler, center, radius, velo, tearRange, damage, clr,canHitPlayer= True,canHitEnemy= False,doExplode=doExplode)
