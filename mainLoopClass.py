'''
mainLoopClass.py

By Nicholas Vardin

This file contains the main loop class for the game. The main loop class is responsible for
initializing the game, updating the game state, and drawing the game screen. 
It also handles events and manages the main loop.
'''


import kingEventClasses as kEC
import pygame as p
import playerClass as pC
import princeEventClasses as pEC
import collisionHandlerClass as cHC
import itemClasses as iC
import floorClass as fC
import loopUIClass as lUIC
import pymunk as pk
import pymunk.pygame_util
import basicGameInfo as bGI
import menuClasses as mC


class mainLoop:
    def __init__(self, screen, oKingEventHandler):
        '''Initialize the main loop. This includes setting up the physics space,
        initializing the player, and setting up the current floor. '''
        # Initialize the main loop with the screen and king event handler
        self.screen = screen
        self.oKingEventHandler = oKingEventHandler

        # Set up the physics space with gravity and damping
        self.space = pk.Space()
        self.space.gravity = (0, 0)
        self.space.damping = 0.6

        # Initialize event handlers, collision handler, and item handler
        self.oPrinceEventHandler = pEC.princeEventHandler(self)
        self.oCollisionHandler = cHC.collisonHandler(self, self.oPrinceEventHandler)
        self.oItemHandler = iC.itemHandler(self.oPrinceEventHandler)

        # Initialize the player and add it to the physics space
        self.oPlayer = pC.player(self.screen, self.space, self.oPrinceEventHandler)
        self.oPlayer.addToSpace()

        # Initialize floor-related variables and set up the first floor
        self.numFloorsCompleted = 0
        self.currentFloor = fC.greyGolferFloor(
            self.screen, self.space, self, self.oPrinceEventHandler, self.oItemHandler, self.oPlayer
        )
        # Define possible floors based on the number of floors completed
        self.possibleFloorsAtCertainNumFloorCompletions = [
            [],
            [fC.boomBrownFloor, fC.fieryRedFloor],
            [fC.endFloor],
        ]

        # Add an event to unlock connecting doors in the current floor
        self.oPrinceEventHandler.addEvent(
            pEC.keyUnlockConnectingDoorsEvent(self.currentFloor.currentRoomIndex)
        )

        # Initialize the UI for the loop
        self.oUI = lUIC.loopUI(self.screen, self)

        # Set up floor switching and play the current floor's music
        self.switchFloor = True
        self.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(self.currentFloor.musicFile))

    def update(self):
        '''Update the main loop. This includes processing events, updating the player,
        updating the current floor, and stepping the physics simulation.'''
        # Process prince events
        self.oPrinceEventHandler.doEvents()
        # Update the current floor and player
        self.currentFloor.update()
        self.oPlayer.update()

        # Step the physics simulation
        self.space.step(1 / bGI.fps)
        # Check and respond to collisions
        self.oCollisionHandler.checkandRespond()

        # Check for key presses to handle specific actions
        keysPressed = p.key.get_pressed()
        if keysPressed[p.K_m]:
            # Switch back to the main menu screen
            self.oKingEventHandler.addEvent(
                kEC.switchToMenu(mC.mainMenu, playMainMenuMusic=True)
            )

    def draw(self):
        '''Draw the current state of the game. This includes drawing the physics space,
        the current floor, and the UI.'''

        # Draw the current floor and UI
        self.currentFloor.draw()
        self.oUI.draw()
