'''
princeEventClasses

By Nicholas Vardin

prince Events that handle event withing a loop
'''



import basicGameInfo as bGI
import basicFunctionsAndClasses as bFC
import numpy as np
import random
import trapDoorClass as tDC
import itemClasses as iC
import pymunk as pk
import kingEventClasses as kEC
import menuClasses as mC
import pygame.mixer

class princeEventHandler:
    '''Prince event handler that handles events in a loop'''
    def __init__(self,oLoop):
        '''initializes the event handler'''
        self.oLoop = oLoop 
        self.eventQueue = []

    def addEvent(self,oEvent):
        '''Adds an event to the event queue'''
        self.eventQueue.insert(0,oEvent)

    def doEvents(self):
        '''Processes all events in the event queue'''
        while len(self.eventQueue) != 0:
            oEvent = self.eventQueue.pop()
            # print(oEvent)
            oEvent.do(self.oLoop)

'''Room Events'''
class switchRoomsEvent:
    def __init__(self,newRoomIndex: tuple):
        '''Switches room within floor
        - new room index is (row,col)'''
        self.newRoomIndex = newRoomIndex
    def do(self,oLoop):
        '''Handles the logic for switching rooms'''
        # print('going to', self.newRoomIndex)
        oldRoomType = oLoop.currentFloor.currentRoom.roomType
        oLoop.currentFloor.switchRooms(self.newRoomIndex)
        newRoomType = oLoop.currentFloor.currentRoom.roomType
        
        # Change music based on room type
        if newRoomType == 'shop' and oldRoomType != 'shop':
            oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(r'music\shopMusic.mp3'))
        elif newRoomType in ['normal','start','item'] and oldRoomType not in ['normal','start','item']:
            oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(oLoop.currentFloor.musicFile))
        elif newRoomType == 'boss' and len(oLoop.currentFloor.currentRoom.lEnemies) != 0:
            oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(oLoop.currentFloor.bossMusicFile))
        elif newRoomType == 'secret':
            oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(r'music\secretRoomMusic.mp3'))
            
        # Handle player teleportation based on door position
        oPlayer = oLoop.oPlayer
        center = oPlayer.body.position
        tpOffsetDistance = 20
        # Based on character top left point position the door can be determined
        if center[0] < bGI.screenWidth/4:
            oPlayer.teleportBasedOnCenter(((bGI.numTilesWide-1)*bGI.basicTileHeight-tpOffsetDistance,center.y))

        elif center[0]> bGI.screenWidth*3/4:
            oPlayer.teleportBasedOnCenter((bGI.basicTileWidth+tpOffsetDistance,center.y))

        elif center[1]< bGI.screenHeight/4:
            oPlayer.teleportBasedOnCenter((center.x,(bGI.numTilesHigh-1)*bGI.basicTileHeight-tpOffsetDistance))
        
        elif center[1]> bGI.screenHeight*3/4:
            oPlayer.teleportBasedOnCenter((center.x,bGI.basicTileHeight+tpOffsetDistance))
        
        # Lock doors if there are enemies in the room
        if  len(oLoop.currentFloor.currentRoom.lEnemies) != 0:
            oLoop.oPrinceEventHandler.addEvent(roomClearLockDoorsEvent(oLoop.currentFloor.currentRoom.lDoors))
        
        # Unlock connecting doors with keys
        oLoop.oPrinceEventHandler.addEvent(keyUnlockConnectingDoorsEvent(self.newRoomIndex))

        # Update room discovery level
        oLoop.currentFloor.currentRoom.discoveryLevel = 2
        oLoop.oPrinceEventHandler.addEvent(slightDiscoverConnectingRoomsEvent(self.newRoomIndex))
        
        # Apply temporary effects to the player
        oLoop.oPlayer.doTempEffects()
        
class slightDiscoverConnectingRoomsEvent:
    def __init__(self,roomIndex):
        '''Discovers connecting rooms slightly
        - roomIndex is the index of the current room'''
        self.roomIndex = roomIndex
    def do(self,oLoop):
        '''Handles the logic for slightly discovering connecting rooms'''
        floorLayout = oLoop.currentFloor.floorLayout
        # Discover room above
        if self.roomIndex[0] != 0:
            if floorLayout[self.roomIndex[0]-1][self.roomIndex[1]] != bGI.empty:
                if floorLayout[self.roomIndex[0]-1][self.roomIndex[1]].discoveryLevel == 0 and floorLayout[self.roomIndex[0]-1][self.roomIndex[1]].roomType != 'secret':
                    floorLayout[self.roomIndex[0]-1][self.roomIndex[1]].discoveryLevel = 1
        # Discover room below
        if self.roomIndex[0] != bGI.numRoomsHigh-1:
            if floorLayout[self.roomIndex[0]+1][self.roomIndex[1]] != bGI.empty:
                if floorLayout[self.roomIndex[0]+1][self.roomIndex[1]].discoveryLevel == 0 and floorLayout[self.roomIndex[0]+1][self.roomIndex[1]].roomType != 'secret':
                    floorLayout[self.roomIndex[0]+1][self.roomIndex[1]].discoveryLevel = 1
        # Discover room to the left
        if self.roomIndex[1] != 0:
            if floorLayout[self.roomIndex[0]][self.roomIndex[1]-1] != bGI.empty:
                if floorLayout[self.roomIndex[0]][self.roomIndex[1]-1].discoveryLevel == 0 and floorLayout[self.roomIndex[0]][self.roomIndex[1]-1].roomType != 'secret':
                    floorLayout[self.roomIndex[0]][self.roomIndex[1]-1].discoveryLevel = 1
        # Discover room to the right
        if self.roomIndex[1] != bGI.numRoomsWide-1:
            if floorLayout[self.roomIndex[0]][self.roomIndex[1]+1] != bGI.empty:
                if floorLayout[self.roomIndex[0]][self.roomIndex[1]+1].discoveryLevel == 0 and floorLayout[self.roomIndex[0]][self.roomIndex[1]+1].roomType != 'secret':
                    floorLayout[self.roomIndex[0]][self.roomIndex[1]+1].discoveryLevel = 1

