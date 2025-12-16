'''
Collision Handler Class

By: Nicholas Vardin

Program to handle collisions using the collision handler object
'''

import princeEventClasses as pEC
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import potClass as pC
import pickupsClasses as pUC
import pymunk as pk
import playerClass as pC
import shopTileClasses as sTC

#turns the class string id into the classes collision id, used for readability
dictCollisionIdsToInt = {'player':1,'wall':2,'rock':3,'pot':4,'door':5,'bomb':6,'bomb barrel':7, 'pickUp':8,
                         'bomb rock': 9,'shop tile':10,'item pedestal':13,'enemy':14,'tear':15,'explosion':16,
                         'spikes':18, 'trap door':19}


def playerDoorCollision(arbiter,space,data):
    '''Function to handle a player colliding with a door'''
    oLoop = data['oLoop']
    oDoorBody = arbiter.shapes[1].body
    #get the door object using its body
    oDoor = bFC.getObjectFromListUsingUniqueBody(oDoorBody,oLoop.currentFloor.currentRoom.lDoors)
    if oLoop.currentFloor.currentRoom.clear: #check if door can be entered
        if oDoor.locked:
            if oLoop.oPlayer.numKeys >0 and oDoor.keyLocked: #if door needs to and can be key unlocked
                #key unlock door
                oLoop.oPrinceEventHandler.addEvent(pEC.keyUnlockDoorEvent(oDoor))
                oLoop.oPrinceEventHandler.addEvent(pEC.removeKeysFromPlayerEvent())
                oLoop.oPrinceEventHandler.addEvent(pEC.playKeyUnlockSound())
        else:
            #enter door and switch rooms
            oLoop.oPrinceEventHandler.addEvent(pEC.switchRoomsEvent(oDoor.leadToIndex))
    return True

def playerBombCollision(arbiter,space,data):
    '''Function to handle when a player collides with a bomb'''
    oBombBody = arbiter.shapes[1].body
    try:
        #pushes bomb away from center of player
        oBombBody.apply_force_at_local_point(arbiter.normal.scale_to_length(10000),(0,0)) #applies force in direction of normal at center of bomb
    except:
        pass
    return True

def playerItemPedestalCollision(arbiter,space,data):
    '''Function to handle when a player collides with an item pedestal'''
    oLoop = data['oLoop']
    oItemPedestalBody = arbiter.shapes[1].body
    #get item pedestal object using its body
    oItemPedestal = bFC.getObjectFromListUsingUniqueBody(oItemPedestalBody,oLoop.currentFloor.currentRoom.lItemPedestals)
    
    if oLoop.oPlayer.canPickUpItems: #if player can pick up item, they do
        oLoop.oPrinceEventHandler.addEvent(pEC.removeItemPedestalFromRoomEvent(oItemPedestal))
        oLoop.oPrinceEventHandler.addEvent(pEC.playerPickUpItemEvent(oItemPedestal.oItem))
    return True

