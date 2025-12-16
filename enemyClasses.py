'''
Enemy Classes

By: Nicholas Vardin

A program containing many enemies and bosses with many different behaviours
'''

'''Bounce back behaviour
Bounce back is present in every enemy with the attribute doesBounceBack = True

Bounce back behaviour makes it when an enemy is hit by a tear they travel in 
the direction of a tear for a certain amount of frames at a certain speed.
The duration and speed are uniquely defined in each enemy class as bounceBackSpeed and bounceBackDuration
'''

'''Death effects
If the enemy has a death effect, once it is killed its doDeathEffect method will be called.
'''

'''Enemy vision
Some enemies check if they can see the player or target.
This is done by drawing a line from each corner of the enemy to each corrisponding corner of the player.
Then using another function for each line, each tile that is crossed by that line is found.
Each object in the tiles is checked to see if it can block the enemy.

If the none of the enemies lines are blocked it can see the player, if else, it cannot,

This can be seen in the super spider class and others
'''

'''Check if in ground obstacle
Some enemies may need to check if they are inside a hard object before the collision handler fixes their position

This is done by getting all the tiles the enemy is in (either fully or slightly), and checking if it is overlapping 
with any objects with the attribute isEnemyGroundObstacle = True. 
'''

'''V Field tracking
The vector field points towards the player (or pretty close) at every tile in the room
Each enemy that uses a vector field to track the player follows a couple of steps.

- obtain vector field from current room object that is calculated every frame.
- Get all tiles the enemy is in and get the vector in the tile
- add all the vectors in each tile and use that as the direction vector

Example code can be seen in the super spider class doMove() method
'''

from perlin_noise import PerlinNoise
import basicFunctionsAndClasses as bFC
import numpy as np
import math
import npVectorMath as npVM
import random
import pymunk as pk
import princeEventClasses as pEC
import tearClasses as tC
import basicGameInfo as bGI
import bombClasses as bC
import pygame as p

#load images here to avoid them repeatedly loading every time an enemy is created
teenyFlyImage1 = p.image.load(r'images\teenyFly1.png')
teenyFlyImage2 = p.image.load(r'images\teenyFly2.png')
trackerFlyImage1 = p.image.load(r'images\trackerFly1.png')
trackerFlyImage2 = p.image.load(r'images\trackerFly2.png')
spiderImage1=p.image.load(r'images\spider1.png')
spiderImage2 = p.image.load(r'images\spider2.png')
superSpiderImage1=p.image.load(r'images\superSpider1.png')
superSpiderImage2 = p.image.load(r'images\superSpider2.png')
smallHeadImage = p.image.load(r'images\smallHead.png')
bigHeadImage = p.image.load(r'images\bigHead.png')
shooterFlyImage1 = p.image.load(r'images\shooterFly1.png')
shooterFlyImage2 = p.image.load(r'images\shooterFly2.png')
shootyMcFlyImage1 = p.image.load(r'images\shootyMcFly1.png')
shootyMcFlyImage2 = p.image.load(r'images\shootyMcFly2.png')
vShooterFlyImage1 = p.image.load(r'images\vShooterFly1.png')
vShooterFlyImage2 = p.image.load(r'images\vShooterFly2.png')
boomFlyImage1 = p.image.load(r'images\boomFly1.png')
boomFlyImage2 = p.image.load(r'images\boomFly2.png')
sadBoomFlyImage1 = p.image.load(r'images\sadBoomFly1.png')
sadBoomFlyImage2 = p.image.load(r'images\sadBoomFly2.png')
chargerWormImageSide = p.image.load(r'images\chargerWormSide.png')
chargerWormImageTop = p.image.load(r'images\chargerWormTop.png')
schmooImageChill = p.image.load(r'images\schmooChill.png')
schmooImageCharge = p.image.load(r'images\schmooCharge.png')
schmeerImage = p.image.load(r'images\schmeer.png')
schmeerOfSchmooImageChill = p.image.load(r'images\schmeerOfSchmooChill.png')
schmeerOfSchmooImageShoot = p.image.load(r'images\schmeerOfSchmooShoot.png')
schmeerestOfSchmooImageChill = p.image.load(r'images\schmeerestOfSchmooChill.png')
schmeerestOfSchmooImageCharge = p.image.load(r'images\schmeerestOfSchmooCharge.png')
schmeerestOfSchmooImageShoot = p.image.load(r'images\schmeerestOfSchmooShoot.png')
gooberImage1 = p.image.load(r'images\goober1.png')
gooberImage2 = p.image.load(r'images\goober2.png')
speedyGooberImage1 = p.image.load(r'images\speedyGoober1.png')
speedyGooberImage2 = p.image.load(r'images\speedyGoober2.png')
explodeyGooberImage1 = p.image.load(r'images\explodeyGoober1.png')
explodeyGooberImage2 = p.image.load(r'images\explodeyGoober2.png')
shootyGooberImage1 = p.image.load(r'images\shootyGoober1.png')
shootyGooberImage2 = p.image.load(r'images\shootyGoober2.png')
regenGooberImage1 = p.image.load(r'images\regenGoober1.png')
regenGooberImage2= p.image.load(r'images\regenGoober2.png')
regenBoogerImage = p.image.load(r'images\regenBooger.png')
multipliterrorImage1 = p.image.load(r'images\multipliterror1.png')
multipliterrorImage2 = p.image.load(r'images\multipliterror2.png')
multipliterrorBoogerImage = p.image.load(r'images\multipliterrorBooger.png')
lordOfTheFliesImage1 = p.image.load(r'images\lordOfTheFlies1.png')
lordOfTheFliesImage2 = p.image.load(r'images\lordOfTheFlies2.png')
kingOfTheFliesImage1 = p.image.load(r'images\kingOfTheFlies1.png')
kingOfTheFliesImage2 = p.image.load(r'images\kingOfTheFlies2.png')
leBroImage = p.image.load(r'images\leBro.jpg')
leBroImageAngry = p.image.load(r'images\leBroAngry.png')
leBombBroImage = p.image.load(r'images\leBombBro.png')
leBombBroImageAngry = p.image.load(r'images\leBombBroAngry.png')
miniJackBlackImage = p.image.load(r'images\miniJackBlack.png')
jackBlackImage = p.image.load(r'images\jackBlack.jpg')
longDividerImage = p.image.load(r'images\longDivider.png')
shortDividerImage = p.image.load(r'images\shortDivider.png')
miniDividerImage = p.image.load(r'images\miniDivider.png')
mrKrabsImage = p.image.load(r'images\mrKrabs.png')
chemistryImage = p.image.load(r'images\chemistry.png') 




class enemy(bFC.physicsRect):
    '''Parent enemy class that initializes unique features of each enemy'''
    def __init__(self, screen, space, oPrinceEventHandler, clr, center, width, height,health,damage = 1,
                 flying = False,isBoss = False,needsTarget = False,doesBounceBack = True,hasDeathEffect = False, 
                 spawnsEnemiesOnDeath = False,needsLayout = False,bouncesOffObstacles = False,needsGroundVField = False,
                 recievesExplosionDamage = True,recievesTearDamage = True,specialEffectOnPlayerContact = False):
        super().__init__(screen, space, clr, center, width, height, collisionType = 14, bodyType=pk.Body.KINEMATIC)
        '''Instantiates attributes'''
        self.oPrinceEventHandler = oPrinceEventHandler
        self.needsTarget = needsTarget
        self.startHealth = health
        self.health = health
        self.damage = damage
        self.flying = flying
        self.isBoss = isBoss
        self.doesBounceBack = doesBounceBack
        self.hasDeathEffect = hasDeathEffect
        self.spawnsEnemiesOnDeath = spawnsEnemiesOnDeath
        self.needsLayout = needsLayout
        self.bouncesOffObstacles = bouncesOffObstacles
        self.needsGroundVField = needsGroundVField
        self.recievesExplosionDamage = recievesExplosionDamage
        self.recievesTearDamage = recievesTearDamage
        self.specialEffectOnPlayerContact = specialEffectOnPlayerContact
        
        self.isDead = False #variable to keep track if an enemy is dead or not to avoid death effects happenign twice
        

class teenyFly(enemy):
    '''The Easiest enemy in the game, moves randomly according to a noise pattern'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width = bGI.basicTileWidth*.5, height= bGI.basicTileHeight*.5, health = 5, damage=1, flying=False, isBoss=False, needsTarget=False, doesBounceBack=True, hasDeathEffect=False, spawnsEnemiesOnDeath=False, needsLayout=False, bouncesOffObstacles=False, needsGroundVField=False):
        clr =(20,20,20)
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,flying = True)
        '''Initializes object'''
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        self.state = 'move'
        
        self.regularSpeed = 1.5
        self.noise = PerlinNoise(octaves=1000,seed = random.randint(0,100000))
        self.noiseIterations = 0
        
        self.pastPos = pk.Vec2d(*self.body.position)
        self.framesTilChangeImage = 4
        self.imageToDrawCount = 0
        self.image = teenyFlyImage1
        
    def update(self):
        '''Updates fly every frame'''
        self.pastPos = pk.Vec2d(*self.body.position) #saves past pos for collision checks
        if self.state == 'move':
            self.doRegularMovement()
        elif self.state == 'bounce back':
            self.doBounceBack()
        
    def initRegularState(self):
        '''Initializes regular state'''
        self.state = 'move'
        self.doesBounceBack = True
        self.velo = np.array([0.0,0.0])
    
    def doRegularMovement(self):
        '''Moves according to perlin noise'''
        direction = [self.noise(self.noiseIterations),self.noise(self.noiseIterations+1000.00907)] #obtain random direction
        if direction != [0,0]: #makes sure direction isnt (0,0) which would result in an error
            self.velo = npVM.scaleVector(direction,self.regularSpeed) #scales direction to speed to create velo vector
        else:
            self.velo = np.array([0.0,0.0])
        self.body.position += pk.Vec2d(*self.velo) #add velo to position
        self.noiseIterations +=random.uniform(.000005,.00001) #update noise iteration randomly
        
    def initBounceBack(self,direction):
        '''Initializes bounce back behaviour'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.body.position += pk.Vec2d(*self.velo) #add velo vector to position vector
        #when bounce back is done go back to regular movement
        if self.bounceBackCount < self.bounceBackDuration: 
            self.bounceBackCount +=1
        else:
            self.initRegularState()
    
    def draw(self):
        '''Draws self to screen'''
        self.imageToDrawCount +=1
        if self.imageToDrawCount ==self.framesTilChangeImage: #switch images when count reaches the threshold
            if self.image == teenyFlyImage1:
                self.image = teenyFlyImage2
            else:
                self.image = teenyFlyImage1
            self.imageToDrawCount = 0 #reset count
        
        #get image position and draw image
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)  

