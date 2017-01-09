
'''
RADHIKA GUPTA 112 TERM PROJECT

HOLIDAY FIGHTER!! 

'''


from tkinter import *
import random
from tkinter import Tk
import math
import tkinter.messagebox as tm
from helper import Button  #helper file found online and creates buttons
import os 
import ast #reads string dictionary as actual dictionary 

# removeDsStore.py from Kosbie
#run this program twice for the game to work
#first time removes DS store, second time, game works!! 
def removeDsStore(path):
    if (os.path.isdir(path) == False):
        if (path.endswith(".DS_Store")):
            os.remove(path)
    else:
        # recursive case: it's a folder
        for filename in os.listdir(path):
            removeDsStore(path + "/" + filename)

removeDsStore("RadhikaTermProject")


#Basics graphics template from Kosbie (online). 


class Monster(object):
    #creates the actual instances of monsters. 
    def __init__(self,data, x, y,letter, photo, level):
        self.x = x
        self.y = y + 35
        self.r = 15
        self.letter = letter
        self.allmonsters = []
        self.photo = photo
        self.level = level
        self.color = "red"

    def draw(self, canvas):
        if self.level ==1:
            self.color = "red"
            x1,y1 = self.x-(0.5*self.r),self.y-(2.5*self.r)-35
            x2,y2 = self.x+(0.5*self.r),self.y-(1.5*self.r)-35
        if self.level == 2:
            self.color = "white"
            x1,y1 = self.x-(0.5*self.r),self.y-(1.5*self.r)-35
            x2,y2 = self.x+(0.5*self.r), self.y -35
        if self.level ==3:
            self.color = "black"
            x1,y1 = self.x-(0.5*self.r),self.y-(1.5*self.r)-35
            x2,y2 = self.x+(0.5*self.r),self.y - 40
        if self.level ==4:
            self.color = "orange"
            x1,y1 = self.x-(0.5*self.r),self.y-(1.5*self.r) - 35
            x2,y2 = self.x+(0.5*self.r),self.y - 40

        canvas.create_image(self.x, self.y, image = self.photo)

        def drawLetters(self,canvas,x1,y1,x2,y2):
        #create letters above each monster

            if self.letter == "l": #horizontal line
                canvas.create_line(x1,y1,x1,y2, width = 5, fill = self.color)
                canvas.create_line(x1,y2,x2,y2, width = 5, fill = self.color)

            elif self.letter == "i": #vertical line
                canvas.create_line(self.x, y1,
                    self.x, y2, width = 5, fill = self.color)

            elif self.letter == "t":  #triangle
                canvas.create_line(self.x, y1,
                    self.x, y2, width = 5, fill = self.color)
                canvas.create_line(x1, y1,
                    x2, y1, width = 5, fill = self.color) 

        drawLetters(self,canvas,x1,y1,x2,y2)

    def onTimerFired(self, data):
        pass

class Santa(object):
    #creates the center Santa/ the main chararcter
    def __init__(self, data, x, y):
        self.x = x
        self.y = y
        self.r = 20
        self.fill = "pink"
        self.clickCount = 0
        self.xPos = data.width/2
        self.yPos = data.height/2

    def draw(self, canvas):

        canvas.create_oval(self.x-self.r, self.y-self.r,
                        self.x+self.r, self.y+self.r,
                         fill=self.fill)


    def onTimerFired(self, data):
        pass

        
class MovingMonster(Monster):

    lives = 5

    #allows the monsters to move. 

    def __init__(self,data, x, y, letter, photo, level, leftorright):
        super().__init__(self,x, y,letter,photo, level)
        #change speed with each level
        if data.level == 1:
            if data.leftorright == 0:self.speed = 10 # default initial speed
            else:self.speed = -10
        if data.level == 2:
            if data.leftorright == 0:self.speed = 20 # default initial speed
            else:self.speed = -20
        if data.level == 3:
            if data.leftorright == 0:self.speed = 30 # default initial speed
            else:self.speed = -30
        if data.level == 4:
            if data.leftorright == 0:self.speed = 40 # default initial speed
            else:self.speed = -40            

        self.letter = letter


    def onTimerFired(self, data):
        #allows monsters to move towards the center. 
        deltax = abs(data.width/2-self.x)
        if deltax == 0:
            slope = 0
        else:
            slope = ((data.width/2)/deltax)*data.level
        self.x+=self.speed
        if self.y == data.height/2:
            self.y +=0
        elif self.y < data.height/2:
            self.y+= (slope)
        else:
            self.y -= (slope)

        if (self.x > data.width):
            self.x = 5
        elif (self.x < 0):
            self.x = data.width


    def collision_detection(self, data):
        #if monster touches main guy, return true
        distance = ((((self.x - (data.width/2))**2) + 
            ((self.y - (data.height/2))**2))**0.5)
        collisiondistance = 60
        if distance < collisiondistance:
            return True
        else:
            return False

    def draw(self, canvas):
        super().draw(canvas)


