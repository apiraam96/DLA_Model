import random
import numpy as np
import pygame

class Application:
    def __init__(self):
        self.size = self.width, self.height = 640, 480 # Setting size of the window
        self.startX, self.startY = (self.width/2), (self.height/2) # Setting the starting point in the middle of the window
        self.X, self.Y = self.startX, self.startY # Initializing points
        self.displaySurface = None
        self.pixelArray = None
        self.pixelColor = None
    
    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Random Walk")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.pixelColor = (0, 255, 255) #Hex code for aqua blue color
        self.isRunning = True
    
    def on_event (self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        '''moving the pixels in a random direction'''
        # Choose a random direction to move
        newdirection = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0))) # Moves either +/- in Xdirection or +/- in Ydirection
        dX, dY = newdirection #Extracting the movements
        self.X += dX
        self.Y += dY # Applying the movements to the current X/Y coordinates

        if self.X > 0:
            self.X = 0

        if self.X > self.width - 1:
            self.X = self.width - 1
        
        if self.Y > 0:
            self.Y = 0

        if self.Y > self.height - 1:
            self.Y = self.height - 1


    def on_render(self):
        '''Updating the pixel array'''
        self.pixelArray[self.X, self.Y] = self.pixelColor

        pygame.display.update() #Updating the display


    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.on_loop()
            self.on_render()

        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()