class trackerFly(enemy):
    '''A fly that flies and goes towards the player at a fixed speed'''
    def __init__(self, screen, space, oPrinceEventHandler,center, width = 30, height = 30, health = 9, damage=1):
        clr = (100,200,120)
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, flying = True, needsTarget = True)
        '''Initializes object'''
        self.speed = 2
        self.velo = np.array([0.0,0.0])
        self.state = 'attack'

        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        self.target = None

        self.image = trackerFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
        
    def update(self,target):
        '''Updates the fly every frame'''
        self.pastPos = pk.Vec2d(*self.body.position) #save past pos for collision checks
        if self.state =='attack':
            self.doAttack(target)
        elif self.state == 'bounce back':
            self.doBounceBack()

    def initBounceBack(self,direction:np.ndarray):
        '''Initializes bounc back state'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed) #obtains new velo
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.body.position += pk.Vec2d(*self.velo) #adds velo to position
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount +=1
        else:
            self.state = 'attack'
        
    def doAttack(self,target):
        '''Does attack behaviour, travelling towards target'''
        targetCenter = target.body.position
        
        distance = math.dist(bFC.npArrayIntoTuple(self.body.position),bFC.npArrayIntoTuple(targetCenter))
        if distance <= self.speed: #if super close, change the position to target position
            
            self.body.position = targetCenter
        else: #set velo and add it to position vector
            self.velo = npVM.scaleVector(np.subtract(targetCenter,np.array(self.body.position)),self.speed)
            self.body.position += pk.Vec2d(*self.velo)

    def draw(self):
        '''Draws self, same as the teeny fly'''
        self.framesTilChangeImageCount -=1
        if self.framesTilChangeImageCount <=0:
            if self.image == trackerFlyImage1:
                self.image = trackerFlyImage2
            else:
                self.image = trackerFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)  
    

class spider(enemy):
    '''Enemy that travels in random direction and randomly changes speed'''
    def __init__(self, screen, space,oPrinceEventHandler, center, width = 30, height = 20, health = 7, damage=1):
        clr = (10,10,50)
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage)
        '''Initializes variables'''
        self.speed = 3
        self.velo = np.array([0.0,0.0])
        self.state = 'attack'
        
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        self.attackState = 'getting direction'
        self.moveCount = 0
        self.moveDurationBounds = (10,20) #frame bounds used for randomly deciding how long the spider should move for
        self.moveDuration = 0
        self.framesTilImageChange = 4
        self.framesTilImageChangeCount = self.framesTilImageChange
        
        self.waitCount = 0
        self.waitDurationUpperBounds = 70
        self.waitDurationLowerBounds = 40
        self.waitImage = spiderImage1

        self.image = self.waitImage
        
    def update(self):
        self.pastPos = pk.Vec2d(*self.body.position)
        if self.state =='attack':
            self.doAttack()
        elif self.state == 'bounce back':
            self.doBounceBack()

    def initBounceBack(self,direction:np.ndarray):
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.addVeloToCenter()
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount +=1
        else:
            self.state = 'attack'

    def doAttack(self):
        '''Does attack and moves randomly at random periods'''
        if self.attackState == 'getting direction':
            direction = np.array([random.uniform(-1,1),random.uniform(-1,1)])
            self.velo = npVM.scaleVector(direction,self.speed)
            self.moveCount = random.randint(*self.moveDurationBounds)
            self.attackState = 'move'
            
        elif self.attackState == 'move':
            self.moveCount -=1
            if self.moveCount == 0:
                self.attackState = 'wait'
                self.waitCount = random.randint(self.waitDurationLowerBounds,self.waitDurationUpperBounds)
                self.velo = np.array([0,0])
                
        elif self.attackState == 'wait':
            self.waitCount -=1
            if self.waitCount == 0:
                self.attackState = 'getting direction'
                
        self.addVeloToCenter()
            
    def addVeloToCenter(self):
        self.body.position += pk.Vec2d(*self.velo)

    def draw(self):
        '''Draws self to screen'''
        if self.state == 'attack' and self.attackState == 'move': #switches images every 4 frames if the spider is moving
            self.framesTilImageChangeCount -=1
            if self.framesTilImageChangeCount ==0:
                self.framesTilImageChangeCount = self.framesTilImageChange
                if self.image == spiderImage1:
                    self.image = spiderImage2
                else:
                    self.image = spiderImage1
        else:
            self.image = self.waitImage
        
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos) #draws the current image
                

class superSpider(enemy):
    '''super spider enemy that charges at the player in random periods, splits into 2 spiders when killed'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width = bGI.basicTileWidth*.9, height = bGI.basicTileHeight*.7, health = 12, damage=1):
        '''initializes variables'''
        
        clr = (10,10,50)
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         hasDeathEffect=True,spawnsEnemiesOnDeath=True,needsGroundVField=True,needsTarget=True,needsLayout=True)
        
        self.state = 'move'

        self.chargeSpeed = 4
        self.chargeDurationBounds = (int(bGI.fps*.6),int(bGI.fps*.8))# bounds for how lng the spider should charge at the player for
        self.chargeIteration =0 

        self.chillSpeed = 1
        self.chillDurationBounds = (int(bGI.fps*.6),int(bGI.fps*.8)) #bounds for how long the spider should chill before charging again
        self.chillIteration = 0

        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        self.framesTilImageChange = 4
        self.framesTilImageChangeCount = self.framesTilImageChange
        self.waitImage = superSpiderImage1
        self.image = self.waitImage

    def update(self,target,layout,vField):
        '''Updates the spider each frame'''
        self.pastPos = pk.Vec2d(*self.body.position) #saves the past pos for collision checks
        if self.state == 'move':
            self.doMove(target,layout,vField)
        elif self.state == 'bounce back':
            self.doBounceBack()
        elif self.state == 'charge':
            self.doCharge(layout)

    def initMove(self):
        '''Initializes move behaviour'''
        self.state = 'move'
        self.chillIteration = random.randint(*self.chillDurationBounds)

    def doMove(self,target,layout,vField):
        '''Does tracking behaviour using a vfield obtained from the current room object and charges at random periods'''
        
        #how enemies track the player using vector fields can be found at the top

        rowCols = [] #get all tiles enemy is in
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0]-self.width/2,self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0]+self.width/2,self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0],self.body.position[1]-self.height/2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0],self.body.position[1]+self.height/2])))
        direction = np.array([0.0,0.0])
        for rowCol in rowCols:  #get all vector values 
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: continue
            if rowCol[0] < 0 or rowCol[0] >= len(vField): continue
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): continue
            direction = np.add(direction,vField[rowCol[0]][rowCol[1]])
        if direction[0] != 0 or direction[1] != 0:
            self.velo = npVM.scaleVector(direction,self.chillSpeed) #scale vector to speed
            self.body.position += pk.Vec2d(*self.velo)

        if self.chillIteration <= 0: #if cool down is done and no ground obstacles are in the way init charge behaviour
            if self.checkIfCanSeeTarget(target,layout):
                self.initCharge(target)
        else:
            self.chillIteration -=1

    def initCharge(self,target):
        '''Initializes charge behaviour'''
        self.state = 'charge'
        targetCenter = target.body.position
        targetDirection = targetCenter -self.body.position
        self.velo = npVM.scaleVector(targetDirection,self.chargeSpeed) #sets new velo to be towards player at a faster speed
        self.chargeIteration = random.randint(*self.chargeDurationBounds) #do charge for random amount of time

    def doCharge(self,layout):
        '''does charge behaviour'''
        self.body.position += pk.Vec2d(*self.velo)
        self.chargeIteration -=1
        if self.chargeIteration<= 0: #if charge is down or collide with ground object, initialize move behaviour
            self.initMove()
        elif self.checkIfInGroundObstacle(layout):
            self.initMove()

    def initBounceBack(self,direction:np.ndarray):
        '''Initializes bounce back behaviour'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount +=1
        else:
            self.initMove()

    def doDeathEffect(self):
        '''does death effect spawning in to regular spiders'''
        oSpiderLeft = spider(self.screen,self.space,self.oPrinceEventHandler,self.body.position)
        oSpiderRight = spider(self.screen,self.space,self.oPrinceEventHandler,self.body.position)
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oSpiderLeft))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oSpiderRight))

    def checkIfCanSeeTarget(self,target,layout):
        '''Checks if ground object is inbetween enemy and player'''
        selfLPoints = self.getLPoints()
        targetLPoints = target.getLPoints()
        for i in range(4):
            interectedRowCols =  bFC.getLineIntersectRowColQuadrants(selfLPoints[i],targetLPoints[i])
            for rowCol in interectedRowCols:
                for oTile in layout[rowCol[0]][rowCol[1]]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.linePolygonCollision(selfLPoints[i],targetLPoints[i],oTile.getLPoints()): return False
                        elif oTile.geometry == 'circle':
                            if bFC.lineCircleCollision(selfLPoints[i],targetLPoints[i],oTile.body.position,oTile.radius):return False
        return True
    
    def checkIfInGroundObstacle(self,layout):
        '''Checks if super spider is in ground obstacle, returns true or false'''
        yTile,xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        for col in range(yTile-1,yTile+2): #get all tiles super spider is in
            if col < 0 or col >= len(layout): continue
            for row in range(xTile-1,xTile+2):
                if row < 0 or row >= len(layout[0]): continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle: #check if they are ground obstacle
                        if oTile.geometry == 'rect':#check if colliding with any
                            if bFC.polygonPolygonCollision(self.getLPoints(),oTile.getLPoints()): return True
                        elif oTile.geometry == 'circle':
                            if bFC.polygonCircleCollision(self.getLPoints(),oTile.body.position,oTile.radius): return True
        return False
    
    def draw(self):
        '''Draws self to screen, follows the same draw behaviour as spider'''
        if self.state != 'bounce back':
            self.framesTilImageChangeCount -=1
            if self.framesTilImageChangeCount ==0:
                self.framesTilImageChangeCount = self.framesTilImageChange
                if self.image == superSpiderImage1:
                    self.image = superSpiderImage2
                else:
                    self.image = superSpiderImage1
        else:
            self.image = self.waitImage
        
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)  

class shooterFly(enemy):
    '''Fly enemy that shoots at the player'''
    def __init__(self, screen, space,oPrinceEventHandler,center, width = 30, height = 30, health = 9, damage=1):
        '''Initializes attributes'''
        
        clr = (0,120,100)

        super().__init__(screen, space,oPrinceEventHandler,  clr, center, width, height, health, damage, 
                         flying = True, needsTarget= True, needsLayout= True)
        
        self.state = 'attack'
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        self.velo = np.array([0.0,0.0])

        self.framesBetweenShots = 45
        self.currentShotIteration = self.framesBetweenShots
        self.movementSpeed = .6

        self.maxTargetDistanceToShoot = 8*bGI.basicTileWidth
        self.maxTargetDistanceToMove = 10 *bGI.basicTileWidth

        self.tearSpeed = 4
        self.tearRange = 7
        self.tearRadius =10
        
        self.image = shooterFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
        

    def update(self,target,layout):
        '''updates the fly every frame'''
        self.pastPos = pk.Vec2d(*self.body.position)
        targetPos = target.body.position
        if self.state == 'bounce back':
            self.doBounceBack()
        elif self.state == 'attack':
            self.doAttackMovement(targetPos)
        self.doShooting(targetPos)
        
    def doAttackMovement(self,targetPos):
        '''Does attack movement behaviour'''
        targetDist = math.dist(targetPos,self.body.position)
        if targetDist <= self.maxTargetDistanceToMove: #only move when within distance threshold to player
            targetDirection = targetPos -self.body.position
            velo = npVM.scaleVector(targetDirection,self.movementSpeed)
            self.body.position += pk.Vec2d(*velo)

    def doShooting(self,targetPos):
        '''Does shooting behaviour'''
        targetDist = math.dist(targetPos,self.body.position)
        if self.currentShotIteration >0:
            self.currentShotIteration -=1
        elif targetDist <= self.maxTargetDistanceToShoot: #only shoot when within distance threshold to player
            self.currentShotIteration = self.framesBetweenShots
            self.shootTear(targetPos)

    def shootTear(self,targetPos):
        '''Shoots tear towards target'''
        targetDirection = targetPos -self.body.position
        tearVelo = pk.Vec2d(*npVM.scaleVector(targetDirection,self.tearSpeed)) #obtains tearVelo vector by scaling direction vector by tear speed
        oTear = tC.enemyTear(self.screen,self.space,self.oPrinceEventHandler,self.body.position,self.tearRadius,tearVelo,self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))
        

    def initBounceBack(self,direction:np.ndarray):
        '''Initializes bounce back behaviour'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount +=1
        else:
            self.state = 'attack'
    
    def draw(self): 
        '''draws self to frame in the same way as teeny fly'''
        self.framesTilChangeImageCount -=1
        if self.framesTilChangeImageCount <=0:
            if self.image == shooterFlyImage1:
                self.image = shooterFlyImage2
            else:
                self.image = shooterFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)  
            
            
class shootyMcFly(enemy):
    '''A fly that shoots the plan more frequently and with faster tears than the shooter fly class'''
    def __init__(self, screen, space,oPrinceEventHandler,center, width = 25, height = 25, health = 13, damage=1):
        '''Initializes Attributes'''
        clr = (0,0,255)  # Cool blue color
        super().__init__(screen, space,oPrinceEventHandler,  clr, center, width, height, health, damage, 
                         flying = True, needsTarget= True)
        
        self.state = 'attack'
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        self.velo = np.array([0.0,0.0])

        self.framesBetweenShots = bGI.fps*.2
        self.currentShotIteration = self.framesBetweenShots
        self.movementSpeed = .6

        self.maxTargetDistanceToShoot = 10*bGI.basicTileWidth
        self.maxTargetDistanceToMove = 12 *bGI.basicTileWidth

        self.tearSpeed = 8
        self.tearRange = 9
        self.tearRadius =8
        
        self.image = shooterFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage


    def update(self,target):
        '''Updates the fly every frame'''
        self.pastPos = pk.Vec2d(*self.body.position) 
        targetPos = target.body.position
        if self.state == 'bounce back':
            self.doBounceBack()
        elif self.state == 'attack':
            self.doAttackMovement(targetPos)
        self.doShooting(targetPos)
        
    def doAttackMovement(self,targetPos):
        '''Does attack behaviour'''
        targetDist = math.dist(targetPos,self.body.position)
        if targetDist <= self.maxTargetDistanceToMove:
            targetDirection = targetPos -self.body.position
            self.velo = npVM.scaleVector(targetDirection,self.movementSpeed)
            self.body.position += pk.Vec2d(*self.velo)

    def doShooting(self,targetPos):
        '''Does shooting behaviour'''
        targetDist = math.dist(targetPos,self.body.position)
        if self.currentShotIteration >0:
            self.currentShotIteration -=1
        elif targetDist <= self.maxTargetDistanceToShoot:
            self.currentShotIteration = self.framesBetweenShots
            self.shootTear(targetPos)

    def shootTear(self,targetPos):
        '''Shoots tear towards target'''
        targetDirection = targetPos -self.body.position
        tearVelo = pk.Vec2d(*npVM.scaleVector(targetDirection,self.tearSpeed))
        oTear = tC.enemyTear(self.screen,self.space,self.oPrinceEventHandler,self.body.position,self.tearRadius,tearVelo,self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))
        

    def initBounceBack(self,direction:np.ndarray):
        '''Initializes bounce back behaviour'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction,self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Does bounce back behaviour'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount +=1
        else:
            self.state = 'attack'

    def draw(self): 
        '''Draws self to screen in the same way as teeny fly'''
        self.framesTilChangeImageCount -=1
        if self.framesTilChangeImageCount <=0:
            if self.image == shootyMcFlyImage1:
                self.image = shootyMcFlyImage2
            else:
                self.image = shootyMcFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)  
            
class vShooterFly(enemy):
    '''A fly enemy that shoots tears in a V-shaped pattern towards the player'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=30, height=30, health=9, damage=1):
        '''Initializes attributes for the vShooterFly enemy'''
        clr = (0, 120, 100)  # Greenish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         flying=True, needsTarget=True)
        
        # State and movement attributes
        self.state = 'move'
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        # Shooting attributes
        self.framesBetweenShots = bGI.fps * 0.9  # Time between shots
        self.currentShotIteration = self.framesBetweenShots
        self.movementSpeed = 0.2

        # Shooting range and tear properties
        self.maxTargetDistanceToShoot = 8 * bGI.basicTileWidth
        self.maxTargetDistanceToMove = 10 * bGI.basicTileWidth
        self.tearSpeed = 3
        self.tearRange = 8
        self.tearRadius = 10
        self.angleOfShotsFromTargetDirection = math.pi / 7  # Angle for V-shaped shots

        # Movement noise for random movement
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0

        # Image attributes
        self.image = shooterFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage

    def update(self, target):
        '''Updates the vShooterFly every frame'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save past position for collision checks
        targetPos = target.body.position
        if self.state == 'bounce back':
            self.doBounceBack()
        elif self.state == 'move':
            self.doRegularMovement()
        self.doShooting(targetPos)

    def doRegularMovement(self):
        '''Moves randomly using Perlin noise'''
        self.velo = [2 * self.noise(self.noiseIterations), 2 * self.noise(self.noiseIterations + 10000)]
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        self.noiseIterations += 0.00001  # Increment noise iterations for smooth movement

    def doShooting(self, targetPos):
        '''Handles shooting behavior'''
        targetDist = math.dist(targetPos, self.body.position)
        if self.currentShotIteration > 0:
            self.currentShotIteration -= 1
        elif targetDist <= self.maxTargetDistanceToShoot:  # Only shoot if within range
            self.currentShotIteration = self.framesBetweenShots
            self.shootTears(targetPos)

    def shootTears(self, targetPos):
        '''Shoots tears in a V-shaped pattern towards the target'''
        targetDirection = targetPos - self.body.position
        tearVelo = pk.Vec2d(*npVM.scaleVector(targetDirection, self.tearSpeed))  # Main tear velocity
        tearVeloCW = npVM.rotateVector(tearVelo, self.angleOfShotsFromTargetDirection)  # Clockwise tear
        tearVeloCCW = npVM.rotateVector(tearVelo, -self.angleOfShotsFromTargetDirection)  # Counter-clockwise tear

        # Spawn the tears
        oTearCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCW))
        oTearCCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCCW))

    def initBounceBack(self, direction: np.ndarray):
        '''Initializes bounce back behavior'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Handles bounce back behavior'''
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount += 1
        else:
            self.state = 'move'  # Return to move state after bounce back

    def draw(self):
        '''Draws the vShooterFly to the screen'''
        self.framesTilChangeImageCount -= 1
        if self.framesTilChangeImageCount <= 0:  # Switch images for animation
            if self.image == vShooterFlyImage1:
                self.image = vShooterFlyImage2
            else:
                self.image = vShooterFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        # Calculate draw position and draw the image
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)
                   
    

class boomFly(enemy):
    '''A fly that flies in a straight line and explodes on contact with the player'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=30, height=30, health=10, damage=1, speed=2, clr=(50, 30, 30)):
        # Initialize the parent enemy class with specific attributes
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         flying=True, doesBounceBack=False, hasDeathEffect=True, bouncesOffObstacles=True)
        
        # Store the previous position for collision checks
        self.pastPos = pk.Vec2d(*self.body.position)
        # Set the initial movement direction and velocity
        self.direction = pk.Vec2d(1, 1)
        self.velo = npVM.scaleVector(self.direction, speed)
        
        # Set the initial image and animation properties
        self.image = boomFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage

    def update(self):
        '''Update the fly's position every frame'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position
        self.doMovement()  # Perform movement logic
    
    def doMovement(self):
        '''Move the fly in a straight line'''
        self.body.position += pk.Vec2d(*self.velo)

    def doDeathEffect(self):
        '''Create an explosion effect when the fly dies'''
        oExplosion = bC.explosion(self.screen, self.space, self.oPrinceEventHandler, self.body.position)
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))
        
    def draw(self): 
        '''Draw the fly on the screen with animation'''
        self.framesTilChangeImageCount -= 1
        # Switch images for animation every few frames
        if self.framesTilChangeImageCount <= 0:
            if self.image == boomFlyImage1:
                self.image = boomFlyImage2
            else:
                self.image = boomFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
        # Calculate the draw position and render the image
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  