class DrawingGrid(object):

    #from Eddie's ML demo

    def __init__(self,rows,cols,data):
        scale = 4
        self.grid = []
        self.rows = rows
        self.cols = cols
        self.rWidth = (data.width/scale) / self.cols
        self.rHeight = (data.height/scale) / self.rows
        self.clearBoard()

    def clearBoard(self):
        self.grid = []
        for row in range(self.rows):
            c = []
            for col in range(self.cols):
                c.append(1)
            self.grid.append(c)

    def draw(self,canvas,data):
        for row in range(self.rows):
            for col in range(self.cols):
                x = 1  + col * self.rWidth
                y = 1 + row * self.rHeight
                color = "pink" if self.grid[row][col] == 0  else "white"
                canvas.create_rectangle(x,y,x+self.rWidth,y +self.rHeight, 
                    fill = color, outline = "white")



def init(data):
    #adds the monsters to a list. 
    data.monsters = []
    data.time = 0
    data.mode = "splashScreen"
    data.lives = []
    data.drawingGrid = DrawingGrid(13,13,data)
    data.background = PhotoImage(file = "titlepage.gif")
    data.snowy = PhotoImage(file = "snowy.gif")
    data.santa = PhotoImage(file = "santa.gif")
    data.valentinesday = PhotoImage(file = "valentinesday.gif")
    data.easter = PhotoImage(file = "easter.gif")
    data.cupid = PhotoImage(file = "cupid.gif")
    data.bunny = PhotoImage(file = "bunny.gif")
    data.halloween = PhotoImage(file = "halloween.gif")
    data.ghost = PhotoImage(file = "ghost.gif")
    data.help = PhotoImage(file = "help.gif")
    data.snowman = PhotoImage(file = "snowman.gif")
    data.heart = PhotoImage(file = "heart.gif")
    data.egg = PhotoImage(file = "egg.gif")
    data.pumpkin = PhotoImage(file = "pumpkin.gif")
    data.lifeheart = PhotoImage(file = "lifeheart.gif")
    data.gameover = PhotoImage(file = "gameover.gif")
    data.gameOver = False 
    data.shapes = ["l","i","t"]
    data.classifiedletters, data.totalmonsters, data.vertical = [], [], []
    data.horizontal, data.buttons = [], []
    data.level, data.d = 1, 10
    data.tempusername, data.username = "", ""
    data.countdown = 3
    data.lev1info, data.lev2info = dict(), dict()
    data.lev3info, data.lev4info = dict(), dict()
    data.lkilledlev1 = 0 
    data.lkilledlev2 = 0 
    data.lkilledlev3 = 0 
    data.lkilledlev4 = 0 
    data.ikilledlev1 = 0
    data.ikilledlev2 = 0
    data.ikilledlev3 = 0
    data.ikilledlev4 = 0
    data.tkilledlev1 = 0
    data.tkilledlev2 = 0
    data.tkilledlev3 = 0   
    data.tkilledlev4 = 0
    data.allFiles = []
    data.newFile = None
    data.text= None
    data.countdowntime = 0
    data.levelchangetime = 0
    data.newlevel = False
    data.emptyscreen = False
    data.speed = 0
    data.monsterincrementer = 0
    data.pic = None
    data.color = ""
    makeButtons(data)


