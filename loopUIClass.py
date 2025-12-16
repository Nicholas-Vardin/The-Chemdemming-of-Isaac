'''
loopUIClass

By Nicholas Vardin

This file contains the loopUI class, which is responsible for drawing the UI elements of the game.
It includes the player stats, inventory, health, and minimap UI.

'''


import basicGameInfo as bGI
import basicFunctionsAndClasses as bFC
import menuWidgetsClasses as mWC
import pygame as p
import pygame.gfxdraw


#load images 
heartImage = p.image.load(r'images\heartUIIcon.png')
evilHeartImage = p.image.load(r'images\evilHeartUIIcon.png')
soulHeartImage = p.image.load(r'images\soulHeartUIIcon.png')
emptyHeartImage = p.image.load(r'images\emptyHeartUIIcon.png')

class loopUI:
    '''Handles the UI elements of the game, including player stats, inventory, health, and minimap.'''
    def __init__(self, screen, oLoop):
        '''Initializes the loopUI and its components.'''
        self.screen = screen
        self.oPlayer = oLoop.oPlayer
        self.oPlayerStatsXTLPos = 20
        self.oLoop = oLoop
        self.oPlayerStatsTextBoxWidth = 100
        self.oPlayerStatsTextBoxHeight = 30

        # Initialize text boxes for player stats
        self.damageStatTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                             tLPos=bFC.tupleIntoNPArray((self.oPlayerStatsXTLPos, 180)),
                                             width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                             text='Damage: ', textSize=20, drawFilled=False)
        self.tearRateStatTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                               tLPos=bFC.tupleIntoNPArray((self.oPlayerStatsXTLPos, 210)),
                                               width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                               text='Tear Rate: ', textSize=20, drawFilled=False)
        self.tearSpeedStatTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                                tLPos=bFC.tupleIntoNPArray((self.oPlayerStatsXTLPos, 240)),
                                                width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                                text='Tear Speed: ', textSize=20, drawFilled=False)
        self.speedStatTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                            tLPos=bFC.tupleIntoNPArray((self.oPlayerStatsXTLPos, 270)),
                                            width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                            text='Speed: ', textSize=20, drawFilled=False)

        # Initialize text boxes for player inventory
        self.inventoryXTLPos = 20
        self.oPlayuerInventoryTextBoxWidth = 100
        self.oPlayerInventoryTextBoxHeight = 30
        self.oPlayerNumCoinsTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                                  tLPos=bFC.tupleIntoNPArray((self.inventoryXTLPos, 90)),
                                                  width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                                  text='Coins: ' + str(self.oPlayer.numCoins), textSize=20, drawFilled=False)
        self.oPlayerNumKeysTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                                 tLPos=bFC.tupleIntoNPArray((self.inventoryXTLPos, 120)),
                                                 width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                                 text='Keys: ' + str(self.oPlayer.numKeys), textSize=20, drawFilled=False)
        self.oPlayerNumBombsTextBox = mWC.textBox(self.screen, clr=(255, 255, 255), fontClr=(0, 0, 0),
                                                  tLPos=bFC.tupleIntoNPArray((self.inventoryXTLPos, 150)),
                                                  width=self.oPlayerStatsTextBoxWidth, height=self.oPlayerStatsTextBoxHeight,
                                                  text='Bombs: ' + str(self.oPlayer.numBombs), textSize=20, drawFilled=False)

        # Initialize boss health bar
        self.bossBarWidth = bGI.screenWidth - 150
        self.bossBarHeight = 20
        self.bossBarTLPos = (bGI.screenWidth // 2 - self.bossBarWidth // 2, bGI.screenHeight - self.bossBarHeight - 10)

        # Initialize minimap and active item UI components
        self.oMiniMapUI = miniMapUI(self.screen, oLoop)
        self.oActiveItemUI = activeItemUI(self.screen, oLoop)

    def updatePlayerStatsTextBoxes(self):
        '''Updates the text in the player stats text boxes.'''
        self.damageStatTextBox.text = 'Damage: ' + str(round(self.oPlayer.tearDamageStat.getValue(), 2))
        self.tearRateStatTextBox.text = 'Tear Rate: ' + str(round(self.oPlayer.tearRateStat.getValue(), 2))
        self.speedStatTextBox.text = 'Speed: ' + str(round(self.oPlayer.maxSpeedStat.getValue(), 2))
        self.tearSpeedStatTextBox.text = 'Tear Speed: ' + str(round(self.oPlayer.tearBaseSpeedStat.getValue(), 2))

    def updatePlayerInventoryTextBoxes(self):
        '''Updates the text in the player inventory text boxes.'''
        self.oPlayerNumCoinsTextBox.text = 'Coins: ' + str(self.oPlayer.numCoins)
        self.oPlayerNumKeysTextBox.text = 'Keys: ' + str(self.oPlayer.numKeys)
        self.oPlayerNumBombsTextBox.text = 'Bombs: ' + str(self.oPlayer.numBombs)

    def drawPlayerStats(self):
        '''Draws the player stats on the screen.'''
        self.updatePlayerStatsTextBoxes()
        self.damageStatTextBox.draw()
        self.tearRateStatTextBox.draw()
        self.tearSpeedStatTextBox.draw()
        self.speedStatTextBox.draw()

    def drawPlayerInventory(self):
        '''Draws the player inventory on the screen.'''
        self.updatePlayerInventoryTextBoxes()
        self.oPlayerNumCoinsTextBox.draw()
        self.oPlayerNumKeysTextBox.draw()
        self.oPlayerNumBombsTextBox.draw()

    def drawPlayerHealth(self):
        '''Draws the player's health on the screen.'''
        lHealth = self.oPlayer.lHealth

        # Map health types to their respective images
        dictIdImage = {'normal': heartImage, 'normal empty': emptyHeartImage, 'soul': soulHeartImage, 'evil': evilHeartImage}
        heartRad = 15  # Represents radius for circle drawn, change later when an actual heart is drawn

        # Spacing and positioning for hearts
        hSpacing = 10
        vSpacing = 10
        topSpacing = 15
        leftSpacing = 160
        maxHeartsPerRow = 6

        # Draw each heart based on the player's health
        for i, healthId in enumerate(lHealth):
            image = dictIdImage[healthId]
            drawPos = (i % maxHeartsPerRow * (hSpacing + heartRad * 2) + leftSpacing,
                       i // maxHeartsPerRow * (heartRad * 2 + vSpacing) + topSpacing)
            self.screen.blit(image, drawPos)

    def drawBossBar(self):
        '''Draws the boss health bar on the screen.'''
        totalStartHealth = 0
        totalCurrentHealth = 0
        lBosses = []

        # Collect all bosses in the current room
        for oEnemy in self.oLoop.currentFloor.currentRoom.lEnemies:
            if oEnemy.isBoss:
                lBosses.append(oEnemy)

        # If no bosses are present, return
        if len(lBosses) == 0:
            return

        # Calculate total health of all bosses
        for oBoss in lBosses:
            totalStartHealth += oBoss.startHealth
            totalCurrentHealth += oBoss.health

        # Calculate the width of the health bar based on remaining health
        healthBarWidth = self.bossBarWidth * totalCurrentHealth / totalStartHealth

        # Draw the background of the health bar
        p.draw.rect(self.screen, (100, 100, 100),
                    (self.bossBarTLPos[0], self.bossBarTLPos[1], self.bossBarWidth, self.bossBarHeight))

        # Draw the health portion of the bar
        p.draw.rect(self.screen, (255, 0, 0),
                    (self.bossBarTLPos[0], self.bossBarTLPos[1], healthBarWidth, self.bossBarHeight))

    def draw(self):
        '''Draws all UI components on the screen.'''
        self.drawPlayerHealth()
        self.drawPlayerStats()
        self.drawPlayerInventory()
        self.drawBossBar()
        self.oMiniMapUI.draw()
        self.oActiveItemUI.draw()
            
class miniMapUI:
    '''Handles the drawing of the minimap UI, showing the player's current position and discovered rooms.'''
    def __init__(self, screen, oLoop, width=100, height=100):
        '''Initializes the minimap UI with dimensions, colors, and room layout.'''
        self.screen = screen
        self.oLoop = oLoop
        self.width = width
        self.height = height
        self.tLPos = (bGI.screenWidth - self.width, 0)
        self.numRoomsWide = bGI.numRoomsWide + bGI.numRoomsWide % 2 - 1  # Ensure odd number of rooms wide
        self.numRoomsHigh = bGI.numRoomsHigh + bGI.numRoomsHigh % 2 - 1  # Ensure odd number of rooms high
        self.roomWidth = self.width / self.numRoomsWide
        self.roomHeight = self.height / self.numRoomsHigh

        # Define colors for different room types and discovery levels
        self.occupiedRoomClr = (0, 255, 0)
        self.discoveredRoomClr = (255, 255, 255)
        self.slightlyDiscoveredRoomClr = (120, 120, 120)

        self.itemRoomDiscoveredClr = (253, 169, 21)
        self.itemRoomOccupiedClr = (255, 220, 100)
        self.itemRoomSlightlyDiscoveredClr = (150, 75, 0)

        self.shopRoomDiscoveredClr = (253, 169, 21)
        self.shopRoomOccupiedClr = (255, 220, 100)
        self.shopRoomSlightlyDiscoveredClr = (150, 75, 0)

        self.bossRoomDiscoveredClr = (255, 0, 0)
        self.bossRoomOccupiedClr = (200, 0, 0)
        self.bossRoomSlightlyDiscoveredClr = (150, 0, 0)

        self.secretRoomDiscoveredClr = (0, 0, 255)
        self.secretRoomOccupiedClr = (0, 0, 200)
        self.secretRoomSlightlyDiscoveredClr = (0, 0, 150)

        # Map room types and discovery levels to their respective colors
        self.dictRoomTypeDiscoveryLvlToClr = {
            'normal': {1: self.slightlyDiscoveredRoomClr, 2: self.discoveredRoomClr, 'occupied': self.occupiedRoomClr},
            'item': {1: self.itemRoomSlightlyDiscoveredClr, 2: self.itemRoomDiscoveredClr, 'occupied': self.itemRoomOccupiedClr},
            'shop': {1: self.shopRoomSlightlyDiscoveredClr, 2: self.shopRoomDiscoveredClr, 'occupied': self.shopRoomOccupiedClr},
            'boss': {1: self.bossRoomSlightlyDiscoveredClr, 2: self.bossRoomDiscoveredClr, 'occupied': self.bossRoomOccupiedClr},
            'secret': {1: self.secretRoomSlightlyDiscoveredClr, 2: self.secretRoomDiscoveredClr, 'occupied': self.secretRoomOccupiedClr}
        }

    def draw(self):
        '''Draws the minimap on the screen, showing discovered and occupied rooms.'''
        currentRoomIndex = self.oLoop.currentFloor.currentRoomIndex
        center = [0, 0]

        # Determine the center of the minimap based on the player's current room
        if currentRoomIndex[0] < self.numRoomsHigh // 2:
            center[0] = bGI.numRoomsHigh // 2
        elif currentRoomIndex[0] >= bGI.numRoomsHigh - self.numRoomsHigh // 2:
            center[0] = bGI.numRoomsWide - 1 - self.numRoomsHigh // 2
        else:
            center[0] = currentRoomIndex[0]

        if currentRoomIndex[1] < self.numRoomsWide // 2:
            center[1] = bGI.numRoomsWide // 2
        elif currentRoomIndex[1] >= bGI.numRoomsWide - self.numRoomsWide // 2:
            center[1] = bGI.numRoomsWide - 1 - self.numRoomsWide // 2
        else:
            center[1] = currentRoomIndex[1]

        # Initialize a grid of rooms to be drawn
        drawnRooms = [[bGI.empty for _ in range(self.numRoomsWide)] for _ in range(self.numRoomsHigh)]
        for i in range(-1 * self.numRoomsHigh // 2, 1 + self.numRoomsHigh // 2):
            for j in range(-1 * self.numRoomsWide // 2, 1 + self.numRoomsWide // 2):
                if self.oLoop.currentFloor.floorLayout[center[0] + i][center[1] + j] != bGI.empty:
                    drawnRooms[i + self.numRoomsHigh // 2][j + self.numRoomsWide // 2] = (
                        self.oLoop.currentFloor.floorLayout[center[0] + i][center[1] + j].roomType,
                        self.oLoop.currentFloor.floorLayout[center[0] + i][center[1] + j].discoveryLevel,
                        (center[0] + i, center[1] + j)
                    )

        # Draw each room on the minimap
        for row in range(self.numRoomsHigh):
            for col in range(self.numRoomsWide):
                if drawnRooms[row][col] != bGI.empty:
                    roomType, discoveryLevel, floorLayoutIndex = drawnRooms[row][col]
                    if roomType == 'start':
                        roomType = 'normal'
                    if discoveryLevel != 0:
                        if floorLayoutIndex == self.oLoop.currentFloor.currentRoomIndex:
                            clr = self.dictRoomTypeDiscoveryLvlToClr[roomType]['occupied']
                        else:
                            clr = self.dictRoomTypeDiscoveryLvlToClr[roomType][discoveryLevel]
                        p.draw.rect(self.screen, clr, (self.tLPos[0] + col * self.roomWidth, self.tLPos[1] + row * self.roomHeight, self.roomWidth, self.roomHeight))
                        pygame.draw.rect(self.screen, (10, 10, 10), (self.tLPos[0] + col * self.roomWidth, self.tLPos[1] + row * self.roomHeight, self.roomWidth, self.roomHeight), 2)

class activeItemUI:
    '''Handles the UI for the player's active item, including its charge bar.'''
    def __init__(self, screen, oLoop):
        '''Initializes the active item UI with dimensions and colors.'''
        self.screen = screen
        self.oLoop = oLoop
        self.leftPadding = 30
        self.topPadding = 10
        self.chargeBarWidth = 20
        self.chargeBarHeight = 70
        self.chargeBarTLPos = (120, self.topPadding)
        self.chargesClr = (0, 255, 0)
        self.emptyClr = (50, 50, 50)
        self.chargeBarBorderClr = (0, 0, 0)
        self.chargeBarBorderWidth = 2

    def draw(self):
        '''Draws the active item's charge bar and icon on the screen.'''
        oItem = self.oLoop.oPlayer.activeItem
        if oItem is not None:
            # Draw the empty charge bar
            p.draw.rect(self.screen, self.emptyClr, (self.chargeBarTLPos[0], self.chargeBarTLPos[1], self.chargeBarWidth, self.chargeBarHeight))

            # Draw the filled portion of the charge bar based on the item's current charge
            chargesHeight = self.chargeBarHeight * oItem.currentCharge / oItem.maxCharge
            chargesTLPos = (self.chargeBarTLPos[0], self.chargeBarTLPos[1] + self.chargeBarHeight - chargesHeight)
            p.draw.rect(self.screen, self.chargesClr, (chargesTLPos[0], chargesTLPos[1], self.chargeBarWidth, chargesHeight))

            # Draw the border of the charge bar
            p.draw.lines(self.screen, self.chargeBarBorderClr, True,
                         [(self.chargeBarTLPos[0], self.chargeBarTLPos[1]),
                          (self.chargeBarTLPos[0] + self.chargeBarWidth, self.chargeBarTLPos[1]),
                          (self.chargeBarTLPos[0] + self.chargeBarWidth, self.chargeBarTLPos[1] + self.chargeBarHeight),
                          (self.chargeBarTLPos[0], self.chargeBarTLPos[1] + self.chargeBarHeight)],
                         self.chargeBarBorderWidth)

            # Draw separators for each charge level
            for i in range(1, oItem.maxCharge):
                y = self.chargeBarTLPos[1] + self.chargeBarHeight * i / oItem.maxCharge
                p.draw.line(self.screen, (0, 0, 0), (self.chargeBarTLPos[0], y), (self.chargeBarTLPos[0] + self.chargeBarWidth, y), 2)

            # Draw the active item's icon
            oItem.drawOnUI((self.leftPadding, self.topPadding + 10))