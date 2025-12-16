'''
Item Classes

By Nicholas Vardin

This file contains the classes for all items in the game. 
Each item class inherits from the base item class and implements its own effect and drawing method.

'''

import pygame as p
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import random
import numpy as np
import tileClass as tlC
import princeEventClasses as pEC
import pygame.image

class itemHandler:
    '''Handles item pools and random item selection'''
    def __init__(self,oPrinceEventHandler):
        '''Initializes the item handler with event handler and item pools'''
        self.oPrinceEventHandler = oPrinceEventHandler

        # List of all items and item pools
        self.allItems = [sadOnionItem,bootsOfSwiftnessItem,chickenAndRiceItem,noShotItem,dollarItem,bombBuddy,
                         giancoliItem,shwarmaItem,superShwarmaItem,kaleItem,croutonItem,ermAkchewallyItem,bentSpoonItem,
                         moreBulletsItem,threeLittlePigsItem,psycicForDummiesItem,evisseratedItem,kamikazeItem]
        self.itemRoomItems = [sadOnionItem,bootsOfSwiftnessItem,chickenAndRiceItem,noShotItem,dollarItem,bombBuddy,
                         giancoliItem,shwarmaItem,superShwarmaItem,kaleItem,croutonItem,bentSpoonItem,evisseratedItem,kamikazeItem]
        self.shopRoomItems = [bootsOfSwiftnessItem,noShotItem,giancoliItem,ermAkchewallyItem,threeLittlePigsItem]
        self.secretRoomItems = [superShwarmaItem,psycicForDummiesItem,moreBulletsItem,ermAkchewallyItem,
                                dollarItem,bentSpoonItem] # For secret rooms

    def getRandomItemBasedOnPool(self,pool):
        '''Returns a random item based on the specified pool'''
        if pool == 'item':
            return random.choice(self.itemRoomItems)
        elif pool == 'shop':
            return random.choice(self.shopRoomItems)
        elif pool == 'all':
            return random.choice(self.allItems)
        elif pool == 'secret':
            return random.choice(self.secretRoomItems)


class itemPedestal(bFC.physicsRect,tlC.tile):
    '''Represents a pedestal that holds an item'''
    def __init__(self, screen, space, item,center,activeItemCharge = None):
        '''Initializes the pedestal with an item and its position'''
        clr = (50,50,50)  # Pedestal color
        width = bGI.basicTileWidth  # Pedestal width
        height = bGI.basicTileHeight  # Pedestal height
        super().__init__(screen, space, clr, center, width, height, collisionType = 13)
        self.baseWidth = width
        self.baseHeight = bGI.basicTileHeight//2
        if activeItemCharge != None: 
            # Determines if the item is an active item and sets its charge
            self.oItem = item(self.screen,np.array([self.body.position[0],self.body.position[1]-self.baseHeight*.65]),activeItemCharge)
        else:
            self.oItem = item(self.screen,np.array([self.body.position[0],self.body.position[1]-self.baseHeight*.65]))

        self.instantiateTileAttributes()
        
    def draw(self):
        '''Draws the pedestal and the item on top of it'''
        p.draw.rect(self.screen,self.clr,(self.body.position[0]-self.baseWidth/2,self.body.position[1],self.baseWidth,self.baseHeight))
        self.oItem.draw()        
            
class item:
    '''Base class for all items'''
    def __init__(self,isActiveItem = False,isPassiveItem = False):
        '''Initializes the item with its type'''
        self.isActiveItem = isActiveItem
        self.isPassiveItem = isPassiveItem

class activeItem(item):
    '''Represents an active item with a charge system'''
    def __init__(self, maxCharge,currentCharge = 0):
        '''Initializes the active item with max and current charge'''
        self.maxCharge = maxCharge
        self.currentCharge = currentCharge
        super().__init__(isActiveItem = True)

