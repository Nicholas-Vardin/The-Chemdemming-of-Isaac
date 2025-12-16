'''
pickupsClasses

By Nicholas Vardin

This file contains all the pickups in the game
'''



import random
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pymunk as pk
import pygame as p 
import os

scriptDir = os.path.dirname(__file__)
os.chdir(scriptDir) #remove weird error in vscode where files arent found properly


#load images
keyImage = p.image.load(r'images\keyIcon.png')
nickelImage = p.image.load(r'images\nickelIcon.png')
pennyImage = p.image.load(r'images\pennyIcon.png')
dimeImage = p.image.load(r'images\dimeIcon.png')
heartImage = p.image.load(r'images\heartPickUpIcon.png')
evilHeartImage = p.image.load(r'images\evilHeartPickUpIcon.png')
soulHeartImage = p.image.load(r'images\soulHeartPickUpIcon.png')
bombImage = p.image.load(r'images\bombPickUpIcon.png')
chestImage = p.image.load(r'images\chestIcon.png')
goldenChestImage = p.image.load(r'images\goldenChestIcon.png')
rockChestImage = p.image.load(r'images\rockChestIcon.png')

class heartPickUp(bFC.physicsRect):
    '''Heart pickup that heals the player if they need healing'''
    def __init__(self, screen, space, center):
        '''Initializes pickup'''
        clr = (150,0,0)
        width = 20
        height = 20
        super().__init__(screen, space, clr, center, width, height, collisionType = 8, bodyType = pk.Body.DYNAMIC)
    
    def draw(self):
        '''Draws pick up to screen'''
        drawPos = np.array([self.body.position[0]-heartImage.get_width()/2,self.body.position[1]-heartImage.get_height()/2])
        self.screen.blit(heartImage,drawPos)

class soulHeartPickUp(bFC.physicsRect):
    '''soul heart pickup that gives the player a soul heart if they are not full on hearts'''
    def __init__(self, screen, space, center):
        '''Initializes Pick up'''
        clr = (0,0,150)
        width = 20
        height = 20
        super().__init__(screen, space, clr, center, width, height, collisionType = 8, bodyType = pk.Body.DYNAMIC)

    def draw(self):
        '''Draws soul heart'''
        drawPos = np.array([self.body.position[0]-soulHeartImage.get_width()/2,self.body.position[1]-soulHeartImage.get_height()/2])
        self.screen.blit(soulHeartImage,drawPos)   
        
class evilHeartPickUp(bFC.physicsRect):
    '''evil heart pickup that gives the player an evil heart if they are not full on hearts'''
    def __init__(self, screen, space, center):
        '''initializes pick up'''
        clr = (0,0,0)
        width = 20
        height = 20
        super().__init__(screen, space, clr, center, width, height, collisionType = 8, bodyType = pk.Body.DYNAMIC)
    
    def draw(self):
        '''Draws evil heart'''
        drawPos = np.array([self.body.position[0]-evilHeartImage.get_width()/2,self.body.position[1]-evilHeartImage.get_height()/2])
        self.screen.blit(evilHeartImage,drawPos)
        
class keyPickUp(bFC.physicsRect):
    '''Key pick up that gives the player a key'''
    def __init__(self, screen, space, center):
        '''Initializes pick up'''
        clr = (150,150,150)
        width = 15
        height = 30
        super().__init__(screen, space, clr, center, width, height, collisionType = 8, bodyType = pk.Body.DYNAMIC)

    def draw(self):
        '''Draws key pick up'''
        drawPos = np.array([self.body.position[0]-keyImage.get_width()/2,self.body.position[1]-keyImage.get_height()/2])
        self.screen.blit(keyImage,drawPos)

class bombPickUp(bFC.physicsCircle):
    '''bomb pick up that gives the player a bomb'''
    def __init__(self, screen, space, center):
        '''Initializes pick up'''
        clr = (10,0,0)
        radius = 15
        super().__init__(screen, space, clr, center, radius, collisionType = 8, bodyType = pk.Body.DYNAMIC)

    def draw(self):
        '''Draws bomb pick up'''
        drawPos = np.array([self.body.position[0]-bombImage.get_width()/2,self.body.position[1]-bombImage.get_height()/2])
        self.screen.blit(bombImage,drawPos)   

