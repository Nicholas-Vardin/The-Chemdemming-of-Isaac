'''
King Event Classes

By Nicholas Vardin

This file contains the king event classes, which are responsible for handling events that occur in the game.
These events can be triggered by the player or by the game itself, and they can affect the game state,
the player, and other objects in the game.
'''

import mainLoopClass as mLC
import menuHandlerClass as mHC
import princeEventClasses
import menuClasses as mC
import pygame.mixer

class kingEventHandler:
    '''Handles events that occur in the game.'''
    def __init__(self,oGame):
        self.oGame = oGame 
        self.eventQueue = []

    def addEvent(self,oEvent):
        '''Adds an event to the event queue. The event will be executed in the order it was added.'''
        self.eventQueue.insert(0,oEvent)

    def doEvents(self):
        '''Executes all events in the event queue. Allows for additional events to be added while executing events.'''
        while len(self.eventQueue) != 0:
            oEvent = self.eventQueue.pop()
            oEvent.do(self.oGame)

class endLoopOnDeathEvent:
    '''Handles the event when the player dies, ending the main loop and switching to the death menu.'''
    def __init__(self):
        pass
    def do(self,oGame):
        # End the main loop
        oGame.oMainLoop = None
        # Add events to switch to the death menu and play the lose music
        oGame.oKingEventHandler.addEvent(switchToMenu(mC.deathMenu))
        oGame.oKingEventHandler.addEvent(playMusicTrackEvent(r'music\loseMusic.mp3',1))

class endLoopOnWinEvent:
    '''Handles the event when the player wins, ending the main loop and switching to the win menu.'''
    def __init__(self):
        pass
    def do(self,oGame):
        # End the main loop
        oGame.oMainLoop = None
        # Add events to switch to the win menu and play the win music
        oGame.oKingEventHandler.addEvent(switchToMenu(mC.winMenu))
        oGame.oKingEventHandler.addEvent(playMusicTrackEvent(r'music\winMusic.mp3'))

class switchToMenu:
    '''Handles switching the game state to a menu.'''
    def __init__(self,cMenu = mC.mainMenu,playMainMenuMusic = False):
        '''
        Initializes the switchToMenu event.
        - If no menu is provided, switches to the main menu.
        - Optionally plays the main menu music.
        '''
        self.cMenu = cMenu
        self.playMainMenuMusic = playMainMenuMusic

    def do(self,oGame):
        # Create the specified menu and set it as the current menu
        oMenu = self.cMenu(oGame.screen,oGame,oGame.oKingEventHandler) 
        oGame.oMenuHandler.currentMenu = oMenu
        # Change the game state to 'menu'
        oGame.state = 'menu'
        # Play main menu music if specified
        if self.playMainMenuMusic:
            oGame.oKingEventHandler.addEvent(playMusicTrackEvent(r'music\menuMusic.mp3'))

class switchGameStateToMainLoop:
    '''Handles switching the game state to the main loop.'''
    def __init__(self):
        pass  
    def do(self,oGame):
        # Change the game state to 'main loop'
        oGame.state = 'main loop'
        # Add an event to play the music for the current floor
        oGame.oKingEventHandler.addEvent(playMusicTrackEvent(oGame.oMainLoop.currentFloor.musicFile))
        
class beginNewLoop:
    '''Handles starting a new main loop.'''
    def __init__(self):
        pass  
    def do(self,oGame):
        # Change the game state to 'main loop'
        oGame.state = 'main loop'
        # Create a new main loop instance
        oGame.oMainLoop = mLC.mainLoop(oGame.screen,oGame.oKingEventHandler)
        
class playMusicTrackEvent:
    '''Handles playing a music track in the game.'''
    def __init__(self, file, numPlays=-1):
        '''
        Initializes the playMusicTrackEvent.
        - file: The path to the music file to be played.
        - numPlays: The number of times the track should loop. Default is -1 (infinite loop).
        '''
        self.file = file
        self.numPlays = numPlays

    def do(self, oLoop):
        '''
        Executes the event to play the specified music track.
        - Unloads any currently loaded music.
        - Loads the specified music file.
        - Plays the music track the specified number of times.
        '''
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play(self.numPlays)