class sadBoomFly(boomFly):
    '''A variant of boomFly that shoots tears in all directions upon death'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=30, height=30, health=10, damage=1, speed=2):
        # Initialize the parent boomFly class with a different color
        clr = (40, 40, 70)
        super().__init__(screen, space, oPrinceEventHandler, center, width, height, health, damage, speed, clr=clr)

        # Set attributes for the tears shot upon death
        self.tearSpeed = 3
        self.tearRange = 8
        self.tearRadius = 10
        self.numTearsOnDeath = 8
        self.angleBetweenShots = 2 * math.pi / self.numTearsOnDeath  # Angle between each tear

    def doDeathEffect(self):
        '''Create an explosion and shoot tears in all directions when the fly dies'''
        # Create an explosion with specific damage values
        oExplosion = bC.explosion(self.screen, self.space, self.oPrinceEventHandler, self.body.position, enemyDamage=0, playerDamage=1)
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))
        
        # Initialize the direction for the first tear
        direction = [1, 0]
        for i in range(self.numTearsOnDeath):
            # Calculate the velocity for the tear
            tearVelo = npVM.scaleVector(direction, self.tearSpeed)
            # Create and spawn the tear
            oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVelo, self.tearRange, damage=self.damage)
            self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))
            # Rotate the direction for the next tear
            direction = npVM.rotateVector(direction, self.angleBetweenShots)
    
    def draw(self): 
        '''draws self to frame in the same way as teeny fly'''
        self.framesTilChangeImageCount -=1
        if self.framesTilChangeImageCount <=0:
            if self.image == sadBoomFlyImage1:
                self.image = sadBoomFlyImage2
            else:
                self.image = sadBoomFlyImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)
        

class chargerWorm(enemy):
    '''An enemy that moves in a regular pattern and charges towards the player when the path is clear.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=30, height=15, health=12, damage=1):
        clr = (223, 179, 133)  # Worm-like color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, needsTarget=True, needsLayout=True)

        # Attributes for regular movement
        self.changeDirectionUpperBounds = int(bGI.fps * 2)
        self.changeDirectionLowerBounds = int(bGI.fps * 0.7)
        self.changeDirectionCount = 0
        self.possibleDirections = [pk.Vec2d(1, 0), pk.Vec2d(-1, 0), pk.Vec2d(0, 1), pk.Vec2d(0, -1)]
        
        self.regularSpeed = 0.7
        self.chargeSpeed = 4
        
        self.initRegularState()
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        self.pastPos = pk.Vec2d(*self.body.position)
    
    def update(self, target, layout):
        '''Updates the worm every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)
        if self.state == 'regular':
            self.doRegularMovement(target, layout)
            self.changeWidthAndHeightBasedOnVeloDirection()
        elif self.state == 'charge':
            self.doCharge(layout)
            self.changeWidthAndHeightBasedOnVeloDirection()
        elif self.state == 'bounce back':
            self.doBounceBack()
    
    def initRegularState(self):
        '''Initializes the regular movement state.'''
        self.state = 'regular'
        self.doesBounceBack = True
        direction = random.choice(self.possibleDirections)
        self.velo = npVM.scaleVector(direction, self.regularSpeed)
        self.changeDirectionCount = random.randint(self.changeDirectionLowerBounds, self.changeDirectionUpperBounds)
    
    def doRegularMovement(self, target, layout):
        '''Handles regular movement.'''
        self.body.position += pk.Vec2d(*self.velo)
        self.changeDirectionCount -= 1
        
        if self.getPathToTargetIsClear(target, layout):
            self.initCharge(target)
        elif self.changeDirectionCount <= 0:
            self.initRegularState()
    
    def getPathToTargetIsClear(self, target, layout):
        '''Checks if the path to the target is clear.'''
        targetCenter = target.body.position
        xOverlap, yOverlap = bFC.getXAndYOverlapsBetweenRects(target.getLPoints(), self.getLPoints())
        if xOverlap == yOverlap: 
            return False
        
        if xOverlap:
            # Check for obstacles in the vertical path
            if self.height < self.width:
                checkWidth = self.height
            else:
                checkWidth = self.width
            leftLine = np.array([[self.body.position[0] - checkWidth / 2, self.body.position[1]],
                                 [self.body.position[0] - checkWidth / 2, targetCenter[1]]])
            rightLine = np.array([[self.body.position[0] + checkWidth / 2, self.body.position[1]],
                                  [self.body.position[0] + checkWidth / 2, targetCenter[1]]])
            startTiles = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
            yTargetTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(targetCenter)[0]
            for col in range(startTiles[0], yTargetTile):
                for oTile in layout[col][startTiles[1]]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.linePolygonCollision(leftLine[0], leftLine[1], oTile.getLPoints()): 
                                return False
                            elif bFC.linePolygonCollision(rightLine[0], rightLine[1], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':
                            if bFC.lineCircleCollision(leftLine[0], leftLine[1], oTile.body.position, oTile.radius): 
                                return False
                            elif bFC.lineCircleCollision(rightLine[0], rightLine[1], oTile.body.position, oTile.radius): 
                                return False
            
        elif yOverlap:
            # Check for obstacles in the horizontal path
            if self.width < self.height:
                checkHeight = self.width
            else:
                checkHeight = self.height
            topLine = np.array([[self.body.position[0], self.body.position[1] - checkHeight / 2],
                                [targetCenter[0], self.body.position[1] - checkHeight / 2]])
            bottomLine = np.array([[self.body.position[0], self.body.position[1] + checkHeight / 2],
                                   [targetCenter[0], self.body.position[1] + checkHeight / 2]])
            startTiles = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
            xTargetTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(targetCenter)[1]
            for row in range(startTiles[1], xTargetTile):
                for oTile in layout[startTiles[0]][row]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.linePolygonCollision(topLine[0], topLine[1], oTile.getLPoints()): 
                                return False
                            elif bFC.linePolygonCollision(bottomLine[0], bottomLine[1], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':
                            if bFC.lineCircleCollision(topLine[0], topLine[1], oTile.body.position, oTile.radius): 
                                return False
                            elif bFC.lineCircleCollision(bottomLine[0], bottomLine[1], oTile.body.position, oTile.radius): 
                                return False
        
        return True
    
    def initCharge(self, target):
        '''Initializes the charge state.'''
        self.state = 'charge'
        self.doesBounceBack = False
        xOverlap, yOverlap = bFC.getXAndYOverlapsBetweenRects(target.getLPoints(), self.getLPoints())
        if xOverlap:
            if target.body.position[1] > self.body.position[1]: 
                yVelo = 1
            else: 
                yVelo = -1
            self.velo = npVM.scaleVector(np.array([0.0, yVelo]), self.chargeSpeed)
        elif yOverlap:
            if target.body.position[0] > self.body.position[0]: 
                xVelo = 1
            else: 
                xVelo = -1 
            self.velo = npVM.scaleVector(np.array([xVelo, 0.0]), self.chargeSpeed)
    
    def doCharge(self, layout):
        '''Handles charge movement.'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.checkIfInGroundObstacle(layout):
            self.initRegularState()
    
    def checkIfInGroundObstacle(self, layout):
        '''Checks if the worm is in a ground obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        for col in range(yTile - 1, yTile + 2):
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 1, xTile + 2):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False
    
    def initBounceBack(self, direction: np.ndarray):
        '''Initializes the bounce back state.'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Handles bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount += 1
        else:
            self.initRegularState()
    
    def changeWidthAndHeightBasedOnVeloDirection(self):
        '''Changes the width and height of the worm based on its movement direction.'''
        if self.velo[0] != 0 and self.velo[1] == 0:
            self.width = 30
            self.height = 15
        elif self.velo[1] != 0 and self.velo[0] == 0:
            self.width = 15
            self.height = 30

    def draw(self):
        '''Draws the worm to the screen.'''
        if abs(self.velo[0])>=abs(self.velo[1]):
            self.image = chargerWormImageSide
            if self.velo[0] <0:
                self.image = p.transform.flip(self.image,True,False)
        else:
            self.image = chargerWormImageTop
            if self.velo[1] >0:
                self.image = p.transform.flip(self.image,False,True)
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position


class schmoo(enemy):
    '''A medium-sized enemy that moves randomly and charges at the player when it has a clear line of sight.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.9, height=bGI.basicTileHeight*.9, health=13, damage=1):
        clr = (121, 81, 35)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         spawnsEnemiesOnDeath=True, needsTarget=True, needsLayout=True, hasDeathEffect=True)
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        # Charge attributes
        self.chargeDuration = bGI.fps * 1.5
        self.chargeSpeed = 5
        
        # Regular movement attributes
        self.regularSpeed = 1
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0
        
        # Debugging attribute for drawing sight lines
        self.drawSightLines = False
        
        # Store past position for collision checks
        self.pastPos = pk.Vec2d(*self.body.position)
        
        # Initialize the regular movement state
        self.initRegularState()
        
    def update(self, target, layout):
        '''Updates the schmoo every frame.'''
        self.layout = layout  # Temporary for debugging
        self.target = target  # Temporary for debugging
        self.pastPos = pk.Vec2d(*self.body.position)
        if self.state == 'move':
            self.doRegularMovement(target, layout)
        elif self.state == 'bounce back':
            self.doBounceBack()
        elif self.state == 'charge':
            self.doCharge(layout)
        
    def initRegularState(self):
        '''Initializes the regular movement state.'''
        self.state = 'move'
        self.doesBounceBack = True
        self.velo = np.array([0.0, 0.0])
    
    def doRegularMovement(self, target, layout):
        '''Moves randomly using Perlin noise and checks if it can charge at the player.'''
        direction = [2 * self.noise(self.noiseIterations), 2 * self.noise(self.noiseIterations + 1000.00907)]
        if direction != [0, 0]:
            self.velo = npVM.scaleVector(direction, self.regularSpeed)
        else:
            self.velo = np.array([0.0, 0.0])
        self.body.position += pk.Vec2d(*self.velo)
        self.noiseIterations += random.uniform(.000005, .00001)
        
        if self.checkIfCanSeeTarget(target, layout):
            self.initCharge(target)
        
    def checkIfCanSeeTarget(self, target, layout):
        '''Checks if there is a clear line of sight to the target.'''
        selfLPoints = self.getLPoints()
        targetLPoints = target.getLPoints()
        for i in range(4):
            interectedRowCols = bFC.getLineIntersectRowColQuadrants(selfLPoints[i], targetLPoints[i])
            for rowCol in interectedRowCols:
                for oTile in layout[rowCol[0]][rowCol[1]]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.linePolygonCollision(selfLPoints[i], targetLPoints[i], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':
                            if bFC.lineCircleCollision(selfLPoints[i], targetLPoints[i], oTile.body.position, oTile.radius): 
                                return False
        return True
    
    def doDeathEffect(self):
        '''Spawns two smaller schmeer enemies upon death.'''
        oBabySchmooLeft = schmeer(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(-self.width / 3, 0))
        oBabySchmooRight = schmeer(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(self.width / 3, 0))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oBabySchmooLeft))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oBabySchmooRight))
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back state.'''
        self.bounceBackDirection = direction
        self.bounceBackCount = 0
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)
        self.state = 'bounce back'

    def doBounceBack(self):
        '''Handles bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.bounceBackCount < self.bounceBackDuration:
            self.bounceBackCount += 1
        else:
            self.initRegularState()
            
    def initCharge(self, target):
        '''Initializes the charge state.'''
        self.state = 'charge'
        self.doesBounceBack = False
        targetCenter = target.body.position
        targetDirection = targetCenter - self.body.position
        self.velo = npVM.scaleVector(targetDirection, self.chargeSpeed)
        
    def doCharge(self, layout):
        '''Handles charge movement and stops if it collides with an obstacle.'''
        self.body.position += pk.Vec2d(*self.velo)
        if self.checkIfInGroundObstacle(layout):
            self.initRegularState()
    
    def checkIfInGroundObstacle(self, layout):
        '''Checks if the schmoo is inside a ground obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        for col in range(yTile - 1, yTile + 2):
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 1, xTile + 2):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle:
                        if oTile.geometry == 'rect':
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False
    
    def draw(self):
        '''Draws the schmoo and optionally its sight lines for debugging.'''
        if self.state  == 'charge':
            self.image = schmooImageCharge
        else:
            self.image = schmooImageChill
        if self.velo[0]< 0:
            self.image = p.transform.flip(self.image,True,False)
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
        
        if self.drawSightLines:
            selfLPoints = self.getLPoints()
            targetLPoints = self.target.getLPoints()
            for i in range(4):
                broken = False
                interectedRowCols = bFC.getLineIntersectRowColQuadrants(selfLPoints[i], targetLPoints[i])
                for rowCol in interectedRowCols:
                    for oTile in self.layout[rowCol[0]][rowCol[1]]:
                        if oTile.isEnemyGroundObstacle:
                            if oTile.geometry == 'rect':
                                if bFC.linePolygonCollision(selfLPoints[i], targetLPoints[i], oTile.getLPoints()): 
                                    broken = True
                            elif oTile.geometry == 'circle':
                                if bFC.lineCircleCollision(selfLPoints[i], targetLPoints[i], oTile.body.position, oTile.radius): 
                                    broken = True
                if broken:
                    p.draw.line(self.screen, (255, 0, 0), selfLPoints[i], targetLPoints[i])
                else:
                    p.draw.line(self.screen, (0, 255, 0), selfLPoints[i], targetLPoints[i])

                            
            
class schmeer(enemy):
    '''A small enemy that moves randomly and bounces back when hit.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.5, height=bGI.basicTileHeight*.5, health=5, damage=1):
        '''Initializes the schmeer enemy with attributes for movement and bounce back.'''
        clr = (121, 81, 35)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage)
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        # Movement attributes
        self.state = 'move'
        self.regularSpeed = 0.5
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0
        
        # Store past position for collision checks
        self.pastPos = pk.Vec2d(*self.body.position)
        
    def update(self):
        '''Updates the schmeer every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position
        if self.state == 'move':
            self.doRegularMovement()  # Perform regular movement
        elif self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        
    def initRegularState(self):
        '''Initializes the regular movement state.'''
        self.state = 'move'
        self.doesBounceBack = True
        self.velo = np.array([0.0, 0.0])  # Reset velocity
    
    def doRegularMovement(self):
        '''Moves randomly using Perlin noise.'''
        direction = [self.noise(self.noiseIterations), self.noise(self.noiseIterations + 1000.00907)]  # Generate random direction
        if direction != [0, 0]:  # Ensure direction is not (0, 0) to avoid errors
            self.velo = npVM.scaleVector(direction, self.regularSpeed)  # Scale direction to speed
        else:
            self.velo = np.array([0.0, 0.0])  # Set velocity to zero if direction is invalid
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        self.noiseIterations += random.uniform(0.000005, 0.00001)  # Increment noise iterations for smooth movement
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back state.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale direction to bounce back speed
        self.state = 'bounce back'  # Set state to bounce back

    def doBounceBack(self):
        '''Handles bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment bounce back counter
        else:
            self.state = 'move'  # Return to regular movement state

    def draw(self):
        '''Draws the schmeer to the screen.'''
        self.image = schmeerImage
        if self.velo[0] >0:
            self.image = p.transform.flip(self.image,True,False)  # Flip image if moving right
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)
            
class schmeerOfSchmoo(enemy):
    '''A medium-sized enemy that shoots tears in three directions and splits into two schmoos upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.9, height=bGI.basicTileHeight*1.9, health=30, damage=1):
        '''Initializes the schmeerOfSchmoo enemy with attributes for movement, shooting, and splitting.'''
        clr = (121, 81, 35)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         needsLayout=True, needsTarget=True, hasDeathEffect=True, spawnsEnemiesOnDeath=True)
        
        # Bounce back attributes
        self.bounceBackSpeed = 2
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        # Shooting attributes
        self.maxDistanceToTargetToShoot = 8 * bGI.basicTileWidth
        self.timeBetweenShots = bGI.fps * 1.5
        self.shotTimer = 0
        self.tearSpeed = 4
        self.tearRange = 8
        self.tearRotateAmount = math.pi / 7
        self.tearRadius = 10
        
        # Initialize attack state
        self.initAttack()
        
    def update(self, target, layout):
        '''Updates the schmeerOfSchmoo every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'attack':
            self.doAttack(target, layout)  # Perform attack behavior
            
    def initAttack(self):
        '''Initializes the attack state.'''
        self.state = 'attack'
        self.doesBounceBack = True
        self.velo = np.array([0.0, 0.0])  # Reset velocity
        
    def doAttack(self, target, layout):
        '''Handles attack behavior, including shooting tears if the target is within range and visible.'''
        distance = math.dist(bFC.npArrayIntoTuple(self.body.position), bFC.npArrayIntoTuple(target.body.position))
        if self.shotTimer > 0:
            self.shotTimer -= 1
        if distance <= self.maxDistanceToTargetToShoot and self.shotTimer <= 0:
            if self.canSeeTarget(target, layout):
                self.shootTears(target)  # Shoot tears in three directions
                self.shotTimer = self.timeBetweenShots  # Reset shot timer
    
    def canSeeTarget(self, target, layout):
        '''Checks if there is a clear line of sight to the target.'''
        intersectedRowCols = bFC.getLineIntersectRowColQuadrants(self.body.position, target.body.position)
        for rowCol in intersectedRowCols:
            for oTile in layout[rowCol[0]][rowCol[1]]:
                if oTile.isEnemyGroundObstacle:
                    if oTile.geometry == 'rect':
                        if bFC.linePolygonCollision(self.body.position, target.body.position, oTile.getLPoints()): 
                            return False
                    elif oTile.geometry == 'circle':
                        if bFC.lineCircleCollision(self.body.position, target.body.position, oTile.body.position, oTile.radius): 
                            return False
        return True
             
    def shootTears(self, target):
        '''Shoots tears in three directions: forward, clockwise, and counterclockwise.'''
        direction = target.body.position - self.body.position
        tearVelo = npVM.scaleVector(direction, self.tearSpeed)
        
        # Forward tear
        oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVelo, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))
        
        # Clockwise tear
        tearVeloCW = npVM.rotateVector(tearVelo, self.tearRotateAmount)
        oTearCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCW))
        
        # Counterclockwise tear
        tearVeloCCW = npVM.rotateVector(tearVelo, -self.tearRotateAmount)
        oTearCCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCCW))
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back state.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale direction to bounce back speed
        self.state = 'bounce back'  # Set state to bounce back
        
    def doBounceBack(self):
        '''Handles bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment bounce back counter
        else:
            self.initAttack()  # Return to attack state
            
    def doDeathEffect(self):
        '''Spawns two schmoos upon death.'''
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(schmoo(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(-self.width / 3, 0))))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(schmoo(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(self.width / 3, 0))))

    def draw(self):
        '''Draws the schmeerOfSchmoo to the screen.'''
        self.image = schmeerOfSchmooImageChill
        if self.velo[0] > 0:
            self.image = p.transform.flip(self.image, True, False)
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position