class sadOnionItem(item):
    '''Item that increases tear rate'''
    def __init__(self, screen,center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem = True)
        self.image = pygame.image.load(r'images/sadOnionIcon.png')
        
    def doEffect(self,oLoop):
        '''Increases the tear rate of the player'''
        oLoop.oPlayer.tearRateStat.base += 1
    
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0]-self.image.get_width()/2,self.center[1]-self.image.get_height()/2])
        self.screen.blit(self.image,drawPos)
        
        
class bootsOfSwiftnessItem(item):
    '''Item that increases the player's speed'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        self.image = pygame.image.load(r'images/bootsOfSwiftnessIcon.png')
        
    def doEffect(self, oLoop):
        '''Increases the player's maximum speed'''
        oLoop.oPlayer.maxSpeed += 1
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.image.get_width() / 2, self.center[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)

class chickenAndRiceItem(item):
    '''Item that boosts damage and speed'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        self.image = pygame.image.load(r'images/chickenAndRiceIcon.jpg')
        
    def doEffect(self, oLoop):
        '''Increases the player's damage and speed'''
        oLoop.oPlayer.tearDamageStat.base += 0.5
        oLoop.oPlayer.maxSpeedStat.base += 0.3
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.image.get_width() / 2, self.center[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)

class noShotItem(item):
    '''Item that modifies tear stats significantly'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        self.image = pygame.image.load(r'images/noShotIcon.png')
        
    def doEffect(self, oLoop):
        '''Increases damage, reduces fire rate, and increases tear radius'''
        oLoop.oPlayer.tearDamageStat.multiplier *= 2.3
        oLoop.oPlayer.tearRateStat.multiplier /= 2
        oLoop.oPlayer.tearRadiusStat.base += 5
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.image.get_width() / 2, self.center[1] - self.image.get_height() / 2])
        self.screen.blit(self.image, drawPos)

class dollarItem(item):
    '''Item that grants a large amount of coins'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images\dollarIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds 100 coins to the player'''
        oLoop.oPrinceEventHandler.addEvent(pEC.addCoinsToPlayerEvent(100))
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 15, self.center[1] - 15])
        self.screen.blit(self.iconImage, drawPos)

class testActiveItem(activeItem):
    '''Test active item that boosts damage temporarily'''
    def __init__(self, screen, center, currentCharge=3):
        '''Initializes the active item'''
        self.screen = screen
        self.center = center
        super().__init__(maxCharge=3, currentCharge=currentCharge)
        
    def doEffect(self, oLoop):
        '''Increases the player's damage significantly'''
        oLoop.oPlayer.tearDamageStat.base += 100
        
    def draw(self):
        '''Draws the item as a black circle'''
        p.draw.circle(self.screen, (0, 0, 0), (int(self.center[0]), int(self.center[1])), bGI.basicTileWidth * 0.25)
    
    def drawOnUI(self, tLPos, width):
        '''Draws the item on the UI as a black circle'''
        p.draw.circle(self.screen, (0, 0, 0), (tLPos[0] + width / 2, tLPos[1] + width / 2), width / 2)

class bombBuddy(activeItem):
    '''Active item that spawns a bomb'''
    def __init__(self, screen, center, currentCharge=2):
        '''Initializes the active item'''
        self.screen = screen
        self.center = center
        super().__init__(maxCharge=2, currentCharge=currentCharge)

        imagePath = r'images/bombBuddyIcon.jpg'
        self.iconImage = pygame.image.load(imagePath)
        uiImagePath = r'images/bombBuddyUIIcon.jpg'
        self.uiImage = pygame.image.load(uiImagePath)
        
    def doEffect(self, oLoop):
        '''Spawns a bomb in the room'''
        import bombClasses as bC  # Avoids circular import
        oBomb = bC.bomb(self.screen, oLoop.space, oLoop.oPrinceEventHandler, oLoop.oPlayer.body.position)
        oLoop.oPrinceEventHandler.addEvent(pEC.addBombToRoomEvent(oBomb))
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.iconImage.get_width() / 2, self.center[1] - self.iconImage.get_height() / 2])
        self.screen.blit(self.iconImage, drawPos)
    
    def drawOnUI(self, tLPos):
        '''Draws the item on the UI'''
        drawPos = np.array([tLPos[0] + 10.5, tLPos[1]])
        self.screen.blit(self.uiImage, drawPos)

