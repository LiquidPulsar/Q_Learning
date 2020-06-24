class GStats():
    def __init__(self): #setup the variables for the game
        self.width = 10 #how many cells wide the play area is
        self.height = 10 #how many cells tall the play area is
        self.TPS = 40 #how many frames we want per second
        self.bgcolour = (255,255,255) #colour the background
        
        self.startlen = 2 #initial snake length
        self.lenstep = 2 #how many segments the snake increases for each fruit eaten
        
        self.cellsize = 40 #size in pixels of a cell
        self.shrink = 0.05 #size of border around each fruit or snake segment proportional to a square

        self.snakeorient = 4 #set to 4 so snake doesnt move until a key is pressed

        self.fruitnum = 1 #how many fruit spawn at a time

        self.points = 0 #duh
        
    def ResetStats(self):  #reset the dymnamic shit
        self.snakeorient = 4
        self.points=0