class schmeerestOfSchmoo(enemy):
    '''A large boss enemy that alternates between charging and shooting attacks.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*2.5, height=bGI.basicTileHeight*2.5, health=80, damage=1):
        '''Initializes attributes for the schmeerestOfSchmoo boss.'''
        clr = (121, 81, 35)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         isBoss=True, needsTarget=True, needsLayout=True, doesBounceBack=False)
        
        # State attributes
        self.state = 'cool down'
        self.attackOptions = ['charge', 'shoot']  # Possible attack types
        self.currentAttack = None
        self.velo = np.array([0.0, 0.0])  # Velocity vector

        # Cool down attributes
        self.moveCoolDownBounds = (int(bGI.fps * 0.8), int(bGI.fps * 1.3))  # Cool down duration bounds
        self.moveCoolDownCount = 0

        # Charge attack attributes
        self.numChargesTotal = 3  # Total number of charges per attack
        self.numChargesLeft = 0  # Remaining charges
        self.chargeSpeed = 7  # Speed during charge
        self.chargeDirection = np.array([0.0, 0.0])  # Direction of charge

        # Shoot attack attributes
        self.numShotsTotal = 3  # Total number of shots per attack
        self.numShotsLeft = self.numShotsTotal  # Remaining shots
        self.shotCoolDown = bGI.fps * 0.7  # Cool down between shots
        self.shotCoolDownCount = 0  # Current cool down count
        self.shotSpread = math.pi / 5  # Spread angle of shots
        self.numTearsPerShot = 3  # Number of tears per shot
        self.angleBetweenTears = self.shotSpread / self.numTearsPerShot  # Angle between tears
        self.tearSpeed = 6  # Speed of tears
        self.tearRange = 15  # Range of tears
        self.tearRadius = 10  # Radius of tears

        # Initialize the cool down state
        self.initCoolDown()

    def update(self, target, layout):
        '''Updates the boss every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position
        if self.state == 'cool down':
            self.doCoolDown(target, layout)  # Perform cool down behavior
        elif self.state == 'attack':
            self.doAttack(target, layout)  # Perform attack behavior

    def initCoolDown(self):
        '''Initializes the cool down state.'''
        self.state = 'cool down'
        self.moveCoolDownCount = random.randint(*self.moveCoolDownBounds)  # Set a random cool down duration
    
    def doCoolDown(self, target, layout):
        '''Handles the cool down behavior.'''
        self.moveCoolDownCount -= 1  # Decrement the cool down counter
        if self.moveCoolDownCount <= 0:  # If cool down is complete, start an attack
            self.initAttack(target, layout)

    def initAttack(self, target, layout):
        '''Initializes an attack.'''
        self.state = 'attack'
        self.currentAttack = random.choice(self.attackOptions)  # Choose a random attack type
        if self.currentAttack == 'charge':
            self.initCharge(target)  # Initialize charge attack
        elif self.currentAttack == 'shoot':
            self.initShoot()  # Initialize shoot attack

    def doAttack(self, target, layout):
        '''Handles the attack behavior.'''
        if self.currentAttack == 'charge':
            self.doCharge(target, layout)  # Perform charge attack
        elif self.currentAttack == 'shoot':
            self.doShoot(target)  # Perform shoot attack

    def initCharge(self, target):
        '''Initializes the charge attack.'''
        self.numChargesLeft = self.numChargesTotal  # Reset the number of charges
        self.chargeDirection = target.body.position - self.body.position  # Set the charge direction
    
    def doCharge(self, target, layout):
        '''Handles the charge attack behavior.'''
        self.velo = npVM.scaleVector(self.chargeDirection, self.chargeSpeed)  # Scale the velocity to the charge speed
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on velocity
        if self.checkIfInGroundObstacle(layout):  # If the boss collides with an obstacle
            self.numChargesLeft -= 1  # Decrement the remaining charges
            if self.numChargesLeft <= 0:  # If no charges are left, return to cool down state
                self.initCoolDown()
            else:  # Otherwise, set a new charge direction
                self.chargeDirection = target.body.position - self.body.position 
                
    def initShoot(self):
        '''Initializes the shoot attack.'''
        self.numShotsLeft = self.numShotsTotal  # Reset the number of shots
        self.shotCoolDownCount = 0  # Reset the shot cool down counter

    def doShoot(self, target):
        '''Handles the shoot attack behavior.'''
        if self.shotCoolDownCount <= 0:  # If the cool down between shots is complete
            self.shotCoolDownCount = self.shotCoolDown  # Reset the cool down counter
            self.numShotsLeft -= 1  # Decrement the remaining shots
            direction = target.body.position - self.body.position  # Direction towards the target
            
            # Shoot multiple tears in a spread pattern
            for i in range(self.numTearsPerShot):
                rotateAmount = -1 * (self.numTearsPerShot // 2) + i
                rotateAmount *= self.angleBetweenTears
                newDirection = npVM.rotateVector(direction, rotateAmount)  # Rotate the direction for each tear
                tearVelo = npVM.scaleVector(newDirection, self.tearSpeed)  # Scale the velocity to the tear speed
                oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                     self.tearRadius, tearVelo, self.tearRange)  # Create a tear object
                self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
            if self.numShotsLeft == 0:  # If no shots are left, return to cool down state
                self.initCoolDown()
        else:
            self.shotCoolDownCount -= 1  # Decrement the cool down counter

    def checkIfInGroundObstacle(self, layout):
        '''Checks if the boss is inside a ground obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)  # Get the tile coordinates
        for col in range(yTile - 2, yTile + 3):  # Check surrounding tiles
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 2, xTile + 3):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle:  # If the tile is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False  # Return false if no collision is detected
    
    def draw(self):
        '''Draws the schmeerestOfSchmoo to the screen.'''
        if self.state == 'cool down':
            self.image = schmeerestOfSchmooImageChill
        elif self.state == 'attack':
            if self.currentAttack == 'charge':
                self.image = schmeerestOfSchmooImageCharge
            elif self.currentAttack == 'shoot':
                self.image = schmeerestOfSchmooImageShoot
        if self.velo[0] > 0:
            self.image = p.transform.flip(self.image, True, False)
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position

class goober(enemy):
    '''A basic enemy that moves towards the player using a vector field.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, clr=(0, 120, 100), width=bGI.basicTileWidth * 0.7, height=bGI.basicTileHeight * 0.8, health=13, damage=1):
        '''Initializes the goober enemy with movement and bounce back behavior.'''
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         needsGroundVField=True)
        self.state = 'move'  # Initial state is movement
        self.velo = np.array([0.0, 0.0])  # Velocity vector
        self.speed = 2  # Movement speed
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        #animation attributes
        self.image = trackerFlyImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
    
    def update(self, vField):
        '''Updates the goober every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doMovement(vField)  # Perform movement behavior
            
    def doMovement(self, vField):
        '''Moves the goober towards the player using a vector field.'''
        rowCols = []  # List to store the tiles the goober is in
        # Get the row and column of the tiles the goober overlaps
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        
        direction = np.array([0.0, 0.0])  # Initialize direction vector
        for rowCol in rowCols:  # Iterate through the tiles
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        
        if direction[0] != 0 or direction[1] != 0:  # If the direction is not zero
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state
            
    def draw(self):
        '''Draws the goober and optionally its sight lines for debugging.'''
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == gooberImage1:
                self.image = gooberImage2
            else:
                self.image = gooberImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        if self.velo[0] == 0 and self.velo[1] == 0:
            self.image = gooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
        
class speedyGoober(goober):
    '''Faster version of the goober enemy.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth * 0.7, height=bGI.basicTileHeight * 0.8, health=20, damage=1):
        super().__init__(screen, space, oPrinceEventHandler, center, width = width, height = height,  clr = (10,10,100),health = health, damage = damage)
        self.speed = 5
        
    def draw(self):
        '''Draws the goober'''
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == speedyGooberImage1:
                self.image = speedyGooberImage2
            else:
                self.image = speedyGooberImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        if self.velo[0] == 0 and self.velo[1] == 0:
            self.image = speedyGooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
            
class explodeyGoober(enemy):
    '''An enemy that moves towards the player and explodes on contact or death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.9, height=bGI.basicTileHeight*.9, health=13, damage=1):
        '''Initializes the explodeyGoober enemy with movement, bounce back, and explosion behavior.'''
        clr = (100, 100, 120)  # Greyish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         needsGroundVField=True, specialEffectOnPlayerContact=True, hasDeathEffect=True)
        
        # Movement attributes
        self.state = 'move'
        self.velo = np.array([0.0, 0.0])
        self.speed = 2
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        #animation attributes
        self.image = explodeyGooberImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
        
    def update(self, vField):
        '''Updates the explodeyGoober every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doMovement(vField)  # Perform movement behavior
            
    def doMovement(self, vField):
        '''Moves the explodeyGoober towards the player using a vector field.'''
        rowCols = []  # List to store the tiles the enemy is in
        # Get the row and column of the tiles the enemy overlaps
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        
        direction = np.array([0.0, 0.0])  # Initialize direction vector
        for rowCol in rowCols:  # Iterate through the tiles
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        
        if direction[0] != 0 or direction[1] != 0:  # If the direction is not zero
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
            
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state
    
    def doSpecialEffectOnPlayerContact(self):
        '''Handles the special effect when the explodeyGoober contacts the player.'''
        self.oPrinceEventHandler.addEvent(pEC.removeEnemyEvent(self))  # Remove the enemy
        self.doDeathEffect()  # Trigger the death effect (explosion)
    
    def doDeathEffect(self):
        '''Creates an explosion effect when the explodeyGoober dies.'''
        oExplosion = bC.explosion(self.screen, self.space, self.oPrinceEventHandler, self.body.position)  # Create an explosion
        self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))  # Add the explosion to the room
    
    def draw(self):
        '''Draws the goober'''
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == explodeyGooberImage1:
                self.image = explodeyGooberImage2
            else:
                self.image = explodeyGooberImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        if self.velo[0] == 0 and self.velo[1] == 0:
            self.image = explodeyGooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
    
    
    
class shootyGoober(enemy):
    '''An enemy that moves using a vector field and shoots at the player when in range.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.8, height=bGI.basicTileHeight*.8, health=13, damage=1, clr=(255, 100, 20)):
        '''Initializes the shootyGoober enemy with movement, shooting, and bounce back behavior.'''
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         needsTarget=True, needsLayout=True, needsGroundVField=True)
        
        # Movement attributes
        self.state = 'move'
        self.velo = np.array([0.0, 0.0])
        self.speed = 2
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        # Shooting attributes
        self.framesBetweenShots = bGI.fps * 1
        self.framesBetweenShotsCount = 0
        self.maxTargetDistanceToShoot = 12 * bGI.basicTileWidth
        self.tearSpeed = 5
        self.tearRange = 10
        self.tearRadius = 10
        
        #animation attributes
        self.image = explodeyGooberImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
    
    def update(self, target, layout, vField):
        '''Updates the shootyGoober every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doMovement(vField)  # Perform movement behavior
            self.doShoot(target, layout)  # Perform shooting behavior
    
    def initMovement(self):
        '''Initializes the movement state.'''
        self.state = 'move'
          
    def doMovement(self, vField):
        '''Moves the shootyGoober using a vector field.'''
        rowCols = []  # List to store the tiles the enemy is in
        # Get the row and column of the tiles the enemy overlaps
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        direction = np.array([0.0, 0.0])  # Initialize direction vector
        for rowCol in rowCols:  # Iterate through the tiles
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        if direction[0] != 0 or direction[1] != 0:  # If the direction is not zero
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
    
    def initShoot(self):
        '''Initializes the shooting behavior.'''
        self.framesBetweenShotsCount = self.framesBetweenShots
    
    def doShoot(self, target, layout):
        '''Handles the shooting behavior.'''
        if self.framesBetweenShotsCount > 0:
            self.framesBetweenShotsCount -= 1  # Decrement the shot cooldown
        else:
            distance = math.dist(self.body.position, target.body.position)  # Calculate the distance to the target
            if distance <= self.maxTargetDistanceToShoot and self.checkIfCanSeeTarget(target, layout):  # Check if the target is in range and visible
                self.shootTear(target)  # Shoot a tear at the target
                self.framesBetweenShotsCount = self.framesBetweenShots  # Reset the shot cooldown
      
    def shootTear(self, target):
        '''Shoots a tear towards the target.'''
        direction = target.body.position - self.body.position  # Calculate the direction to the target
        tearVelo = npVM.scaleVector(direction, self.tearSpeed)  # Scale the direction to the tear speed
        oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVelo, self.tearRange)  # Create a tear object
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
    
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.initMovement()  # Return to the movement state
            self.initShoot()  # Reinitialize the shooting behavior
            
    def checkIfCanSeeTarget(self, target, layout):
        '''Checks if there is a clear line of sight to the target.'''
        selfLPoints = self.getLPoints()  # Get the line points of the enemy
        targetLPoints = target.getLPoints()  # Get the line points of the target
        for i in range(4):  # Iterate through the line points
            interectedRowCols = bFC.getLineIntersectRowColQuadrants(selfLPoints[i], targetLPoints[i])  # Get the intersected tiles
            for rowCol in interectedRowCols:  # Iterate through the intersected tiles
                for oTile in layout[rowCol[0]][rowCol[1]]:  # Iterate through the objects in the tile
                    if oTile.isEnemyGroundObstacle:  # Check if the object is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.linePolygonCollision(selfLPoints[i], targetLPoints[i], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.lineCircleCollision(selfLPoints[i], targetLPoints[i], oTile.body.position, oTile.radius): 
                                return False
        return True  # Return true if no collision is detected
    
    def draw(self):
        '''Draws the goober'''
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == shootyGooberImage1:
                self.image = shootyGooberImage2
            else:
                self.image = shootyGooberImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        if self.velo[0] == 0 and self.velo[1] == 0:
            self.image = shootyGooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
      
        
class regenGoober(enemy):
    '''An enemy that moves using a vector field and spawns a regenBooger upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.7, height=bGI.basicTileHeight*.8, health=13, damage=1):
        '''Initializes the regenGoober enemy with movement, bounce back, and death effect behavior.'''
        clr = (120, 50, 0)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         needsGroundVField=True, hasDeathEffect=True, spawnsEnemiesOnDeath=True)
        self.state = 'move'
        self.velo = np.array([0.0, 0.0])
        self.speed = 2
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        #animation attributes
        self.image = regenGooberImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
    
    def update(self, vField):
        '''Updates the regenGoober every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doMovement(vField)  # Perform movement behavior
            
    def doMovement(self, vField):
        '''Moves the regenGoober using a vector field.'''
        rowCols = []  # List to store the tiles the enemy is in
        # Get the row and column of the tiles the enemy overlaps
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        direction = np.array([0.0, 0.0])  # Initialize direction vector
        for rowCol in rowCols:  # Iterate through the tiles
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        if direction[0] != 0 or direction[1] != 0:  # If the direction is not zero
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state
            
    def doDeathEffect(self):
        '''Spawns a regenBooger upon death.'''
        oRegenBooger = regenBooger(self.screen, self.space, self.oPrinceEventHandler, self.body.position)
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oRegenBooger))

    def draw(self):
        '''Draws the goober'''
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == regenGooberImage1:
                self.image = regenGooberImage2
            else:
                self.image = regenGooberImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        if self.velo[0] == 0 and self.velo[1] == 0:
            self.image = shootyGooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage

        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position

