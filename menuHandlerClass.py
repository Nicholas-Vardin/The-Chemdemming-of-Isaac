'''
MenuHandlerClass

By Nicholas Vardin

This files contains the menu handler class, a useless class that bloats the program
'''


import menuClasses as mC


class menuHandler:
    '''Class that handles menus'''
    def __init__(self,screen,oGame,oKingEventHandler):
        '''Initializes the handlers'''
        self.screen = screen
        self.oKingEventHandler = oKingEventHandler
        self.currentMenu = mC.mainMenu(self.screen,oGame,self.oKingEventHandler)

    def update(self):
        '''updates the menu'''
        self.currentMenu.update()

    def draw(self):
        '''draws the menu'''
        self.currentMenu.draw()
    
