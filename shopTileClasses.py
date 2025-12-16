'''
ShopTileClasses

By Nicholas Vardin

This file contians a shop tile class that can be used to buy things from
'''


import pygame as p
import itemClasses as iC
import basicFunctionsAndClasses as bFC
import tileClass as tC
import basicGameInfo as bGI
import menuWidgetsClasses as mWC
import numpy as np
import pickupsClasses as pC
import random
import itemClasses as iC

class shopTile(bFC.physicsRect, tC.tile):
    '''Shop tile where goods can be bought'''
    def __init__(self, screen, space, center, content, price, width=bGI.basicTileWidth, height=bGI.basicTileHeight):
        '''Initializes the shop tile class'''
        # Initialize the parent physicsRect class
        bFC.physicsRect.__init__(self, screen, space, (0, 0, 0), center, width, height, collisionType=10)
        
        # Set up tile attributes
        self.instantiateTileAttributes()
        
        # Store the content and price of the shop tile
        self.content = content
        self.price = price
        
        # Calculate the position for the price text box
        tLPos = np.array([self.body.position[0] - bGI.basicTileWidth / 2, self.body.position[1] + bGI.basicTileHeight / 2])
        
        # Create a text box to display the price
        self.priceTextBox = mWC.textBox(self.screen, (255, 255, 255), tLPos=tLPos, width=bGI.basicTileWidth, height=bGI.basicTileHeight / 2,
                                        textSize=20, fontClr=(255, 255, 255), text=str(self.price) + '$')

    def draw(self):
        '''Draws the shop tile content and price'''
        # Draw the content of the shop tile
        self.content.draw()
        
        # Draw the price text box
        self.priceTextBox.drawText()

class pickUpShopTile(shopTile):
    '''Shop tile specifically for pickups'''
    def __init__(self, screen, space, center, content=None, price=5):
        '''Initializes the pickup shop tile'''
        # If no content is provided, randomly select a pickup item
        if content is None:
            content = random.choice([pC.keyPickUp, pC.bombPickUp, pC.evilHeartPickUp, pC.soulHeartPickUp])
            content = content(screen, space, center)
        
        # Initialize the parent shopTile class
        super().__init__(screen, space, center, content=content, price=price)

class itemShopTile(shopTile):
    '''Shop tile specifically for items'''
    def __init__(self, screen, space, oItemHandler, center, content='random', price=15):
        '''Initializes the item shop tile'''
        # If content is set to 'random', get a random item from the shop pool
        if content == 'random':
            content = oItemHandler.getRandomItemBasedOnPool('shop')
            content = content(screen, center)
        
        # Initialize the parent shopTile class
        super().__init__(screen, space, center, content, price)