class giancoliItem(item):
    '''Item that increases tear rate'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/giancoliIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Increases the tear rate of the player'''
        oLoop.oPlayer.tearRateStat.base += 1
    
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 11.5, self.center[1] - 15])
        self.screen.blit(self.iconImage, drawPos)

class shwarmaItem(item):
    '''Item that grants a health container'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/shwarmaIcon.jpg'
        self.iconImage = pygame.image.load(imagePath)

    def doEffect(self, oLoop):
        '''Adds a health container to the player'''
        oLoop.oPrinceEventHandler.addEvent(pEC.addHealthContainerEvent(1))
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 11.5, self.center[1] - 15])
        self.screen.blit(self.iconImage, drawPos)

class superShwarmaItem(item):
    '''Item that grants a health container and boosts damage'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/superShwarmaIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a health container and increases damage'''
        oLoop.oPrinceEventHandler.addEvent(pEC.addHealthContainerEvent(1))
        oLoop.oPlayer.tearDamageStat.base += 0.8
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 20])
        self.screen.blit(self.iconImage, drawPos)
        
class kaleItem(item):
    '''Item that grants a health container and boosts stats'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/kaleIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a health container and increases damage and tear rate'''
        oLoop.oPrinceEventHandler.addEvent(pEC.addHealthContainerEvent(1))
        oLoop.oPlayer.tearDamageStat.base += 0.2
        oLoop.oPlayer.tearRateStat.base += 0.2
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 13.5])
        self.screen.blit(self.iconImage, drawPos)

class croutonItem(item):
    '''Item that grants a health container'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/croutonsIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a health container to the player'''
        oLoop.oPrinceEventHandler.addEvent(pEC.addHealthContainerEvent(1))
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 11.5])
        self.screen.blit(self.iconImage, drawPos)
    
class ermAkchewallyItem(item):
    '''Item that modifies shooting behavior and stats'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/nerdIcon.webp'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a new shooting behavior and modifies stats'''
        oLoop.oPlayer.addShootingBehaviour('2 middle')
        oLoop.oPlayer.tearRateStat.multiplier *= 2
        oLoop.oPlayer.tearDamageStat.base -= 1
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 20])
        self.screen.blit(self.iconImage, drawPos)

class bentSpoonItem(item):
    '''Item that enables tear tracking'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/bentSpoonIcon.jpg'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Enables tear tracking for the player'''
        oLoop.oPlayer.tearTrackingLevel = 1
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 20])
        self.screen.blit(self.iconImage, drawPos)

class moreBulletsItem(item):
    '''Item that adds shooting behavior and modifies stats'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/moreBulletsIcon.jpg'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a new shooting behavior and modifies stats'''
        oLoop.oPlayer.addShootingBehaviour('4 middle')
        oLoop.oPlayer.tearRateStat.multiplier *= 0.5
        oLoop.oPlayer.tearDamageStat.base -= 1
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 20])
        self.screen.blit(self.iconImage, drawPos)
        
class threeLittlePigsItem(item):
    '''Item that adds shooting behavior and reduces speed'''
    def __init__(self, screen, center):
        '''Initializes the item'''
        self.screen = screen
        self.center = center
        super().__init__(isPassiveItem=True)
        imagePath = r'images/threeLittlePigsIcon.webp'
        self.iconImage = pygame.image.load(imagePath)
        
    def doEffect(self, oLoop):
        '''Adds a new shooting behavior and reduces speed'''
        oLoop.oPlayer.addShootingBehaviour('3 spread')
        oLoop.oPlayer.maxSpeedStat.base -= 0.5
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - 20, self.center[1] - 13])
        self.screen.blit(self.iconImage, drawPos)
        