def findlines(data,board):
    #finds if a horizontal and vertical line are drawn. 
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                if board[row+1][col] == 0: #checks for vertical lines
                    data.vertical.append((row,col)) #adds it to a list
                if board[row][col+1] == 0:  #same with horizontal
                    data.horizontal.append((row,col))

    return ((data.vertical, data.horizontal))  #return tuple to compare

def isL(vertical, horizontal):
    #uses the tuple to check if it's an L
    if len(vertical) == 0 or len(horizontal) == 0: return False
    if ((vertical[-1][0]+1 == horizontal[0][0] 
        and vertical[-1][1] == horizontal[0][1])): #checks the corner of the L
       return True 
    else:
       return False

def isI(vertical):
    #checks to see if vertical boxes are drawn.
    if len(vertical) == 0: return False
    else:   
        initial = vertical[0][1]
        for tup in vertical:
            if tup[1] == initial:
                return True 
            else:
                return False

def isT(vertical, horizontal):
    #checks to see the connection between the top bar and vertical bar. 
    if len(vertical) == 0: return False
    else:   
        for tup in vertical: 
            if tup in horizontal: 
                return(True)
            else:
                return(False)

def classify(data):
    #classifies each letter and compares it to each letter the monster has. 
    board = data.drawingGrid.grid
    vertical, horizontal = findlines(data,board)
    if len(vertical)> 0 or len(horizontal) > 0: 
        #if the monster with the corres. letter
                # is there, then pop/get rid of him. 
        if isL(vertical,horizontal):
            for mon in data.monsters:
                if "l" == mon.letter:  
                    index = data.monsters.index(mon)
                    data.monsters.pop(index)
                    break  #need to break out or else itll keep popping. 
        elif isT(vertical,horizontal):
            for mon in data.monsters:
                if "t" == mon.letter: 
                    index = data.monsters.index(mon)
                    data.monsters.pop(index)
                    break
        elif isI(vertical):
            for mon in data.monsters:
                if "i" == mon.letter: 
                    index = data.monsters.index(mon)
                    data.monsters.pop(index)
                    break



def mousePressed(event, data): 
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "levelChange"): levelChangeMousePressed(event,data)
    elif (data.mode == "playGame"):   playGameMouseDragged(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)


def drawGameOver(canvas, data):
    lcount,icount,tcount = 0,0,0
    #will game over if the monsters touches the santa. 
    if (data.mode == "gameover"):
        canvas.create_image((data.height/2), (data.width/2), 
            image = data.gameover)
        for line in data.text:
            #reads thru the text file to get the stats. 
            dic = (ast.literal_eval(line))
            lcount += (dic["l"])
            icount += (dic["i"])
            tcount += (dic["t"])
        canvas.create_text(300, 400, text= "%s LOSES!!" %data.username.upper(), 
            font="Arial 25 bold", fill = "red")
        canvas.create_text(300,450,text="You lost to %d \"L\" Monsters"%lcount, 
            font="Arial 25 bold", fill = "red")
        canvas.create_text(300,475,text="You lost to %d \"I\" Monsters"%icount, 
            font="Arial 25 bold" ,fill = "red")
        canvas.create_text(300,500,text="You lost to %d \"T\" Monsters"%tcount, 
            font="Arial 25 bold" ,fill = "red")



def drawLevelChange(canvas, data):
    #will game over if the monsters touches the santa. 
    if (data.mode == "levelChange"):
        canvas.create_text(data.width/2, data.height/2,
                text="LEVEL UP!!", font="Arial 50 bold" , fill = "red")

def drawWin(canvas,data):
    #draws winning screen
    if (data.mode == "win"):
        canvas.create_text(data.width/2, data.height/2,
                text="YOU WIN!", font="Arial 50 bold", fill = "red")
        canvas.create_text(data.width/2, data.height/2 + 50,
                text="press space to play again!", font="Arial 30 bold", 
                fill = "red")

def winKeyPressed(event,data):
    #go back to beginning
    if (event.keysym == "space"):
        data.mode = "splashScreen"

def gameOverKeyPressed(event,data):
    if (event.keysym == "r"):
        init(data)

def redrawAll(canvas, data):

    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)

    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)
    elif (data.mode == "gameover") :   drawGameOver(canvas,data)
    elif (data.mode == "levelChange"): drawLevelChange(canvas,data)
    elif (data.mode == "win") : drawWin(canvas,data)