class regenBooger(enemy):
    '''A smaller enemy that regenerates health and transforms into a regenGoober when fully healed.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.6, height=bGI.basicTileHeight*.6, health=6, damage=1):
        '''Initializes the regenBooger enemy with regeneration and bounce back behavior.'''
        clr = (120, 50, 0)  # Brownish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage)
        self.regenAmountPerFrame = 1 / bGI.fps  # Regenerates 1 health point per second
        self.healthTilFullyRegenerated = 9  # Health threshold to transform into a regenGoober
        
        self.state = 'normal'

        self.image = regenBoogerImage
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
    def update(self):
        '''Updates the regenBooger every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        self.health += self.regenAmountPerFrame  # Increment health by the regeneration amount
        if self.health >= self.healthTilFullyRegenerated:  # Check if health is fully regenerated
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(regenGoober(self.screen, self.space, self.oPrinceEventHandler, self.body.position)))  # Transform into a regenGoober
            self.oPrinceEventHandler.addEvent(pEC.removeEnemyEvent(self))  # Remove the current regenBooger
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'normal'  # Return to the normal state
    
    def draw(self):
        drawPos = (self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2)
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position
            
            
class multipliTerror(enemy):
    def __init__(self, screen, space, oPrinceEventHandler, center, width = bGI.basicTileWidth*.8, height=bGI.basicTileHeight*.8, health = 13, damage=1):
        '''Initialize the multipliTerror enemy with attributes for movement, bounce back, and death effect behavior'''
        clr = (76, 69, 81)  # Greyish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                        needsGroundVField = True, hasDeathEffect=True, spawnsEnemiesOnDeath=True)
        
        # Set the initial state to 'move'
        self.state = 'move'
        
        # Initialize velocity vector to zero
        self.velo = np.array([0.0, 0.0])
        
        # Set the movement speed
        self.speed = 2
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        #animation attributes
        self.image = multipliterrorImage1
        self.framesTilChangeImage = 4
        self.framesTilChangeImageCount = self.framesTilChangeImage
    
    def update(self, vField):
        '''Updates the multipliTerror every frame.'''
        # Save the current position for collision checks
        self.pastPos = pk.Vec2d(*self.body.position)
        # Check the current state and perform the corresponding behavior
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doMovement(vField)  # Perform movement behavior
            
    def doMovement(self, vField):
        '''Moves the multipliTerror using a vector field.'''
        # Get the row and column indices of the tiles the enemy overlaps
        rowCols = []
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        
        # Initialize the direction vector
        direction = np.array([0.0, 0.0])
        
        # Iterate through the tiles and sum up the vectors from the vector field
        for rowCol in rowCols:
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        
        # If the direction is not zero, scale it to the speed and update the position
        if direction[0] != 0 or direction[1] != 0:
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state
            
    def doDeathEffect(self):
        '''Handles the death effect by spawning two multipliTerrorBoogers upon death.'''
        # Create two multipliTerrorBoogers at positions offset from the current position
        booger1 = multipliTerrorBooger(self.screen, self.space, self.oPrinceEventHandler, self.body.position - pk.Vec2d(self.width / 4, 0))
        booger2 = multipliTerrorBooger(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(self.width / 4, 0))
        # Add the newly created boogers to the game
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(booger1))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(booger2))

    def draw(self):
        '''Draws the multipliTerror enemy to the screen with animation.'''
        # Switch images for animation every few frames
        if self.framesTilChangeImageCount <= 0:
            self.framesTilChangeImageCount = self.framesTilChangeImage
            if self.image == multipliterrorImage1:
                self.image = multipliterrorImage2
            else:
                self.image = multipliterrorImage1
        else:
            self.framesTilChangeImageCount -= 1
        
        # Determine the image to draw based on velocity
        if self.velo[0] == 0 and self.velo[1] == 0:  # If not moving, use the default image
            self.image = shootyGooberImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage
            drawnImage = self.image
        elif self.velo[0] < 0:  # If moving left, flip the image horizontally
            drawnImage = p.transform.flip(self.image, True, False)
        else:  # Otherwise, use the current image
            drawnImage = self.image
        
        # Calculate the position to draw the image and render it on the screen
        drawPos = np.array([self.body.position[0] - drawnImage.get_width() / 2, self.body.position[1] - drawnImage.get_height() / 2])
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position


class multipliTerrorBooger(enemy):
    '''A smaller enemy that regenerates health and transforms into a multipliTerror when fully healed.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.5, height=bGI.basicTileHeight*.5, health=12, damage=1):
        '''Initializes the multipliTerrorBooger enemy with regeneration and bounce back behavior.'''
        clr = (76, 69, 81)  # Greyish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage)
        
        # Regeneration attributes
        self.regenAmountPerFrame = 2 / bGI.fps  # Regenerates 2 health points per second
        self.healthTilFullyRegenerated = 19  # Health threshold to transform into a multipliTerror
        
        # State attributes
        self.state = 'normal'
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        # Image attributes
        self.image = multipliterrorBoogerImage
        self.velo = np.array([0.0, 0.0])  # Velocity vector
        
    def update(self):
        '''Updates the multipliTerrorBooger every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        self.health += self.regenAmountPerFrame  # Increment health by the regeneration amount
        if self.health >= self.healthTilFullyRegenerated:  # Check if health is fully regenerated
            # Transform into a multipliTerror and remove the current multipliTerrorBooger
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(multipliTerror(self.screen, self.space, self.oPrinceEventHandler, self.body.position)))
            self.oPrinceEventHandler.addEvent(pEC.removeEnemyEvent(self))
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
            
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
        
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state

    def draw(self):
        '''Draws the multipliTerrorBooger to the screen.'''
        drawPos = (self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2)  # Calculate draw position
        self.screen.blit(self.image, drawPos)  # Draw the image at the calculated position

class lordOfTheFlies(enemy):
    '''A boss enemy that moves randomly and spawns trackerFly enemies.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width= bGI.basicTileWidth*1.9, height= bGI.basicTileHeight* 1.9, health = 60, damage=1):
        '''Initializes the lordOfTheFlies enemy with movement, spawning, and death effect behavior.'''
        clr = (120,111,113)  # Greyish color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         flying=True, doesBounceBack=False, isBoss=True, needsLayout=True, hasDeathEffect=True,
                         spawnsEnemiesOnDeath=True, bouncesOffObstacles=True)
        
        # Attributes for spawning flies
        self.numFliesSpawnedBounds = (1, 3)  # Number of flies spawned during gameplay
        self.numFliesSpawnedOnDeathBounds = (4, 5)  # Number of flies spawned upon death
        self.state = 'cool down'  # Initial state is cool down
        
        # Movement attributes
        self.speed = 3  # Movement speed
        self.velo = np.array([-1, -1])  # Initial velocity
        self.velo = npVM.scaleVector(self.velo, self.speed)  # Scale velocity to speed

        # Cool down attributes
        self.coolDownBounds = (int(bGI.fps*2.3), int(bGI.fps*5))  # Cool down duration bounds
        self.coolDownCount = 0  # Current cool down count

        # Animation attributes
        self.image = lordOfTheFliesImage1  # Initial image
        self.framesTilChangeImage = 4  # Frames until image changes
        self.framesTilChangeImageCount = self.framesTilChangeImage  # Counter for image change

        # Initialize cool down state
        self.initCoolDown()

    def update(self, layout):
        '''Updates the lordOfTheFlies every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'cool down':
            self.doCoolDown()  # Perform cool down behavior
        elif self.state == 'spawn':
            self.doSpawn(layout)  # Perform spawn behavior
        
        # Update position based on velocity
        self.body.position += pk.Vec2d(*self.velo)

    def initCoolDown(self):
        '''Initializes the cool down state.'''
        self.state = 'cool down'  # Set state to cool down
        self.coolDownCount = random.randint(*self.coolDownBounds)  # Set a random cool down duration
    
    def doCoolDown(self):
        '''Handles the cool down behavior.'''
        self.coolDownCount -= 1  # Decrement the cool down counter
        if self.coolDownCount <= 0:  # If cool down is complete, start spawning flies
            self.initSpawn()
    
    def initSpawn(self):
        '''Initializes the spawn state.'''
        self.state = 'spawn'  # Set state to spawn
    
    def doSpawn(self, layout):
        '''Handles the spawn behavior by spawning trackerFly enemies.'''
        # Get the row and column of the tiles around the enemy
        centerRowCol = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        minCol = max(0, centerRowCol[1] - 2)
        maxCol = min(bGI.numTilesWide - 1, centerRowCol[1] + 2)
        minRow = max(0, centerRowCol[0] - 2)
        maxRow = min(bGI.numTilesHigh - 1, centerRowCol[0] + 2)
        
        # Generate possible spawn locations
        possibleRowCols = [(row, minCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(row, maxCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(minRow, col) for col in range(minCol + 1, maxCol)]
        possibleRowCols += [(maxRow, col) for col in range(minCol + 1, maxCol)]

        # Spawn a random number of trackerFly enemies
        numFliesSpawn = random.randint(*self.numFliesSpawnedBounds)
        for i in range(numFliesSpawn):
            while True:
                spot = random.choice(possibleRowCols)  # Choose a random spawn location
                if layout[spot[0]][spot[1]] != bGI.empty:  # Check if the location is not empty
                    blocked = False
                    for oTile in layout[spot[0]][spot[1]]:
                        if oTile.isEnemyAirObstacle:  # Check if the location is not blocked
                            blocked = True
                    if blocked:
                        continue
                break
            # Create and add a trackerFly enemy at the chosen location
            oFly = trackerFly(self.screen, self.space, self.oPrinceEventHandler, ((spot[1] + 0.5) * bGI.basicTileWidth, (spot[0] + 0.5) * bGI.basicTileHeight))
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oFly))
        
        # Return to cool down state
        self.initCoolDown()

    def doDeathEffect(self):
        '''Handles the death effect by spawning trackerFly enemies.'''
        # Spawn a random number of trackerFly enemies at random positions around the enemy
        numFliesSpawn = random.randint(*self.numFliesSpawnedOnDeathBounds)
        for i in range(numFliesSpawn):
            addedWidth = random.randint(int(-1 * bGI.basicTileWidth), int(1 * bGI.basicTileWidth))
            addedHeight = random.randint(int(-1 * bGI.basicTileHeight), int(1 * bGI.basicTileHeight))
            oFly = trackerFly(self.screen, self.space, self.oPrinceEventHandler, (self.body.position[0] + addedWidth, self.body.position[1] + addedHeight))
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oFly))
    
    def draw(self):
        '''Draws the lordOfTheFlies to the screen.'''
        self.framesTilChangeImageCount -= 1  # Decrement the image change counter
        if self.framesTilChangeImageCount <= 0:  # Switch images for animation
            if self.image == lordOfTheFliesImage1:
                self.image = lordOfTheFliesImage2
            else:
                self.image = lordOfTheFliesImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage  # Reset the image change counter

        # Calculate draw position and draw the image
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)

class kingOfTheFlies(enemy):
    '''A boss enemy that moves randomly and spawns various types of flies.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width= bGI.basicTileWidth*2.5, height= bGI.basicTileHeight* 2.5, health = 100, damage=1):
        '''Initializes the kingOfTheFlies enemy with movement, spawning, and death effect behavior.'''
        clr = (212,175,55)  # Golden grey color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         flying=True, doesBounceBack=False, isBoss=True, needsLayout=True, hasDeathEffect=True,
                         spawnsEnemiesOnDeath=True, bouncesOffObstacles=True)
        
        # Attributes for spawning flies
        self.numFliesSpawnedBounds = (1, 3)  # Number of flies spawned during gameplay
        self.numFliesSpawnedOnDeathBounds = (4, 5)  # Number of flies spawned upon death
        self.fliesThatCanBeSpawned = [trackerFly, vShooterFly, shooterFly, shootyMcFly]  # Types of flies that can be spawned
        
        self.state = 'cool down'  # Initial state is cool down
        
        # Movement attributes
        self.speed = 3  # Movement speed
        self.velo = np.array([-1, -1])  # Initial velocity
        self.velo = npVM.scaleVector(self.velo, self.speed)  # Scale velocity to speed

        # Cool down attributes
        self.coolDownBounds = (int(bGI.fps*2), int(bGI.fps*4))  # Cool down duration bounds
        self.coolDownCount = 0  # Current cool down count

        # Animation attributes
        self.image = kingOfTheFliesImage1  # Initial image
        self.framesTilChangeImage = 4  # Frames until image changes
        self.framesTilChangeImageCount = self.framesTilChangeImage  # Counter for image change

        # Initialize cool down state
        self.initCoolDown()

    def update(self, layout):
        '''Updates the kingOfTheFlies every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'cool down':
            self.doCoolDown()  # Perform cool down behavior
        elif self.state == 'spawn':
            self.doSpawn(layout)  # Perform spawn behavior
        
        # Update position based on velocity
        self.body.position += pk.Vec2d(*self.velo)

    def initCoolDown(self):
        '''Initializes the cool down state.'''
        self.state = 'cool down'  # Set state to cool down
        self.coolDownCount = random.randint(*self.coolDownBounds)  # Set a random cool down duration
    
    def doCoolDown(self):
        '''Handles the cool down behavior.'''
        self.coolDownCount -= 1  # Decrement the cool down counter
        if self.coolDownCount <= 0:  # If cool down is complete, start spawning flies
            self.initSpawn()
    
    def initSpawn(self):
        '''Initializes the spawn state.'''
        self.state = 'spawn'  # Set state to spawn
    
    def doSpawn(self, layout):
        '''Handles the spawn behavior by spawning various types of flies.'''
        # Get the row and column of the tiles around the enemy
        centerRowCol = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        minCol = max(0, centerRowCol[1] - 2)
        maxCol = min(bGI.numTilesWide - 1, centerRowCol[1] + 2)
        minRow = max(0, centerRowCol[0] - 2)
        maxRow = min(bGI.numTilesHigh - 1, centerRowCol[0] + 2)
        
        # Generate possible spawn locations
        possibleRowCols = [(row, minCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(row, maxCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(minRow, col) for col in range(minCol + 1, maxCol)]
        possibleRowCols += [(maxRow, col) for col in range(minCol + 1, maxCol)]

        # Spawn a random number of flies
        numFliesSpawn = random.randint(*self.numFliesSpawnedBounds)
        for i in range(numFliesSpawn):
            while True:
                spot = random.choice(possibleRowCols)  # Choose a random spawn location
                if layout[spot[0]][spot[1]] != bGI.empty:  # Check if the location is not empty
                    blocked = False
                    for oTile in layout[spot[0]][spot[1]]:
                        if oTile.isEnemyAirObstacle:  # Check if the location is not blocked
                            blocked = True
                    if blocked:
                        continue
                break
            # Create and add a fly at the chosen location
            flyClass = random.choice(self.fliesThatCanBeSpawned)
            oFly = flyClass(self.screen, self.space, self.oPrinceEventHandler, ((spot[1] + 0.5) * bGI.basicTileWidth, (spot[0] + 0.5) * bGI.basicTileHeight))
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oFly))
        
        # Return to cool down state
        self.initCoolDown()

    def doDeathEffect(self):
        '''Handles the death effect by spawning various types of flies.'''
        # Spawn a random number of flies at random positions around the enemy
        numFliesSpawn = random.randint(*self.numFliesSpawnedOnDeathBounds)
        for i in range(numFliesSpawn):
            addedWidth = random.randint(int(-1 * bGI.basicTileWidth), int(1 * bGI.basicTileWidth))
            addedHeight = random.randint(int(-1 * bGI.basicTileHeight), int(1 * bGI.basicTileHeight))
            flyClass = random.choice(self.fliesThatCanBeSpawned)
            oFly = flyClass(self.screen, self.space, self.oPrinceEventHandler, (self.body.position[0] + addedWidth, self.body.position[1] + addedHeight))
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oFly))
    
    def draw(self):
        '''Draws the kingOfTheFlies to the screen.'''
        self.framesTilChangeImageCount -= 1  # Decrement the image change counter
        if self.framesTilChangeImageCount <= 0:  # Switch images for animation
            if self.image == kingOfTheFliesImage1:
                self.image = kingOfTheFliesImage2
            else:
                self.image = kingOfTheFliesImage1
            self.framesTilChangeImageCount = self.framesTilChangeImage  # Reset the image change counter

        # Calculate draw position and draw the image
        drawPos = np.array([self.body.position[0] - self.image.get_width() / 2, self.body.position[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)


class leBro(enemy):
    '''A boss enemy that moves randomly and charges at the player, angering other leBro enemies upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.1, height=bGI.basicTileHeight*1.1, health=40, damage=1):
        '''Initializes the leBro enemy with movement, charging, and angering behavior.'''
        clr = (115, 0, 0)  # Dark red color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         isBoss=True, hasDeathEffect=True, needsTarget=True, needsLayout=True, doesBounceBack=False)

        # Mental state attributes
        self.mentalState = 'calm'

        # Cool down attributes
        self.calmCooldDownBounds = (int(bGI.fps * 0.5), int(bGI.fps * 1))
        self.coolDownCount = 0

        # Movement speed attributes
        self.normalSpeed = 1
        self.chargeSpeed = 6
        self.angryChargeSpeed = 8

        # Noise for random movement
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0

        # Image attributes
        self.image = leBroImage

        # Initialize the regular movement state
        self.initRegularState()

    def update(self, target, layout):
        '''Updates the leBro every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'normal':
            self.doRegularMovement(target, layout)  # Perform regular movement
        elif self.state == 'charge':
            self.doCharge(layout)  # Perform charge behavior

    def initRegularState(self):
        '''Initializes the regular movement state.'''
        self.state = 'normal'
        self.velo = np.array([0.0, 0.0])  # Reset velocity
        if self.mentalState == 'calm':
            self.coolDownCount = random.randint(*self.calmCooldDownBounds)  # Set a random cool down duration

    def doRegularMovement(self, target, layout):
        '''Moves randomly using Perlin noise and checks if it can charge at the player.'''
        direction = [self.noise(self.noiseIterations), self.noise(self.noiseIterations + 1000.00907)]  # Generate random direction
        if direction != [0, 0]:  # Ensure direction is not (0, 0) to avoid errors
            self.velo = npVM.scaleVector(direction, self.normalSpeed)  # Scale direction to speed
        else:
            self.velo = np.array([0.0, 0.0])  # Set velocity to zero if direction is invalid
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        self.noiseIterations += random.uniform(0.000005, 0.00001)  # Increment noise iterations for smooth movement

        self.coolDownCount -= 1  # Decrement cool down counter
        if self.coolDownCount <= 0:  # Check if cool down is complete
            if self.checkIfCanSeeTarget(target, layout):  # Check if the target is visible
                self.initCharge(target)  # Initialize charge behavior

    def initCharge(self, target):
        '''Initializes the charge behavior.'''
        self.state = 'charge'
        targetCenter = target.body.position  # Get the target's position
        targetDirection = targetCenter - self.body.position  # Calculate the direction to the target
        if self.mentalState == 'calm':
            self.velo = npVM.scaleVector(targetDirection, self.chargeSpeed)  # Scale direction to charge speed
        elif self.mentalState == 'angry':
            self.velo = npVM.scaleVector(targetDirection, self.angryChargeSpeed)  # Scale direction to angry charge speed

    def doCharge(self, layout):
        '''Handles the charge movement and stops if it collides with obstacles.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        if self.checkIfInGroundObstacle(layout):  # Check if the enemy collides with an obstacle
            self.initRegularState()  # Return to the regular movement state

    def checkIfInGroundObstacle(self, layout):
        '''Checks if the leBro is inside a ground obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)  # Get the tile coordinates
        for col in range(yTile - 1, yTile + 2):  # Check surrounding tiles
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 1, xTile + 2):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle:  # If the tile is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False  # Return false if no collision is detected

    def checkIfCanSeeTarget(self, target, layout):
        '''Checks if there is a clear line of sight to the target.'''
        selfLPoints = self.getLPoints()  # Get the line points of the enemy
        targetLPoints = target.getLPoints()  # Get the line points of the target
        for i in range(4):  # Iterate through the line points
            interectedRowCols = bFC.getLineIntersectRowColQuadrants(selfLPoints[i], targetLPoints[i])  # Get the intersected tiles
            for rowCol in interectedRowCols:  # Iterate through the intersected tiles
                for oTile in layout[rowCol[0]][rowCol[1]]:  # Iterate through the objects in the tile
                    if oTile.isEnemyGroundObstacle:  # Check if the object is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.linePolygonCollision(selfLPoints[i], targetLPoints[i], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.lineCircleCollision(selfLPoints[i], targetLPoints[i], oTile.body.position, oTile.radius): 
                                return False
        return True  # Return true if no collision is detected

    def doDeathEffect(self):
        '''Handles the death effect by angering all other leBro enemies.'''
        self.oPrinceEventHandler.addEvent(pEC.angerEnemiesOfCertainTypeEvent(leBro))  # Trigger anger event for leBro enemies

    def draw(self):
        '''Draws the leBro to the screen.'''
        if self.mentalState == 'calm':  # Check the mental state to determine the image
            image = leBroImage
        else:
            image = leBroImageAngry
        drawPos = np.array([self.body.position[0] - image.get_width() / 2, self.body.position[1] - image.get_height() / 2])  # Calculate draw position
        self.screen.blit(image, drawPos)  # Draw the image at the calculated position



