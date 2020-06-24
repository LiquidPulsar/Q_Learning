import random,math,json
from GAME import Game

class Q_Learner():
    
    def __init__(self,fullset,infin,useJson):
        self.idle_decay = -0.1
        self.learningRate = 0.85
        self.discountFactor = 0.9
        self.randomFactor = 0.05

        self.qTable = {}

        self.availableActions = ['up', 'down', 'left', 'right']
        self.opposite = {0:"down",2:"up",3:"right",1:"left"}
        self.convert_to_int = {"up":0,"down":2,"left":3,"right":1}
        self.score = 0
        self.missed = 0

        #self.fullSetOfStates = False
        self.fullSetOfStates = fullset
        #self.infin = True
        self.infin = infin

        self.useJson = useJson

    def whichStateNow(self):
        #tileCount = self.game.GS.width #length of arena, assume its square
        self.player = self.game.Snake
        
        self.fruit = self.game.fruits
        self.fruitRelativePose = {"x":0,"y":0}

        self.trail = [{"x":x,"y":y} for x,y in self.player.body]
        self.trail,self.headx,self.heady = self.trail[:-1],self.trail[-1]["x"],self.trail[-1]["y"]
        #we remove head piece cos eh thats what other guys code uses
        self.trailRelativePose = []

        #N.B: this is set to work with one fruit only
        self.fruitRelativePose["x"] = (self.fruit.ARRAY[0][0] - self.headx)
        self.fruitRelativePose["y"] = (self.fruit.ARRAY[0][1] - self.heady)

        stateName = str(self.fruitRelativePose["x"])+","+str(self.fruitRelativePose["y"])
        maxLength = len(self.trail) if self.fullSetOfStates else 1

        for index in range(maxLength):
            if index >= len(self.trailRelativePose):
                self.trailRelativePose.append({"x":0,"y":0})
            self.trailRelativePose[index]["x"] = (self.trail[index]["x"] - self.headx)
            self.trailRelativePose[index]["y"] = (self.trail[index]["y"] - self.heady)
            stateName += ","+str(self.trailRelativePose[index]["x"])+","+str(self.trailRelativePose[index]["y"])
        return stateName

    def whichTable(self,s):
        try:
            _ = self.qTable[s]
        except KeyError:
            self.qTable[s] = { 'up':0, 'down':0, 'left':0, 'right':0 }
        return self.qTable[s]
    
    def bestAction(self,s,dir):
        q = self.whichTable(s)
        self.availableActions = ['up', 'down', 'left', 'right']
        if not self.infin:
            mypos = self.game.Snake.body[-1]
            if mypos[0] <= 0:
                self.availableActions.remove("left")
            elif mypos[0] >= self.game.GS.width-1:
                self.availableActions.remove("right")
            
            if mypos[1] <= 0:
                self.availableActions.remove("up")
            elif mypos[1] >= self.game.GS.height-1:
                self.availableActions.remove("down")

        
        if dir != 4: #4 is special starting direction
            try:
                self.availableActions.remove(self.opposite[dir])
            except ValueError:
                pass
        
        if random.random() < self.randomFactor: #select random one sometimes so we can improve performance
            return random.choice(self.availableActions)
        
        maxValue = q[self.availableActions[0]]
        chooseAction = self.availableActions[0]
        actionsBest = []

        for elem in self.availableActions:
            if q[elem] >= maxValue:
                maxValue = q[elem]
                actionsBest.append(elem)
                chooseAction = elem

        if len(actionsBest) > 1:
            chooseAction = random.choice(actionsBest)
        
        #print(f"Chose: {chooseAction}, weights of {q}, bestlist: {actionsBest}")

        self.game.GS.snakeorient = self.convert_to_int[chooseAction]

        return chooseAction
    
    def updateQTable(self,state0,state1,reward,act):
        q0 = self.whichTable(state0)
        q1 = self.whichTable(state1)

        newValue =  reward + self.discountFactor * max(q1["up"],q1["down"],q1["left"],q1["right"]) - q0[act]
        self.qTable[state0][act] = q0[act] + self.learningRate*newValue
    
    def Algorithm(self):
        self.currentState = self.whichStateNow()
        action = self.bestAction(self.currentState,self.game.GS.snakeorient)
        self.game.run_loop(action)
        instantReward = self.game.reward
        nextState = self.whichStateNow()

        self.updateQTable(self.currentState, nextState, instantReward, action)

        if instantReward > 0:
            self.score += int(instantReward)
        elif instantReward < 0:
            self.missed += int(instantReward)
        
        
    def Train(self,num):
        if self.useJson:
            self.load()
        self.game = Game(False,self.infin)
        for _ in range(num):
            self.Algorithm()
        if self.useJson:
            self.dump()
        self.game = Game(True,self.infin)
        while True:
            self.Algorithm()

    def reset(self):
        self.qTable = {}
        self.score = 0
        self.missed = 0
    
    def dump(self):
        #with open("qTablefsos.txt","w") as file:
        with open("qTable.txt","w") as file:
            json.dump(self.qTable, file)
    
    def load(self):
        #with open("qTablefsos.txt") as file:
        with open("qTable.txt") as file:
            self.qTable = json.load(file)



def UI():
    print("For the following settings, simply pressing enter will use the default, and typing t then ENTER will use the other option")
    fullset = True if input("To see a slower, but eventually better at playing the game version type 't', otherwise this is off by default\n").lower() == "t" else False 
    infin = False if input("If you want to confine the snake in the play area with walls instead of having the game wrap around, type 't' or this is infinite by default\n").lower() == "t" else True 
    useJson = not fullset and infin

    try:
        num = int(input("Input the number of actions the AI should take before making the game visible. Invalid or blank answer will use the default of 100,000 training loops\n"))
    except:
        num = 100000

    learner = Q_Learner(fullset,infin,useJson)
    learner.Train(num)

UI()

#https://github.com/italohdc/LearnSnake
#https://github.com/italohdc/LearnSnake/blob/master/game.js
#https://github.com/italohdc/LearnSnake/blob/master/q-learning.js