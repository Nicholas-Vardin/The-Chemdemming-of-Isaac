'''
mainGame

by: Nicholas Vardin

This file contains the main game loop and the game class. 
The game class is responsible for initializing the game, updating the game state, 
and drawing the game screen. It also handles events and manages the main loop.

'''


import pygame as p
import pygameBasic as pb
import basicGameInfo as bGI
import kingEventClasses as kEC
import menuHandlerClass as mHC
import pygame.mixer


class game:
    def __init__(self): 
        '''Initializes the game class. This includes setting up the screen, clock,
        event handler, and menu handler. It also initializes the game state and timer.'''
        # Initialize the game screen and clock using pygameBasic setup
        self.screen, self.clock = pb.setup(bGI.screenWidth, bGI.screenHeight)
        
        # Set the initial state of the game to 'menu'
        self.state = 'menu' 
        
        # Initialize the king event handler and menu handler
        self.oKingEventHandler = kEC.kingEventHandler(self)
        self.oMainLoop = None
        self.oMenuHandler = mHC.menuHandler(self.screen, self, self.oKingEventHandler)
        
        # Timer for debugging or other purposes
        self.timer = 2
        
        # Add an event to play the menu music
        self.oKingEventHandler.addEvent(kEC.playMusicTrackEvent(r'music\menuMusic.mp3'))
        
        # Initialize the pygame mixer and set the music volume
        pygame.mixer.init()
        pygame.mixer.music.set_volume(.2)

    def update(self):
        '''Updates the game state. This includes processing events, updating the menu or main loop'''
        # Process all events using the king event handler
        self.oKingEventHandler.doEvents()

        # Update based on the current state of the game
        if self.state == 'menu':
            # Update the menu handler if in 'menu' state
            self.oMenuHandler.update()        
        elif self.state == 'main loop':
            # Update the main loop if in 'main loop' state
            self.oMainLoop.update()
            
            # Debugging: Stop after a limited number of frames
            # if self.timer == 0:
            #     raise Exception('stop')
            # else:
            #     self.timer -= 1

        # Debugging: Check and print FPS at intervals
        # if self.timer == 0:
        #     print(self.clock.get_fps())
        #     self.timer = 30
        # else:
        #     self.timer -= 1

        # Limit the frame rate to the defined FPS
        self.clock.tick(bGI.fps)
    
    def draw(self):
        '''Draws the current state of the game on the screen. This includes clearing the screen and drawing the menu or main loop.'''
        # Clear the screen with a white background
        self.screen.fill((255, 255, 255))
        
        # Draw based on the current state of the game
        if self.state == 'menu':
            # Draw the menu if in 'menu' state
            self.oMenuHandler.draw()
        elif self.state == 'main loop':
            # Draw the main loop if in 'main loop' state
            self.oMainLoop.draw()

def main():
    '''Main function to run the game. It initializes the game class and starts the main loop.'''
    # Create an instance of the game class and run the game
    oGame = game()
    pb.run(oGame)

# Run the main function if this file is executed directly
if __name__ == '__main__':
    main()