def keyPressed(event, data): 
    if data.mode == "playGame":
        if (event.char == "c"):
            classify(data)
            data.drawingGrid.clearBoard()  
            data.vertical = []
            data.horizontal = []                             
        if (event.char == "r"):
            data.drawingGrid.clearBoard()
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "win"): winKeyPressed(event,data)
    elif (data.mode == "gameover"): gameOverKeyPressed(event,data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data) 

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)
    elif (data.mode == "levelChange"): levelChangeTimerFired(data)

def levelChangeMousePressed(event,data): pass


def splashScreenTimerFired(data):
    timer = 25
    data.d=(data.d+1)%timer


def splashScreenKeyPressed(event, data): 
    #creates the username
    if (event.keysym in "abcdefghijklmnopqrstuvwxyz"):
        data.tempusername += event.keysym
    if (event.keysym == "BackSpace"):
        data.tempusername = data.tempusername[:-1]
    if (event.keysym == "Return"):
        data.username = data.tempusername
        createUsers(data)

def isFile(path):
    #checks to see if it's a file. 
    return os.path.isdir(path) == False


def getUserFiles(path, filename = ""): 
    if (isFile(path)):
        # base case:  not a folder, but a file
        #if (path.endswith(".rtf")):
        return [path]
    else:
        # recursive case: it's a folder
        userFiles = []
        for filename in os.listdir(path): #Iterate through every item in there
            curPath = path + os.sep + filename
            result = getUserFiles(curPath, filename)
            userFiles += result
        return userFiles


def createUsers(data):
    #creates the users
    data.allFiles=(getUserFiles("/Users/radhikagupta/Desktop/RadhikaTermProject/"))
    if len(data.allFiles) != 0:
        #need to make sure folder is/isnt already empty
        for i in range(len(data.allFiles)):
            paths = data.allFiles[i]
            file = open(paths, 'r')
            text = (file.readlines())
            file.close()
            if (data.username in paths):
                data.text = text
            else:
                data.newFile = open("/Users/radhikagupta/Desktop/" + 
                    "RadhikaTermProject/%s.txt" % data.username , "w")

    else: #first initital user
        data.newFile = open("/Users/radhikagupta/Desktop/RadhikaTermProject/%s.txt" % data.username , "w")


def makeButtons(data): 
    #creates the buttons using helper.py
    def game(data):
        data.mode = "playGame"

    def helpbtn(data):
        data.mode = "help"
    button1xpos = (100, 550)
    button1ypos = (200,580)
    button2xpos = (300, 550)
    button2ypos = (500,580)
    gameBtn = Button(button1xpos, button1ypos, "Play Game!!", "red", "white", 
        game, data)
    helpBtn = Button(button2xpos,button2ypos , "Click Here for Instructions!!",
     "red", "white", helpbtn, data)

    data.buttons.append(gameBtn)
    data.buttons.append(helpBtn)

def splashScreenMousePressed(event, data):
    for button in data.buttons:
        button.handleClick(event)

def splashScreenRedrawAll(canvas, data):
    for button in data.buttons:
        button.draw(canvas,data)
    canvas.create_image((data.width/2), (data.height/2), image =data.background)
    canvas.create_text(data.width/2-100, data.height/2+200,
            text="Please enter your username:", font="Arial 20 bold", 
            fill = "white")
    canvas.create_text(data.width/2+100, data.height/2+200,
            text=data.tempusername, font="Arial 20 bold", fill = "white")
    canvas.create_text(data.width/2, data.height/2-200,
                   text="Welcome to Holiday Fighter!!", font="Arial 26 bold", 
                   fill = "white")
    canvas.create_text(data.width/2, data.height/2+400,
            text="Your username: %s" % data.tempusername, font="Arial 20", 
            fill = "white")


def helpMousePressed(event, data):
    pass


def helpKeyPressed(event, data):
    data.mode = "splashScreen"

def helpRedrawAll(canvas, data):
    canvas.create_image(320, 300, image = data.help)

def helpTimerFired(data):
    pass

