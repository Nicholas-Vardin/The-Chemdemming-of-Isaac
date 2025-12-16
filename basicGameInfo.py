'''
Basic Game Info

By: Nicholas Vardin

A program that stores constants for the game
'''

import numpy as np

screenHeight = 600 
screenWidth = 1200
fps = 60

numTilesWide = 24
numTilesHigh =12

basicTileWidth = screenWidth/numTilesWide #50
basicTileHeight = screenHeight/numTilesHigh #50

# numRoomsWide = 9
# numRoomsHigh = 9
numRoomsWide = 5
numRoomsHigh = 5

empty = '' #a variable to represent an empty space used for readablity

normalFont = 'Arial' #default font used for text boxes

roomLayoutsFileName = 'roomLayouts.txt'
roomLayoutsTxtNumLines = 7 #num lines used to define a room in room layouts text file

itemRoomWallClr = (253,169,21) #clrs for special rooms
shopRoomWallClr = (100,50,10)
shopFloorClr = (170,120,80)

#positions for doors based on which direction there are given
basicDoorCenterPos = {'up':np.array([basicTileWidth*numTilesWide/2,basicTileHeight/2]),
                  'down':np.array([basicTileWidth*numTilesWide/2,basicTileHeight*(numTilesHigh-.5)]),
                  'left':np.array([basicTileWidth/2,basicTileHeight*numTilesHigh/2]),
                  'right':np.array([basicTileWidth*(numTilesWide-.5),basicTileHeight*numTilesHigh/2])} 

#door priority to see which is placed over the other
doorPriority = ['secret','boss','item','shop','normal','start'] #lower index has the highest priority