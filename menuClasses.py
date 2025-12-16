'''
menuClasses.py

By Nicholas Vardin

This file contains the menu classes for the game.
The menu classes are responsible for displaying the main menu, death menu, and win menu.

'''


import menuWidgetsClasses as mWC
import basicFunctionsAndClasses as bFC
import basicGameInfo as bGI
import numpy as np
import pygameBasic as pb
import kingEventClasses as kEC


class menu:
    '''This class is the base class for all menus.'''
    def __init__(self,screen,oGame, oKingEventHandler,backgroundClr,lWidgets = []):
        '''Initializes the menu class.'''
        self.screen = screen
        self.oKingEventHandler = oKingEventHandler
        self.backgroundClr = backgroundClr
        self.lWidgets = lWidgets
        self.oGame = oGame
    
    def update(self):
        '''Updates the menu. This includes updating all widgets and checking for events.'''
        for oWidget in self.lWidgets:
            if hasattr(oWidget,'update'):
                oWidget.update()
    
    def draw(self):
        '''Draws the menu. This includes drawing all widgets.'''
        self.screen.fill(self.backgroundClr)
        for oWidget in self.lWidgets:
            oWidget.draw()

class mainMenu(menu):
    '''This class represents the main menu of the game.'''
    def __init__(self,screen,oGame,oKingEventHandler):
        '''Initializes the main menu with buttons and widgets.'''
        self.oGame = oGame
        newGameButtonWidth = 400
        newGameButtonHeight = 150
        continueGameButtonWidth = 400
        continueGameButtonHeight = 150
        
        # Define colors for the continue game button based on game state
        continueGameButtonNoCurrentLoopClr = (255,0,0)
        continueGameButtonCurrentLoopClr = (0,255,0)
        if oGame.oMainLoop == None:
            continueGameButtonClr = continueGameButtonNoCurrentLoopClr
        else:
            continueGameButtonClr = continueGameButtonCurrentLoopClr
            
        # Create the title text box
        self.titleTextBox = mWC.textBox(screen,(0,0,0),fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth/2-200,bGI.screenHeight/2-200]),
                                        width = 400, height= 150,
                                        text= 'The Chemdemming of Isaac', textSize= 50,drawFilled=False,
                                        fontType= 'Comic Sans MS')

        # Create the new game button
        self.newGameButton  = mWC.button(screen,(0,255,0),fontClr=(0,0,0),
                                       tLPos=np.array([100,bGI.screenHeight/2]),
                                        width = newGameButtonWidth, height= newGameButtonHeight,
                                        text= 'Start New Game', textSize= 50)
        
        # Create the continue game button
        self.continueGameButton  = mWC.button(screen,continueGameButtonClr,fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth-continueGameButtonWidth-100,
                                                       bGI.screenHeight/2]),
                                        width = continueGameButtonWidth, height= continueGameButtonHeight,
                                        text= 'Continue Game', textSize= 50)
        
        # List of widgets for the main menu
        lWidgets = [self.newGameButton,self.continueGameButton,self.titleTextBox]
        super().__init__(screen,oGame,oKingEventHandler,(220,220,255),lWidgets)

    def update(self):
        '''Updates the main menu and handles button events.'''
        super().update()

        # Check if the new game button is released
        if self.newGameButton.state == 'released':
            self.oKingEventHandler.addEvent(kEC.beginNewLoop())
        # Check if the continue game button is released and a game loop exists
        elif self.continueGameButton.state == 'released' and self.oGame.oMainLoop != None:
            self.oKingEventHandler.addEvent(kEC.switchGameStateToMainLoop())
        
class deathMenu(menu):
    '''This class represents the death menu of the game.'''
    def __init__(self, screen,oGame, oKingEventHandler):
        '''Initializes the death menu with buttons and widgets.'''
        backToMenuButtonWidth = 400
        backToMenuButtonHeight = 200
        
        # Create the "You Lose" text box
        self.youLoseTextBox = mWC.textBox(screen,(0,0,0),fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth/2-200,bGI.screenHeight/2-200]),
                                        width = 400, height= 150,
                                        text= 'You Lose', textSize= 70,drawFilled=False,
                                        fontType= 'Comic Sans MS')
        
        # Create the back to main menu button
        self.backToMenuButton  = mWC.button(screen,(0,255,0),fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth/2-backToMenuButtonWidth/2,
                                                       bGI.screenHeight/2]),
                                        width = backToMenuButtonWidth, height= backToMenuButtonHeight,
                                        text= 'Back to Main Menu', textSize= 50)
        
        # List of widgets for the death menu
        lWidgets = [self.backToMenuButton,self.youLoseTextBox]
        super().__init__(screen, oGame,oKingEventHandler, (255,220,220), lWidgets)
    
    def update(self):
        '''Updates the death menu and handles button events.'''
        super().update()
        
        # Check if the back to main menu button is released
        if self.backToMenuButton.state == 'released':
            self.oKingEventHandler.addEvent(kEC.switchToMenu(mainMenu,playMainMenuMusic= True))
    
class winMenu(menu):
    '''This class represents the win menu of the game.'''
    def __init__(self, screen,oGame, oKingEventHandler):
        '''Initializes the win menu with buttons and widgets.'''
        backToMenuButtonWidth = 400
        backToMenuButtonHeight = 200
        
        # Create the "You Win" text box
        self.youWinTextBox = mWC.textBox(screen,(0,0,0),fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth/2-200,bGI.screenHeight/2-200]),
                                        width = 400, height= 150,
                                        text= 'You Win', textSize= 70,drawFilled=False,
                                        fontType= 'Comic Sans MS')
        
        # Create the back to main menu button
        self.backToMenuButton  = mWC.button(screen,(0,255,0),fontClr=(0,0,0),
                                       tLPos=np.array([bGI.screenWidth/2-backToMenuButtonWidth/2,
                                                       bGI.screenHeight/2]),
                                        width = backToMenuButtonWidth, height= backToMenuButtonHeight,
                                        text= 'Back to Main Menu', textSize= 50)
        
        # List of widgets for the win menu
        lWidgets = [self.backToMenuButton,self.youWinTextBox]
        super().__init__(screen, oGame,oKingEventHandler, (220,200,255), lWidgets)
    
    def update(self):
        '''Updates the win menu and handles button events.'''
        super().update()
        
        # Check if the back to main menu button is released
        if self.backToMenuButton.state == 'released':
            self.oKingEventHandler.addEvent(kEC.switchToMenu(mainMenu,playMainMenuMusic=True))  


class test:
    '''This class is used for testing the menu system.'''
    def __init__(self):
        '''Initializes the test environment.'''
        self.screen, self.clock = pb.setup(bGI.screenWidth,bGI.screenHeight)
        self.mainMenu = mainMenu(self.screen,1)
    def update(self):
        '''Updates the test environment.'''
        self.mainMenu.update()

    def draw(self):
        '''Draws the test environment.'''
        self.screen.fill((255,255,255))
        self.mainMenu.draw()
        

def main():
    '''Main function to run the test environment.'''
    oTest = test()
    pb.run(oTest)

if __name__ == '__main__':
    main()