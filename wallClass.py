'''
Wall Class

By Nicholas Vardin

This file contains the wall class that is a wall
'''

import pygame as p
import numpy as np
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import pymunk as pk
import tileClass as tlC

class wall(bFC.physicsRect,tlC.tile):
    '''Wall Class that is a wall'''
    def __init__(self, screen, space, clr, center, width = bGI.basicTileWidth, height = bGI.basicTileHeight):
        '''Initializes object'''
        super().__init__(screen, space, clr, center, width, height, collisionType = 2)
        self.instantiateTileAttributes(isEnemyGroundObstacle=True,isEnemyAirObstacle=True,
                                       isPlayerGroundObstacle=True,isPlayerAirObstacle=True)
