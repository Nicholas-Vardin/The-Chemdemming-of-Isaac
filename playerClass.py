'''
playerClass

By Nicholas Vardin

This file contians the player class that is controlled through WASD and can shoot tears with arrows
'''


import pygame as p
import pygameBasic as pb
import princeEventClasses as pEC
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import npVectorMath as npVM
import tearClasses as tC
import bombClasses as bC
import pymunk as pk
import pymunk.pygame_util
import math

class player(bFC.physicsRect):
    '''Player class that is controlled with WASD and shoots with arrows'''
    def __init__(self, screen, space:pk.Space, oPrinceEventHandler:pEC.princeEventHandler):
        '''Intializes the player'''
        clr = (255,0,0)  # Player color
        width = 35  # Player width
        height = 35  # Player height
        center = np.array([bGI.screenWidth/2,bGI.screenHeight/2])  # Player starting position
        super().__init__(screen, space, clr, center, width, height, collisionType =1, bodyType= pk.Body.KINEMATIC)

        self.oPrinceEventHandler = oPrinceEventHandler
        
        self.maxSpeed = 6  # Maximum speed of the player
        self.accelMag = .6  # Acceleration magnitude
        self.velo = np.array([0.0,0.0])  # Initial velocity
        self.frictionMag = .3  # Friction magnitude
        
        self.tearClr = (40,40,255)  # Color of the tears
        
        # Player stats and inventory
        self.numNormalHealthContainers=3
        self.maxHealth = 12
        self.lHealth = ['normal','normal','normal']  # Health containers
        self.evilHeartDamage = 20  # Damage dealt by evil hearts
        self.numKeys = 2
        self.numBombs = 2
        self.numCoins = 5
        
        self.timeBetweenBombs = bGI.fps*1  # Cooldown time between bombs
        self.currentBombIteration = 0

        # Tear stats
        self.tearRateStat = stat(2.4,maximum=5)
        self.tearBaseSpeedStat = stat(7)
        self.tearRadiusStat = stat(13)
        self.tearRangeStat = stat(7,minimum=1)
        self.tearDamageStat = stat(4,minimum=.5)
        self.maxSpeedStat = stat(12)

        self.currentTearIteration = 0

        # Item-related attributes
        self.items = []
        self.activeItem = None
        self.canPickUpItems = True
        self.pickUpItemCoolDown = bGI.fps*.6
        self.pickUpItemCoolDownIteration = 0

        # Invincibility attributes
        self.invincible = False
        self.invincibilityTimer = 0  # Timer for invincibility
        self.numInvincibilityFramesAfterDamaged = bGI.fps*1.3
        self.invincibilityClr = (255,100,100)  # Color when invincible
        self.nonInvincibilityClr = self.clr  # Normal color
        
        self.flying = False  # Whether the player is flying
        self.tearTrackingLevel = 0  # Level of tear tracking
        self.tearSplitBehaviours = set()  # Tear split behaviors
        self.shootingBehaviourHierarchy = ['4 middle','3 middle','4 spread','2 middle','3 spread','2 spread','normal']
        self.shootingBehaviour = 'normal'  # Default shooting behavior
        self.shotSpread = math.pi/3  # Spread angle for tears
        self.distanceBetweenMiddleShots = 10  # Distance between middle shots
        
        self.trackingTearClr = (136,26,209)  # Color for tracking tears
        
        self.temporaryTracking = False  # Temporary tracking flag
        self.tempararyTrackingRoomsLeft = 0  # Rooms left for temporary tracking

    def update(self):
        '''Updates the player state'''
        self.keys = p.key.get_pressed()  # Get pressed keys
        self.pastPos = pk.Vec2d(*self.body.position)  # Store past position
        self.doTears()  # Handle tear shooting

        self.doBombs()  # Handle bomb usage
        
        self.doMovement()  # Handle movement
        
        self.doActiveItem()  # Handle active item usage

        self.doInvincibility()  # Handle invincibility

        self.doPickUpItemCooldown()  # Handle item pickup cooldown
        

    def doMovement(self):
        '''Handles player movement'''
        self.keys = p.key.get_pressed()
        
        self.doAccel()  # Creates acceleration vector
        self.doFriction()  # Creates friction vector and applies it to velocity
        self.doVelo()  # Updates velocity vector
    
        self.addVeloToPosition()  # Updates position based on velocity
               
    def doAccel(self):
        '''Calculates acceleration based on input'''
        self.accel = np.array([0.0,0.0])  # Reset acceleration vector
        # Take in movement inputs and change acceleration
        if self.keys[p.K_w]:
            self.accel[1]-= self.accelMag
        if self.keys[p.K_s]:
            self.accel[1]+= self.accelMag
        if self.keys[p.K_a]:
            self.accel[0]-= self.accelMag
        if self.keys[p.K_d]:
            self.accel[0]+= self.accelMag
        
        # Scale back acceleration vector if larger than the max acceleration
        inputAccelMag = npVM.absValue(self.accel)
        if self.accelMag < inputAccelMag:
            self.accel[0] = self.accelMag*self.accel[0]/inputAccelMag
            self.accel[1] = self.accelMag*self.accel[1]/inputAccelMag
    
    def doFriction(self):
        '''Applies friction to velocity'''
        friction = np.array([0.0,0.0])  # Reset friction
        veloMag = npVM.absValue(self.velo)
        if veloMag != 0:
            friction = np.multiply(-1,(npVM.scaleVector(self.velo,self.frictionMag)))
        if self.frictionMag >= veloMag:
            self.velo = np.array([0.0,0.0])
        else:
            self.velo = np.add(friction,self.velo)
        
    def doVelo(self):
        '''Updates velocity based on acceleration'''
        self.velo = np.add(self.velo,self.accel)
        veloMag = npVM.absValue(self.velo)

        # Scale velocity vector to max velocity if it's too large
        if min(self.maxSpeed,self.maxSpeedStat.getValue()) < veloMag and veloMag != 0:
            self.velo = npVM.scaleVector(self.velo,min(self.maxSpeed,self.maxSpeedStat.getValue()))

    def addVeloToPosition(self):
        '''Updates position based on velocity'''
        self.body.position += pk.Vec2d(*self.velo)


    def doActiveItem(self):
        '''Handles active item usage'''
        if self.keys[p.K_SPACE]:
            if self.activeItem != None:
                if self.activeItem.currentCharge == self.activeItem.maxCharge:
                    self.oPrinceEventHandler.addEvent(pEC.useActiveItemEvent(self.activeItem))
    
    def takeDamage(self, damageAmount =1):
        '''Handles player taking damage'''
        for j in range(damageAmount):
            for i in range(len(self.lHealth)-1,-1,-1):
                foundHeart = False
                if self.lHealth[i] != 'normal empty':
                    lost = self.lHealth.pop(i)
                    foundHeart = True
                    if lost == 'normal':  # Replace the removed heart with an empty heart
                        self.lHealth.append('normal empty')
                    if lost == 'evil':
                        self.oPrinceEventHandler.addEvent(pEC.damageAllEnemiesInRoomEvent(self.evilHeartDamage))
                    # If heart isn't normal, it is not replaced
                    break
            if not foundHeart:
                raise Exception('Found No Health', self.lHealth)

    def doTears(self):
        '''Handles tear shooting'''
        # Tear rate cooldown
        if self.currentTearIteration >0:
            self.currentTearIteration -=1
            return
        
        # If inputted directions oppose, do not spawn tear
        if not (self.keys[p.K_RIGHT] or self.keys[p.K_LEFT] or self.keys[p.K_UP] or self.keys[p.K_DOWN]):  # Makes sure an arrow is pressed
            return
        if self.keys[p.K_RIGHT] and self.keys[p.K_LEFT] or self.keys[p.K_UP] and self.keys[p.K_DOWN]: 
            return
        # self.oPrinceEventHandler.addEvent(pEC.playTearSound())
        direction = self.getBaseTearDirection()
        if self.shootingBehaviour == 'normal':
            self.shootTear(direction)
        elif self.shootingBehaviour == '4 spread':
            self.doSpreadShot(4,direction)
        elif self.shootingBehaviour == '3 spread':
            self.doSpreadShot(3,direction)
        elif self.shootingBehaviour == '2 spread':
            self.doSpreadShot(2,direction)
        elif self.shootingBehaviour == '4 middle':
            self.doMiddleShot(4,direction)
        elif self.shootingBehaviour == '3 middle':
            self.doMiddleShot(3,direction)
        elif self.shootingBehaviour == '2 middle':
            self.doMiddleShot(2,direction)
            

        self.currentTearIteration = bGI.fps/self.tearRateStat.getValue()

    def resetInvincibility(self):
        '''Resets invincibility timer'''
        self.invincibilityTimer = self.numInvincibilityFramesAfterDamaged
        self.invincible = True

    def doInvincibility(self):
        '''Handles invincibility logic'''
        if self.invincibilityTimer >0:
            self.clr = self.invincibilityClr
            self.invincibilityTimer -=1

        elif self.invincibilityTimer ==0:
            self.clr = self.nonInvincibilityClr
            self.invincible = False

    def doBombs(self):
        '''Handles bomb usage'''
        if self.keys[p.K_e] and self.currentBombIteration == 0 and self.numBombs > 0:
            self.numBombs -=1
            self.currentBombIteration = self.timeBetweenBombs
            oBomb =bC.bomb(self.screen,self.space,self.oPrinceEventHandler,self.body.position)
            self.oPrinceEventHandler.addEvent(pEC.addBombToRoomEvent(oBomb))
        if self.currentBombIteration > 0:
            self.currentBombIteration -=1

    def getBaseTearDirection(self):
        '''Returns the direction of the tear velocity before it is affected by player movement'''
        direction = np.array([0.0,0.0])

        if self.keys[p.K_RIGHT]:
            direction[0] += 1
        if self.keys[p.K_LEFT]:
            direction[0] -= 1
        if self.keys[p.K_UP]:
            direction[1] -=1
        if self.keys[p.K_DOWN]:
            direction[1] +=1
        
        return direction
    
    def initPickUpItemCooldown(self):
        '''Initializes item pickup cooldown'''
        self.canPickUpItems = False
        self.pickUpItemCoolDownIteration = self.pickUpItemCoolDown

    def doPickUpItemCooldown(self):
        '''Handles item pickup cooldown logic'''
        if not self.canPickUpItems:
            if self.pickUpItemCoolDownIteration<= 0:
                self.canPickUpItems = True
            else:
                self.pickUpItemCoolDownIteration -=1

    def addShootingBehaviour(self,behaviour:str):
        '''Adds a new shooting behavior'''
        behaviourIndex = self.shootingBehaviourHierarchy.index(behaviour)
        currentBehaviourIndex = self.shootingBehaviourHierarchy.index(self.shootingBehaviour)
        if behaviourIndex < currentBehaviourIndex:
            self.shootingBehaviour = behaviour
    
    def doSpreadShot(self,numShots,direction):
        '''Handles spread shot logic'''
        angleBetweenShots = self.shotSpread/numShots
        for i in range(numShots):
            newDirection = npVM.rotateVector(direction,angleBetweenShots*(i-numShots/2+.5))
            self.shootTear(newDirection)
    
    def doMiddleShot(self,numShots,direction):
        '''Handles middle shot logic'''
        normal = npVM.rotateVector(direction,math.pi/2)
        for i in range(numShots):
            newCenter = np.add(self.body.position,npVM.scaleVector(normal,(i-numShots/2+.5)*self.distanceBetweenMiddleShots))
            self.shootTear(direction,newCenter)
     

    def shootTear(self,direction,center = None):
        '''Shoots a tear'''
        if type(center) != np.ndarray:
            center = self.body.position
        tearVelo = npVM.scaleVector(direction,self.tearBaseSpeedStat.getValue())
        if self.tearTrackingLevel > 0:
            clr = self.trackingTearClr
        else:
            clr = self.tearClr
        oTear = tC.tear(self.screen,self.space, self.oPrinceEventHandler, center,self.tearRadiusStat.getValue(),
                        tearVelo,self.tearRangeStat.getValue(),self.tearDamageStat.getValue(),clr = clr,trackingLevel=self.tearTrackingLevel)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))
    
    def doTempEffects(self):
        '''Handles temporary effects'''
        if self.temporaryTracking:
            self.tempararyTrackingRoomsLeft -=1
            if self.tempararyTrackingRoomsLeft <= 0:
                self.temporaryTracking = False
                self.tearTrackingLevel = 0


class stat:
    '''Stat class to handle all player classes'''
    def __init__(self, base,multiplier = 1, minimum = 0,maximum = 1000000):
        '''Initializes stat'''
        self.min = minimum
        self.max = maximum
        self.base = base
        self.multiplier = multiplier
    
    def getValue(self):
        '''Gets the value of the stat'''
        return min(self.max,max(self.base*self.multiplier,self.min))

#testing code
class test:
    def __init__(self):
        self.screen, self.clock = pb.setup(bGI.screenWidth,bGI.screenHeight)
        self.player = player(self.screen,0)
    def update(self):
        self.player.update()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill((255,255,255))
        self.player.draw()
   

def main():
    oTest = test()
    pb.run(oTest)

if __name__ == '__main__':
    main()
