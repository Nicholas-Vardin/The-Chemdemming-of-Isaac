'''
Tile class

By Nicholas Vardin

This file contains the basic tile class that acts as a parent to all tiles
'''


class tile:
    '''Tile class that gives additional attributes to tiles'''
    def __init__(self):
        pass
    
    def instantiateTileAttributes(self,isEnemyGroundObstacle = False,isEnemyAirObstacle= False,isPlayerGroundObstacle = False,
                                  isPlayerAirObstacle = False,doesPhysicsWithPickUps = True,doesPhysicsWithBombs = True,
                                  damagesPlayerOnContact = False,breaksUponExplosion = False,hasContentInside = False):
        '''Gives additional attributes to tiles'''
        
        self.isEnemyGroundObstacle = isEnemyGroundObstacle
        self.isEnemyAirObstacle = isEnemyAirObstacle
        self.isPlayerGroundObstacle = isPlayerGroundObstacle
        self.isPlayerAirObstacle = isPlayerAirObstacle

        #add in more attributes later maybe
        # self.doesPhysicsWithBombs = doesPhysicsWithBombs
        # self.doesPhysicsWithPickUps = doesPhysicsWithPickUps
        # self.damagesPlayerOnContact = damagesPlayerOnContact
        # self.breaksUponExplosion = breaksUponExplosion
        # self.hasContentInside = hasContentInside

