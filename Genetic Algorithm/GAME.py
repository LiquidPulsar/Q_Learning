from GAME_STATS import GStats #get stats, so it looks clean
from SNAKE import Snek #get the snake class
from FRUIT import Fruits #get fruit class
from Score import Scoreboard as Sb #get score drawing stuff


import pygame, time, math, random #duh

class Game():
    def __init__(self,isgui,infin):
        self.GS = GStats() #init stats
        self.reward = 0
        self.infin = infin
        if isgui:
            self.isgui = True
            pygame.init() #start pygame session
            self.screen = pygame.display.set_mode((self.GS.width*self.GS.cellsize,self.GS.height*self.GS.cellsize)) #initialise display with size relative to cellsize and num of cells on board
            self.score=Sb(self.screen,self.GS) #prepare our score class
            pygame.display.set_caption("Snake") #Title
            self.Snake = Snek(self.GS,self.screen,self.infin) #initialise a Snek
            self.fruits = Fruits(self.GS,self.screen) #make a set of fruits
        else:
            self.isgui = False
            self.Snake = Snek(self.GS,False,self.infin) #initialise a Snek, no screen
            self.fruits = Fruits(self.GS,False) #make a set of fruits w/o screen imteraction
        
    def run_loop(self,AI_ACTION=False): #4 isnt a valid direction so we can ignore
        dist_to_fruit = min((self.Snake.Get_Fruitdist(self.Snake.body[-1],self.fruits.ARRAY[i])) for i in range(len(self.fruits.ARRAY)))
        maxdist = math.sqrt(self.GS.width**2+self.GS.height**2)
        self.reward = (dist_to_fruit / maxdist)*-0.4 #decay that varies depending on how close we are to fruit
        if self.isgui:
            self.screen.fill(self.GS.bgcolour) #wipe the screen from previous frame
            self.CheckEvents() #Change the movement direction according to user input
        #self.GS.snakeorient = self.Player.return_action(self.Snake.body[-1],self.GS.snakeorient,self.fruits.ARRAY,self.Snake)
        
        if AI_ACTION:
            dict_ = {'up':0, 'down':2, 'left':3, 'right':1} 
            self.Snake.self_update(dict_[AI_ACTION])
        else:
            self.Snake.self_update(self.GS.snakeorient) #move the snake
        

        if self.isgui:
            self.fruits.blitus() #draw the fruits
            self.Snake.blitme() #draw the snake
            self.score.blitme(self.screen,self.GS.points) #draw the score

        if self.Snake.Death(): #check if move was invalid
            self.reward = -10 #punish snake-san
            if self.isgui:
                self.screen.fill((255,255,255))#wipe
            self.GS.ResetStats() #reset all dynamic stats
            self.Snake.respawn() #new snek
            self.fruits.respawn(self.Snake.body) #get new fruits, avoid placing em in the snake

        elif self.Snake.body[-1] in self.fruits.ARRAY: #is snake head on top of a fruit?
            self.reward =  100 #reward snake-san
            if len(self.fruits.ARRAY)>1: #will we still have fruits after this fruit is eaten?
                self.fruits.ARRAY.remove(self.Snake.body[-1]) #remove the fruit at the head location, we ok
            else:
                self.fruits.respawn(self.Snake.body) #make a new set of fruits if this was last fruit - dont need to delete as the respawn wipes all fruits anyway
            self.Snake.Longer(self.GS.lenstep) #increase length of snake by step
            self.GS.points+=1 #add to score
        
        
        if self.isgui:
            pygame.display.flip() #render the display
            pygame.time.Clock().tick(self.GS.TPS) #regulated fps
            #pygame.time.Clock().tick(1000)
            #time.sleep(1/500)

        

    def CheckEvents(self):
        for event in pygame.event.get(): #check events
            if event.type == pygame.KEYDOWN: #only need keypress down, as snake will not stop if key released
                if event.key == pygame.K_RIGHT: #snakeorient represents direction of movement: N,E,S,W is 0,1,2,3
                    if self.GS.snakeorient != 3: #always check if the move would involve a straight U turn which is impossible
                        self.GS.snakeorient = 1
                elif event.key == pygame.K_LEFT:
                    if self.GS.snakeorient != 1:
                        self.GS.snakeorient = 3
                elif event.key == pygame.K_UP:
                    if self.GS.snakeorient != 2:
                        self.GS.snakeorient = 0
                elif event.key == pygame.K_DOWN:
                    if self.GS.snakeorient != 0:
                        self.GS.snakeorient = 2

if __name__ == "__main__": #only do this if we are running the file manually and not from our AI section
    game=Game(True,infin=False)
    while True:
        game.run_loop() #call gameloop