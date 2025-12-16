'''
floorClass

By Nicholas Vardin

This file contains the floor class and all the subclasses of the floor class.
The floor class is responsible for generating the floor layout, placing the rooms, and managing the rooms.
'''


import princeEventClasses as pEC
import basicGameInfo as bGI
import roomClass as rC
import pymunk as pk
import random
from collections import defaultdict
import basicFunctionsAndClasses as bFC


class floor:
    '''The floor class is responsible for generating the floor layout, placing the rooms, and managing the rooms.'''
    def __init__(self,screen,space,oLoop, oPrinceEventHandler:pEC.princeEventHandler,oItemHandler,oPlayer,floorTileClr,wallClr,basicDoorClr,
                 numRooms = 10,numItemRooms = 1, numBossRooms = 1, numStartRooms = 1, numSecretRooms = 1,
                 numShopRooms = 1, possibleRoomIds = [],musicFile = r'music\greyGolferMusic.mp3',bossMusicFile = r'music\bossMusic.mp3'):
        '''Initializes the floor class'''
        
        self.screen = screen
        self.oPrinceEventHandler = oPrinceEventHandler
        self.oItemHandler = oItemHandler
        self.oLoop = oLoop
        self.musicFile = musicFile
        self.bossMusicFile = bossMusicFile
        
        self.space = space
        
        self.floorTileClr = floorTileClr
        self.wallClr = wallClr
        self.basicDoorClr = basicDoorClr
        
        self.oPlayer = oPlayer
        
        self.numRooms = numRooms
        self.numItemRooms = numItemRooms
        self.numBossRooms = numBossRooms
        self.numStartRooms = numStartRooms
        self.numSecretRooms = numSecretRooms
        self.numShopRooms = numShopRooms
        self.possibleRoomIds = possibleRoomIds
        
        self.floorLayout = self.generateFloorLayout()
        self.instantiateRoomObjects()
        self.spawnDoorsInRooms()
        
        self.startingRoomIndex = (bGI.numRoomsHigh//2,bGI.numRoomsWide//2)
        
        #init starting room
        self.currentRoomIndex = self.startingRoomIndex #records indexes as y,x pair
        self.currentRoom = self.floorLayout[self.currentRoomIndex[0]][self.currentRoomIndex[1]]
        self.currentRoom.discoveryLevel = 2
        self.oPrinceEventHandler.addEvent(pEC.slightDiscoverConnectingRoomsEvent(self.currentRoomIndex))
        
        self.currentRoom.addPhysicsObjectsToSpace()

    def update(self):
        self.currentRoom.update()

    def instantiateRoomObjects(self):
        '''Turns id tags in floor layout into room objects'''
        for row in range(len(self.floorLayout)): ### Change into list comprehension later
            for col in range(len(self.floorLayout[row])):
                if self.floorLayout[row][col] != bGI.empty:
                    doorDirections = self.getDoorDirectionTuple(row,col)
                    self.floorLayout[row][col] = rC.room(self.screen,self.space,self.oLoop, self.oPrinceEventHandler,self.oItemHandler,self.oPlayer,doorDirections,self.floorLayout[row][col],
                                                         self.floorTileClr,self.wallClr,self.basicDoorClr)

    def getDoorDirectionTuple(self,row,col):
        '''Gets the door directions tuple based on a position in floor layout'''
        directions = []
        #check if door needs to be added above
        if row !=0:
            if self.floorLayout[row-1][col] != bGI.empty:
                directions.append('up')

        #check if door needs to be added on the bottom
        if row != len(self.floorLayout)-1:
            if self.floorLayout[row+1][col] != bGI.empty:
                directions.append('down')
        
        #Check if door needs to be added on left
        if col != 0:
            if self.floorLayout[row][col-1] != bGI.empty:
                directions.append('left')
        
        #check if door needs to be added on right
        if col != len(self.floorLayout[row])-1:
            if self.floorLayout[row][col+1] != bGI.empty:
                directions.append('right')
        
        return tuple(directions)

    def spawnDoorsInRooms(self):
        '''Adds doors into room objects based on the connecting rooms'''
        for iRow,row in enumerate(self.floorLayout):
            for iCol, spot in enumerate(row):
                if spot != bGI.empty: #checks to make the spot is a room
                    if 'up' in spot.doorDirections:
                        doorAboveType = self.floorLayout[iRow-1][iCol].roomType
                        doorType = spot.roomType
                        doorType = bGI.doorPriority[min(bGI.doorPriority.index(doorAboveType),bGI.doorPriority.index(doorType))]

                        spot.spawnDoor((iRow-1,iCol),doorType,self.basicDoorClr,direction = 'up')

                    if 'down' in spot.doorDirections:
                        doorAboveType = self.floorLayout[iRow+1][iCol].roomType
                        doorType = spot.roomType
                        doorType = bGI.doorPriority[min(bGI.doorPriority.index(doorAboveType),bGI.doorPriority.index(doorType))]

                        spot.spawnDoor((iRow+1,iCol),doorType,self.basicDoorClr,direction = 'down')
                    
                    if 'left' in spot.doorDirections:
                        doorAboveType = self.floorLayout[iRow][iCol-1].roomType
                        doorType = spot.roomType
                        doorType = bGI.doorPriority[min(bGI.doorPriority.index(doorAboveType),bGI.doorPriority.index(doorType))]

                        spot.spawnDoor((iRow,iCol-1),doorType,self.basicDoorClr,direction = 'left')
                    
                    if 'right' in spot.doorDirections:
                        doorAboveType = self.floorLayout[iRow][iCol+1].roomType
                        doorType = spot.roomType
                        doorType = bGI.doorPriority[min(bGI.doorPriority.index(doorAboveType),bGI.doorPriority.index(doorType))]

                        spot.spawnDoor((iRow,iCol+1),doorType,self.basicDoorClr,direction = 'right')

    def switchRooms(self,newRoomIndex):
        '''Switches rooms'''
        self.currentRoom.resetObjectsAfterRoomChange() #includes removing physics objects from space
        self.currentRoomIndex = newRoomIndex
        self.currentRoom = self.floorLayout[self.currentRoomIndex[0]][self.currentRoomIndex[1]]
        self.currentRoom.addPhysicsObjectsToSpace()
        
    def generateFloorLayout(self):
        '''Generates rooms in floor layout'''
        while True:
            roomIndexes = {(bGI.numRoomsHigh//2,bGI.numRoomsWide//2)}
            floorLayout = [[bGI.empty for i in range(bGI.numRoomsWide)] for j in range(bGI.numRoomsHigh)] #creates empty floor layout
            for i in range(self.numRooms-1):
                while True:
                    row = random.randint(0,bGI.numRoomsHigh-1)
                    col = random.randint(0,bGI.numRoomsWide-1) 
                    if not (row,col) in roomIndexes: #checks if the room is already in the set
                        if self.checkIfRoomIndexIsValid(roomIndexes,row,col):
                            roomIndexes.add((row,col))
                            break
            for index in roomIndexes:
                floorLayout[index[0]][index[1]] = 'r' #sets all indexes in floor layout to empty
                    
            floorLayout = self.placeRoomTypesOnFloorLayout(floorLayout)
            floorLayout = self.addSecretRoomTypes(floorLayout) 
            floorLayout = self.placeRoomConnections(floorLayout) #places the connections between rooms in the floor layout
            
            endPoints = self.getEndPoints(floorLayout)
            if (bGI.numRoomsHigh//2,bGI.numRoomsWide//2) in endPoints: #makes sure the start room is not overriden by special end point rooms
                endPoints.remove((bGI.numRoomsHigh//2,bGI.numRoomsWide//2))
            if len(endPoints) >= self.numItemRooms + self.numBossRooms + self.numShopRooms:
                break
        floorLayout = self.addSpecialRoomTypes(floorLayout,endPoints)     
        floorLayout = self.placeRoomIds(floorLayout) #places the room ids in the floor layout 
        
        return floorLayout
            
    def checkIfRoomIndexIsValid(self,roomIndexes,row,col):
        '''Checks if a room Index is valid'''
        tL = (row-1,col-1) in roomIndexes #top left
        t = (row-1,col) in roomIndexes #top
        tR = (row-1,col+1) in roomIndexes #top right
        l = (row,col-1) in roomIndexes #left
        r = (row,col+1) in roomIndexes #row
        bL = (row+1,col-1) in roomIndexes #bottom left
        b = (row+1,col) in roomIndexes #bottom 
        bR = (row+1,col+1) in roomIndexes #bottom right
        
        if tL and t and l:
            return False
        if t and tR and r:
            return False
        if bL and b and l:
            return False
        if b and bR and r:
            return False
        if t or b or l or r:
            return True
        return False
    
    def placeRoomTypesOnFloorLayout(self,floorLayout):
        
        for row in range(len(floorLayout)):
            for col in range(len(floorLayout[row])):
                if floorLayout[row][col] != bGI.empty:
                    if row == bGI.numRoomsHigh//2 and col == bGI.numRoomsWide//2:
                        floorLayout[row][col] = 'start'
                    else:
                        floorLayout[row][col] = 'normal'
        return floorLayout
    
    def placeRoomConnections(self,floorLayout):
        '''Places the connections between rooms in the floor layout'''
        for row in range(len(floorLayout)):
            for col in range(len(floorLayout[row])):
                if floorLayout[row][col] != bGI.empty:
                    floorLayout[row][col] = [floorLayout[row][col]]
                    if col != 0:
                        if floorLayout[row][col-1] != bGI.empty:
                            floorLayout[row][col].append('l')
                    if col != len(floorLayout[row])-1:
                        if floorLayout[row][col+1] != bGI.empty:
                            floorLayout[row][col].append('r')
                    if row != 0:
                        if floorLayout[row-1][col] != bGI.empty:
                            floorLayout[row][col].append('u')
                    if row != len(floorLayout)-1:
                        if floorLayout[row+1][col] != bGI.empty:
                            floorLayout[row][col].append('d')
        return floorLayout
        
    def placeRoomIds(self,floorLayout):
        '''Places the room ids in the floor layout'''
        dictConnectionsToRoomIds = defaultdict(set)
        dictRoomTypesToRoomIds = defaultdict(set)
        with open(bGI.roomLayoutsFileName) as f:
            lines = f.readlines()
        for i in range(7,7*len(lines)//7, 7):
            roomId = lines[i][:-1]
            roomType = lines[i+1][:-1]
            roomConnections = bFC.getTuplefromString(lines[i+6][:-1]) #line must have a \n at the end of it
            if roomId in self.possibleRoomIds:
                dictConnectionsToRoomIds[roomConnections].add(roomId)
                dictRoomTypesToRoomIds[roomType].add(roomId)
                
        for row in range(len(floorLayout)):
            for col in range(len(floorLayout[row])):
                if floorLayout[row][col] != bGI.empty:
                    roomConnections = tuple(floorLayout[row][col][1:])
                    roomType = floorLayout[row][col][0]
                    possibleRoomsBasedOnConnections = set()
                    for directionsKey in dictConnectionsToRoomIds.keys():
                        directionsIn = True
                        for direction in roomConnections:
                            if not direction in directionsKey:
                                directionsIn = False
                                break
                        if directionsIn:
                            possibleRoomsBasedOnConnections |= dictConnectionsToRoomIds[directionsKey]
                    possibleRoomsBasedOnType = dictRoomTypesToRoomIds[roomType]
                    possibleRooms = possibleRoomsBasedOnConnections.intersection(possibleRoomsBasedOnType)
                    floorLayout[row][col] = random.choice(tuple(possibleRooms))
            
        return floorLayout
    
    def addSpecialRoomTypes(self,floorLayout,endPoints):
        '''Adds in boss and item rooms into the floor layout'''
        for i in range(self.numItemRooms):
            roomIndex = random.choice(endPoints)
            endPoints.remove(roomIndex)
            floorLayout[roomIndex[0]][roomIndex[1]][0] = 'item'
        
        for i in range(self.numBossRooms):
            roomIndex = random.choice(endPoints)
            endPoints.remove(roomIndex)
            floorLayout[roomIndex[0]][roomIndex[1]][0] = 'boss'
        
        for i in range(self.numShopRooms):
            roomIndex = random.choice(endPoints)
            endPoints.remove(roomIndex)
            floorLayout[roomIndex[0]][roomIndex[1]][0] = 'shop'
        return floorLayout

    def addSecretRoomTypes(self,floorLayout):
        '''Adds in secret rooms into the floor layout'''
        numConnectionsIndexes = [[] for i in range(5)]
        for row in range(len(floorLayout)):
            for col in range(len(floorLayout[row])):
                numConnections = 0
                if floorLayout[row][col] == bGI.empty:
                    if col != 0:
                        if floorLayout[row][col-1] != bGI.empty:
                            numConnections += 1
                    if col != len(floorLayout[row])-1:
                        if floorLayout[row][col+1] != bGI.empty:
                            numConnections += 1
                    if row != 0:
                        if floorLayout[row-1][col] != bGI.empty:
                            numConnections += 1
                    if row != len(floorLayout)-1:
                        if floorLayout[row+1][col] != bGI.empty:
                            numConnections += 1
                    numConnectionsIndexes[numConnections].append((row,col))
        for i in range(self.numSecretRooms):
            for numConnections in range(4,-1,-1):
                if len(numConnectionsIndexes[numConnections]) != 0:
                    roomIndex = random.choice(numConnectionsIndexes[numConnections])
                    numConnectionsIndexes[numConnections].remove(roomIndex)
                    floorLayout[roomIndex[0]][roomIndex[1]] = 'secret'
                    break
        return floorLayout
            
    def getEndPoints(self,floorLayout):
        '''gets room end points that only have 1 connection'''
        endPoints = []
        for row in range(len(floorLayout)):
            for col in range(len(floorLayout[row])):
                if floorLayout[row][col] != bGI.empty:
                    directions = floorLayout[row][col][1:]
                    if len(directions) == 1:
                        endPoints.append((row,col))
        return endPoints
    
    def draw(self):
        '''draws the current room'''
        self.currentRoom.draw()

#child floor classes that have unique colours, music, and possible rooms
class boomBrownFloor(floor):
    def __init__(self, screen,space,oLoop, oPrinceEventHandler,oItemHandler,oPlayer):
        floorTileClr = (160,120,90)
        wallClr = (181,140,99)
        basicDoorClr = (123,63,0)
        shopRoomIds = ['normal shop room','cheap shop room','super shop room']
        normalRoomIds = ['corner spike room','rock goober room','spike cage room','blow up escape room']
        secretRoomIds = ['chest secret room','item secret room','item item secret room']
        itemRoomIds = ['normal item room','chest item room','double item room']
        bossRoomIds = ['leBoomBro boss room','leBro boss room','jackBlack boss room']
        startRoomIds = ['test start room']
        possibleRoomIds = normalRoomIds + itemRoomIds + bossRoomIds + startRoomIds + secretRoomIds + shopRoomIds
        numRooms = random.randint(8,12)
        musicFile = r'music\boomBrownMusic.mp3'
        super().__init__(screen,space,oLoop, oPrinceEventHandler,oItemHandler,oPlayer, floorTileClr, wallClr, basicDoorClr,
                         possibleRoomIds=possibleRoomIds,numRooms=numRooms,musicFile=musicFile)

class greyGolferFloor(floor):
    def __init__(self, screen,space, oLoop,oPrinceEventHandler,oItemHandler,oPlayer):
        floorTileClr = (100,120,100)
        wallClr = (120,120,120)
        basicDoorClr = (50,50,50)
        shopIds = ['normal shop room','cheap shop room']
        normalRoomIds = ['corner spike room','basic fly room','other fly room']
        secretRoomIds = ['normal secret room','chest secret room']
        itemRoomIds = ['normal item room','chest item room']
        bossRoomIds = ['longDivider boss room','schmeerestOfSchmoo boss room','lordOfTheFlies boss room',]
        startRoomIds = ['test start room']
        possibleRoomIds = normalRoomIds + itemRoomIds + bossRoomIds + startRoomIds + secretRoomIds + shopIds
        numRooms = random.randint(6,8)
        # numRooms = 15
        super().__init__(screen,space, oLoop,oPrinceEventHandler,oItemHandler,oPlayer, floorTileClr, wallClr, basicDoorClr,
                         possibleRoomIds=possibleRoomIds,numRooms=numRooms)
        
class fieryRedFloor(floor):
    def __init__(self, screen, space, oLoop, oPrinceEventHandler, oItemHandler, oPlayer):
        floorTileClr = (100, 120, 255)  # Bright blue
        wallClr = (60, 60, 200)         # Deep blue
        basicDoorClr = (40, 40, 150)    # Dark blue
        shopIds = ['normal shop room','cheap shop room','super shop room']
        normalRoomIds = ['corner spike room','rock cave room','spike cage room','blow up escape room','rock grid']
        secretRoomIds = ['chest secret room','item secret room','item item secret room']
        itemRoomIds = ['normal item room','chest item room','double item room']
        bossRoomIds = ['leBro boss room','kingOfTheFlies boss room','mrKrabs boss room']
        startRoomIds = ['test start room']
        possibleRoomIds = normalRoomIds + itemRoomIds + bossRoomIds + startRoomIds + secretRoomIds + shopIds
        numRooms = random.randint(9, 13)
        super().__init__(screen, space, oLoop, oPrinceEventHandler, oItemHandler, oPlayer, floorTileClr, wallClr, basicDoorClr,
                         possibleRoomIds=possibleRoomIds, numRooms=numRooms, musicFile=r'music\fieryRedMusic.mp3')

        
class endFloor(floor):
    def __init__(self, screen, space, oLoop, oPrinceEventHandler, oItemHandler, oPlayer):
        floorTileClr = (120, 80, 160)  # Deep lavender
        wallClr = (100, 50, 140)       # Deep indigo
        basicDoorClr = (140, 60, 170)  # Dark magenta
        shopIds = ['normal shop room','super shop room']
        normalRoomIds = ['saucy spike cage room','blow up escape room','saucy rock grid','saucy corner spike room']
        secretRoomIds = ['item secret room','item item secret room']
        itemRoomIds = ['double item room']
        bossRoomIds = ['chemistry boss room']
        startRoomIds = ['test start room']
        possibleRoomIds = normalRoomIds + itemRoomIds + bossRoomIds + startRoomIds + secretRoomIds + shopIds
        numRooms = random.randint(10, 15)
        super().__init__(screen, space, oLoop, oPrinceEventHandler, oItemHandler, oPlayer, floorTileClr, wallClr, basicDoorClr,
                         possibleRoomIds=possibleRoomIds, numRooms=numRooms,numItemRooms=1,musicFile=r'music\endFloorMusic.mp3')

