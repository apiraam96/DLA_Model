import random
import pygame

MOVES = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1))
FILLED = 0x808080
WIDTH = 640
HEIGHT = 480

class Application:
    def __init__(self):
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.startX, self.startY = round(self.width/2), round(self.height/2) # Setting the starting point in the middle of the window
        self.X, self.Y = self.startX, self.startY # Initializing points

        self.minX, self.minY = self.X, self.Y
        self.maxX, self.maxY = self.X, self.Y
        self.PadSize = 5

        self.domainMinX = self.startX - self.PadSize
        self.domainMinY = self.startY - self.PadSize
        self.domainMaxX = self.startX + self.PadSize
        self.domainMaxY = self.startX + self.PadSize

        self.displaySurface = None
        self.pixelArray = None
        self.updateFlag = False
    
    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Random Walk")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.isRunning = True
    
        #set a seed point
        self.pixelArray[self.startX, self.startY + 10] = FILLED
        pygame.display.update()

    def on_event (self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        '''moving the pixels in a random direction'''
        # Choose a random direction to move
        dX, dY = random.choice(MOVES)
        newX = self.X + dX
        newY = self.Y + dY # Applying the movements to the current X/Y coordinates

        if newX < self.domainMinX:
            newX = self.domainMaxX #implements a wrap around

        if newX > self.domainMaxX:
            newX = self.domainMinX
        
        if newY < self.domainMinY:
            newY = self.domainMaxY

        if newY > self.domainMaxY:
            newY = self.domainMinY

        #Check if this pixel is already set
        if (self.pixelArray[newX, newY] == FILLED):
            self.updateFlag = True

            #Modify the extent of the simulation domain
            if self.X < self.minX:
                self.minX = self.X

            if self.X > self.maxX:
                self.maxX = self.X

            if self.Y < self.minY:
                self.minY = self.Y

            if self.Y > self.maxY:
                self.maxY = self.Y

            #Modify the domain
            self.domainMinX = max([self.minX - self.PadSize, 1])
            self.domainMaxX = min([self.maxX + self.PadSize, self.width - 1])
            self.domainMinY = max([self.minY - self.PadSize, 1])
            self.domainMaxY = min([self.maxY + self.PadSize, self.height - 1])
            
        else:
            self.updateFlag = False
            self.X, self.Y = newX, newY
    
    def on_render(self):
        '''Updating the pixel array'''
        if self.updateFlag:
            self.pixelArray[self.X, self.Y] = FILLED
            pygame.display.update() #Updating the display

            #reset the update flag and random walk
            self.updateFlag = False
            #reset at a random point from all 4 sides of the domain
            newside = random.choice([1, 2, 3, 4])
            if newside == 1:
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMaxY
            elif newside == 2:
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
                self.X = self.domainMaxX
            elif newside == 3:
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMinY
            elif newside == 4:
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
                self.X = self.domainMinX

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