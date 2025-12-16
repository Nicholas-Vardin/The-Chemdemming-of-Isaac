'''
RoomClass

By Nicholas Vardin

This file contains the room class, the building blocks of floors
'''

import os
import princeEventClasses as pEC
import basicGameInfo as bGI
import rockClass as roC
import basicFunctionsAndClasses as bFC
import numpy as np
import doorClasses as dC
import wallClass as wC
import potClass as pC
import enemyClasses as eC
import pickupsClasses as pUC
import bombBarrelClass as bBC
import itemClasses as iC
import pymunk as pk
import spikesClass as sC
import trapDoorClass as tDC
import shopTileClasses as sTC
import npVectorMath as npVM
import pygame as p


scriptDir = os.path.dirname(__file__)
os.chdir(scriptDir)

class room:
    '''Room object that handles everything inside the room'''
    def __init__(self,screen,space:pk.Space,oLoop,oPrinceEventHandler:pEC.princeEventHandler,oItemHandler:iC.itemHandler,oPlayer,doorDirections:tuple,layoutId:str,floorTileClr,wallClr,basicDoorClr):
        '''Initializes room object'''
        self.screen = screen
        self.space = space
        self.oLoop = oLoop
        self.oPrinceEventHandler = oPrinceEventHandler
        self.oItemHandler = oItemHandler
        self.layoutId = layoutId
        self.doorDirections = doorDirections

        self.floorTileClr = floorTileClr
        self.wallClr = wallClr
        self.basicDoorClr = basicDoorClr

        self.oPlayer = oPlayer
        self.enemyTarget = self.oPlayer
        
        self.discoveryLevel= 0
        #0 for undiscovered, 1 for slightly discovered, 2 for discovered

        self.lRocks = []
        self.lPots = []
        self.lDoors = []
        self.lWalls = []
        self.lTears = []
        self.lEnemies = []
        self.lPickUps = []
        self.lBombs = []
        self.lExplosions = []
        self.lBombBarrels = []
        self.lItemPedestals = []
        self.lSpikes = []
        self.lTrapDoors = []
        self.lBombRocks = []
        self.lShopTiles = []
        self.layout = [[[] for j in range(bGI.numTilesWide)] for i in range(bGI.numTilesHigh)]
        

        with open(bGI.roomLayoutsFileName,'r') as roomLayoutsFile:
            roomLayouts = roomLayoutsFile.readlines()
        
        for line in range(len(roomLayouts)):
            if roomLayouts[line][:-1] == self.layoutId:
                self.getInfoFromTxtFile(roomLayouts[line:line+bGI.roomLayoutsTxtNumLines])
    
        self.spawnWalls()
        
        self.clear = self.lEnemies == []

    def getInfoFromTxtFile(self,roomLayoutLines):
        '''Looks at the data for the room layout from the file and adds the data into their respective lists
        and changes wall colour if room type has a special room colour'''
        roomTypeLine = 1
        tilesTypePosLine = 2
        pickupsTypePosLine = 3
        enemyTypePosLine = 4
        self.roomType = roomLayoutLines[roomTypeLine][:-1] #[:-1] to remove \n
        if self.roomType == 'item':
            self.wallClr = bGI.itemRoomWallClr
        elif self.roomType == 'shop':
            self.wallClr = bGI.shopRoomWallClr
            self.floorTileClr = bGI.shopFloorClr
        #layout index is (row,col) aka (y,x)
        for tileInfo in bFC.getTuplesFromLine(roomLayoutLines[tilesTypePosLine],str):
            id = tileInfo[0]
            row = int(tileInfo[1])
            col = int(tileInfo[2])
            if id == 'rock':
                oRock = roC.rock(self.screen,self.space,center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lRocks.append(oRock)
                self.layout[row][col].append(oRock)
            elif id == 'pot':
                oPot = pC.pot(self.screen,self.space, center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lPots.append(oPot)
                self.layout[row][col].append(oPot)
            elif id == 'bomb barrel':
                oBombBarrel = bBC.bombBarrel(self.screen,self.space, oPrinceEventHandler=self.oPrinceEventHandler,
                                            center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lBombBarrels.append(oBombBarrel)
                self.layout[row][col].append(oBombBarrel)
            elif id == 'item pedestal':
                item = self.oItemHandler.getRandomItemBasedOnPool(self.roomType)
                oItemPedestal = iC.itemPedestal(self.screen,self.space,item,center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lItemPedestals.append(oItemPedestal)
                self.layout[row][col].append(oItemPedestal)
            elif id == 'spikes':
                oSpikes = sC.spikes(self.screen,self.space,center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lSpikes.append(oSpikes)
                self.layout[row][col].append(oSpikes)
            elif id == 'trap door': 
                oTrapDoor = tDC.trapDoor(self.screen,self.space,self.oPlayer, center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lTrapDoors.append(oTrapDoor)
                self.layout[row][col].append(oTrapDoor)
                
            elif id == 'bomb rock':
                oBombRock = roC.bombRock(self.screen,self.space,self.oPrinceEventHandler,center =np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lBombRocks.append(oBombRock)
                self.layout[row][col].append(oBombRock)

            elif id == 'pickup shop tile':
                oShopTile = sTC.pickUpShopTile(self.screen,self.space,center = np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lShopTiles.append(oShopTile)
                self.layout[row][col].append(oShopTile)

            elif id == 'item shop tile':
                oShopTile = sTC.itemShopTile(self.screen,self.space,self.oItemHandler,center = np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
                self.lShopTiles.append(oShopTile)
                self.layout[row][col].append(oShopTile)

                 
            
        for pickUpInfo in bFC.getTuplesFromLine(roomLayoutLines[pickupsTypePosLine],str):
            id = pickUpInfo[0]
            row = int(pickUpInfo[1])
            col = int(pickUpInfo[2])
            
            if id == 'random':
                pickupType = pUC.getRandomPickupObject()
            else:
                pickupType = pUC.dictPickupIdsToObjects[id]
                
            oPickup = pickupType(self.screen,self.space,np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
            self.lPickUps.append(oPickup)
        
        for enemyInfo in bFC.getTuplesFromLine(roomLayoutLines[enemyTypePosLine],str):
            id = enemyInfo[0]
            row = int(enemyInfo[1])
            col = int(enemyInfo[2])
            # enemyType = eC.dictEnemyIdsObjects[id]
            enemyType = getattr(eC,id)
            oEnemy = enemyType(self.screen,self.space,self.oPrinceEventHandler,np.array([(col+.5)*bGI.basicTileWidth,(row+.5)*bGI.basicTileHeight]))
            self.lEnemies.append(oEnemy)

    def spawnDoor(self,leadToIndex:tuple,doorType:str,doorClr:tuple,direction = None,center = np.array([]),width = bGI.basicTileWidth,height = bGI.basicTileHeight):
        '''Spawns a door object in room
        - By inputting a direction the door will be automatically placed at the top, bottom, right, or left of the room
        - Direction inputs up down left right
        - Direction can be ignored if a tLPos width and height or points are defined using np arrays
        - Direction > points > tLPos
        - startLocked is used for rooms that can be locked like item rooms'''
        
        if direction != None:
            if direction != 'up' and direction != 'down' and direction != 'left' and direction != 'right':
                raise Exception('Faulty direction was inputted', direction)
            if direction == 'up' or direction == 'down':
                width = 2*bGI.basicTileWidth
            
            elif direction == 'left' or direction == 'right':
                height = 2*bGI.basicTileHeight

            center = bGI.basicDoorCenterPos[direction]

        if doorType == 'normal' or doorType == 'start':
            oDoor = dC.door(self.screen,self.space,leadToIndex,doorClr,center = center,width = width,height = height)
        elif doorType == 'item':
            oDoor = dC.itemRoomDoor(self.screen,self.space,leadToIndex,center = center,
                                    width = width,height = height,startKeyLocked = True)
        elif doorType == 'boss':
            oDoor = dC.bossRoomDoor(self.screen,self.space,leadToIndex,center = center,width = width,height = height)
        elif doorType == 'secret':
            oDoor = dC.secretRoomDoor(self.screen,self.space,leadToIndex,self.wallClr,center = center,width = width,height = height)
        elif doorType == 'shop':
            oDoor = dC.shopRoomDoor(self.screen,self.space,leadToIndex,center,
                                    width = width,height = height,startKeyLocked = True)
        self.lDoors.append(oDoor)
        rowColTuple = bFC.xYNPArrayIntoRoomLayoutRowColTuple(center)
        row = rowColTuple[0]
        col = rowColTuple[1]
        self.layout[row][col].append(oDoor)
        if direction == 'up' or direction =='down':
            self.layout[row][col+1].append(oDoor)
        elif direction == 'left' or direction == 'right':
            self.layout[row+1][col]

    def spawnWalls(self):
        '''Spawns walls in room'''
        '''Spawns walls as so
        11111111
        3      4
        3      4
        22222222'''
        if 'up' in self.doorDirections:
            oWallLeft = wC.wall(self.screen,self.space,self.wallClr,
                                center = np.array([bGI.basicTileWidth*(bGI.numTilesWide/4-.5),bGI.basicTileHeight/2]), 
                                width = bGI.basicTileWidth*(bGI.numTilesWide/2-1))
            oWallRight = wC.wall(self.screen,self.space,self.wallClr,
                                center = np.array([bGI.basicTileWidth*(3*bGI.numTilesWide/4+.5),bGI.basicTileHeight/2]), 
                                width = bGI.basicTileWidth*(bGI.numTilesWide/2-1))
            self.lWalls.append(oWallLeft)
            self.lWalls.append(oWallRight)

            #add in walls to layout
            for col in range(bGI.numTilesWide//2-1):
                self.layout[0][col].append(oWallLeft)
            for col in range(bGI.numTilesWide//2+1,bGI.numTilesWide):
                self.layout[0][col].append(oWallRight)
            
        else:
            oWall = wC.wall(self.screen,self.space,self.wallClr,
                            center = np.array([bGI.basicTileWidth*(bGI.numTilesWide/2),bGI.basicTileHeight/2]),
                            width = bGI.basicTileWidth*bGI.numTilesWide)
            self.lWalls.append(oWall)
            for col in range(bGI.numTilesWide):
                self.layout[0][col].append(oWall)

        if 'down' in self.doorDirections:
            oWallLeft = wC.wall(self.screen,self.space,self.wallClr,
                                       center = np.array([bGI.basicTileWidth*(bGI.numTilesWide/4-.5),bGI.basicTileHeight*(bGI.numTilesHigh-.5)]), 
                                       width = bGI.basicTileWidth*(bGI.numTilesWide/2-1))
            oWallRight = wC.wall(self.screen,self.space,self.wallClr,
                                       center = np.array([bGI.basicTileWidth*(3*bGI.numTilesWide/4+.5),bGI.basicTileHeight*(bGI.numTilesHigh-.5)]), 
                                       width = bGI.basicTileWidth*(bGI.numTilesWide/2-1))
            self.lWalls.append(oWallLeft)
            self.lWalls.append(oWallRight)
            #add in walls to layout
            for col in range(bGI.numTilesWide//2-1):
                self.layout[bGI.numTilesHigh-1][col].append(oWallLeft)
            for col in range(bGI.numTilesWide//2+1,bGI.numTilesWide):
                self.layout[bGI.numTilesHigh-1][col].append(oWallRight)
            
        else:
            oWall = wC.wall(self.screen,self.space,self.wallClr,
                            center = np.array([bGI.basicTileWidth*(bGI.numTilesWide/2),bGI.basicTileHeight*(bGI.numTilesHigh-.5)]),
                            width = bGI.basicTileWidth*bGI.numTilesWide)
            self.lWalls.append(oWall)
            for col in range(bGI.numTilesWide):
                self.layout[bGI.numTilesHigh-1][col].append(oWall)
        
        if 'left' in self.doorDirections:
            oWallTop = wC.wall(self.screen,self.space,self.wallClr,
                                       center= np.array([bGI.basicTileWidth/2,bGI.basicTileHeight*(bGI.numTilesHigh/4)]), 
                                       height = bGI.basicTileHeight*(bGI.numTilesHigh/2-2))
            oWallBottom = wC.wall(self.screen,self.space,self.wallClr,
                                       center= np.array([bGI.basicTileWidth/2,bGI.basicTileHeight*(3*bGI.numTilesHigh/4)]), 
                                       height = bGI.basicTileHeight*(bGI.numTilesHigh/2-2))
            self.lWalls.append(oWallTop)
            self.lWalls.append(oWallBottom)
            
            #add walls to layout
            for row in range(1,bGI.numTilesHigh//2-1):
                self.layout[row][0].append(oWallTop)
            for row in range(bGI.numTilesHigh//2+1,bGI.numTilesHigh-1):
                self.layout[row][0].append(oWallBottom)
                
        else:
            oWall = wC.wall(self.screen,self.space,self.wallClr,
                            center= np.array([bGI.basicTileWidth/2,bGI.basicTileHeight*(bGI.numTilesHigh/2)]),
                            height = bGI.basicTileHeight*(bGI.numTilesHigh-2))
            self.lWalls.append(oWall)

            #add walls to layout
            for row in range(1,bGI.numTilesHigh-1):
                self.layout[row][0].append(oWall)
 
        if 'right' in self.doorDirections:
            oWallTop = wC.wall(self.screen,self.space,self.wallClr,
                                center= np.array([bGI.basicTileWidth*(bGI.numTilesWide-.5),bGI.basicTileHeight*(bGI.numTilesHigh/4)]), 
                                height = bGI.basicTileHeight*(bGI.numTilesHigh/2-2))
            oWallBottom = wC.wall(self.screen,self.space,self.wallClr,
                                    center= np.array([bGI.basicTileWidth*(bGI.numTilesWide-.5),bGI.basicTileHeight*(3*bGI.numTilesHigh/4)]), 
                                    height = bGI.basicTileHeight*(bGI.numTilesHigh/2-2))
            
            self.lWalls.append(oWallTop)
            self.lWalls.append(oWallBottom)
            #add walls to layout
            for row in range(1,bGI.numTilesHigh//2-1):
                self.layout[row][bGI.numTilesWide-1].append(oWallTop)
            for row in range(bGI.numTilesHigh//2+1,bGI.numTilesHigh-1):
                self.layout[row][bGI.numTilesWide-1].append(oWallBottom)

        else:
            oWall = wC.wall(self.screen,self.space,self.wallClr,
                            center= np.array([bGI.basicTileWidth*(bGI.numTilesWide-.5),bGI.basicTileHeight*(bGI.numTilesHigh/2)]),
                            height = bGI.basicTileHeight*(bGI.numTilesHigh-2))
            self.lWalls.append(oWall)
            #add walls to layout
            for row in range(1,bGI.numTilesHigh-1):
                self.layout[row][bGI.numTilesWide-1].append(oWall)

    
    def spawnTrapDoorInCenter(self):
        oTrapDoor = tDC.trapDoor(self.screen,self.space,self.oPlayer, center = np.array([bGI.basicTileWidth*(bGI.numTilesWide/2+.5),bGI.basicTileHeight*(bGI.numTilesHigh/2+.5)]))
        self.oPrinceEventHandler.addEvent(pEC.addTrapDoorToRoomEvent(oTrapDoor))
    
    def update(self):
        '''Updates all objects in the room'''
        for oTear in self.lTears:
            oTear.update(self.oLoop)  # Update tears in the room
        
        for oBomb in self.lBombs:
            oBomb.update()  # Update bombs in the room
        
        for oTrapDoor in self.lTrapDoors:
            oTrapDoor.update()  # Update trap doors in the room
            
        vField = self.getGroundVectorFieldToTarget()  # Get vector field for enemy movement
        for oEnemy in self.lEnemies:
            arguments = []
            if oEnemy.needsTarget:
                arguments.append(self.enemyTarget)  # Add target if enemy needs it
            if oEnemy.needsLayout:
                arguments.append(self.layout)  # Add layout if enemy needs it
            if oEnemy.needsGroundVField:
                arguments.append(vField)  # Add vector field if enemy needs it
            oEnemy.update(*arguments)  # Update enemy with required arguments
        
        for oExplosion in self.lExplosions:
            oExplosion.update()  # Update explosions in the room
        
        if len(self.lEnemies) == 0 and not self.clear:
            self.oPrinceEventHandler.addEvent(pEC.roomClearEvent())  # Trigger room clear event if no enemies remain

    def resetObjectsAfterRoomChange(self):
        '''Resets objects in the room after a room change'''
        self.removePhysicsObjectsFromSpace()  # Remove all physics objects from the space
        self.lTears = []  # Clear tears list
        self.lExplosions = []  # Clear explosions list

    def addPhysicsObjectsToSpace(self):
        '''Adds all physics objects in the room to the physics space'''
        for oWall in self.lWalls:
            self.space.add(oWall.body, oWall.shape)  # Add wall to space
        for oDoor in self.lDoors:
            self.space.add(oDoor.body, oDoor.shape)  # Add door to space
        for oPot in self.lPots:
            oPot.addToSpace()  # Add pot to space
        for oShopTile in self.lShopTiles:
            oShopTile.addToSpace()  # Add shop tile to space
        for oRock in self.lRocks:
            oRock.addToSpace()  # Add rock to space
        for oBombBarrel in self.lBombBarrels:
            oBombBarrel.addToSpace()  # Add bomb barrel to space
        for oPickUp in self.lPickUps:
            oPickUp.addToSpace()  # Add pickup to space
        for oEnemy in self.lEnemies:
            oEnemy.addToSpace()  # Add enemy to space
        for oTear in self.lTears:
            oTear.addToSpace()  # Add tear to space
        for oItemPedestal in self.lItemPedestals:
            oItemPedestal.addToSpace()  # Add item pedestal to space
        for oSpikes in self.lSpikes:
            oSpikes.addToSpace()  # Add spikes to space
        for oTrapDoor in self.lTrapDoors:
            oTrapDoor.addToSpace()  # Add trap door to space
        for oBombRock in self.lBombRocks:
            oBombRock.addToSpace()  # Add bomb rock to space

    def removePhysicsObjectsFromSpace(self):
        '''Removes all physics objects in the room from the physics space'''
        for oWall in self.lWalls:
            oWall.removeFromSpace()  # Remove wall from space
        for oDoor in self.lDoors:
            oDoor.removeFromSpace()  # Remove door from space
        for oPot in self.lPots:
            oPot.removeFromSpace()  # Remove pot from space
        for oShopTile in self.lShopTiles:
            oShopTile.removeFromSpace()  # Remove shop tile from space
        for oRock in self.lRocks:
            oRock.removeFromSpace()  # Remove rock from space
        for oBombBarrel in self.lBombBarrels:
            oBombBarrel.removeFromSpace()  # Remove bomb barrel from space
        for oPickUp in self.lPickUps:
            oPickUp.removeFromSpace()  # Remove pickup from space
        for oEnemy in self.lEnemies:
            oEnemy.removeFromSpace()  # Remove enemy from space
        for oTear in self.lTears:
            oTear.removeFromSpace()  # Remove tear from space
        for oItemPedestal in self.lItemPedestals:
            oItemPedestal.removeFromSpace()  # Remove item pedestal from space
        for oSpikes in self.lSpikes:
            oSpikes.removeFromSpace()  # Remove spikes from space
        for oTrapDoor in self.lTrapDoors:
            oTrapDoor.removeFromSpace()  # Remove trap door from space
        for oBombRock in self.lBombRocks:
            oBombRock.removeFromSpace()  # Remove bomb rock from space
        for oExplosion in self.lExplosions:
            oExplosion.removeFromSpace()  # Remove explosion from space

    def getGroundVectorFieldToTarget(self):
        '''Generates a vector field for enemies to navigate towards the target'''
        vField = [[np.array([0.0,0.0]) for i in range(bGI.numTilesWide)] for j in range(bGI.numTilesHigh)]  # Initialize vector field with zero vectors
        target = self.enemyTarget  # Get the target (usually the player)
        targetRowCol = (int(target.body.position[1]//bGI.basicTileHeight),int(target.body.position[0]//bGI.basicTileWidth))  # Determine target's tile position
        targetTileDirection = target.body.position - pk.Vec2d(targetRowCol[1]*bGI.basicTileWidth+0.5*bGI.basicTileWidth,targetRowCol[0]*bGI.basicTileHeight+0.5*bGI.basicTileHeight)  # Calculate direction to target's tile center
        queue = [targetRowCol]  # Initialize queue with the target's tile position
        vField = [[None for i in range(bGI.numTilesWide)] for j in range(bGI.numTilesHigh)]  # Reset vector field to None
        vField[targetRowCol[0]][targetRowCol[1]] = np.array(targetTileDirection)  # Set vector at target's tile position
        while queue != []:  # Process tiles in the queue
            copiedQueue = queue.copy()  # Copy the current queue
            queue = []  # Reset queue for the next iteration
            for rowCol in copiedQueue:  # Iterate through tiles in the copied queue
                row = rowCol[0]
                col = rowCol[1]
                # Check left neighbor
                if col != 0:
                    if type(vField[row][col-1]) != np.ndarray:  # If the left neighbor hasn't been processed
                        clear = True
                        for oTile in self.layout[row][col-1]:  # Check if the tile is an obstacle
                            if oTile.isEnemyGroundObstacle:
                                clear = False
                                break
                        if clear:  # If the tile is clear, set the vector and add it to the queue
                            vField[row][col-1] = np.array([1,0])
                            queue.append((row,col-1))
                # Check top neighbor
                if row != 0:
                    if type(vField[row-1][col]) != np.ndarray:  # If the top neighbor hasn't been processed
                        clear = True
                        for oTile in self.layout[row-1][col]:  # Check if the tile is an obstacle
                            if oTile.isEnemyGroundObstacle:
                                clear = False
                                break
                        if clear:  # If the tile is clear, set the vector and add it to the queue
                            vField[row-1][col] = np.array([0,1])
                            queue.append((row-1,col))
                # Check right neighbor
                if col != bGI.numTilesWide -1:
                    if type(vField[row][col+1]) != np.ndarray:  # If the right neighbor hasn't been processed
                        clear = True
                        for oTile in self.layout[row][col+1]:  # Check if the tile is an obstacle
                            if oTile.isEnemyGroundObstacle:
                                clear = False
                                break
                        if clear:  # If the tile is clear, set the vector and add it to the queue
                            vField[row][col+1] = np.array([-1,0])
                            queue.append((row,col+1))
                # Check bottom neighbor
                if row != bGI.numTilesHigh -1:
                    if type(vField[row+1][col]) != np.ndarray:  # If the bottom neighbor hasn't been processed
                        clear = True
                        for oTile in self.layout[row+1][col]:  # Check if the tile is an obstacle
                            if oTile.isEnemyGroundObstacle:
                                clear = False
                                break
                        if clear:  # If the tile is clear, set the vector and add it to the queue
                            vField[row+1][col] = np.array([0,-1])
                            queue.append((row+1,col))
        return vField  # Return the generated vector field
    def draw(self):
        '''Draws all objects in the room'''
        self.screen.fill(self.floorTileClr)  # Fill the screen with the floor tile color
        
        for oExplosion in self.lExplosions:
            oExplosion.draw()  # Draw explosions in the room
            
        for oRock in self.lRocks:
            oRock.draw()  # Draw rocks in the room
        for oPot in self.lPots:
            oPot.draw()  # Draw pots in the room
        for oSpikes in self.lSpikes:
            oSpikes.draw()  # Draw spikes in the room
        for oTrapDoor in self.lTrapDoors:
            oTrapDoor.draw()  # Draw trap doors in the room
        for oBombBarrel in self.lBombBarrels:
            oBombBarrel.draw()  # Draw bomb barrels in the room
        for oBombRock in self.lBombRocks:
            oBombRock.draw()  # Draw bomb rocks in the room
        for oShopTile in self.lShopTiles:
            oShopTile.draw()  # Draw shop tiles in the room
        
        for oItemPedestal in self.lItemPedestals:
            oItemPedestal.draw()  # Draw item pedestals in the room

        self.oPlayer.draw()  # Draw the player

        for oPickup in self.lPickUps:
            oPickup.draw()  # Draw pickups in the room
        
        for oBomb in self.lBombs:
            oBomb.draw()  # Draw bombs in the room
        for oEnemy in self.lEnemies:
            oEnemy.draw()  # Draw enemies in the room
        for oTear in self.lTears:
            oTear.draw()  # Draw tears in the room
        for oWall in self.lWalls:
            oWall.draw()  # Draw walls in the room
        for oDoor in self.lDoors:
            oDoor.draw()  # Draw doors in the room
