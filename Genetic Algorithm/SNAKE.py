import pygame #duh
from random import randint as r_i #used when getting start location
import math

class Snek(): #Snake class
    def __init__(self,GS,screen,infin): #we need Game stats and the screen to draw snake on
        self.screen=screen #get all the gamestats in
        if self.screen != False:
            self.screen=screen #get all the gamestats in
        self.length=GS.startlen
        self.areaH=GS.height
        self.areaW=GS.width
        self.cs=GS.cellsize
        self.shrink=GS.shrink
        x = r_i(0,self.areaW)
        y = r_i(0,self.areaH-self.length)
        #self.body = [[x,y] for y in range(y,y+self.length)]
        self.body = [[x,y] for i in range(y,y+self.length)]

        self.infin = infin
    
    def respawn(self): #make a new bebe snek
        x = r_i(1,self.areaW-1) #can take any x position, but preference not on border
        y = r_i(1,self.areaH-1) #any y position too, same as above
        #self.body = [[x,y] for y in range(y,y+self.length)]
        self.body = [[x,y] for i in range(self.length)] #stack segments on the same block, things will end up normal once snake moves, this allows for movement in any direction to start off the game

    def blitme(self): #draw bebe snek
        #for segment in [[i%self.areaW,i//self.areaW]for i in range(self.areaH*self.areaW)]:
        for segment in self.body:
            if self.screen != False:
                scalefactor=self.cs
                drawpos = (segment[0]*scalefactor+self.shrink*self.cs/2,segment[1]*scalefactor+self.shrink*self.cs/2,self.cs*(1-self.shrink),self.cs*(1-self.shrink))
                pygame.draw.rect(self.screen,(0,255,0),drawpos)

    def self_update(self,orient): #move according to the direction given in orient
        if orient == 0: #where the head will be
            futureheadpos=[self.body[-1][0],self.body[-1][1]-1]
        elif orient == 1:
            futureheadpos=[self.body[-1][0]+1,self.body[-1][1]]
        elif orient == 2:
            futureheadpos=[self.body[-1][0],self.body[-1][1]+1]
        elif orient == 3:
            futureheadpos=[self.body[-1][0]-1,self.body[-1][1]]
        else:
            return #this works with the orient=4 at start of game, so snek doesnt move until key pressed and orient becomes 0-3
        #self.body.append(futureheadpos) #we add a new segment to show where the head is
        if self.infin:
            self.body.append([futureheadpos[0]%self.areaW,futureheadpos[1]%self.areaH])
        else:
            self.body.append([futureheadpos[0],futureheadpos[1]])
        self.body.pop(0) #remove tail block, so overall we have moved the snake 1 along

    def Death(self): #check if illegal move happened
        if self.infin:
            if self.body[-1] in self.body[:-1]:
                return True
        elif self.body[-1] in self.body[:-1] or self.body[-1][0]<0 or self.body[-1][0]>=self.areaW or self.body[-1][1]<0 or self.body[-1][1]>=self.areaH: #did we hit a body segment or exit the play area?
            return True
        return False

    def Longer(self,num): #increase length
        for _ in range(num):
            self.body.insert(0,self.body[0]) #copy the tail segment num times, so the snake will end up longer visibly after a few moves
        
    def Get_Fruitdist(self,head,fruit):
        return(math.sqrt((fruit[0]-head[0])**2+(fruit[1]-head[1])**2))