class psycicForDummiesItem(activeItem):
    '''Active item that temporarily enables tear tracking'''
    def __init__(self, screen, center, currentCharge=3):
        '''Initializes the active item'''
        self.screen = screen
        self.center = center
        super().__init__(maxCharge=3, currentCharge=currentCharge)
        imagePath = r'images/psycicForDummiesIcon.png'
        self.iconImage = pygame.image.load(imagePath)
        uiImagePath = r'images/psycicForDummiesUIIcon.png'
        self.uiImage = pygame.image.load(uiImagePath)
        
    def doEffect(self, oLoop):
        '''Temporarily enables tear tracking'''
        if oLoop.oPlayer.tearTrackingLevel == 0:
            oLoop.oPlayer.temporaryTracking = True
            oLoop.oPlayer.tempararyTrackingRoomsLeft = 1
            oLoop.oPlayer.tearTrackingLevel = 1
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.iconImage.get_width() / 2, self.center[1] - self.iconImage.get_height() / 2])
        self.screen.blit(self.iconImage, drawPos)
    
    def drawOnUI(self, tLPos):
        '''Draws the item on the UI'''
        drawPos = np.array([tLPos[0] + 10.5, tLPos[1]])
        self.screen.blit(self.uiImage, drawPos)

class kamikazeItem(activeItem):
    '''Active item that creates an explosion'''
    def __init__(self, screen, center, currentCharge=1):
        '''Initializes the active item'''
        self.screen = screen
        self.center = center
        super().__init__(maxCharge=1, currentCharge=currentCharge)
        imagePath = r'images/kamikazeIcon.webp'
        self.iconImage = pygame.image.load(imagePath)
        uiImagePath = r'images/kamikazeUIIcon.webp'
        self.uiImage = pygame.image.load(uiImagePath)
        
    def doEffect(self, oLoop):
        '''Creates an explosion at the player's position'''
        import bombClasses as bC #import bombClasses here to avoid circular import
        oExplosion = bC.explosion(self.screen, oLoop.space, oLoop.oPrinceEventHandler, oLoop.oPlayer.body.position)
        oLoop.oPrinceEventHandler.addEvent(pEC.addExplosionToRoomEvent(oExplosion))
    
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.iconImage.get_width() / 2, self.center[1] - self.iconImage.get_height() / 2])
        self.screen.blit(self.iconImage, drawPos)
    
    def drawOnUI(self, tLPos):
        '''Draws the item on the UI'''
        drawPos = np.array([tLPos[0], tLPos[1] + 4])
        self.screen.blit(self.uiImage, drawPos)

class evisseratedItem(activeItem):
    '''Active item that damages all enemies in the room'''
    def __init__(self, screen, center, currentCharge=4):
        '''Initializes the active item'''
        self.screen = screen
        self.center = center
        super().__init__(maxCharge=4, currentCharge=currentCharge)
        imagePath = r'images/evisseratedIcon.webp'
        self.iconImage = pygame.image.load(imagePath)
        uiImagePath = r'images/evisseratedUIIcon.webp'
        self.uiImage = pygame.image.load(uiImagePath)
        
    def doEffect(self, oLoop):
        '''Damages all enemies in the room and plays a sound'''
        oLoop.oPrinceEventHandler.addEvent(pEC.damageAllEnemiesInRoomEvent(30))
        oLoop.oPrinceEventHandler.addEvent(pEC.playSound(r'sound\evisseratedSound.mp3', volume=0.5))
        
    def draw(self):
        '''Draws the item on the screen'''
        drawPos = np.array([self.center[0] - self.iconImage.get_width() / 2, self.center[1] - self.iconImage.get_height() / 2])
        self.screen.blit(self.iconImage, drawPos)
    
    def drawOnUI(self, tLPos):
        '''Draws the item on the UI'''
        drawPos = np.array([tLPos[0], tLPos[1]])
        self.screen.blit(self.uiImage, drawPos)