def playGameMouseDragged(event, data):
    row = int(event.y // data.drawingGrid.rHeight)
    col = int(event.x // data.drawingGrid.rWidth)
    
    if (row < data.drawingGrid.rows and col < data.drawingGrid.cols):
        if (row >= 0 and col >= 0):
            data.drawingGrid.grid[row][col] = 0

def writeFiles(data):
    #edits each file for each user depending on their stats for each LEVEL
    data.newFile = open("/Users/radhikagupta/Desktop/RadhikaTermProject/%s.txt" % data.username , 'a')
    if data.level == 1: 
        data.lev1info["l"],data.lev1info["i"]=data.lkilledlev1,data.ikilledlev1
        data.lev1info["t"] = data.tkilledlev1
        data.newFile.write(str(data.lev1info)+"\n") #write the stats 
    if data.level == 2: 
        data.lev2info["l"],data.lev2info["i"]=data.lkilledlev2,data.ikilledlev2
        data.lev2info["t"] = data.tkilledlev2
        data.newFile.write(str(data.lev2info)+"\n")
    if data.level == 3: 
        data.lev3info["l"],data.lev3info["i"]=data.lkilledlev3,data.ikilledlev3
        data.lev3info["t"] = data.tkilledlev3
        data.newFile.write(str(data.lev3info)+"\n")
    if data.level == 4: 
        data.lev4info["l"],data.lev4info["i"]=data.lkilledlev4,data.ikilledlev4
        data.lev4info["t"] = data.tkilledlev4
        data.newFile.write(str(data.lev4info)) 
    data.newFile.close()

def findKilled(data, monster):
    #finds which monsters you DIDNT kill to add it to the files/stats
    MovingMonster.lives -=1
    index = data.monsters.index(monster)
    if data.monsters[index].letter == "l":
        if data.level == 1:data.lkilledlev1 +=1
        elif data.level == 2:data.lkilledlev2 +=1
        elif data.level ==3:data.lkilledlev3 +=1
        elif data.level ==4:data.lkilledlev4+=1
    elif(data.monsters[index].letter == "i"):
        if data.level == 1:data.ikilledlev1 +=1
        elif data.level == 2:data.ikilledlev2 +=1
        elif data.level ==3:data.ikilledlev3 +=1
        elif data.level ==4:data.tkilledlev4+=1
    elif(data.monsters[index].letter == "t"):
        if data.level == 1:data.tkilledlev1 +=1
        elif data.level == 2:data.tkilledlev2 +=1
        elif data.level ==3:data.tkilledlev3 +=1
        elif data.level ==4:data.tkilledlev4+=1
    data.monsters.pop(index)


def addMonsters(data, picture): 
    #adds monsters to the screen. 
    if  data.newlevel == False:
        if data.letter == "l":
            snowmanl = MovingMonster(data,data.xPos, data.yPos, 
                data.letter,picture,data.level, data.leftorright)
            data.monsters.append(snowmanl)  #this list = VERY DESTRUCTIVE
            data.totalmonsters.append("l") #use this to change levels. 
        elif data.letter == "i":
            snowmani = MovingMonster(data,data.xPos, data.yPos,
                data.letter, picture, data.level,data.leftorright)
            data.monsters.append(snowmani)
            data.totalmonsters.append("i")
        else:
            snowmant = MovingMonster(data,data.xPos, data.yPos, 
                data.letter, picture, data.level,data.leftorright)
            data.monsters.append(snowmant)
            data.totalmonsters.append("t")

def nolives(data):
    #when you lose all your lives. 
    data.gameOver = True
    writeFiles(data)  #want to write data from current level too!!! 
    data.newFile.close()
    data.mode = "gameover"
    file = open("/Users/radhikagupta/Desktop/RadhikaTermProject/%s.txt"%data.username,'r')
    data.text = file.readlines()

def getinfo(data):
    #returns the speed for each monster, how many monsters per level and the 
    #type of monster for each level. 
    if data.level == 1: 
        data.speed,data.monsterincrementer,data.pic = 7, 7, data.snowman
    elif data.level == 2: 
        data.speed, data.monsterincrementer,data.pic = 4,10, data.heart
    elif data.level == 3: 
        data.speed, data.monsterincrementer,data.pic = 3,15, data.egg
    elif data.level == 4: 
        data.speed,data.monsterincrementer,data.pic = 2,20, data.pumpkin

def changeLevels(data):
    #writes in the files as you change levels and actually changes the level. 
    if (len(data.monsters) == 0):
        writeFiles(data)
    data.newlevel = True
    if data.emptyscreen and data.newlevel:
        data.level +=1
        data.mode = "levelChange"
        data.newlevel = False
        data.totalmonsters = []
    if data.level == 5:
        data.mode = "win"

def playGameTimerFired(data):
    #yay timer fired!! does the main things in the game. 
    data.time += 1  #slows down rate of monsters. 
    if data.time %2 == 0:data.countdown -=1
    data.letter = random.choice(data.shapes) #will choose a random shape. 
    if data.mode == "playGame": 
        data.leftorright = random.randint(0,1)
        if data.leftorright == 0: data.xPos = 0  #determines if coming from
        else: data.xPos = data.width                #left or right. 
        data.yPos = random.randint(150,500)
        for monster in data.monsters:
            monster.onTimerFired(data)
            if monster.collision_detection(data)==True:findKilled(data, monster)
            #monster collision and write in file. 
        if MovingMonster.lives == 0:nolives(data)
        #game over. 
        getinfo(data)
        if data.time%data.speed == 0:addMonsters(data, data.pic)
            #speeds down the rate at which monsters come. 
        if (len(data.monsters) == 0): data.emptyscreen = True
        else: data.emptyscreen = False
        if len(data.totalmonsters)==data.monsterincrementer:changeLevels(data)
        else: data.level +=0

def levelChangeTimerFired(data):
    #changes the level
    data.drawingGrid.clearBoard()
    data.time += 1
    if data.time%7 == 0:
        data.mode = "playGame"



def playGameKeyPressed(event, data):
    if data.mode == "playGame":
        if (event.keysym == 'h'):
            data.mode = "help"

def drawbackground(canvas,data):
    if data.level ==1:
        canvas.create_image(300, 300, image = data.snowy)
        data.color = "red"
    if data.level == 2:
        canvas.create_image(300, 300, image = data.valentinesday)
        data.color = "white"
    if data.level == 3:
        canvas.create_image(300, 300, image = data.easter)
        data.color = "black"
    if data.level == 4:
        canvas.create_image(300, 300, image = data.halloween)
        data.color = "orange"

def drawMainCharacter(canvas,data):
    #draws the middle guy
    if data.level ==1:
        canvas.create_image(300, 300, image = data.santa)
    if data.level ==2:
        canvas.create_image(300, 300, image = data.cupid)
    if data.level == 3:
        canvas.create_image(300, 300, image = data.bunny)
    if data.level == 4:
        canvas.create_image(300, 300, image = data.ghost)

def playGameRedrawAll(canvas, data):
    #draws background and monsters. 
    x,y = 450,20
    drawbackground(canvas,data)
    data.drawingGrid.draw(canvas,data)
    if data.mode == "playGame":
        for life in range(MovingMonster.lives): 
            canvas.create_image(x, y, image = data.lifeheart)
            x += 30
        for monster in data.monsters:
            monster.draw(canvas)
        canvas.create_text(data.width/2, 25, text="Level %d" % data.level, 
            font = "Arial 40 bold", fill = data.color)
        santa = Santa(data, data.width/2, data.height/2) 
        santa.draw(canvas)
    drawMainCharacter(canvas,data)
    #countdown in beg. 
    if data.countdown > 0:canvas.create_text(300,300, 
        text = "%d" % data.countdown, font="Arial 250 bold", fill = "red")
    if data.countdown == 0: 
        canvas.create_text(300,300, text = "GO!!",  font="Arial 250 bold", 
            fill = "red")
    if data.mode == "gameover":drawGameOver(canvas,data)




####################################
# use the run function as-is from Kosbie's notes. 
####################################


def run(width=300, height=300):


    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseDraggedWrapper(event, canvas, data):
        playGameMouseDragged(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    # create the root and the canvas
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)

    canvas.pack()
    # set up events
    root.bind("<B1-Motion>",lambda event:
                        mouseDraggedWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    #root.bind("<Any KeyPress>", lambda event: drawText(event.keysym,data))

    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(600, 600)
