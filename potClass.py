'''
potClass

By Nicholas Vardin

This file contains the pot class that contains pick ups and can be broken with an explosion
'''


import pygame as p
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pymunk as pk
import pickupsClasses as pUC
import random
import tileClass as tlC

class pot(bFC.physicsCircle,tlC.tile):
    '''A hard object that spits out pickups when broken'''
    def __init__(self, screen, space, center, radius=bGI.basicTileWidth/2, content = 'random'):
        '''Initializes pot'''
        clr = (200,200,200)  # Default color of the pot
        super().__init__(screen, space, clr, center, radius, collisionType = 4)  # Initialize parent classes
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isPlayerGroundObstacle=True)  # Set tile attributes
        
        # Define possible content that the pot can contain
        possiblePotContent = [pUC.heartPickUp,pUC.soulHeartPickUp,pUC.evilHeartPickUp,pUC.keyPickUp,pUC.bombPickUp]
                
        if content == 'random':  # If content is random, randomly select pickups
            self.content = []
            for i in range(random.randint(1,3)):  # Randomly choose between 1 to 3 pickups
                self.content.append(random.choice(possiblePotContent))
        elif content != None:  # If specific content is provided, use it
            self.content = content
        else:  # If content is None, set it to an empty list
            self.content = []

        self.image = p.image.load(r'images\potIcon.png')  # Load the pot icon image
        
    def draw(self):
        '''Draws the pot on the screen'''
        drawPos = np.array([self.body.position[0]-self.image.get_width()/2,self.body.position[1]-self.image.get_height()/2])  # Calculate draw position
        self.screen.blit(self.image,drawPos)  # Draw the pot image at the calculated position
