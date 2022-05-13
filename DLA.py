import random
import pygame

class Application:
    def __init__(self):
        self.size = self.width, self.height = 640, 480 # Setting size of the window
        self.startX, self.startY = round(self.width/2), round(self.height/2) # Setting the starting point in the middle of the window
        self.X, self.Y = self.startX, self.startY # Initializing points
        self.displaySurface = None
        self.pixelArray = None
        self.pixelColor = None
        self.updateFlag = False
    
    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Random Walk")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.pixelColor = (0, 0, 255) # Hex code for blue color
        self.isRunning = True
    
        #sest a seed point
        self.pixelArray[self.startX, self.startY + 10] = 4278190335
        pygame.display.update()
    def on_event (self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        '''moving the pixels in a random direction'''
        # Choose a random direction to move
        newdirection = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0))) # Moves either +/- in Xdirection or +/- in Ydirection
        dX, dY = newdirection #Extracting the movements
        newX = self.X + dX
        newY = self.Y + dY # Applying the movements to the current X/Y coordinates

        if newX < 0:
            newX = 0

        if newX > self.width:
            newX = self.width
        
        if newY < 0:
            newY = 0

        if newY > self.height:
            newY = self.height

        #Check if this pixel is already set
        if (self.pixelArray[newX, newY] == 4278190335):
            self.updateFlag = True
        else:
            self.updateFlag = False
            self.X, self.Y = newX, newY
    
    def on_render(self):
        '''Updating the pixel array'''
        print(self.pixelArray[self.X, self.Y])
        if self.updateFlag == True:
            self.pixelArray[self.X, self.Y] = self.pixelColor
            pygame.display.update() #Updating the display

            #reset the update flag and random walk
            self.updateFlag = False
            self.X, self.Y = self.startX, self.startY


    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.on_loop()
            self.on_render()

        pygame.quit()


t = Application()
t.on_execute()