class leBombBro(enemy):
    '''A boss enemy that moves randomly and charges at the player, exploding on collision with obstacles.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.3, height=bGI.basicTileHeight*1.3, health=60, damage=1):
        '''Initializes the leBombBro enemy with movement, charging, and explosion behavior.'''
        clr = (0, 0, 0)  # Black color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         isBoss=True, hasDeathEffect=True, needsTarget=True, needsLayout=True, doesBounceBack=False, recievesExplosionDamage=False)

        # Mental state attributes
        self.mentalState = 'calm'

        # Cool down attributes
        self.calmCooldDownBounds = (int(bGI.fps * 0.5), int(bGI.fps * 1))
        self.coolDownCount = 0

        # Movement speed attributes
        self.normalSpeed = 1
        self.chargeSpeed = 6
        self.angryChargeSpeed = 8

        # Noise for random movement
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0

        # Initialize the regular movement state
        self.initRegularState()

    def update(self, target, layout):
        '''Updates the leBombBro every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'normal':
            self.doRegularMovement(target, layout)  # Perform regular movement
        elif self.state == 'charge':
            self.doCharge(layout)  # Perform charge behavior

    def initRegularState(self):
        '''Initializes the regular movement state.'''
        self.state = 'normal'
        self.velo = np.array([0.0, 0.0])  # Reset velocity
        if self.mentalState == 'calm':
            self.coolDownCount = random.randint(*self.calmCooldDownBounds)  # Set a random cool down duration

    def doRegularMovement(self, target, layout):
        '''Moves randomly using Perlin noise and checks if it can charge at the player.'''
        direction = [self.noise(self.noiseIterations), self.noise(self.noiseIterations + 1000.00907)]  # Generate random direction
        if direction != [0, 0]:  # Ensure direction is not (0, 0) to avoid errors
            self.velo = npVM.scaleVector(direction, self.normalSpeed)  # Scale direction to speed
        else:
            self.velo = np.array([0.0, 0.0])  # Set velocity to zero if direction is invalid
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        self.noiseIterations += random.uniform(0.000005, 0.00001)  # Increment noise iterations for smooth movement

        self.coolDownCount -= 1  # Decrement cool down counter
        if self.coolDownCount <= 0:  # Check if cool down is complete
            if self.checkIfCanSeeTarget(target, layout):  # Check if the target is visible
                self.initCharge(target)  # Initialize charge behavior

    def initCharge(self, target):
        '''Initializes the charge behavior.'''
        self.state = 'charge'
        targetCenter = target.body.position  # Get the target's position
        targetDirection = targetCenter - self.body.position  # Calculate the direction to the target
        if self.mentalState == 'calm':
            self.velo = npVM.scaleVector(targetDirection, self.chargeSpeed)  # Scale direction to charge speed
        elif self.mentalState == 'angry':
            self.velo = npVM.scaleVector(targetDirection, self.angryChargeSpeed)  # Scale direction to angry charge speed

    def doCharge(self, layout):
        '''Handles the charge movement and triggers an explosion on collision with obstacles.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        if self.checkIfInGroundObstacle(layout):  # Check if the enemy collides with an obstacle
            oExplosion = bC.explosion(self.screen, self.space, self.oPrinceEventHandler, self.body.position)  # Create an explosion
            self.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))  # Add the explosion to the room
            self.initRegularState()  # Return to the regular movement state

    def checkIfInGroundObstacle(self, layout):
        '''Checks if the leBombBro is inside a ground obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)  # Get the tile coordinates
        for col in range(yTile - 1, yTile + 2):  # Check surrounding tiles
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 1, xTile + 2):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyGroundObstacle:  # If the tile is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False  # Return false if no collision is detected

    def checkIfCanSeeTarget(self, target, layout):
        '''Checks if there is a clear line of sight to the target.'''
        selfLPoints = self.getLPoints()  # Get the line points of the enemy
        targetLPoints = target.getLPoints()  # Get the line points of the target
        for i in range(4):  # Iterate through the line points
            interectedRowCols = bFC.getLineIntersectRowColQuadrants(selfLPoints[i], targetLPoints[i])  # Get the intersected tiles
            for rowCol in interectedRowCols:  # Iterate through the intersected tiles
                for oTile in layout[rowCol[0]][rowCol[1]]:  # Iterate through the objects in the tile
                    if oTile.isEnemyGroundObstacle:  # Check if the object is a ground obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.linePolygonCollision(selfLPoints[i], targetLPoints[i], oTile.getLPoints()): 
                                return False
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.lineCircleCollision(selfLPoints[i], targetLPoints[i], oTile.body.position, oTile.radius): 
                                return False
        return True  # Return true if no collision is detected

    def doDeathEffect(self):
        '''Handles the death effect by angering all other leBombBro enemies.'''
        self.oPrinceEventHandler.addEvent(pEC.angerEnemiesOfCertainTypeEvent(leBombBro))  # Trigger anger event for leBombBro enemies

    def draw(self):
        '''Draws the leBombBro to the screen.'''
        if self.mentalState == 'calm':  # Check the mental state to determine the image
            image = leBombBroImage
        else:
            image = leBombBroImageAngry
        drawPos = np.array([self.body.position[0] - image.get_width() / 2, self.body.position[1] - image.get_height() / 2])  # Calculate draw position
        self.screen.blit(image, drawPos)  # Draw the image at the calculated position


class bigHead(enemy):
    '''A boss enemy that moves using a vector field and spawns a smallHead enemy.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*.95, height=bGI.basicTileHeight*.95, health=35, damage=1):
        '''Initializes the bigHead enemy with movement, spawning, and bounce back behavior.'''
        clr = (255, 182, 193)  # Fleshy pink color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         isBoss=True, needsGroundVField=True, doesBounceBack=False, hasDeathEffect=True, spawnsEnemiesOnDeath=True)
        
        self.state = 'normal'  # Initial state is normal
        self.velo = np.array([0.0, 0.0])  # Velocity vector
        self.speed = 2  # Movement speed

        self.spawnedInSmallHead = False  # Flag to check if smallHead has been spawned
    
    def update(self, vField):
        '''Updates the bigHead every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if not self.spawnedInSmallHead:
            self.spawnInSmallHead()  # Spawn a smallHead if not already spawned
        self.doMovement(vField)  # Perform movement behavior

    def spawnInSmallHead(self):
        '''Spawns a smallHead enemy and links it to the bigHead.'''
        self.spawnedInSmallHead = True  # Set the flag to true
        self.smallHead = smallHead(self.screen, self.space, self.oPrinceEventHandler, self.body.position, bigHead=self)  # Create a smallHead
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(self.smallHead))  # Add the smallHead to the game
    
    def doMovement(self, vField):
        '''Moves the bigHead using a vector field.'''
        rowCols = []  # List to store the tiles the bigHead is in
        # Get the row and column of the tiles the bigHead overlaps
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] - self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0] + self.width / 2, self.body.position[1]])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] - self.height / 2])))
        rowCols.append(bFC.xYNPArrayIntoRoomLayoutRowColTuple(np.array([self.body.position[0], self.body.position[1] + self.height / 2])))
        
        direction = np.array([0.0, 0.0])  # Initialize direction vector
        for rowCol in rowCols:  # Iterate through the tiles
            if type(vField[rowCol[0]][rowCol[1]]) != np.ndarray: 
                continue  # Skip if the tile does not contain a vector
            if rowCol[0] < 0 or rowCol[0] >= len(vField): 
                continue  # Skip if the row is out of bounds
            if rowCol[1] < 0 or rowCol[1] >= len(vField[0]): 
                continue  # Skip if the column is out of bounds
            direction = np.add(direction, vField[rowCol[0]][rowCol[1]])  # Add the vector from the tile to the direction
        
        if direction[0] != 0 or direction[1] != 0:  # If the direction is not zero
            self.velo = npVM.scaleVector(direction, self.speed)  # Scale the direction to the speed
            self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
            
    def doDeathEffect(self):
        '''Handles the death effect by unlinking the smallHead from the bigHead.'''
        self.smallHead.bigHead = None  # Unlink the smallHead from the bigHead
    
    def draw(self):
        '''Draws the bigHead to the screen.'''
        drawPos = np.array([self.body.position[0] - bigHeadImage.get_width() / 2, self.body.position[1] - bigHeadImage.get_height() / 2])
        self.screen.blit(bigHeadImage, drawPos)  # Draw the image at the calculated position

class smallHead(enemy):
    '''A smaller enemy that moves towards the player and stays within a certain distance of its bigHead.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth * 0.6, height=bGI.basicTileHeight * 0.6, health=25, damage=1, bigHead=None):
        '''Initializes the smallHead enemy with movement, shooting, and bounce back behavior.'''
        clr = (6, 114, 160)  # Fleshy pink color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, isBoss=True,
                         needsTarget=True, flying=True, doesBounceBack=True)
        
        # Attributes for maintaining distance from the bigHead
        self.maxDistanceFromBigHead = bGI.basicTileWidth * 3
        self.bigHead = bigHead
        
        # State and movement attributes
        self.state = 'attack'
        self.velo = np.array([0.0, 0.0])
        self.speed = 3
        
        # Bounce back attributes
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0
        
        # Shooting attributes
        self.shotCoolDownBounds = (int(bGI.fps * 1), int(bGI.fps * 2))
        self.shotCoolDownCount = 0
        self.tearSpeed = 4
        self.tearRange = 7
        self.tearRadius = 10
        
    def update(self, target):
        '''Updates the smallHead every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'attack':
            self.doAttack(target)  # Perform attack behavior
        self.doShooting(target)  # Perform shooting behavior
        if self.bigHead is not None:
            self.fixDistanceFromBigHead()  # Ensure it stays within a certain distance of the bigHead
    
    def doShooting(self, target):
        '''Handles shooting behavior.'''
        targetPos = target.body.position
        if self.shotCoolDownCount > 0:
            self.shotCoolDownCount -= 1  # Decrement the shot cooldown
        else:
            self.shotCoolDownCount = random.randint(*self.shotCoolDownBounds)  # Reset the cooldown
            self.shootTear(targetPos)  # Shoot a tear at the target
    
    def shootTear(self, targetPos):
        '''Shoots a tear towards the target.'''
        targetDirection = targetPos - self.body.position  # Calculate the direction to the target
        tearVelo = pk.Vec2d(*npVM.scaleVector(targetDirection, self.tearSpeed))  # Scale the direction to the tear speed
        oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVelo, self.tearRange)  # Create a tear object
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
    
    def fixDistanceFromBigHead(self):
        '''Ensures the smallHead stays within a certain distance of the bigHead.'''
        bigHeadPos = self.bigHead.body.position  # Get the position of the bigHead
        distance = math.dist(self.body.position, bigHeadPos)  # Calculate the distance to the bigHead
        if distance > self.maxDistanceFromBigHead:  # Check if the distance exceeds the maximum allowed
            direction = self.body.position - bigHeadPos  # Calculate the direction away from the bigHead
            direction = npVM.scaleVector(direction, self.maxDistanceFromBigHead)  # Scale the direction to the maximum distance
            self.body.position = self.bigHead.body.position + pk.Vec2d(*direction)  # Update the position to stay within the maximum distance
            
    def initAttack(self):
        '''Initializes the attack state.'''
        self.state = 'attack'
        
    def doAttack(self, target):
        '''Handles attack behavior by moving towards the target.'''
        targetCenter = target.body.position  # Get the target's position
        targetDirection = targetCenter - self.body.position  # Calculate the direction to the target
        self.velo = npVM.scaleVector(targetDirection, self.speed)  # Scale the direction to the speed
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on velocity
        
    def initBounceBack(self, direction):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back
    
    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.initAttack()  # Return to the attack state
            
    def doDeathEffect(self):
        '''Handles the death effect by unlinking the smallHead from the bigHead.'''
        if self.bigHead is not None:
            self.bigHead.smallHead = None  # Unlink the smallHead from the bigHead
            
    def draw(self):
        '''Draws the smallHead to the screen.'''
        if self.bigHead is not None:
            # Draw a line from the smallHead to the bigHead
            p.draw.line(self.screen, self.clr, self.body.position, self.bigHead.body.position, 5)
        drawPos = np.array([self.body.position[0] - smallHeadImage.get_width() / 2, self.body.position[1] - smallHeadImage.get_height() / 2])  # Calculate draw position
        self.screen.blit(smallHeadImage, drawPos)  # Draw the image at the calculated position
            