class roomClearEvent:
    def __init__(self):
        '''Event to handle clearing a room'''
        pass
    def do(self,oLoop):
        '''Handles the logic for clearing a room'''
        oRoom = oLoop.currentFloor.currentRoom
        oRoom.clear = True
        
        # Unlock doors in the room
        oLoop.oPrinceEventHandler.addEvent(roomUnlockRoomDoorsEvent(oRoom.lDoors))
        # Handle boss room logic
        if oRoom.roomType == 'boss':
            oRoom.spawnTrapDoorInCenter()
            oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(oLoop.currentFloor.musicFile))
        # Recharge active item if applicable
        if oLoop.oPlayer.activeItem != None:
            if oLoop.oPlayer.activeItem.currentCharge < oLoop.oPlayer.activeItem.maxCharge:
                oLoop.oPlayer.activeItem.currentCharge += 1
                     
# Removing and placing objects and pickups in room
class addTileToRoomEvent:
    def __init__(self,oTile,tileType):
        '''Adds a tile to the room
        - oTile is the tile object
        - tileType is given as a string with no capitals and spaces'''
        self.oTile = oTile
        self.tileType = tileType
    def do(self,oLoop):
        '''Handles the logic for adding a tile to the room'''
        col = int(self.oTile.body.position[0]//bGI.basicTileWidth)
        row = int(self.oTile.body.position[1]//bGI.basicTileHeight)
        currentRoom = oLoop.currentFloor.currentRoom
        currentRoom.layout[row][col].append(self.oTile)
        # Add tile to the appropriate list based on its type
        if self.tileType == 'rock':
            currentRoom.lRocks.append(self.oTile)
        elif self.tileType == 'bomb barrel':
            currentRoom.lBombBarrels.append(self.oTile)
        elif self.tileType == 'pot':
            currentRoom.lPots.append(self.oTile)
        elif self.tileType == 'item pedestal':
            currentRoom.lItemPedestals.append(self.oTile)
        elif self.tileType == 'bomb rock':
            currentRoom.lBombRocks.append(self.oTile)
        elif self.tileType == 'trap door':
            currentRoom.lTrapDoors.append(self.oTile)
        else:
            raise Exception('Tile type is not set up', self.tileType)

class addItemPedestalToRoomEvent:
    def __init__(self,oItemPedestal):
        '''Adds an item pedestal to the room
        - oItemPedestal is the item pedestal object'''
        self.oItemPedestal = oItemPedestal

    def do(self,oLoop):
        '''Handles the logic for adding an item pedestal to the room'''
        self.oItemPedestal.addToSpace()
        xTileIndex = int(self.oItemPedestal.body.position.x//bGI.basicTileWidth)
        yTileIndex = int(self.oItemPedestal.body.position.y//bGI.basicTileHeight)
        oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].append(self.oItemPedestal)
        oLoop.currentFloor.currentRoom.lItemPedestals.append(self.oItemPedestal)


class removeItemPedestalFromRoomEvent:
    def __init__(self,oItemPedestal):
        '''Event to remove item pedestal in current room
        - oItemPedestal is the item pedestal object'''
        self.oItemPedestal = oItemPedestal
    
    def do(self,oLoop):
        '''Removes the item pedestal, if it has already been removed do nothing'''
        xTileIndex = int(self.oItemPedestal.body.position.x//bGI.basicTileWidth)
        yTileIndex = int(self.oItemPedestal.body.position.y//bGI.basicTileHeight)
        oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oItemPedestal)
        oLoop.currentFloor.currentRoom.lItemPedestals.remove(self.oItemPedestal)
        self.oItemPedestal.removeFromSpace()


class removeBombBarrelFromRoomEvent:
    def __init__(self,oBombBarrel):
        '''Event to remove bomb barrel in current room
        - oBombBarrel is the bomb barrel object'''
        self.oBombBarrel = oBombBarrel
    
    def do(self,oLoop):
        '''Attempts to remove the bomb barrel, if it has already been removed do nothing'''
        try:
            xTileIndex = int(self.oBombBarrel.body.position[0]//bGI.basicTileWidth)
            yTileIndex = int(self.oBombBarrel.body.position[1]//bGI.basicTileHeight)
            oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oBombBarrel)
            oLoop.currentFloor.currentRoom.lBombBarrels.remove(self.oBombBarrel)
            self.oBombBarrel.removeFromSpace()
        except:
            pass

class addBombToRoomEvent:
    def __init__(self,oBomb):
        '''Event to spawn a bomb in the current room
        - oBomb is the bomb object'''
        self.oBomb = oBomb

    def do(self,oLoop):
        '''Handles the logic for adding a bomb to the room'''
        oLoop.currentFloor.currentRoom.lBombs.append(self.oBomb)
        self.oBomb.addToSpace()

class removeBombFromRoomEvent:
    def __init__(self,oBomb):
        '''Event to remove bomb in current room
        - oBomb is the bomb object'''
        self.oBomb = oBomb

    def do(self,oLoop):
        '''Attempts to remove the bomb, if it has already been removed do nothing'''
        try:
            self.oBomb.removeFromSpace()
            oLoop.currentFloor.currentRoom.lBombs.remove(self.oBomb)
        except:
            pass 
    
class addExplosionToRoomEvent:
    def __init__(self,oExplosion,doSoundEffect = True):
        '''Event to spawn an explosion in the current room
        - oExplosion is the explosion object
        - doSoundEffect determines if the explosion sound effect should play'''
        self.oExplosion = oExplosion
        self.doSoundEffect = doSoundEffect

    def do(self,oLoop):
        '''Handles the logic for adding an explosion to the room'''
        oLoop.currentFloor.currentRoom.lExplosions.append(self.oExplosion)
        self.oExplosion.addToSpace()
        if self.doSoundEffect:
            oLoop.oPrinceEventHandler.addEvent(playExplosionSound())
            
            
class removeExplosionFromRoomEvent:
    def __init__(self,oExplosion):
        '''Event to remove explosion in current room'''
        self.oExplosion = oExplosion
        
    def do(self,oLoop):
        '''Attempts to remove the explosion, if it has already been removed do nothing'''
        try:
            oLoop.currentFloor.currentRoom.lExplosions.remove(self.oExplosion)
            self.oExplosion.removeFromSpace()
        except:
            pass

class removeShopTileEvent:
    def __init__(self,oShopTile):
        '''Event to remove shop tile in current room'''
        self.oShopTile = oShopTile
        
    def do(self,oLoop):
        '''Attempts to remove the shop tile, if it has already been removed do nothing'''
        try:
            self.oShopTile.removeFromSpace()
            xTileIndex = int(self.oShopTile.body.position[0]//bGI.basicTileWidth)
            yTileIndex = int(self.oShopTile.body.position[1]//bGI.basicTileHeight)
            oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oShopTile)
            oLoop.currentFloor.currentRoom.lShopTiles.remove(self.oShopTile)
        except:
            pass

class removeRockEvent:
    def __init__(self,oRock):
        '''Event to remove rock in current room'''
        self.oRock = oRock
        
    def do(self,oLoop):
        '''Attempts to remove the rock, if it has already been removed do nothing'''
        try:
            self.oRock.removeFromSpace()
            xTileIndex = int(self.oRock.body.position[0]//bGI.basicTileWidth)
            yTileIndex = int(self.oRock.body.position[1]//bGI.basicTileHeight)
            oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oRock)
            oLoop.currentFloor.currentRoom.lRocks.remove(self.oRock)
        except:
            pass

class removeBombRockFromRoomEvent:
    def __init__(self,oBombRock):
        '''Event to remove bomb rock in current room'''
        self.oBombRock = oBombRock
        
    def do(self,oLoop):
        '''Attempts to remove the bomb rock, if it has already been removed do nothing'''
        try:
            self.oBombRock.removeFromSpace()
            xTileIndex = int(self.oBombRock.body.position[0]//bGI.basicTileWidth)
            yTileIndex = int(self.oBombRock.body.position[1]//bGI.basicTileHeight)
            oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oBombRock)
            oLoop.currentFloor.currentRoom.lBombRocks.remove(self.oBombRock)
        except:
            pass

class removePotEvent:
    def __init__(self,oPot):
        '''Event to remove pot in current room'''
        self.oPot = oPot
        
    def do(self,oLoop):
        '''Attempts to remove the pot, if it has already been removed do nothing'''
        try:
            xTileIndex = int(self.oPot.body.position[0]//bGI.basicTileWidth)
            yTileIndex = int(self.oPot.body.position[1]//bGI.basicTileHeight)
            oLoop.currentFloor.currentRoom.layout[yTileIndex][xTileIndex].remove(self.oPot)
            oLoop.currentFloor.currentRoom.lPots.remove(self.oPot)
            self.oPot.removeFromSpace()
        except:
            pass
        
class addPickupEvent:
    def __init__(self,oPickup):
        '''Event to spawn in pickup in current room'''
        self.oPickup = oPickup

    def do(self,oLoop):
        oLoop.currentFloor.currentRoom.lPickUps.append(self.oPickup)
        self.oPickup.addToSpace()

class removePickupEvent:
    def __init__(self,oPickup):
        self.oPickup = oPickup
    
    def do(self,oLoop):
        try:
            oLoop.currentFloor.currentRoom.lPickUps.remove(self.oPickup)
            self.oPickup.removeFromSpace()
        except:
            pass

class spawnTearEvent:
    def __init__(self,oTear,playSoundEffect = True):
        '''Event to spawn in tear in current room
        - oTear must be fully defined with everything in the brackets'''
        self.oTear = oTear
        self.playSoundEffect = playSoundEffect

    def do(self,oLoop):
        self.oTear.addToSpace()
        oLoop.currentFloor.currentRoom.lTears.append(self.oTear)
        if self.playSoundEffect:
            oLoop.oPrinceEventHandler.addEvent(playTearSound())

class removeTearEvent:
    def __init__(self,oTear):
        '''Event to remove tear in current room
        - oTear must be fully defined with everything in the brackets'''
        self.oTear = oTear

    def do(self,oLoop):
        '''attempts to remove the tear, if it has already been removed do nothing'''
        try:
            oLoop.currentFloor.currentRoom.lTears.remove(self.oTear)
            self.oTear.removeFromSpace()
        except:
            pass

class addTrapDoorToRoomEvent:
    def __init__(self,oTrapDoor):
        '''Event to add a trap door to the room
        - oTrapDoor is the trap door object'''
        self.oTrapDoor = oTrapDoor

    def do(self,oLoop):
        '''Handles the logic for adding a trap door to the room'''
        oLoop.currentFloor.currentRoom.lTrapDoors.append(self.oTrapDoor)
        oLoop.currentFloor.currentRoom.layout[int(self.oTrapDoor.body.position.y//bGI.basicTileHeight)][int(self.oTrapDoor.body.position.x//bGI.basicTileWidth)].append(self.oTrapDoor)
        self.oTrapDoor.addToSpace()

class removeTrapDoorFromRoomEvent:
    def __init__(self,oTrapDoor):
        '''Event to remove a trap door from the room
        - oTrapDoor is the trap door object'''
        self.oTrapDoor = oTrapDoor

    def do(self,oLoop):
        '''Attempts to remove the trap door, if it has already been removed do nothing'''
        try:
            oLoop.currentFloor.currentRoom.lTrapDoors.remove(self.oTrapDoor)
            self.oTrapDoor.removeFromSpace()
        except:
            pass
        

# Unlocking and Locking doors
class roomUnlockRoomDoorsEvent:
    def __init__(self,lDoors):
        '''Event to unlock all doors in the room
        - lDoors is the list of door objects'''
        self.lDoors = lDoors
        
    def do(self,oLoop):
        '''Handles the logic for unlocking all doors in the room'''
        for oDoor in self.lDoors:
            oLoop.oPrinceEventHandler.addEvent(roomClearUnlockDoorEvent(oDoor))
            oDoor.updateLockedStatus()

class keyUnlockConnectingDoorsEvent:
    '''Event to unlock doors in connecting rooms that lead to the current room'''
    def __init__(self,roomIndex):
        '''Initializes the event
        - roomIndex is the index of the current room'''
        self.roomIndex = roomIndex
    
    def do(self,oLoop):
        '''Handles the logic for unlocking connecting doors with keys'''
        floorLayout = oLoop.currentFloor.floorLayout
        
        # Connecting door above
        try:
            if self.roomIndex[0] != 0:
                lDoors = floorLayout[self.roomIndex[0]-1][self.roomIndex[1]].lDoors
                for oDoor in lDoors:
                    if oDoor.leadToIndex == self.roomIndex:
                        oLoop.oPrinceEventHandler.addEvent(keyUnlockDoorEvent(oDoor))
                        # print('unlocking door above')            
        except:
            # print('failed to key unlock above')
            pass
        
        # Connecting door below
        try:
            lDoors = floorLayout[self.roomIndex[0]+1][self.roomIndex[1]].lDoors
            for oDoor in lDoors:
                if oDoor.leadToIndex == self.roomIndex:
                    oLoop.oPrinceEventHandler.addEvent(keyUnlockDoorEvent(oDoor))
                    # print('unlocking door below')            
        except:
            # print('failed to key unlock below')
            pass
        
        # Connecting door on the left
        try:
            if self.roomIndex[1] != 0:
                lDoors = floorLayout[self.roomIndex[0]][self.roomIndex[1]-1].lDoors
                for oDoor in lDoors:
                    if oDoor.leadToIndex == self.roomIndex:
                        oLoop.oPrinceEventHandler.addEvent(keyUnlockDoorEvent(oDoor))
                        # print('unlocking door left')  
            # else:
                # print('failed to key unlock left on 0 x index')          
        except:
            # print('failed to key unlock left')
            pass
        
        # Connecting door on the right
        try:
            lDoors = floorLayout[self.roomIndex[0]][self.roomIndex[1]+1].lDoors
            for oDoor in lDoors:
                if oDoor.leadToIndex == self.roomIndex:
                    oLoop.oPrinceEventHandler.addEvent(keyUnlockDoorEvent(oDoor))
                    # print('unlocking door right')            
        except:
            # print('failed to key unlock right')
            pass
                           
class keyUnlockDoorEvent:
    def __init__(self,oDoor):
        '''Event to unlock a door with a key
        - oDoor is the door object'''
        self.oDoor = oDoor
        
    def do(self,oLoop):
        '''Handles the logic for unlocking the door with a key'''
        self.oDoor.keyLocked = False
        self.oDoor.updateLockedStatus()

class explosionUnlockDoorEvent:
    def __init__(self,oDoor):
        '''Event to unlock a door with an explosion
        - oDoor is the door object'''
        self.oDoor = oDoor
        
    def do(self,oLoop):
        '''Handles the logic for unlocking a door with an explosion'''
        self.oDoor.explosionLocked = False
        currentRoomIndex = oLoop.currentFloor.currentRoomIndex
        connectingRoom = oLoop.currentFloor.floorLayout[self.oDoor.leadToIndex[0]][self.oDoor.leadToIndex[1]]
        for oDoor in connectingRoom.lDoors:
            if tuple(oDoor.leadToIndex) == tuple(currentRoomIndex):
                oDoor.explosionLocked = False
                oDoor.updateLockedStatus()
        self.oDoor.updateLockedStatus()
    
class roomClearLockDoorsEvent:
    def __init__(self,lDoors):
        '''Event to lock all doors in the room until it is cleared
        - lDoors is the list of door objects'''
        self.lDoors = lDoors
        
    def do(self,oLoop):
        '''Handles the logic for locking all doors in the room'''
        for oDoor in self.lDoors:
            oDoor.roomClearLocked = True
            oDoor.updateLockedStatus()

class roomClearUnlockDoorEvent:
    def __init__(self,oDoor):
        '''Event to unlock a door after the room is cleared
        - oDoor is the door object'''
        self.oDoor = oDoor
        
    def do(self,oLoop):
        '''Handles the logic for unlocking a door after the room is cleared'''
        self.oDoor.roomClearLocked = False
        self.oDoor.updateLockedStatus()
        

'''Player Events'''
# Pickups and Items
class playerPickUpItemEvent:
    def __init__(self,oItem):
        '''Event for the player to pick up an item
        - oItem is the item object'''
        self.oItem = oItem
    def do(self,oLoop):
        '''Handles the logic for the player picking up an item'''
        if self.oItem.isPassiveItem:
            self.oItem.doEffect(oLoop)
        elif self.oItem.isActiveItem:
            if oLoop.oPlayer.activeItem != None:
                playerPos = oLoop.oPlayer.body.position
                center = ((playerPos[0]//bGI.basicTileWidth+.5)*bGI.basicTileWidth,(playerPos[1]//bGI.basicTileHeight+.5)*bGI.basicTileHeight)
                newItemPedestal = iC.itemPedestal(oLoop.screen,oLoop.space,type(oLoop.oPlayer.activeItem),center,activeItemCharge=oLoop.oPlayer.activeItem.currentCharge)
                oLoop.oPrinceEventHandler.addEvent(addItemPedestalToRoomEvent(newItemPedestal))
            oLoop.oPlayer.activeItem = self.oItem
            
        oLoop.oPlayer.initPickUpItemCooldown()

class useActiveItemEvent:
    def __init__(self,oItem):
        '''Event to use the player's active item
        - oItem is the active item object'''
        self.oItem = oItem
    def do(self,oLoop):
        '''Handles the logic for using the active item'''
        self.oItem.doEffect(oLoop)
        self.oItem.currentCharge = 0

class addBombsToPlayerEvent:
    def __init__(self,numBombs = 1):
        '''Event to add bombs to the player's inventory
        - numBombs is the number of bombs to add (default is 1)'''
        self.numBombs = numBombs
    def do(self,oLoop):
        '''Handles the logic for adding bombs to the player's inventory'''
        oLoop.oPlayer.numBombs += self.numBombs

class removeBombsFromPlayerEvent:
    def __init__(self, numBombs=1):
        '''Event to remove bombs from the player's inventory
        - numBombs is the number of bombs to remove (default is 1)'''
        self.numBombs = numBombs

    def do(self, oLoop):
        '''Handles the logic for removing bombs from the player's inventory'''
        if oLoop.oPlayer.numBombs - self.numBombs < 0:
            raise Exception(f'Player has {oLoop.oPlayer.numBombs} bombs and is trying to remove {self.numBombs} bombs')
        oLoop.oPlayer.numBombs -= self.numBombs


class addKeysToPlayerEvent:
    def __init__(self, numKeys=1):
        '''Event to add keys to the player's inventory
        - numKeys is the number of keys to add (default is 1)'''
        self.numKeys = numKeys

    def do(self, oLoop):
        '''Handles the logic for adding keys to the player's inventory'''
        oLoop.oPlayer.numKeys += self.numKeys


class removeKeysFromPlayerEvent:
    def __init__(self, numKeys=1):
        '''Event to remove keys from the player's inventory
        - numKeys is the number of keys to remove (default is 1)'''
        self.numKeys = numKeys

    def do(self, oLoop):
        '''Handles the logic for removing keys from the player's inventory'''
        if oLoop.oPlayer.numKeys - self.numKeys < 0:
            raise Exception(f'Player has {oLoop.oPlayer.numKeys} keys and is trying to remove {self.numKeys} keys')
        oLoop.oPlayer.numKeys -= self.numKeys


class addCoinsToPlayerEvent:
    def __init__(self, numCoins=1):
        '''Event to add coins to the player's inventory
        - numCoins is the number of coins to add (default is 1)'''
        self.numCoins = numCoins

    def do(self, oLoop):
        '''Handles the logic for adding coins to the player's inventory'''
        oLoop.oPlayer.numCoins += self.numCoins


class removeCoinsFromPlayerEvent:
    def __init__(self, numCoins=1):
        '''Event to remove coins from the player's inventory
        - numCoins is the number of coins to remove (default is 1)'''
        self.numCoins = numCoins

    def do(self, oLoop):
        '''Handles the logic for removing coins from the player's inventory'''
        if oLoop.oPlayer.numCoins - self.numCoins < 0:
            raise Exception(f'Player has {oLoop.oPlayer.numCoins} coins and is trying to remove {self.numCoins} coins')
        oLoop.oPlayer.numCoins -= self.numCoins


# Health

class addHealthContainerEvent:
    def __init__(self, numContainers=1, healAmount=1):
        '''Event to add health containers to the player
        - numContainers is the number of health containers to add (default is 1)
        - healAmount is the amount of health to heal (default is 1)'''
        self.numContainers = numContainers
        self.healAmount = healAmount

    def do(self, oLoop):
        '''Handles the logic for adding health containers to the player'''
        oPlayer = oLoop.oPlayer
        for i in range(min(self.numContainers, oPlayer.maxHealth - oPlayer.numNormalHealthContainers)):
            if len(oPlayer.lHealth) >= oPlayer.maxHealth:
                oPlayer.lHealth.pop()
            numNormalHealth = oPlayer.lHealth.count('normal')
            oPlayer.lHealth.insert(numNormalHealth, 'normal empty')

        oLoop.oPrinceEventHandler.addEvent(healPlayerEvent(self.healAmount))


class healPlayerEvent:
    def __init__(self, healAmount=1):
        '''Event to heal the player
        - healAmount is the amount of health to heal (default is 1)'''
        self.healAmount = healAmount

    def do(self, oLoop):
        '''Handles the logic for healing the player'''
        oPlayer = oLoop.oPlayer
        for i in range(self.healAmount):
            try:
                oPlayer.lHealth[oPlayer.lHealth.index('normal empty')] = 'normal'
            except:
                break


class addSoulHeartsToPlayerEvent:
    def __init__(self, numSoulHearts=1):
        '''Event to add soul hearts to the player
        - numSoulHearts is the number of soul hearts to add (default is 1)'''
        self.numSoulHearts = numSoulHearts

    def do(self, oLoop):
        '''Handles the logic for adding soul hearts to the player'''
        numSoulHeartsAdded = min(self.numSoulHearts, oLoop.oPlayer.maxHealth - len(oLoop.oPlayer.lHealth))
        oLoop.oPlayer.lHealth += ['soul' for i in range(numSoulHeartsAdded)]


class addEvilHeartsToPlayerEvent:
    def __init__(self, numEvilHearts=1):
        '''Event to add evil hearts to the player
        - numEvilHearts is the number of evil hearts to add (default is 1)'''
        self.numEvilHearts = numEvilHearts

    def do(self, oLoop):
        '''Handles the logic for adding evil hearts to the player'''
        numEvilHeartsAdded = min(self.numEvilHearts, oLoop.oPlayer.maxHealth - len(oLoop.oPlayer.lHealth))
        oLoop.oPlayer.lHealth += ['evil' for i in range(numEvilHeartsAdded)]


class damagePlayer:
    def __init__(self, damageAmount=1):
        '''Event to damage the player
        - damageAmount is the amount of damage to deal (default is 1)'''
        self.damageAmount = damageAmount

    def do(self, oLoop):
        '''Handles the logic for damaging the player'''
        oPlayer = oLoop.oPlayer
        if oPlayer.lHealth.count('normal empty') + self.damageAmount >= len(oPlayer.lHealth):
            self.damageAmount = len(oPlayer.lHealth) - oPlayer.lHealth.count('normal empty')
            oLoop.oKingEventHandler.addEvent(kEC.endLoopOnDeathEvent())
        oPlayer.takeDamage(self.damageAmount)

class playerHitByTear:
    def __init__(self, oTear):
        '''Event for the player being hit by a tear
        - oTear is the tear object'''
        self.oTear = oTear

    def do(self, oLoop):
        '''Handles the logic for the player being hit by a tear'''
        oPlayer = oLoop.oPlayer
        if self.oTear.doExplode:
            self.oTear.explode()
        else:
            if not oPlayer.invincible:
                oLoop.oPrinceEventHandler.addEvent(damagePlayer(self.oTear.damage))
                oPlayer.resetInvincibility()
        oLoop.oPrinceEventHandler.addEvent(removeTearEvent(self.oTear))


class playerHitBySpikes:
    def __init__(self, oSpikes):
        '''Event for the player being hit by spikes
        - oSpikes is the spikes object'''
        self.oSpikes = oSpikes

    def do(self, oLoop):
        '''Handles the logic for the player being hit by spikes'''
        oPlayer = oLoop.oPlayer
        if not oPlayer.invincible:
            oLoop.oPrinceEventHandler.addEvent(damagePlayer(self.oSpikes.playerDamage))
            oPlayer.resetInvincibility()


class playerHitByEnemy:
    def __init__(self, oEnemy):
        '''Event for the player being hit by an enemy
        - oEnemy is the enemy object'''
        self.oEnemy = oEnemy

    def do(self, oLoop):
        '''Handles the logic for the player being hit by an enemy'''
        oPlayer = oLoop.oPlayer
        if not oPlayer.invincible:
            oLoop.oPrinceEventHandler.addEvent(damagePlayer(self.oEnemy.damage))
            oPlayer.resetInvincibility()
        if self.oEnemy.specialEffectOnPlayerContact:
            self.oEnemy.doSpecialEffectOnPlayerContact()


class playerHitByExplosion:
    def __init__(self, oExplosion):
        '''Event for the player being hit by an explosion
        - oExplosion is the explosion object'''
        self.oExplosion = oExplosion

    def do(self, oLoop):
        '''Handles the logic for the player being hit by an explosion'''
        oPlayer = oLoop.oPlayer
        if not oPlayer.invincible and self.oExplosion.canDamageEntities:
            oLoop.oPrinceEventHandler.addEvent(damagePlayer(self.oExplosion.playerDamage))
            oPlayer.resetInvincibility()


# Tears
class bombBarrelHitByTearEvent:
    def __init__(self, oBombBarrel, oTear):
        '''Event for a bomb barrel being hit by a tear
        - oBombBarrel is the bomb barrel object
        - oTear is the tear object'''
        self.oBombBarrel = oBombBarrel
        self.oTear = oTear

    def do(self, oLoop):
        '''Handles the logic for a bomb barrel being hit by a tear'''
        oLoop.oPrinceEventHandler.addEvent(removeTearEvent(self.oTear))
        oLoop.oPrinceEventHandler.addEvent(damageBombBarrel(self.oBombBarrel, self.oTear.damage))


'''Enemy Events'''
class damageEnemy:
    def __init__(self, oEnemy, damage):
        '''Event to damage an enemy
        - oEnemy is the enemy object
        - damage is the amount of damage to deal'''
        self.oEnemy = oEnemy
        self.damage = damage

    def do(self, oLoop):
        '''Handles the logic for damaging an enemy'''
        self.oEnemy.health -= self.damage
        if self.oEnemy.health <= 0:
            if self.oEnemy.hasDeathEffect and not self.oEnemy.isDead:
                self.oEnemy.doDeathEffect()
            self.oEnemy.isDead = True
            oLoop.oPrinceEventHandler.addEvent(removeEnemyEvent(self.oEnemy))


class enemyHitBySpikesEvent:
    def __init__(self, oEnemy, oSpikes):
        '''Event for an enemy being hit by spikes
        - oEnemy is the enemy object
        - oSpikes is the spikes object'''
        self.oEnemy = oEnemy
        self.oSpikes = oSpikes

    def do(self, oLoop):
        '''Handles the logic for an enemy being hit by spikes'''
        if not self.oEnemy.flying:
            oLoop.oPrinceEventHandler.addEvent(damageEnemy(self.oEnemy, self.oSpikes.enemyDamage))


class enemyHitByExplosionEvent:
    def __init__(self, oEnemy, oExplosion):
        '''Event for an enemy being hit by an explosion
        - oEnemy is the enemy object
        - oExplosion is the explosion object'''
        self.oEnemy = oEnemy
        self.oExplosion = oExplosion

    def do(self, oLoop):
        '''Handles the logic for an enemy being hit by an explosion'''
        if self.oEnemy.recievesExplosionDamage:
            oLoop.oPrinceEventHandler.addEvent(damageEnemy(self.oEnemy, self.oExplosion.enemyDamage))


class addEnemyEvent:
    def __init__(self, oEnemy):
        '''Event to add an enemy to the room
        - oEnemy is the enemy object'''
        self.oEnemy = oEnemy

    def do(self, oLoop):
        '''Handles the logic for adding an enemy to the room'''
        oLoop.currentFloor.currentRoom.lEnemies.append(self.oEnemy)
        self.oEnemy.addToSpace()


class removeEnemyEvent:
    def __init__(self, oEnemy):
        '''Event to remove an enemy from the room
        - oEnemy is the enemy object'''
        self.oEnemy = oEnemy

    def do(self, oLoop):
        '''Attempts to remove the enemy, if it has already been removed do nothing'''
        try:
            oLoop.currentFloor.currentRoom.lEnemies.remove(self.oEnemy)
            self.oEnemy.removeFromSpace()
        except:
            pass

class enemyHitByTearEvent:
    def __init__(self, oTear, oEnemy):
        '''Event for an enemy being hit by a tear
        - oTear is the tear object
        - oEnemy is the enemy object'''
        self.oTear = oTear
        self.oEnemy = oEnemy

    def do(self, oLoop):
        '''Handles the logic for an enemy being hit by a tear'''
        if self.oTear.doExplode:
            self.oTear.explode()
        else:
            if self.oEnemy.recievesTearDamage:
                oLoop.oPrinceEventHandler.addEvent(damageEnemy(self.oEnemy, self.oTear.damage))
            if self.oEnemy.health > 0:
                if self.oEnemy.doesBounceBack:
                    self.oEnemy.initBounceBack(self.oTear.velo)
        oLoop.oPrinceEventHandler.addEvent(removeTearEvent(self.oTear))


class angerEnemiesOfCertainTypeEvent:
    def __init__(self, enemyType):
        '''Event to anger all enemies of a certain type in the room
        - enemyType is the type of enemy to anger'''
        self.enemyType = enemyType

    def do(self, oLoop):
        '''Handles the logic for angering enemies of a certain type'''
        for oEnemy in oLoop.currentFloor.currentRoom.lEnemies:
            if type(oEnemy) == self.enemyType:
                oEnemy.mentalState = 'angry'


'''Floor'''
class switchFloorEvent:
    def __init__(self, newFloorClass):
        '''Event to switch to a new floor
        - newFloorClass is the class of the new floor'''
        self.newFloorClass = newFloorClass

    def do(self, oLoop):
        '''Handles the logic for switching to a new floor'''
        oLoop.currentFloor.currentRoom.resetObjectsAfterRoomChange()
        newFloor = self.newFloorClass(oLoop.screen, oLoop.space, oLoop, oLoop.oPrinceEventHandler, oLoop.oItemHandler, oLoop.oPlayer)
        oLoop.currentFloor = newFloor
        oPlayer = oLoop.oPlayer
        oPlayer.teleportBasedOnCenter((bGI.numTilesWide * bGI.basicTileWidth / 2, bGI.numTilesHigh * bGI.basicTileHeight / 2))
        oPlayer.velo = pk.Vec2d(0.0, 0.0)
        oLoop.oPrinceEventHandler.addEvent(keyUnlockConnectingDoorsEvent(oLoop.currentFloor.currentRoomIndex))
        oLoop.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(newFloor.musicFile))


class switchFloorsBasedOnProgression:
    def __init__(self):
        '''Event to switch floors based on progression'''
        pass

    def do(self, oLoop):
        '''Handles the logic for switching floors based on progression'''
        oLoop.numFloorsCompleted += 1
        if oLoop.numFloorsCompleted >= len(oLoop.possibleFloorsAtCertainNumFloorCompletions):
            oLoop.oKingEventHandler.addEvent(kEC.endLoopOnWinEvent())
        else:
            newFloorClass = random.choice(oLoop.possibleFloorsAtCertainNumFloorCompletions[oLoop.numFloorsCompleted])
            oLoop.oPrinceEventHandler.addEvent(switchFloorEvent(newFloorClass))


'''Extras'''
class damageBombBarrel:
    def __init__(self, oBombBarrel, damage):
        '''Event to damage a bomb barrel
        - oBombBarrel is the bomb barrel object
        - damage is the amount of damage to deal'''
        self.oBombBarrel = oBombBarrel
        self.damage = damage

    def do(self, oLoop):
        '''Handles the logic for damaging a bomb barrel'''
        self.oBombBarrel.health -= self.damage
        if self.oBombBarrel.health <= 0:
            self.oBombBarrel.explode()  # Adds explosion and removes bomb barrel


class openChestEvent:
    def __init__(self, oChest):
        '''Event to open a chest
        - oChest is the chest object'''
        self.oChest = oChest

    def do(self, oLoop):
        '''Handles the logic for opening a chest'''
        oLoop.oPrinceEventHandler.addEvent(removePickupEvent(self.oChest))
        for pickUpClass in self.oChest.content:
            center = np.array([self.oChest.body.position.x + random.randint(-5, 5), self.oChest.body.position.y + random.randint(-5, 5)])
            oPickUp = pickUpClass(oLoop.screen, oLoop.space, center)
            oLoop.oPrinceEventHandler.addEvent(addPickupEvent(oPickUp))
class breakPotEvent:
    def __init__(self, oPot):
        '''Event to break a pot
        - oPot is the pot object'''
        self.oPot = oPot

    def do(self, oLoop):
        '''Handles the logic for breaking a pot'''
        oLoop.oPrinceEventHandler.addEvent(removePotEvent(self.oPot))
        for pickUpClass in self.oPot.content:
            center = np.array([self.oPot.body.position.x + random.randint(-5, 5), self.oPot.body.position.y + random.randint(-5, 5)])
            oPickUp = pickUpClass(oLoop.screen, oLoop.space, center)
            oLoop.oPrinceEventHandler.addEvent(addPickupEvent(oPickUp))


class damageAllEnemiesInRoomEvent:
    def __init__(self, damage):
        '''Event to damage all enemies in the room
        - damage is the amount of damage to deal'''
        self.damage = damage

    def do(self, oLoop):
        '''Handles the logic for damaging all enemies in the room'''
        for oEnemy in oLoop.currentFloor.currentRoom.lEnemies:
            oLoop.oPrinceEventHandler.addEvent(damageEnemy(oEnemy, self.damage))


class playTearSound:
    def __init__(self):
        '''Event to play the sound of a tear being shot'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the tear sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\playerTearShootSound.mp3', volume=0.3))


class playExplosionSound:
    def __init__(self):
        '''Event to play the sound of an explosion'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the explosion sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\explosionSound.mp3', volume=0.3))


class playKeyUnlockSound:
    def __init__(self):
        '''Event to play the sound of a key unlocking a door'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the key unlock sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\keyUnlockSound2.mp3', volume=0.5))


class playCoinPickUpSound:
    def __init__(self):
        '''Event to play the sound of picking up a coin'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the coin pickup sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\coinPickUpSound.mp3', volume=0.4))


class playKeyPickUpSound:
    def __init__(self):
        '''Event to play the sound of picking up a key'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the key pickup sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\keyPickUpSound.mp3', volume=0.4))


class playKachingSound:
    def __init__(self):
        '''Event to play the "kaching" sound'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the kaching sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\kachingSound.mp3', volume=0.4))


class playHeartPickUpSound:
    def __init__(self):
        '''Event to play the sound of picking up a heart'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the heart pickup sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\heartPickUpSound.mp3', volume=0.4))


class playBombPickUpsSound:
    def __init__(self):
        '''Event to play the sound of picking up a bomb'''
        pass

    def do(self, oLoop):
        '''Handles the logic for playing the bomb pickup sound'''
        oLoop.oPrinceEventHandler.addEvent(playSound(r'sound\bombPickUpSound.mp3', volume=3))


class playSound:
    def __init__(self, file, volume=0.2):
        '''Event to play a sound
        - file is the path to the sound file
        - volume is the volume of the sound (default is 0.2)'''
        self.file = file
        self.volume = volume

    def do(self, oLoop):
        '''Handles the logic for playing a sound'''
        oSound = pygame.mixer.Sound(self.file)
        oSound.set_volume(self.volume)
        oSound.play()