class chestPickUp(bFC.physicsRect):
    '''Chest pick up that contains other pickups'''
    def __init__(self, screen, space, center, content = 'random', clr =(100,50,0), numContents =random.randint(1,3),  keyLocked = False, explosionLocked = False, roomClearLocked = False):
        '''Initializes chest,
        Contents can be defined as random for random pickups, a list of pickups for predifined pickups,
        or None for an empty chest'''
        width = bGI.basicTileWidth*1.2
        height = bGI.basicTileHeight*.9
        super().__init__(screen, space, clr, center, width, height, collisionType = 8, bodyType = pk.Body.DYNAMIC, mass = 5)

        self.keyLocked = keyLocked
        self.explosionLocked = explosionLocked
        self.roomClearLocked = roomClearLocked
        
        self.locked = self.keyLocked or self.explosionLocked or self.roomClearLocked

        possibleChestContent = [heartPickUp,soulHeartPickUp,evilHeartPickUp,keyPickUp,bombPickUp,
                                pennyPickUp,nickelPickUp,dimePickUp]        
        if content == 'random': # sets up the contents of the chest            
            self.content = []
            for i in range(numContents):
                self.content.append(random.choice(possibleChestContent))
        elif content != None:
            self.content = content
        else:
            self.content = []
            
    def updateLockedStatus(self):
        '''Updates the locked status of the chest based off the three locked attributes'''
        self.locked = self.keyLocked or self.explosionLocked or self.roomClearLocked
    
    def draw(self):
        '''Draws chest pick up'''
        drawPos = np.array([self.body.position[0]-chestImage.get_width()/2,self.body.position[1]-chestImage.get_height()/2])
        self.screen.blit(chestImage,drawPos) 
        
class goldenChestPickUp(chestPickUp):
    '''Golden chest pick up that needs to be opened by a key'''
    def __init__(self, screen, space, center, content = 'random'):
        '''initializes chest'''
        super().__init__(screen, space, center, clr = (255, 215, 0), content = content, keyLocked = True, numContents =random.randint(4,5))

    def draw(self):
        '''Draws chest'''
        drawPos = np.array([self.body.position[0]-goldenChestImage.get_width()/2,self.body.position[1]-goldenChestImage.get_height()/2])
        self.screen.blit(goldenChestImage,drawPos) 

class rockChestPickUp(chestPickUp):
    '''Rock chest pick up that needs to be opened by an explosion'''
    def __init__(self, screen, space, center, content = 'random'):
        '''Initializes chest'''
        super().__init__(screen, space, center, clr = (100, 100, 100), content = content, numContents =random.randint(3,4),explosionLocked=True) 

    def draw(self):
        '''Draws chest'''
        drawPos = np.array([self.body.position[0]-rockChestImage.get_width()/2,self.body.position[1]-rockChestImage.get_height()/2])
        self.screen.blit(rockChestImage,drawPos)  

class pennyPickUp(bFC.physicsCircle):
    '''penny pick up that gives the player 1 coin'''
    def __init__(self, screen, space, center):
        '''Initializes pick up '''
        clr = (255, 215, 0)
        radius = 10
        super().__init__(screen, space, clr, center, radius, collisionType = 8, bodyType = pk.Body.DYNAMIC)
        self.worth = 1

    def draw(self):
        '''draws penny'''
        drawPos = np.array([self.body.position[0]-pennyImage.get_width()/2,self.body.position[1]-pennyImage.get_height()/2])
        self.screen.blit(pennyImage,drawPos)
        
class nickelPickUp(bFC.physicsCircle):
    '''Nickel pick up that gives the player 5 coins'''
    def __init__(self, screen, space, center):
        '''Initializes nickel pick up'''
        clr = (100,120,100)  # Color of the nickel
        radius = 10  # Radius of the nickel
        super().__init__(screen, space, clr, center, radius, collisionType = 8, bodyType = pk.Body.DYNAMIC)
        self.worth = 5  # Value of the nickel in coins

    def draw(self):
        '''Draws nickel pick up'''
        drawPos = np.array([self.body.position[0]-nickelImage.get_width()/2,self.body.position[1]-nickelImage.get_height()/2])
        self.screen.blit(nickelImage,drawPos)

class dimePickUp(bFC.physicsCircle):
    '''Dime pick up that gives the player 10 coins'''
    def __init__(self, screen, space, center):
        '''Initializes dime pick up'''
        clr = (200,200,200)  # Color of the dime
        radius = 10  # Radius of the dime
        super().__init__(screen, space, clr, center, radius, collisionType = 8, bodyType = pk.Body.DYNAMIC)
        self.worth = 10  # Value of the dime in coins

    def draw(self):
        '''Draws dime'''
        drawPos = np.array([self.body.position[0]-dimeImage.get_width()/2,self.body.position[1]-dimeImage.get_height()/2])
        self.screen.blit(dimeImage,drawPos)

#dict containing all the string ids to pick up objects
dictPickupIdsToObjects = {'heart':heartPickUp,'soul heart': soulHeartPickUp,'evil heart':evilHeartPickUp, 'key':keyPickUp, 
                          'bomb':bombPickUp, 'chest':chestPickUp, 'golden chest':goldenChestPickUp,'rock chest':rockChestPickUp,
                          'penny':pennyPickUp,'nickel':nickelPickUp,'dime':dimePickUp}
   
def getRandomPickupObject():
    '''Function to return a random pick up object'''
    return random.choice(tuple(dictPickupIdsToObjects.values()))
    