class miniJackBlack(enemy):
    '''A smaller version of the Jack Black boss enemy that moves randomly and shoots tears in three directions.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=30, height=45, health=15, damage=1):
        '''Initializes the miniJackBlack enemy with movement, shooting, and bounce back behavior.'''
        clr = (0, 0, 255)  # Blue color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         flying=True, needsTarget=True)
        
        # State and movement attributes
        self.state = 'move'
        self.bounceBackSpeed = 5
        self.bounceBackDuration = 5
        self.bounceBackCount = 0

        # Shooting attributes
        self.framesBetweenShots = bGI.fps * 0.9
        self.currentShotIteration = self.framesBetweenShots
        self.movementSpeed = 0.2

        self.maxTargetDistanceToShoot = 8 * bGI.basicTileWidth
        self.maxTargetDistanceToMove = 10 * bGI.basicTileWidth

        self.tearSpeed = 4
        self.tearRange = 10
        self.tearRadius = 12
        self.angleOfShotsFromTargetDirection = math.pi / 9  # Angle for V-shaped shots

        # Noise for random movement
        self.noise = PerlinNoise(octaves=1000, seed=random.randint(0, 100000))
        self.noiseIterations = 0

    def update(self, target):
        '''Updates the miniJackBlack every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        targetPos = target.body.position
        if self.state == 'bounce back':
            self.doBounceBack()  # Perform bounce back behavior
        elif self.state == 'move':
            self.doRegularMovement()  # Perform regular movement
        self.doShooting(targetPos)  # Perform shooting behavior
        
    def doRegularMovement(self):
        '''Moves randomly using Perlin noise.'''
        self.velo = [2 * self.noise(self.noiseIterations), 2 * self.noise(self.noiseIterations + 10000)]  # Generate random velocity
        self.body.position += pk.Vec2d(*self.velo)  # Update position based on velocity
        self.noiseIterations += 0.00001  # Increment noise iterations for smooth movement
        
    def doShooting(self, targetPos):
        '''Handles shooting behavior.'''
        targetDist = math.dist(targetPos, self.body.position)  # Calculate the distance to the target
        if self.currentShotIteration > 0:
            self.currentShotIteration -= 1  # Decrement the shot cooldown
        elif targetDist <= self.maxTargetDistanceToShoot:  # Check if the target is within range
            self.currentShotIteration = self.framesBetweenShots  # Reset the cooldown
            self.shootTears(targetPos)  # Shoot tears at the target

    def shootTears(self, targetPos):
        '''Shoots tears in three directions: forward, clockwise, and counterclockwise.'''
        targetDirection = targetPos - self.body.position  # Calculate the direction to the target
        tearVelo = pk.Vec2d(*npVM.scaleVector(targetDirection, self.tearSpeed))  # Scale the direction to the tear speed
        tearVeloCW = npVM.rotateVector(tearVelo, self.angleOfShotsFromTargetDirection)  # Clockwise tear
        tearVeloCCW = npVM.rotateVector(tearVelo, -self.angleOfShotsFromTargetDirection)  # Counterclockwise tear

        # Spawn the tears
        oTearCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCW))
        oTearCCW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVeloCCW, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearCCW))
        oTearFW = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position, self.tearRadius, tearVelo, self.tearRange)
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTearFW))
    
    def initBounceBack(self, direction: np.ndarray):
        '''Initializes the bounce back behavior.'''
        self.bounceBackDirection = direction  # Set the direction of bounce back
        self.bounceBackCount = 0  # Reset the bounce back counter
        self.velo = npVM.scaleVector(direction, self.bounceBackSpeed)  # Scale the direction to the bounce back speed
        self.state = 'bounce back'  # Set the state to bounce back

    def doBounceBack(self):
        '''Handles the bounce back movement.'''
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on the velocity
        if self.bounceBackCount < self.bounceBackDuration:  # Check if the bounce back duration is not exceeded
            self.bounceBackCount += 1  # Increment the bounce back counter
        else:
            self.state = 'move'  # Return to the movement state
            
    def draw(self):
        '''Draws the miniJackBlack to the screen.'''
        drawPos = np.array([self.body.position[0] - miniJackBlackImage.get_width() / 2, self.body.position[1] - miniJackBlackImage.get_height() / 2])  # Calculate draw position
        self.screen.blit(miniJackBlackImage, drawPos)  # Draw the image at the calculated position
  
class jackBlack(enemy):
    '''A boss enemy that teleports, spawns miniJackBlack enemies, and shoots tears in multiple directions.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.42, height=bGI.basicTileHeight*2.2, health=150, damage=1):
        '''Initializes the jackBlack enemy with movement, teleportation, spawning, and shooting behavior.'''
        clr = (0, 0, 255)  # Blue color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         flying=True, needsTarget=True, doesBounceBack=False, needsLayout=True, isBoss=True)
        
        # Attack options and cooldown attributes
        self.attackOptions = ['tp', 'spawn', 'shoot']
        self.coolDownBounds = (int(bGI.fps * 1.3), int(bGI.fps * 2))
        self.coolDownCount = 0
        self.attackType = None
        
        # Teleportation attributes
        self.minDistanceToTargetToTP = 4 * bGI.basicTileWidth

        # Shooting attributes
        self.numTearsPerShot = 5
        self.numShots = 3
        self.shotCount = 0
        self.framesBetweenShots = bGI.fps * 0.3
        self.framesBetweenShotsCount = 0
        self.shotAngles = [math.pi / 7, -math.pi / 7, 0]
        self.shotSpread = math.pi / 7
        self.angleBetweenTears = self.shotSpread / self.numTearsPerShot

        self.tearSpeed = 6
        self.tearRange = 10
        self.tearRadius = 10

        # Spawning attributes
        self.numSpawnAmount = 1
        
        # Velocity vector
        self.velo = np.array([0.0, 0.0])
        self.initCoolDown()
        
    def update(self, target, layout):
        '''Updates the jackBlack every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'cool down':
            self.doCoolDown(target)  # Perform cooldown behavior
        elif self.state == 'attack':
            self.doAttack(target, layout)  # Perform attack behavior
            
    def initCoolDown(self):
        '''Initializes the cooldown state.'''
        self.state = 'cool down'
        self.coolDownCount = random.randint(*self.coolDownBounds)  # Set a random cooldown duration
    
    def doCoolDown(self, target):
        '''Handles the cooldown behavior.'''
        self.coolDownCount -= 1  # Decrement the cooldown counter
        if self.coolDownCount <= 0:  # If cooldown is complete, start an attack
            self.initAttack(target)

    def shoot(self, direction):
        '''Shoots tears in multiple directions.'''
        for i in range(self.numTearsPerShot):
            rotateAmount = -1 * (self.numTearsPerShot // 2) + i
            rotateAmount *= self.angleBetweenTears
            newDirection = npVM.rotateVector(direction, rotateAmount)  # Rotate the direction for each tear
            tearVelo = npVM.scaleVector(newDirection, self.tearSpeed)  # Scale the velocity to the tear speed
            oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                 self.tearRadius, tearVelo, self.tearRange)  # Create a tear object
            self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear

    def initAttack(self, target):
        '''Initializes an attack.'''
        self.state = 'attack'
        attackType = random.choice(self.attackOptions)  # Choose a random attack type
        if attackType == 'tp':
            self.initTeleport()  # Initialize teleportation
        elif attackType == 'spawn':
            self.initSpawn()  # Initialize spawning
        elif attackType == 'shoot':
            self.initShoot(target)  # Initialize shooting
    
    def doAttack(self, target, layout):
        '''Handles the attack behavior.'''
        if self.currentAttack == 'tp':
            self.doTeleport(target, layout)  # Perform teleportation
        elif self.currentAttack == 'shoot':
            self.doShoot()  # Perform shooting
        elif self.currentAttack == 'spawn':
            self.doSpawn(layout)  # Perform spawning

    def initShoot(self, target):
        '''Initializes the shooting behavior.'''
        self.currentAttack = 'shoot'
        self.shotCount = self.numShots  # Reset the shot count
        self.framesBetweenShotsCount = 0  # Reset the cooldown between shots
        self.shootingDirection = target.body.position - self.body.position  # Calculate the direction to the target
    
    def doShoot(self):
        '''Handles the shooting behavior.'''
        if self.framesBetweenShotsCount <= 0:  # If the cooldown between shots is complete
            self.shotCount -= 1  # Decrement the remaining shots
            direction = npVM.rotateVector(self.shootingDirection, self.shotAngles[self.shotCount])  # Rotate the shooting direction
            self.shoot(direction)  # Shoot tears in the rotated direction
            if self.shotCount == 0:  # If no shots are left, return to cooldown state
                self.initCoolDown()
            self.framesBetweenShotsCount = self.framesBetweenShots  # Reset the cooldown counter
        else:
            self.framesBetweenShotsCount -= 1  # Decrement the cooldown counter
        
    def initTeleport(self):
        '''Initializes the teleportation behavior.'''
        self.currentAttack = 'tp'
    
    def doTeleport(self, target, layout):
        '''Handles the teleportation behavior.'''
        while True:
            x = random.randint(0, int((bGI.numTilesWide - 1) * bGI.basicTileWidth))
            y = random.randint(0, int((bGI.numTilesHigh - 1) * bGI.basicTileHeight))
            pos = np.array([x, y])  # Generate a random position
            self.body.position = pk.Vec2d(*pos)  # Set the position
            if not self.checkIfInAirObstacle(layout):  # Check if the position is not in an air obstacle
                if self.checkIfFarEnoughFromTargetToTP(target):  # Check if the position is far enough from the target
                    break
        self.initCoolDown()  # Return to cooldown state

    def initSpawn(self):
        '''Initializes the spawning behavior.'''
        self.currentAttack = 'spawn'
    
    def doSpawn(self, layout):
        '''Handles the spawning behavior by spawning miniJackBlack enemies.'''
        centerRowCol = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        minCol = max(0, centerRowCol[1] - 2)
        maxCol = min(bGI.numTilesWide - 1, centerRowCol[1] + 2)
        minRow = max(0, centerRowCol[0] - 2)
        maxRow = min(bGI.numTilesHigh - 1, centerRowCol[0] + 2)
        
        possibleRowCols = [(row, minCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(row, maxCol) for row in range(minRow, maxRow + 1)]
        possibleRowCols += [(minRow, col) for col in range(minCol + 1, maxRow)]
        possibleRowCols += [(maxRow, col) for col in range(minCol + 1, maxRow)]

        for i in range(self.numSpawnAmount):  # Spawn the specified number of miniJackBlack enemies
            while True:
                spot = random.choice(possibleRowCols)  # Choose a random spawn location
                if layout[spot[0]][spot[1]] != bGI.empty:  # Check if the location is not empty
                    for oTile in layout[spot[0]][spot[1]]:
                        if oTile.isEnemyAirObstacle:  # Check if the location is not blocked
                            blocked = True
                    if blocked:
                        continue
                break
            oMiniJB = miniJackBlack(self.screen, self.space, self.oPrinceEventHandler, ((spot[1] + 0.5) * bGI.basicTileWidth, (spot[0] + 0.5) * bGI.basicTileHeight))
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oMiniJB))  # Add the miniJackBlack to the game
        
        self.initCoolDown()  # Return to cooldown state
        
    def checkIfInAirObstacle(self, layout):
        '''Checks if the jackBlack is inside an air obstacle.'''
        yTile, xTile = bFC.xYNPArrayIntoRoomLayoutRowColTuple(self.body.position)
        for col in range(yTile - 2, yTile + 3):  # Check surrounding tiles
            if col < 0 or col >= len(layout): 
                continue
            for row in range(xTile - 3, xTile + 4):
                if row < 0 or row >= len(layout[0]): 
                    continue
                for oTile in layout[col][row]:
                    if oTile.isEnemyAirObstacle:  # If the tile is an air obstacle
                        if oTile.geometry == 'rect':  # Check for collision with a rectangular obstacle
                            if bFC.polygonPolygonCollision(self.getLPoints(), oTile.getLPoints()): 
                                return True
                        elif oTile.geometry == 'circle':  # Check for collision with a circular obstacle
                            if bFC.polygonCircleCollision(self.getLPoints(), oTile.body.position, oTile.radius): 
                                return True
        return False  # Return false if no collision is detected
    
    def checkIfFarEnoughFromTargetToTP(self, target):
        '''Checks if the jackBlack is far enough from the target to teleport.'''
        distance = bFC.getDistanceBetween2RectsEdges(self.getLPoints(), target.getLPoints())  # Calculate the distance to the target
        if distance > self.minDistanceToTargetToTP:  # Check if the distance exceeds the minimum required
            return True
        return False  # Return false if the distance is not sufficient
    
    def draw(self):
        '''Draws the jackBlack to the screen.'''
        drawPos = np.array([self.body.position[0] - jackBlackImage.get_width() / 2, self.body.position[1] - jackBlackImage.get_height() / 2])  # Calculate draw position
        self.screen.blit(jackBlackImage, drawPos)  # Draw the image at the calculated position
    

class longDivider(enemy):
    '''A boss enemy that moves in a random direction and splits into two shortDividers upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*3.9, height=bGI.basicTileWidth*3.9, health=40, damage=1):
        '''Initializes the longDivider enemy with movement and splitting behavior.'''
        clr = (255, 255, 255)  # White color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         doesBounceBack=False, bouncesOffObstacles=True, isBoss=True, hasDeathEffect=True)
        speed = 3  # Movement speed
        while True:
            direction = pk.Vec2d(random.randint(-1000, 1000), random.randrange(-1000, 1000))  # Generate a random direction
            if direction[0] != 0 or direction[1] != 0:  # Ensure the direction is not zero
                break
        self.velo = npVM.scaleVector(direction, speed)  # Scale the direction to the speed

    def update(self):
        '''Updates the longDivider every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on velocity

    def doDeathEffect(self):
        '''Handles the death effect by spawning two shortDividers upon death.'''
        leftDivider = shortDivider(self.screen, self.space, self.oPrinceEventHandler, self.body.position - pk.Vec2d(self.width / 2, 0))
        rightDivider = shortDivider(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(self.width / 2, 0))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(leftDivider))  # Add the left shortDivider to the game
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(rightDivider))  # Add the right shortDivider to the game
        
    def draw(self):
        '''Draws the longDivider to the screen.'''
        drawPos = np.array([self.body.position[0] - longDividerImage.get_width() / 2, self.body.position[1] - longDividerImage.get_height() / 2])
        self.screen.blit(longDividerImage, drawPos)  # Draw the image at the calculated position

class shortDivider(enemy):
    '''A smaller boss enemy that moves in a random direction and splits into two miniDividers upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.9, height=bGI.basicTileWidth*1.9, health=30, damage=1):
        '''Initializes the shortDivider enemy with movement and splitting behavior.'''
        clr = (255, 255, 255)  # White color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         doesBounceBack=False, bouncesOffObstacles=True, isBoss=True, hasDeathEffect=True)
        speed = 5  # Movement speed
        while True:
            direction = pk.Vec2d(random.randint(-1000, 1000), random.randrange(-1000, 1000))  # Generate a random direction
            if direction[0] != 0 or direction[1] != 0:  # Ensure the direction is not zero
                break
        self.velo = npVM.scaleVector(direction, speed)  # Scale the direction to the speed

    def update(self):
        '''Updates the shortDivider every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on velocity

    def doDeathEffect(self):
        '''Handles the death effect by spawning two miniDividers upon death.'''
        leftDivider = miniDivider(self.screen, self.space, self.oPrinceEventHandler, self.body.position - pk.Vec2d(self.width / 2, 0))
        rightDivider = miniDivider(self.screen, self.space, self.oPrinceEventHandler, self.body.position + pk.Vec2d(self.width / 2, 0))
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(leftDivider))  # Add the left miniDivider to the game
        self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(rightDivider))  # Add the right miniDivider to the game
    
    def draw(self):
        '''Draws the shortDivider to the screen.'''
        drawPos = np.array([self.body.position[0] - shortDividerImage.get_width() / 2, self.body.position[1] - shortDividerImage.get_height() / 2])
        self.screen.blit(shortDividerImage, drawPos)  # Draw the image at the calculated position

