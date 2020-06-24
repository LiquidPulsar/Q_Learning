import pygame #needed to draw the fruits
from random import choice as c #we will need to do random spawn spots

class Fruits(): #make an array of fruits
    def __init__(self,GS,screen): #need stats and screen to draw to
        self.fruitnum = GS.fruitnum #get stuff treated for use in code here
        self.areaH=GS.height
        self.areaW=GS.width
        self.cs=GS.cellsize
        self.shrink=GS.shrink
        self.screen=screen
        game = [[i%self.areaW,i//self.areaW]for i in range(3,self.areaH*self.areaW)] #initialise a matrix of all cells in the play area, except for top left 3 as they have the score in them and dont want to overlap
        self.ARRAY = [] #no fruits
        for i in range(self.fruitnum): #add fruitnum fruits
            x = c(game) #randomly choose an available spot !can coincide with snake, must fix!
            game.remove(x) #cant choose this square again
            self.ARRAY.append(x) #add to list of fruit
        

    def blitus(self): #draw em
        for fruit in self.ARRAY: #draw for each fruit
            scalefactor=self.cs
            drawpos = (fruit[0]*scalefactor+self.shrink*self.cs/2,fruit[1]*scalefactor+self.shrink*self.cs/2,self.cs*(1-self.shrink),self.cs*(1-self.shrink))#format the position from matrix index to pixel value, take into account the shrink value
            pygame.draw.rect(self.screen,(255,0,0),drawpos) #draw it in, with colour red
    
    def respawn(self,snake): #need to avoid the snake segments
        game = [[i%self.areaW,i//self.areaW] for i in range(3,self.areaH*self.areaW)] #get matric for game again
        for [x,y] in snake:
            if [x,y] in game:
                game.remove([x,y]) #try and remove spawn slots so we dont overlap with snake
        self.ARRAY = [] #remove any fruit that would be there, always has to remove last fruit with current code iteration
        for i in range(self.fruitnum): #obvious tbh
            x = c(game)
            if x in game:
                game.remove(x)
            self.ARRAY.append(x) #same as before