def playerTearCollision(arbiter,space,data):
    '''Function to handle when a player collides with a tear projectile'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[1].body
    #get tear object using its body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.canHitPlayer: #if tear can hit player, it does
        oLoop.oPrinceEventHandler.addEvent(pEC.playerHitByTear(oTear))
    return True

def tearEnemyCollision(arbiter,space,data):
    '''Function to handle when a tear collides with an enemy'''
    oLoop = data['oLoop']
    oEnemyBody = arbiter.shapes[1].body
    oTearBody = arbiter.shapes[0].body
    # get enemy and tear objects using their bodies
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.canHitEnemy: #if tear can hit enemy, it does
        oLoop.oPrinceEventHandler.addEvent(pEC.enemyHitByTearEvent(oTear,oEnemy))
    return True

def tearPickUpCollision(arbiter,space,data):
    '''Function to handle tears colliding with pickups, makes sure nothing happens'''
    return False

def tearWallCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a wall'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    #get tear object using its body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.doExplode: #if tear can explode it will
        oTear.explode()
    #removes tear from room
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True

def tearDoorCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a door, acts the same as tear wall collision'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True

def tearRockCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a rock, acts the same as tear wall collision'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True

def tearBombRockCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a bomb rock, acts the same as tear wall collision'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True

def tearPotCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a pot, acts the same as tear wall collision'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True

def tearBombBarrelCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a bomb barrel, acts the same as tear wall collision'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oBombBarrelBody = arbiter.shapes[1].body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    oBombBarrel = bFC.getObjectFromListUsingUniqueBody(oBombBarrelBody,oLoop.currentFloor.currentRoom.lBombBarrels)
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.bombBarrelHitByTearEvent(oBombBarrel,oTear))
    return True

def tearBombCollision(arbiter,space,data):
    '''Function to handle when a tear collides with a bomb'''
    oLoop = data['oLoop']
    oTearBody = arbiter.shapes[0].body
    oBombBody = arbiter.shapes[1].body
    #get tear object using its body
    oTear = bFC.getObjectFromListUsingUniqueBody(oTearBody,oLoop.currentFloor.currentRoom.lTears)
    #pushes bomb away from tears center
    oBombBody.apply_force_at_local_point(arbiter.normal.scale_to_length(7000),(0,0)) #applies force in direction of normal at center of bomb
    if oTear.doExplode:
        oTear.explode()
    oLoop.oPrinceEventHandler.addEvent(pEC.removeTearEvent(oTear))
    return True
    

def bombExplosionCollision(arbiter,space,data):
    '''function to handle when a bomb collides with an explosion'''
    oLoop = data['oLoop']
    oBombBody = arbiter.shapes[0].body
    oBomb = bFC.getObjectFromListUsingUniqueBody(oBombBody,oLoop.currentFloor.currentRoom.lBombs)
    oBomb.explode() #explodes bomb
    return True

def rockExplosionCollision(arbiter,space,data):
    '''Function to handle when a bomb collides with an explosion
    removes the bomb'''
    oLoop = data['oLoop']
    oRockBody = arbiter.shapes[0].body
    oRock = bFC.getObjectFromListUsingUniqueBody(oRockBody,oLoop.currentFloor.currentRoom.lRocks)
    oLoop.oPrinceEventHandler.addEvent(pEC.removeRockEvent(oRock))
    return True

def bombRockExplosionCollision(arbiter,space,data):
    '''Function to handle when a bomb rock collides with an explosion'''
    oLoop = data['oLoop']
    oBombRockBody = arbiter.shapes[0].body
    oBombRock = bFC.getObjectFromListUsingUniqueBody(oBombRockBody,oLoop.currentFloor.currentRoom.lBombRocks)
    oBombRock.explode() #explodes bomb rock
    return True

def bombSpikesCollision(arbiter,space,data):
    '''Function to handle when a bomb collides with spikes'''
    return False #removes interaction between bomb and spikes

def potExplosionCollision(arbiter,space,data):
    '''Function to handle when a pot collides with an explosion'''
    oLoop = data['oLoop']
    oPotBody = arbiter.shapes[0].body
    oPot = bFC.getObjectFromListUsingUniqueBody(oPotBody,oLoop.currentFloor.currentRoom.lPots)
    oLoop.oPrinceEventHandler.addEvent(pEC.breakPotEvent(oPot))
    return True

def bombBarrelExplosionCollision(arbiter,space,data):
    '''Function to handle when a bomb barrel collides with an explosion,
    explodes the bomb barrel'''
    oLoop = data['oLoop']
    oBombBarrelBody = arbiter.shapes[0].body
    oBombBarrel = bFC.getObjectFromListUsingUniqueBody(oBombBarrelBody,oLoop.currentFloor.currentRoom.lBombBarrels)
    oBombBarrel.explode()
    return True

def playerPickUpCollision(arbiter,space,data):
    '''Function to handle when the player collides with a pick up'''
    oLoop = data['oLoop']
    oPickUpBody = arbiter.shapes[1].body
    oPlayer = oLoop.oPlayer 
    #get pick up object using its body
    oPickUp = bFC.getObjectFromListUsingUniqueBody(oPickUpBody,oLoop.currentFloor.currentRoom.lPickUps)
    if type(oPickUp) == pUC.heartPickUp: #adds heart to player and removes it if player has room for a heart
        if oLoop.oPlayer.lHealth.count('normal empty') != 0:
            oLoop.oPrinceEventHandler.addEvent(pEC.healPlayerEvent())
            oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
            oLoop.oPrinceEventHandler.addEvent(pEC.playHeartPickUpSound())
    elif type(oPickUp) == pUC.soulHeartPickUp: #adds soul heart to player and removes it if player has room for a soul heart
        oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
        if oLoop.oPlayer.maxHealth > len(oLoop.oPlayer.lHealth):
            oLoop.oPrinceEventHandler.addEvent(pEC.addSoulHeartsToPlayerEvent())
            oLoop.oPrinceEventHandler.addEvent(pEC.playHeartPickUpSound())
    elif type(oPickUp) == pUC.evilHeartPickUp: #adds evil heart to player and removes it if player has room for a evil heart
        oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
        if oLoop.oPlayer.maxHealth > len(oLoop.oPlayer.lHealth):
            oLoop.oPrinceEventHandler.addEvent(pEC.addEvilHeartsToPlayerEvent())
            oLoop.oPrinceEventHandler.addEvent(pEC.playHeartPickUpSound())
    elif type(oPickUp) == pUC.keyPickUp: #adds key to player and removes it from room
        oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
        oLoop.oPrinceEventHandler.addEvent(pEC.addKeysToPlayerEvent())
        oLoop.oPrinceEventHandler.addEvent(pEC.playKeyPickUpSound())
    elif type(oPickUp) == pUC.bombPickUp: #adds bomb to player and removes it from room
        oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
        oLoop.oPrinceEventHandler.addEvent(pEC.addBombsToPlayerEvent())
        oLoop.oPrinceEventHandler.addEvent(pEC.playBombPickUpsSound())
    elif type(oPickUp) == pUC.chestPickUp: #opens chest
        oLoop.oPrinceEventHandler.addEvent(pEC.openChestEvent(oPickUp))
    elif type(oPickUp) == pUC.goldenChestPickUp: #opens chest if player has a key
        if oPlayer.numKeys>=1:
            oLoop.oPrinceEventHandler.addEvent(pEC.openChestEvent(oPickUp))
            oLoop.oPrinceEventHandler.addEvent(pEC.removeKeysFromPlayerEvent())
            oLoop.oPrinceEventHandler.addEvent(pEC.playKeyUnlockSound())
    elif type(oPickUp) == pUC.pennyPickUp or type(oPickUp) == pUC.nickelPickUp or type(oPickUp) == pUC.dimePickUp: 
        #removes key and adds coins to player based on what coin is picked up
        oLoop.oPrinceEventHandler.addEvent(pEC.removePickupEvent(oPickUp))
        oLoop.oPrinceEventHandler.addEvent(pEC.addCoinsToPlayerEvent(oPickUp.worth))
        oLoop.oPrinceEventHandler.addEvent(pEC.playCoinPickUpSound())
    return True


def playerEnemyCollision(arbiter,space,data):
    '''function to handle when the player collides with an enemy'''
    oLoop = data['oLoop']
    oEnemyBody = arbiter.shapes[1].body
    #gets enemy object from its body
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    oLoop.oPrinceEventHandler.addEvent(pEC.playerHitByEnemy(oEnemy))
    return True

def playerExplosionCollision(arbiter,space,data):
    '''function to handle when the player collides with an explosion'''
    oLoop = data['oLoop']
    oExplosionBody = arbiter.shapes[1].body
    oExplosion = bFC.getObjectFromListUsingUniqueBody(oExplosionBody,oLoop.currentFloor.currentRoom.lExplosions)
    if type(oExplosion) != bool: #makes sure explosion is still in room as hasnt been removed
        oLoop.oPrinceEventHandler.addEvent(pEC.playerHitByExplosion(oExplosion))
    return True

def playerSpikesCollision(arbiter,space,data):
    '''function to handle when the player collides with a spike'''
    oLoop = data['oLoop']
    oSpikeBody = arbiter.shapes[1].body
    oSpikes = bFC.getObjectFromListUsingUniqueBody(oSpikeBody,oLoop.currentFloor.currentRoom.lSpikes)
    oLoop.oPrinceEventHandler.addEvent(pEC.playerHitBySpikes(oSpikes))
    return True
    

def enemyBombCollision(arbiter,space,data):
    '''Function to handle when an enemy collides with a bomb'''
    oLoop = data['oLoop']
    oEnemyBody = arbiter.shapes[0].body
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    if oEnemy.flying: #if enemy is flying it will have no effect on the bomb
        return False
    return True #else the bomb is slightly pushed

def enemyExplosionCollision(arbiter,space,data):
    '''Function to handle when an enemy collides with an explosion'''
    oLoop = data['oLoop']
    #get objects using thier bodies
    oEnemyBody = arbiter.shapes[0].body
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    oExplosionBody = arbiter.shapes[1].body
    oExplosion = bFC.getObjectFromListUsingUniqueBody(oExplosionBody,oLoop.currentFloor.currentRoom.lExplosions)
    oLoop.oPrinceEventHandler.addEvent(pEC.enemyHitByExplosionEvent(oEnemy,oExplosion))
    return True

def enemySpikesCollision(arbiter,space,data):
    '''Function to handle when an enemy collides with spikes'''
    oLoop = data['oLoop']
    #get objects using their bodies
    oEnemyBody = arbiter.shapes[0].body
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    oSpikesBody = arbiter.shapes[1].body
    oSpikes = bFC.getObjectFromListUsingUniqueBody(oSpikesBody,oLoop.currentFloor.currentRoom.lSpikes)
    oLoop.oPrinceEventHandler.addEvent(pEC.enemyHitBySpikesEvent(oEnemy,oSpikes))
    return True

def enemyPickUpCollision(arbiter,space,data):
    '''Function to handle when an enemy collides with a pickup'''
    oLoop = data['oLoop']
    oEnemyBody = arbiter.shapes[0].body
    oEnemy = bFC.getObjectFromListUsingUniqueBody(oEnemyBody,oLoop.currentFloor.currentRoom.lEnemies)
    if oEnemy.flying: #if enemy is flying nothing happens
        return False
    return True #Else the pickup is slightly pushed

def spikesPickUpCollision(arbiter,space,data):
    '''Function to make sure spikes do not interact with pickups'''
    return False 

def explosionPickUpCollision(arbiter,space,data):
    '''Function to handle when an explosion collides with a pick up'''
    oLoop = data['oLoop']
    oPickUpBody = arbiter.shapes[1].body
    #applies force onto pickup pushing it away from the center of the explosion
    oPickUpBody.apply_force_at_local_point(arbiter.normal.scale_to_length(20000),(0,0)) #applies force in direction of normal at center of bomb
    oPickUp = bFC.getObjectFromListUsingUniqueBody(oPickUpBody,oLoop.currentFloor.currentRoom.lPickUps)
    if type(oPickUp) == pUC.rockChestPickUp:
        oLoop.oPrinceEventHandler.addEvent(pEC.openChestEvent(oPickUp))
    return False #make sure no further interaction happens

def explosionDoorCollision(arbiter,space,data):
    '''Function to handle when an explosion collides with a door'''
    oLoop = data['oLoop']
    oDoorBody = arbiter.shapes[1].body
    oDoor = bFC.getObjectFromListUsingUniqueBody(oDoorBody,oLoop.currentFloor.currentRoom.lDoors)
    if oDoor.explosionLocked: #explosion unlocks doors if they are explosion locked
        oLoop.oPrinceEventHandler.addEvent(pEC.explosionUnlockDoorEvent(oDoor))
    return True

def trapDoorPickUpCollision(arbiter,space,data):
    '''Function to remove interaction between a trapdoor and pickups'''
    return False 

def trapDoorPlayerCollision(arbiter,space,data):
    '''Function to handle when the player collides with a trapdoor'''
    oLoop =  data['oLoop']
    oTrapDoorBody = arbiter.shapes[0].body
    oTrapDoor = bFC.getObjectFromListUsingUniqueBody(oTrapDoorBody,oLoop.currentFloor.currentRoom.lTrapDoors)
    if oTrapDoor.open: #if trapdoor is open, progress the game
        oLoop.oPrinceEventHandler.addEvent(pEC.switchFloorsBasedOnProgression())
    return True

def shopTileDynamicObjectCollision(arbiter,space,data):
    '''Function to remove collision between shop tiles and pickups'''
    return False

def playerShopTileCollision(arbiter,space,data):
    '''Function to handle when a player collides with a shop tile'''
    oLoop =  data['oLoop']
    oPrinceEventHandler = oLoop.oPrinceEventHandler
    oPlayer = oLoop.oPlayer
    #get the shop tile object using its body
    oShopTileBody = arbiter.shapes[1].body
    oShopTile = bFC.getObjectFromListUsingUniqueBody(oShopTileBody,oLoop.currentFloor.currentRoom.lShopTiles)
    if oPlayer.numCoins >= oShopTile.price: #Check if player can buy the content
        content = oShopTile.content
        #add the content to player and remove players coins if player can take content
        if type(content) == pUC.keyPickUp:
            oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
            oPrinceEventHandler.addEvent(pEC.addKeysToPlayerEvent())
            oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
            oPrinceEventHandler.addEvent(pEC.playKachingSound())

        elif type(content) == pUC.bombPickUp:
            oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
            oPrinceEventHandler.addEvent(pEC.addBombsToPlayerEvent())
            oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
            oPrinceEventHandler.addEvent(pEC.playKachingSound())

        elif type(content) == pUC.heartPickUp:
            if oLoop.oPlayer.lHealth.count('normal empty') != 0:
                oLoop.oPrinceEventHandler.addEvent(pEC.healPlayerEvent())
                oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
                oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
                oPrinceEventHandler.addEvent(pEC.playKachingSound())
        
        elif type(content) == pUC.soulHeartPickUp:
            if oPlayer.maxHealth > len(oPlayer.lHealth):
                oLoop.oPrinceEventHandler.addEvent(pEC.addSoulHeartsToPlayerEvent())
                oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
                oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
                oPrinceEventHandler.addEvent(pEC.playKachingSound())

        elif type(content) == pUC.evilHeartPickUp:
            if oPlayer.maxHealth > len(oPlayer.lHealth):
                oLoop.oPrinceEventHandler.addEvent(pEC.addEvilHeartsToPlayerEvent())
                oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
                oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
                oPrinceEventHandler.addEvent(pEC.playKachingSound())

        elif type(oShopTile) == sTC.itemShopTile:
            oPrinceEventHandler.addEvent(pEC.playerPickUpItemEvent(content))
            oPrinceEventHandler.addEvent(pEC.removeShopTileEvent(oShopTile))
            oPrinceEventHandler.addEvent(pEC.removeCoinsFromPlayerEvent(numCoins=oShopTile.price))
            oPrinceEventHandler.addEvent(pEC.playKachingSound())
    return True

class collisonHandler:
    '''Handles all collision related events'''
    def __init__(self,oLoop,oPrinceEventHandler:pEC.princeEventHandler):
        self.oPrinceEventHandler = oPrinceEventHandler
        self.oLoop = oLoop
        self.space:pk.Space = oLoop.space

        '''Define all functions needed for each interaction for the pymunk collision handler'''
        
        #Player Door
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['door']).pre_solve = playerDoorCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['door']).data['oLoop'] = self.oLoop

        #Player Bomb
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['bomb']).begin = playerBombCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['bomb']).data['oLoop'] = self.oLoop

        #Player Item Pedestal
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['item pedestal']).pre_solve = playerItemPedestalCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['item pedestal']).data['oLoop'] = self.oLoop
        
        #player spikes
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['spikes']).pre_solve = playerSpikesCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['spikes']).data['oLoop'] = self.oLoop
        
        #player shop tiles 
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['shop tile']).pre_solve = playerShopTileCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['shop tile']).data['oLoop'] = self.oLoop

        #Player enemy tear
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['tear']).pre_solve = playerTearCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['tear']).data['oLoop'] = self.oLoop

        #Player Pick Up
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['pickUp']).begin = playerPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #Tear Enemy
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['enemy']).begin = tearEnemyCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['enemy']).data['oLoop'] = self.oLoop
        
        #Tear Pick Ups
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['pickUp']).begin = tearPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #tear wall
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['wall']).begin = tearWallCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['wall']).data['oLoop'] = self.oLoop
        
        #tear door
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['door']).begin = tearDoorCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['door']).data['oLoop'] = self.oLoop
        
        #tear rock
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['rock']).begin = tearRockCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['rock']).data['oLoop'] = self.oLoop
        
        #tear bomb rock
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb rock']).begin = tearBombRockCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb rock']).data['oLoop'] = self.oLoop
        
        #tear pot
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['pot']).begin = tearPotCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['pot']).data['oLoop'] = self.oLoop
        
        #tear bomb barrel
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb barrel']).begin = tearBombBarrelCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb barrel']).data['oLoop'] = self.oLoop
        
        #tear bomb
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb']).begin = tearBombCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['tear'],dictCollisionIdsToInt['bomb']).data['oLoop'] = self.oLoop
        
        #Bomb Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb'],dictCollisionIdsToInt['explosion']).begin = bombExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #Bomb Spikes
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb'],dictCollisionIdsToInt['spikes']).begin = bombSpikesCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb'],dictCollisionIdsToInt['spikes']).data['oLoop'] = self.oLoop
        
        #rock Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['rock'],dictCollisionIdsToInt['explosion']).begin = rockExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['rock'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #bomb rock Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb rock'],dictCollisionIdsToInt['explosion']).begin = bombRockExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb rock'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #pot Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['pot'],dictCollisionIdsToInt['explosion']).begin = potExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['pot'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #Bomb Barrel Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb barrel'],dictCollisionIdsToInt['explosion']).begin = bombBarrelExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['bomb barrel'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #player Enemy
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['enemy']).begin = playerEnemyCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['enemy']).data['oLoop'] = self.oLoop
        
        #player Explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['explosion']).begin = playerExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['player'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #enemy bomb
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['bomb']).pre_solve = enemyBombCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['bomb']).data['oLoop'] = self.oLoop
        
        #enemy explosion
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['explosion']).begin = enemyExplosionCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['explosion']).data['oLoop'] = self.oLoop
        
        #enemy spikes
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['spikes']).pre_solve = enemySpikesCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['spikes']).data['oLoop'] = self.oLoop
        
        #enemy pick up
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['pickUp']).pre_solve = enemyPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['enemy'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #spikes pick up
        self.space.add_collision_handler(dictCollisionIdsToInt['spikes'],dictCollisionIdsToInt['pickUp']).begin = spikesPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['spikes'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #explosion pick up
        self.space.add_collision_handler(dictCollisionIdsToInt['explosion'],dictCollisionIdsToInt['pickUp']).begin = explosionPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['explosion'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #explosion door
        self.space.add_collision_handler(dictCollisionIdsToInt['explosion'],dictCollisionIdsToInt['door']).begin = explosionDoorCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['explosion'],dictCollisionIdsToInt['door']).data['oLoop'] = self.oLoop
        
        #trap door pick up
        self.space.add_collision_handler(dictCollisionIdsToInt['trap door'],dictCollisionIdsToInt['pickUp']).begin = trapDoorPickUpCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['trap door'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
        #trap door player
        self.space.add_collision_handler(dictCollisionIdsToInt['trap door'],dictCollisionIdsToInt['player']).begin = trapDoorPlayerCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['trap door'],dictCollisionIdsToInt['player']).data['oLoop'] = self.oLoop

        #shop tiles dynamic objects
        self.space.add_collision_handler(dictCollisionIdsToInt['shop tile'],dictCollisionIdsToInt['bomb']).begin = shopTileDynamicObjectCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['shop tile'],dictCollisionIdsToInt['bomb']).data['oLoop'] = self.oLoop

        self.space.add_collision_handler(dictCollisionIdsToInt['shop tile'],dictCollisionIdsToInt['pickUp']).begin = shopTileDynamicObjectCollision
        self.space.add_collision_handler(dictCollisionIdsToInt['shop tile'],dictCollisionIdsToInt['pickUp']).data['oLoop'] = self.oLoop
        
    def checkandRespond(self):
        '''Does additional checks to handle more complicated collision'''
        oPlayer = self.oLoop.oPlayer
        currentRoom = self.oLoop.currentFloor.currentRoom
        lEnemies = currentRoom.lEnemies

        sHardObjects = self.getCollidableObjectsNearObject(oPlayer) #get all hard object the player can possibly not pass through
        
        if self.hardObjectsObjectCollision(oPlayer,sHardObjects): #if player is in a hard object fix the players position
            self.fixObjectPosition(oPlayer,sHardObjects)
            
        # enemies and hard objects
        for oEnemy in lEnemies:  #do collision checks for each enemy
            #get the hard objects around the enemy, accounting for additional width and height
            sHardObjects = self.getCollidableObjectsNearObject(oEnemy,tileRange=max(int(oEnemy.width//bGI.basicTileWidth+1),int(oEnemy.height//bGI.basicTileHeight+1)))
            if self.hardObjectsObjectCollision(oEnemy,sHardObjects): #if enemy is colliding fix collision
                self.fixObjectPosition(oEnemy,sHardObjects)

    def getSetofLockedDoors(self,sDoors):
        '''Function to get the set of locked doors given a set of locked doors'''
        sLocked = set()
        for oDoor in sDoors: #loop through the set, taking all the doors that our locked
            if oDoor.locked:
                sLocked.add(oDoor)
        return sLocked
    
    def getCollidableObjectsNearObject(self,object,tileRange =1):
        '''Returns a dict of all possible collidable types containing a set with the type of collidable in it
        - Only records a collidable if it is in the objects spot or adjacent spots within tile range'''
        roomLayout = self.oLoop.currentFloor.currentRoom.layout

        sCollidableObjects = set()
        objectIndexLocale = bFC.xYNPArrayIntoRoomLayoutRowColTuple(object.body.position)

        #only get the adjacent spots and the object spots collidable objects
        for row in range(objectIndexLocale[0]-tileRange,objectIndexLocale[0]+tileRange+1):
            if row <0 or row >= bGI.numTilesHigh: #makes sure row is valid
                continue
            for col in range(objectIndexLocale[1]-tileRange,objectIndexLocale[1]+tileRange+1):
                if col<0 or col>= bGI.numTilesWide: #makes sure row and col are valid
                    continue
                for oTile in roomLayout[row][col]:
                    #accounts for if the object is flying or on the ground and an enemy or a player
                    if object.flying:
                        if type(object) == pC.player:
                            if oTile.isPlayerAirObstacle:
                                sCollidableObjects.add(oTile)
                        else:
                            if oTile.isEnemyAirObstacle:
                                sCollidableObjects.add(oTile)
                    else:
                        if type(object) == pC.player:
                            if oTile.isPlayerGroundObstacle:
                                sCollidableObjects.add(oTile)
                        else:
                            if oTile.isEnemyGroundObstacle:
                                sCollidableObjects.add(oTile)
        return sCollidableObjects

    def hardObjectsObjectCollision(self,object,sHardObjects):
        '''Checks if an object like a player or enemy is overlapping a hard object they cant be in'''
        '''PsuedoCode
        Check geometry/shape,
            Loop through hard objects
                Check geometry of hard object
                return true if they overlap
                
        if no overlaps
            return false'''
        
        if object.geometry == 'rect':
            for collidable in sHardObjects:
                if collidable.geometry == 'rect':
                    if bFC.polygonPolygonCollision(collidable.getLPoints(),object.getLPoints()):
                        return True
                elif collidable.geometry == 'circle':
                    if bFC.polygonCircleCollision(object.getLPoints(),collidable.body.position,collidable.radius):
                        return True
        elif object.geometry == 'circle':
            for collidable in sHardObjects:
                if collidable.geometry == 'rect':
                    if bFC.polygonCircleCollision(collidable.getLPoints(),object.body.position,object.radius):
                        return True
                elif collidable.geometry == 'circle':
                    if bFC.circleCircleCollision(collidable.body.position,collidable.radius,object.body.position,object.radius):
                        return True

    def fixObjectPosition(self, object, sHardObjects):
        '''Fixes the object position based on the hard objects'''

        xIsProblem = False 
        yIsProblem = False
        
        #chec if x velo is issue
        object.teleportBasedOnCenter((object.pastPos.x + object.velo[0],object.pastPos.y))
        if self.hardObjectsObjectCollision(object,sHardObjects):
            xIsProblem = True
        # check if y velo is issue
        object.teleportBasedOnCenter((object.pastPos.x,object.pastPos.y + object.velo[1]))
        if self.hardObjectsObjectCollision(object,sHardObjects):
            yIsProblem = True
            
        #fix the position and apply bounce if needed
        if (xIsProblem and yIsProblem) or (not xIsProblem and not yIsProblem):
            if hasattr(object,'bouncesOffObstacles'):
                if object.bouncesOffObstacles:
                    object.velo[0] *= -1
                    object.velo[1] *= -1
                    return
            object.teleportBasedOnCenter(object.pastPos)
            object.velo[0] = 0.0
            object.velo[1] = 0.0
        elif xIsProblem:
            if hasattr(object,'bouncesOffObstacles'):
                if object.bouncesOffObstacles:
                    object.velo[0] *=-1
                    return 
            object.teleportBasedOnCenter((object.pastPos.x,object.pastPos.y+object.velo[1]))
            object.velo[0] = 0.0
        elif yIsProblem:
            if hasattr(object,'bouncesOffObstacles'):
                if object.bouncesOffObstacles:
                    object.velo[1]*=-1
                    return
            object.teleportBasedOnCenter((object.pastPos.x+object.velo[0],object.pastPos.y))
            object.velo[1] = 0.0
                
            