class miniDivider(enemy):
    '''A smaller enemy that moves in a random direction and does not split upon death.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*1.2, height=bGI.basicTileWidth*1.2, health=20, damage=1):
        '''Initializes the miniDivider enemy with movement behavior.'''
        clr = (255, 255, 255)  # White color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         doesBounceBack=False, bouncesOffObstacles=True, isBoss=True)
        speed = 5  # Movement speed
        while True:
            direction = pk.Vec2d(random.randint(-1000, 1000), random.randrange(-1000, 1000))  # Generate a random direction
            if direction[0] != 0 or direction[1] != 0:  # Ensure the direction is not zero
                break
        self.velo = npVM.scaleVector(direction, speed)  # Scale the direction to the speed

    def update(self):
        '''Updates the miniDivider every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        self.body.position += pk.Vec2d(*self.velo)  # Update the position based on velocity
    
    def draw(self):
        '''Draws the miniDivider to the screen.'''
        drawPos = np.array([self.body.position[0] - miniDividerImage.get_width() / 2, self.body.position[1] - miniDividerImage.get_height() / 2])
        self.screen.blit(miniDividerImage, drawPos)  # Draw the image at the calculated position


class mrKrabs(enemy):
    '''A boss enemy that moves horizontally or vertically and shoots tears in multiple directions.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, clr=(255, 10, 10), width=bGI.basicTileWidth*2, height=bGI.basicTileHeight*2, health=200, damage=1):
        '''Initializes the mrKrabs enemy with movement, shooting, and cooldown behavior.'''
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage,
                         isBoss=True, needsTarget=True, doesBounceBack=False)
        
        # Movement speed attributes
        self.vertSpeed = 2
        self.horSpeed = 6

        # Cooldown attributes
        self.coolDownBounds = (int(bGI.fps*2), int(bGI.fps*3))
        self.coolDownCount = 0

        # Shooting attributes
        self.numTearsPerShot = 12
        self.totalShots = 3
        self.shotCount = 0
        self.framesBetweenShots = bGI.fps * 0.3
        self.framesBetweenShotsCount = 0
        self.shotStartAngles = [math.pi / 12, 0, math.pi / 12]
        self.angleBetweenTears = 2 * math.pi / self.numTearsPerShot

        self.tearSpeed = 6
        self.tearRange = 10
        self.tearRadius = 10
        self.tearClr = (255, 200, 0)

        # Initialize the movement state
        self.initMovement()

    def update(self, target):
        '''Updates the mrKrabs every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'move':
            self.doMovement(target)  # Perform movement behavior
        elif self.state == 'shoot':
            self.doShoot()  # Perform shooting behavior

    def initMovement(self):
        '''Initializes the movement state.'''
        self.state = 'move'
        self.coolDownCount = random.randint(*self.coolDownBounds)  # Set a random cooldown duration
    
    def doMovement(self, target):
        '''Handles movement behavior by moving horizontally or vertically towards the target.'''
        self.coolDownCount -= 1  # Decrement the cooldown counter
        xDist = target.body.position[0] - self.body.position[0]  # Calculate horizontal distance to the target
        yDist = target.body.position[1] - self.body.position[1]  # Calculate vertical distance to the target

        # Determine movement direction based on proximity to the target
        if abs(yDist) <= target.height / 2 + self.height / 2:  # If aligned vertically with the target
            if xDist < 0:
                self.velo = np.array([-self.horSpeed, 0])  # Move left
            else:
                self.velo = np.array([self.horSpeed, 0])  # Move right
        else:  # Otherwise, move vertically
            if yDist < 0:
                self.velo = np.array([0, -self.vertSpeed])  # Move up
            else:
                self.velo = np.array([0, self.vertSpeed])  # Move down
        
        # Update position based on velocity
        self.body.position += pk.Vec2d(*self.velo)

        # If cooldown is complete, initialize shooting behavior
        if self.coolDownCount <= 0:
            self.initShoot()

    def initShoot(self):
        '''Initializes the shooting behavior.'''
        self.state = 'shoot'
        self.shotCount = self.totalShots  # Reset the shot count
        self.framesBetweenShotsCount = 0  # Reset the cooldown between shots
    
    def doShoot(self):
        '''Handles the shooting behavior by shooting tears in multiple directions.'''
        if self.framesBetweenShotsCount <= 0:  # If the cooldown between shots is complete
            self.shotCount -= 1  # Decrement the remaining shots
            direction = npVM.rotateVector(np.array([1, 0]), self.shotStartAngles[self.shotCount])  # Rotate the shooting direction
            self.shoot(direction)  # Shoot tears in the rotated direction
            if self.shotCount == 0:  # If no shots are left, return to movement state
                self.initMovement()
            self.framesBetweenShotsCount = self.framesBetweenShots  # Reset the cooldown counter
        else:
            self.framesBetweenShotsCount -= 1  # Decrement the cooldown counter
    
    def shoot(self, direction):
        '''Shoots tears in multiple directions based on the given direction.'''
        for i in range(self.numTearsPerShot):
            rotateAmount = -1 * (self.numTearsPerShot // 2) + i  # Calculate the rotation amount for each tear
            rotateAmount *= self.angleBetweenTears
            newDirection = npVM.rotateVector(direction, rotateAmount)  # Rotate the direction for each tear
            tearVelo = npVM.scaleVector(newDirection, self.tearSpeed)  # Scale the velocity to the tear speed
            oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                 self.tearRadius, tearVelo, self.tearRange, clr=self.tearClr)  # Create a tear object
            self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
            
    def draw(self):
        '''Draws the mrKrabs to the screen.'''
        drawPos = np.array([self.body.position[0] - mrKrabsImage.get_width() / 2, self.body.position[1] - mrKrabsImage.get_height() / 2])  # Calculate draw position
        self.screen.blit(mrKrabsImage, drawPos)  # Draw the image at the calculated position
        
class chemistry(enemy):
    '''A boss enemy with multiple attack patterns, including spawning other bosses, shooting tears, and rapid fire.'''
    def __init__(self, screen, space, oPrinceEventHandler, center, width=bGI.basicTileWidth*3, height=bGI.basicTileHeight*3, health=300, damage=1):
        '''Initializes the chemistry boss with various attack patterns and cooldown behavior.'''
        clr = (0, 255, 100)  # Green color
        super().__init__(screen, space, oPrinceEventHandler, clr, center, width, height, health, damage, 
                         isBoss=True, needsTarget=True, doesBounceBack=False, hasDeathEffect=True)
        
        # Attack options
        self.attackOptions = ['spawn', 'shoot all round', 'shotgun', 'rapid fire at target', 'exploding shot']
        self.currentAttack = None
        self.coolDownBounds = (int(bGI.fps * 0.2), int(bGI.fps * 1))  # Cooldown duration bounds
        self.coolDownCount = 0

        # Spawn attributes
        self.spawnBossesOptions = [bigHead, leBombBro, leBro, lordOfTheFlies]  # Bosses that can be spawned
        self.spawnCenters = [(8.5 * bGI.basicTileWidth, 6.5 * bGI.basicTileHeight), (15.5 * bGI.basicTileWidth, 6.5 * bGI.basicTileHeight)]  # Spawn locations
        self.numBossesSpawnedBounds = (1, 1)  # Number of bosses to spawn
        self.spawnAdditionCoolDownBounds = (int(bGI.fps * 1), int(bGI.fps * 3))  # Cooldown after spawning

        # Shoot all round attributes
        self.numTearsPerShot = 12  # Number of tears per shot
        self.numShotsAllRound = 10  # Total number of shots
        self.angleBetweenTears = math.pi * 2 / self.numTearsPerShot  # Angle between tears
        self.angleShift = math.pi * 2 / (self.numTearsPerShot * 2 * self.numShotsAllRound)  # Angle shift per shot
        self.framesBetweenShots = bGI.fps * 0.02  # Frames between shots
        self.framesBetweenShotsCount = 0
        self.allRoundTearRange = 10  # Range of tears
        self.allRoundTearSpeed = 5  # Speed of tears
        self.allRoundTearRadius = 10  # Radius of tears
        self.allRoundTearClr = (0, 255, 0)  # Green color for tears

        # Rapid fire attributes
        self.numShotsRapid = 20  # Number of rapid shots
        self.framesBetweenShots = bGI.fps * 0.1  # Frames between shots
        self.rapidTearRange = 15  # Range of tears
        self.rapidTearSpeed = 8  # Speed of tears
        self.rapidTearRadius = 10  # Radius of tears
        self.rapidTearClr = (0, 0, 255)  # Blue color for tears

        # Shotgun attributes
        self.shotgunTearSpeedBounds = (4, 9)  # Speed bounds for shotgun tears
        self.shotgunTearAngleShiftBounds = (0, int(2 * math.pi))  # Angle shift bounds for shotgun tears
        self.shotgunTearRadiusBounds = (7, 15)  # Radius bounds for shotgun tears
        self.shotgunTearRange = 15  # Range of shotgun tears
        self.shotgunNumTearsPerShotBounds = (15, 30)  # Number of tears per shotgun shot

        # Exploding shot attributes
        self.explodeShotSpeed = 6  # Speed of exploding shot
        self.explodeShotRange = 6  # Range of exploding shot
        self.explodeShotRadius = 15  # Radius of exploding shot

        # Velocity vector
        self.velo = np.array([0.0, 0.0])
        self.initCoolDown()  # Initialize cooldown state

    def update(self, target):
        '''Updates the chemistry boss every frame.'''
        self.pastPos = pk.Vec2d(*self.body.position)  # Save the current position for collision checks
        if self.state == 'cool down':
            self.doCoolDown()  # Perform cooldown behavior
        elif self.state == 'attack':
            self.doAttack(target)  # Perform attack behavior

    def initCoolDown(self, coolDownBounds=None):
        '''Initializes the cooldown state.'''
        self.state = 'cool down'
        if coolDownBounds is None:
            coolDownBounds = self.coolDownBounds
        self.coolDownCount = random.randint(*coolDownBounds)  # Set a random cooldown duration

    def doCoolDown(self):
        '''Handles the cooldown behavior.'''
        self.coolDownCount -= 1  # Decrement the cooldown counter
        if self.coolDownCount <= 0:  # If cooldown is complete, start an attack
            self.initAttack()

    def initAttack(self):
        '''Initializes an attack.'''
        self.state = 'attack'
        self.currentAttack = random.choice(self.attackOptions)  # Choose a random attack type
        if self.currentAttack == 'spawn':
            self.initSpawn()
        elif self.currentAttack == 'shoot all round':
            self.initShootAllRound()
        elif self.currentAttack == 'rapid fire at target':
            self.initRapid()
        elif self.currentAttack == 'shotgun':
            self.initShotgun()
        elif self.currentAttack == 'exploding shot':
            self.initExplodeShot()

    def doAttack(self, target):
        '''Handles the attack behavior.'''
        if self.currentAttack == 'spawn':
            self.doSpawn()
        elif self.currentAttack == 'shoot all round':
            self.doShootAllRound()
        elif self.currentAttack == 'rapid fire at target':
            self.doRapid(target)
        elif self.currentAttack == 'shotgun':
            self.doShotgun(target)
        elif self.currentAttack == 'exploding shot':
            self.doExplodeShot(target)

    def initSpawn(self):
        '''Initializes the spawn behavior.'''
        pass

    def doSpawn(self):
        '''Handles the spawn behavior by spawning other bosses.'''
        numBosses = random.randint(*self.numBossesSpawnedBounds)  # Number of bosses to spawn
        nonRepeatingSpawnCenters = self.spawnCenters.copy()  # Copy the spawn centers
        for i in range(numBosses):
            boss = random.choice(self.spawnBossesOptions)  # Choose a random boss to spawn
            center = nonRepeatingSpawnCenters.pop(random.randint(0, len(nonRepeatingSpawnCenters) - 1))  # Choose a random spawn location
            oBoss = boss(self.screen, self.space, self.oPrinceEventHandler, center)  # Create the boss
            self.oPrinceEventHandler.addEvent(pEC.addEnemyEvent(oBoss))  # Add the boss to the game
        self.initCoolDown(self.spawnAdditionCoolDownBounds)  # Return to cooldown state

    def initShootAllRound(self):
        '''Initializes the shoot all round behavior.'''
        self.framesBetweenShotsCount = 0  # Reset the cooldown between shots
        self.shotCount = self.numShotsAllRound  # Reset the shot count

    def doShootAllRound(self):
        '''Handles the shoot all round behavior by shooting tears in all directions.'''
        if self.framesBetweenShotsCount <= 0:  # If the cooldown between shots is complete
            self.framesBetweenShotsCount = self.framesBetweenShots  # Reset the cooldown counter
            startingDirection = npVM.rotateVector(np.array([1, 0]), self.angleShift * self.shotCount)  # Calculate the starting direction
            for j in range(self.numTearsPerShot):  # Shoot tears in all directions
                rotateAmount = j * self.angleBetweenTears
                newDirection = npVM.rotateVector(startingDirection, rotateAmount)  # Rotate the direction for each tear
                tearVelo = npVM.scaleVector(newDirection, self.allRoundTearSpeed)  # Scale the velocity to the tear speed
                oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                     self.allRoundTearRadius, tearVelo, self.allRoundTearRadius, clr=self.allRoundTearClr)  # Create a tear object
                self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
            self.shotCount -= 1  # Decrement the remaining shots
            if self.shotCount <= 0:  # If no shots are left, return to cooldown state
                self.initCoolDown()
        else:
            self.framesBetweenShotsCount -= 1  # Decrement the cooldown counter

    def initShotgun(self):
        '''Initializes the shotgun behavior.'''
        pass

    def doShotgun(self, target):
        '''Handles the shotgun behavior by shooting multiple tears in random directions.'''
        for i in range(random.randint(*self.shotgunNumTearsPerShotBounds)):  # Shoot a random number of tears
            direction = target.body.position - self.body.position  # Calculate the direction to the target
            direction = npVM.rotateVector(direction, random.randint(*self.shotgunTearAngleShiftBounds))  # Rotate the direction randomly
            tearVelo = npVM.scaleVector(direction, random.randint(*self.shotgunTearSpeedBounds))  # Scale the velocity to a random speed
            tearRadius = random.randint(*self.shotgunTearRadiusBounds)  # Choose a random radius for the tear
            oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                 tearRadius, tearVelo, self.shotgunTearRange)  # Create a tear object
            self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
        self.initCoolDown()  # Return to cooldown state

    def initRapid(self):
        '''Initializes the rapid fire behavior.'''
        self.shotCount = self.numShotsRapid  # Reset the shot count

    def doRapid(self, target):
        '''Handles the rapid fire behavior by shooting tears rapidly at the target.'''
        if self.framesBetweenShotsCount <= 0:  # If the cooldown between shots is complete
            direction = target.body.position - self.body.position  # Calculate the direction to the target
            tearVelo = npVM.scaleVector(direction, self.rapidTearSpeed)  # Scale the velocity to the tear speed
            oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                                 self.rapidTearRadius, tearVelo, self.rapidTearRange, clr=self.rapidTearClr)  # Create a tear object
            self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
            self.shotCount -= 1  # Decrement the remaining shots
            if self.shotCount <= 0:  # If no shots are left, return to cooldown state
                self.initCoolDown()
        else:
            self.framesBetweenShotsCount -= 1  # Decrement the cooldown counter

    def initExplodeShot(self):
        '''Initializes the exploding shot behavior.'''
        pass

    def doExplodeShot(self, target):
        '''Handles the exploding shot behavior by shooting an exploding tear at the target.'''
        direction = target.body.position - self.body.position  # Calculate the direction to the target
        tearVelo = npVM.scaleVector(direction, self.explodeShotSpeed)  # Scale the velocity to the tear speed
        oTear = tC.enemyTear(self.screen, self.space, self.oPrinceEventHandler, self.body.position,
                             self.explodeShotRadius, tearVelo, self.explodeShotRange, doExplode=True)  # Create an exploding tear object
        self.oPrinceEventHandler.addEvent(pEC.spawnTearEvent(oTear))  # Spawn the tear
        self.initCoolDown()  # Return to cooldown state

    def doDeathEffect(self):
        '''Handles the death effect for the chemistry boss.'''
        pass

    def draw(self):
        '''Draws the chemistry boss to the screen.'''
        drawPos = np.array([self.body.position[0] - chemistryImage.get_width() / 2, self.body.position[1] - chemistryImage.get_height() / 2])  # Calculate draw position
        self.screen.blit(chemistryImage, drawPos)  # Draw the image at the calculated position





