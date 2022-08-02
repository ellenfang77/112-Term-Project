#TP
#andrewid: ellenf
import tkinter as tk
from cmu_112_graphics import *
import math as math
import random as random

def appStarted(app):
    resetApp(app)

class Lshape(object):
    def __init__(self, shape):
        self.shape = shape
    def addShape(self):
        self.shape = (self.shape + 1) % 4
    def __repr__(self):
        return repr(object)

class Ishape(object):
    def __init__(self, shape):
        self.shape = shape
    def addShape(self):
        self.shape = (self.shape + 1) % 2
    def __repr__(self):
        return repr(object)

def resetApp(app):
    app.maplevel = 0
    app.startGame = False
    app.startEasy = False
    app.startMed = False
    app.startHard = False
    app.drawEnd = False
    app.overflow = 0
    app.possShapes = []
    app.possShapesSoln = []
    if(app.startEasy):
        app.possShapes = easyMaps(app)
    elif(app.startMed):
        app.possShapes = medMaps(app)
    elif(app.startHard):
        app.possShapes = hardMaps(app)
    if(app.startEasy or app.startMed or app.startHard):
        app.shapes = app.possShapes[0]
    resetGrid(app)

def resetGrid(app):
    app.level = ""
    app.rows = 6
    app.cols = 9
    app.margin = 70
    app.grid = []
    app.hintmargin = 100
    app.gameOver = False
    app.a = None

    for row in range(app.rows):
        for col in range(app.cols):
            bounds = getCellBounds(app, row, col)
            app.grid.append(bounds)
    
    app.shapes = [] #[[-1 for x in range(app.cols)] for y in range(app.rows)] 
    app.shapesonly = []  #contains only rows and cols of the tiles with shapes
    app.usedindeces = []

    for a in range(len(app.shapes)):
        for b in range(len(app.shapes[0])):
            if (app.shapes[a][b] != -1):
                app.shapesonly.append((app.shapes[a][b], a, b))

    app.B = []
    app.gems = int(readFile("gems.txt"))
    app.runwater = []

    app.hints = []
    app.giveHint = 0
    app.hintGrid = []
    app.hintPathLegal = False

    for row in range(app.rows):
        for col in range(app.cols):
            bounds = getCellBoundsHint(app, row, col)
            app.hintGrid.append(bounds)
    
    app.hintShapes = []
    hintShapes(app)
    app.hintRow = 0
    app.hintCol = 0
    app.hintShape = ""
    app.hintShapeNum = 0
    app.overflow = 0
    app.drawEnd = False
    app.drawShop = False
    app.drawInstr = False
    app.background = 0
    app.bought = ""

    app.rect_y_3 = 0
    app.rect_x_3 = 1/4
    app.rect_x2_3 = 3/4

    app.rect_y_0 = 1/4
    app.rect_x_0 = 1/4
    app.rect_x2_0 = 3/4

    app.bx_0 = 0
    app.by_0 = 1/4
    app.by2_0 = 3/4

    app.L023x = 0
    app.L023y = 1/4

    app.L032x = 1/4
    app.L032y = 0

    app.L134x = 1/4
    app.L134y = 0

    app.L143x = 0
    app.L143y = 1/4

    app.L214x = 1/4
    app.L214y = 0

    app.L241x = 0
    app.L241y = 1/4

    app.L312x = 1/4
    app.L312y = 1/4

    app.L321x = 0
    app.L321y = 1/4

    app.I1y = 0
    app.I0x = 0

    app.waternum = 0
    app.waternumhelper = 0

    app.overflow = 0
    app.possShapes = []
    app.image1 = app.loadImage('sand.jpg')
    app.image2 = app.scaleImage(app.image1, 1)
    app.image3 = app.loadImage('sand2.jpg')
    app.image4 = app.scaleImage(app.image3, 1)
    app.water0 = app.loadImage('water0.jpg')
    app.water1 = app.loadImage('water1.jpg')
    app.water2 = app.loadImage('water2.jpg')
    app.sidesand = app.loadImage('sidesand.jpg')
    app.water1display = app.loadImage('water1display.jpg')
    app.water2display = app.loadImage('water2display.jpg')
    app.price1 = 15
    app.price2 = 30

#citation: http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def pointInGrid(app, x, y):
    return ((app.margin <= x <= 1000-app.margin) and
            (app.margin <= y <= 700-app.margin))

#citation: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = 1000 - 2*app.margin #1000 - 140 = 860
    gridHeight = 700 - 2*app.margin
    cellWidth  = gridWidth / app.cols #860/9 = 95
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

#citation: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    #returns (x0, y0, x1, y1) bounds box of given cell in grid
    gridWidth  = 1000 - 2*app.margin
    gridHeight = 700 - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    cx = x0 + (0.5 * cellWidth)
    cy = y0 + (0.5 * cellHeight)
    return (x0, y0, x1, y1, cx, cy)

#citation: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBoundsHint(app, row, col):
    gridWidth  = 800 - 2*app.margin
    gridHeight = 500 - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + app.hintmargin + col * cellWidth
    x1 = app.margin + app.hintmargin + (col+1) * cellWidth
    y0 = app.margin + app.hintmargin + row * cellHeight
    y1 = app.margin + app.hintmargin + (row+1) * cellHeight
    cx = x0 + (0.5 * cellWidth)
    cy = y0 + (0.5 * cellHeight)
    return (x0, y0, x1, y1, cx, cy)

def mousePressed(app, event):
    x = event.x
    y = event.y
    if(app.startGame == False and app.drawShop == False):
        if(x>100 and x<250 and y>200 and y<280 and app.startEasy == False):
            app.level = "Easy"
            app.startEasy = True
            app.possShapes = easyMaps(app)
            app.shapes = app.possShapes[app.maplevel]
        elif(x>325 and x<475 and y>200 and y<280 and app.startMed == False):
            app.level = "Medium"
            app.startMed = True
            app.possShapes = medMaps(app)
            app.shapes = app.possShapes[app.maplevel]
        elif(x>550 and x<700 and y>200 and y<280 and app.startHard == False):
            app.level = "Hard"
            app.startHard = True
            app.possShapes = hardMaps(app)
            app.shapes = app.possShapes[app.maplevel]

    if(x>900 and x<990 and y>10 and y<40):
        app.B = []
        app.usedindeces = []
        if(app.startGame == True):
            if(app.maplevel < 9):
                app.overflow = 0
                app.maplevel += 1
                app.shapes = app.possShapes[app.maplevel]
                app.hintPathLegal = False
            if(app.maplevel >= 9):
                app.overflow = 0
                app.drawEnd = True
                app.hintPathLegal = False
    
    if(x>800 and x<880 and y>10 and y<40):
        app.gems = 0
        app.overflow = 0
        resetApp(app)
    
    #next level when win
    if(x>440 and x<560 and y>500 and y<540 and (app.overflow == 1 or app.overflow == 2)): 
        if(app.maplevel < 9):
            app.overflow = 0
            app.maplevel += 1
            app.shapes = app.possShapes[app.maplevel] 
            app.gameOver = True
            app.hintPathLegal = False
        app.B = []
        app.usedindeces = []
        
    #redo the level
    if(x>450 and x<550 and y>430 and y<470 and (app.overflow == 1 or app.overflow == 2)): 
        app.B = []
        app.usedindeces = []
        app.overflow = 0
        app.shapes = app.possShapes[app.maplevel]
        app.gems += len(app.B)
        writeFile('gems.txt', str(app.gems))
        app.hintPathLegal = False
        app.giveHint == 0
        resetGrid(app)

    if(x>250 and x<550 and y>300 and y<400):
        if(app.startGame == False and 
        (app.startEasy == True or app.startMed == True or app.startHard == True)):
            app.startGame = True

    #when the square is clicked on, it rotates the grid 90 degrees clockwise
    if(event.x>70 and event.x<930 and event.y>70 and event.y<630):
        if(app.startGame == True and app.overflow == 0):
            (row, col) = getCell(app, event.x, event.y)
            if(isinstance(app.shapes[row][col], Lshape)):
                n = app.shapes[row][col] 
                n.addShape()
            if(isinstance(app.shapes[row][col], Ishape)):
                n = app.shapes[row][col] 
                n.addShape()
        
    if(event.x >835 and event.x < 855 and event.y>150 and event.y<170):
        app.giveHint = 0
        app.B = []
        app.hintShapes = []

    if(event.x > 450 and event.x < 550 and event.y > 500 and event.y < 550 and app.drawEnd == True):
        resetApp(app)

    if(event.x > 450 and event.x < 550 and event.y > 450 and event.y < 500 and app.startGame == False):
        app.drawShop = True
    
    if(app.drawShop == True and event.x > 200 and event.x < 450 and event.y > 200 and event.y <450):
        if(app.gems > app.price1):
            app.background = 1
            app.water = app.water1
            writeFile('gems.txt', str(app.gems - app.price1))
            app.bought = "Bought Pacific"
        else:
            app.bought = "Not Enough Gems"
    
    if(app.drawShop == True and event.x > 550 and event.x < 800 and event.y > 200 and event.y <450):
        if(app.gems > app.price2):
            app.background = 2
            app.water = app.water2
            writeFile('gems.txt', str(app.gems - app.price2))
            app.bought = "Bought Atlantic"
        else:
            app.bought = "Not Enough Gems"
    
    if(app.drawShop and event.x > 900 and event.x < 970 and event.y > 20 and event.y < 60):
        app.drawShop = False

    if(app.startGame == False and event.x > 250 and event.x < 350 and event.y > 450 and event.y < 500):
        app.drawInstr = True
    
    if(app.drawInstr and event.x > 900 and event.x < 970 and event.y > 20 and event.y < 60):
        app.drawInstr = False

def keyPressed(app, event):
    if(event.key == "r"):
        if(isPathLegal(app, 0, 0, 5)):
            app.overflow = 1
            app.gems += len(app.B)
            writeFile('gems.txt', str(app.gems))
            app.hintPathLegal = False
            app.giveHint = 0
            
        else:
            app.overflow = 2

    if(event.key == "h"):
        getHint(app)
        hintShapes(app)
        app.giveHint = 1
    
def getDirection(app, row, col):
    n = app.shapes[row][col]
    if(isinstance(n, Lshape)):
        shape = n.shape
        if(shape == 0):
            return (2,3)
        elif(shape == 1):
            return (3,4)
        elif(shape == 2):
            return(1,4)
        else:
            return (1,2)
    elif(isinstance(n, Ishape)):
        shape = n.shape
        if(shape == 0):
            return (2,4)
        else: 
            return (1,3)

def moveDirection(app,d,r1, c1):
        a = r1
        b = c1
        if(d==1):
            a -= 1
        elif(d==2):
            b += 1
        elif(d==3):
            a+= 1
        elif(d==4):
            b -= 1
        if(a<0 or a>app.rows-1 or b<0 or b> app.cols-1):
            return False
        return (a,b)

def isPathLegal(app, r1, c1, r2): 
    t = getDirection(app, r1, c1)
    app.usedindeces.append((r1,c1))
    if(t[0]==1):
        app.B.append(t)
    elif(t[1]==1):
        app.B.append((t[1],t[0]))
    else:
        return False
    d = app.B[0][1] 
    if(moveDirection(app, d, r1, c1)==False):
        return False
    else:
        (R1, C1) = moveDirection(app, d, r1, c1) 
    t2 = getDirection(app, R1, C1) 
    if(abs(t[1] - t2[0]) == 2):
        app.B.append(t2)
    elif(abs(t[1] - t2[1]) == 2):
        app.B.append((t2[1],t2[0]))
    else:
        return False
    (r1, c1) = (R1, C1) 
    index = 1
    app.usedindeces.append((R1, C1))
    while(True):
        d = app.B[index][1]
        if(moveDirection(app, d, r1, c1)==False):
            return False
        else:
            (R1, C1) = moveDirection(app, d, r1, c1)
        t_next = getDirection(app, R1, C1)
        if(t_next == None):
            return False
        if(abs(d-t_next[0])==2):
            app.B.append(t_next)
            app.usedindeces.append((R1,C1))
            (r1, c1) = (R1, C1)
        elif(abs(d-t_next[1])==2):
            app.B.append((t_next[1], t_next[0]))
            app.usedindeces.append((R1,C1))
            (r1, c1) = (R1, C1)
        else:
            return False
        n = app.shapes[r1][c1]
        if(r1 == r2 and ((isinstance(n, Lshape) and (n.shape == 0 or n.shape == 1)) or
                        (isinstance(n, Ishape) and (n.shape == 1)))):
            return True 
        index += 1
    
def drawShape(app, canvas, shape, row, col):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, row, col)
    gridWidth  = 1000 - 2*app.margin
    gridHeight = 700- 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    if(shape == 0):
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x1
        big_y1 = y1   
        small_x0 = x0 + (3/4)*cellWidth
        small_y0 = y0 + (3/4)*cellHeight
        small_x1 = x1
        small_y1 = y1
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="tan4")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="black")
        canvas.create_image(x1 - ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))
    elif(shape == 1):
        big_x0 = x0
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y1
        small_x0 = x0
        small_y0 = y0 + (3/4)*cellHeight
        small_x1 = x0 + (1/4)*cellWidth
        small_y1 = y1
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="tan4")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="black")
        canvas.create_image(x0 + ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))
    elif(shape == 2):
        big_x0 = x0
        big_y0 = y0
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y0 + (3/4)*cellHeight
        small_x0 = x0
        small_y0 = y0
        small_x1 = x0 + (1/4)*cellWidth
        small_y1 = y0 + (1/4)*cellHeight
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="tan4")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="black")
        canvas.create_image(x0 + ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))
    elif(shape == 3):
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0
        big_x1 = x1
        big_y1 = y0 + (3/4)*cellHeight
        small_x0 = x0 + (3/4)*cellWidth
        small_y0 = y0
        small_x1 = x1
        small_y1 = y0 + (1/4)*cellWidth
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="tan4")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="black")
        canvas.create_image(x1 - ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def drawShape2(app, canvas, shape, row, col):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, row, col)
    gridWidth  = 1000 - 2*app.margin
    gridHeight = 700 - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    if(shape == 0): #horizontal
        big_x0 = x0
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x1
        big_y1 = y0 + (3/4)*cellHeight
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill = "tan4")
    elif(shape == 1): #vertical
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y1
        canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
         image=ImageTk.PhotoImage(app.image2))
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill = "tan4")

def drawShapeHint(app, canvas, shape, row, col):
    (x0, y0, x1, y1, cx, cy) = getCellBoundsHint(app, row, col)
    gridWidth  = 800 - 2*app.margin
    gridHeight = 500 - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    if(shape == 0):
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x1
        big_y1 = y1
        small_x0 = x0 + (3/4)*cellWidth
        small_y0 = y0 + (3/4)*cellHeight
        small_x1 = x1
        small_y1 = y1
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="white")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="red")
    elif(shape == 1):
        big_x0 = x0
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y1
        small_x0 = x0
        small_y0 = y0 + (3/4)*cellHeight
        small_x1 = x0 + (1/4)*cellWidth
        small_y1 = y1
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="white")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="red")
    elif(shape == 2):
        big_x0 = x0
        big_y0 = y0
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y0 + (3/4)*cellHeight
        small_x0 = x0
        small_y0 = y0
        small_x1 = x0 + (1/4)*cellWidth
        small_y1 = y0 + (1/4)*cellHeight
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="white")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="red")
    elif(shape == 3):
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0
        big_x1 = x1
        big_y1 = y0 + (3/4)*cellHeight
        small_x0 = x0 + (3/4)*cellWidth
        small_y0 = y0
        small_x1 = x1
        small_y1 = y0 + (1/4)*cellWidth
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill="white")
        canvas.create_rectangle(small_x0, small_y0, small_x1, small_y1, fill="red")

def drawShape2Hint(app, canvas, shape, row, col):
    (x0, y0, x1, y1, cx, cy) = getCellBoundsHint(app, row, col)
    gridWidth  = 800 - 2*app.margin
    gridHeight = 510 - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    if(shape == 0): #horizontal
        big_x0 = x0
        big_y0 = y0 + (1/4)*cellHeight
        big_x1 = x1
        big_y1 = y0 + (3/4)*cellHeight
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill = "white")
    elif(shape == 1): #vertical
        big_x0 = x0 + (1/4)*cellWidth
        big_y0 = y0
        big_x1 = x0 + (3/4)*cellWidth
        big_y1 = y1
        canvas.create_rectangle(big_x0, big_y0, big_x1, big_y1, fill = "white")

def createEasyMapSolution(app):
    L = easyPathGenerator(app)
    shapes = [[-1 for x in range(app.cols)] for y in range(app.rows)] 
    for x in L:
        if(x[0] == "L"):
            shapes[x[2]][x[3]] = Lshape(x[1])
        elif(x[0] == "I"):
            shapes[x[2]][x[3]] = Ishape(x[1])
    return shapes

def createEasyMap(app):
    L = easyPathGenerator(app)
    app.possShapesSoln.append(L)
    if(L == None):
        return
    shapes = [[-1 for x in range(app.cols)] for y in range(app.rows)] 
    for b in L:
        if(b[0] == "L"):
            a = random.randrange(0,4,1)
            shapes[b[2]][b[3]] = Lshape(a)
        elif(b[0] == "I"):
            a = random.randrange(0,2,1)
            shapes[b[2]][b[3]] = Ishape(a)
    return shapes

def createMedMap(app):
    shapes = createEasyMap(app)
    noshapes = []
    for row in range(len(shapes)):
        for col in range(len(shapes[0])):
            if shapes[row][col] == -1:
                noshapes.append((row, col))
    newshapes = []
    r = random.randrange(1,len(noshapes)-3, 1)
    for i in range(r):
        length = len(noshapes)
        index = random.randrange(0,length,1)
        newshapes.append(noshapes.pop(index))
        
    for s in newshapes:
        shapetype = random.randrange(0,2,1)
        if(shapetype == 0): #shape L
            shapenum = random.randrange(0,4,1)
            if(shapenum == 0):
                shapes[s[0]][s[1]] = Lshape(0)
            elif(shapenum == 1):
                shapes[s[0]][s[1]] = Lshape(1)
            elif(shapenum == 2):
                shapes[s[0]][s[1]] = Lshape(2)
            else:
                shapes[s[0]][s[1]] = Lshape(3)
        elif(shapetype == 1):
            shapenum = random.randrange(0,2,1)
            if(shapenum == 0):
                shapes[s[0]][s[1]] = Ishape(0)
            else:
                shapes[s[0]][s[1]] = Ishape(1)
    return shapes

def createHardMap(app):
    shapes = createEasyMap(app)
    noshapes = []
    for row in range(len(shapes)):
        for col in range(len(shapes[0])):
            if (shapes[row][col] == -1):
                noshapes.append((row, col))
    newshapes = []
    r = len(noshapes)
    for i in range(r):
        length = len(noshapes)
        index = random.randrange(0,length,1)
        newshapes.append(noshapes.pop(index))
        
    for s in newshapes:
        shapetype = random.randrange(0,2,1)
        if(shapetype == 0): #shape L
            shapenum = random.randrange(0,4,1)
            if(shapenum == 0):
                shapes[s[0]][s[1]] = Lshape(0)
            elif(shapenum == 1):
                shapes[s[0]][s[1]] = Lshape(1)
            elif(shapenum == 2):
                shapes[s[0]][s[1]] = Lshape(2)
            else:
                shapes[s[0]][s[1]] = Lshape(3)
        elif(shapetype == 1):
            shapenum = random.randrange(0,2,1)
            if(shapenum == 0):
                shapes[s[0]][s[1]] = Ishape(0)
            else:
                shapes[s[0]][s[1]] = Ishape(1)
    return shapes

def getHint(app):
    soln = app.possShapesSoln[app.maplevel]
    app.hintPathLegal = isPathLegal(app, 0, 0, 5)
    length = len(app.B)
    hint = soln[0:length+1]
    app.hints = hint

def hintGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            bounds = getCellBoundsHint(app, row, col)
            app.hintGrid.append(bounds)

def hintShapes(app):
    for hint in app.hints:
        if(hint[0] == "L"):
            if(hint[1] == 0):
                app.hintShapes.append(Lshape(0))
            elif(hint[1] == 1):
                app.hintShapes.append(Lshape(1))
            elif(hint[1] == 2):
                app.hintShapes.append(Lshape(2))
            elif(hint[1] == 3):
                app.hintShapes.append(Lshape(3))
        elif(hint[0] == "I"):
            if(hint[1] == 0):
                app.hintShapes.append(Ishape(0))
            elif(hint[1] == 1):
                app.hintShapes.append(Ishape(1))
                           
def isTileHintLegal(app, curr, s):
    currDir = getDirection(app, curr[0], curr[1])

    newDir = getDirection2(app, s)
    if(abs(currDir[1] - newDir[0])==2):
        return True
    else:
        return False

def possTiles(app, r, c, usedtiles):
    poss = [(r-1, c),
            (r+1, c),
            (r, c-1),
            (r, c+1)]
    x = 0
    while(x<len(poss)):
        i = poss[x]
        if (i[0]<0 or i[0]>app.rows-1 or
            i[1]<0 or i[1]>app.cols-1 or
            i in usedtiles):
            poss.pop(x)
        else:
            x += 1
    possTiles = []
    
    for j in poss:
        shape = app.shapes[j[0]][j[1]]
        if(isinstance(shape, Lshape)):
            shapenum = shape.shape
            possTiles.append((j[0], j[1], Lshape(0)))
            possTiles.append((j[0], j[1], Lshape(1)))
            possTiles.append((j[0], j[1], Lshape(2)))
            possTiles.append((j[0], j[1], Lshape(3)))

        elif(isinstance(shape, Lshape)):
            shapenum = shape.shape
            possTiles.append((j[0], j[1], Ishape(0)))
            possTiles.append((j[0], j[1], Ishape(1)))
    return possTiles

def getDirection2(app, n):
    if(isinstance(n, Lshape)):
            shape = n.shape
            if(shape == 0):
                return (2,3)
            elif(shape == 1):
                return (3,4)
            elif(shape == 2):
                return(1,4)
            else:
                return (1,2)
    elif(isinstance(n, Ishape)):
        shape = n.shape
        if(shape == 0):
            return (2,4)
        else: 
            return (1,3)

def easyPathGenerator(app): 
    m = random.randrange(0,6,1)
    return easyPathGenHelper(app, (0,0), (5, m), 3, [("I", 1, 0, 0)], [(0,0)])

def easyPathGenHelper(app, curr, goal, opening, shapestiles, shapeindeces): 
    if(curr == goal and opening == 3):
        return shapestiles
    else:
        poss = possOptions(app, opening, curr[0], curr[1])
       
        for p in poss: 

            if(isTileLegal(app, (p[2], p[3]), shapeindeces)): 
                shapestiles.append((p[0], p[1], p[2], p[3]))
                shapeindeces.append((p[2], p[3]))
                newopening = p[4]
                newcurr = (p[2], p[3])
                solution = easyPathGenHelper(app, newcurr, goal, newopening, shapestiles, shapeindeces)
                if(solution != None):
                    return solution
                shapestiles.pop()
                shapeindeces.pop()
        return None

def possOptions(app, opening, r, c): 
    #if opening 1 => 3: shape L0 L1 I1
    #                    2  4  1  
    if (opening == 1):
        return {("L", 0, r-1, c, 2),
                ("L", 1, r-1, c, 4),
                ("I", 1, r-1, c, 1)}
    #if opening 2 ==> 4: shape L1 L2 I0
    elif(opening == 2):
        return {("L", 1, r, c+1, 3),
                ("L", 2, r, c+1, 1),
                ("I", 0, r, c+1, 2)}
    #if opening 3 => 1: shape L2 L3 I1
    elif(opening == 3):
        return {("L", 2, r+1, c, 4),
                ("L", 3, r+1, c, 2),
                ("I", 1, r+1, c, 3)}
    #if opening 4 => 2: shape L0 L3 I0
    else:
        return [("L", 0, r, c-1, 3),
                ("L", 3, r, c-1, 1),
                ("I", 0, r, c-1, 4)]

def isTileLegal(app, p, shapeindeces):
    if(p[0]<0 or p[0]>app.rows-1 or p[1]<0 or p[1]>app.cols-1 or
        p in shapeindeces):
        return False
    return True

def easyMaps(app):
    possShapes = []
    for i in range(10):
        shape = createEasyMap(app)
        possShapes.append(shape)
    return possShapes
    
def medMaps(app):
    possShapes = []
    for i in range(10):
        shape = createMedMap(app)
        possShapes.append(shape)
    return possShapes

def hardMaps(app):
    possShapes = []
    for i in range(10):
        shape = createHardMap(app)
        possShapes.append(shape)
    return possShapes

def timerFired(app):
    
    #waterShapeL0_23
    if(app.L023x <= 3/4):
        app.L023x += 1/30
    elif(app.L023x > 3/4):
        if(app.L023y <= 1):
            app.L023y += 1/30

    #waterShapeL0_32
    if(app.L032y <= 3/4):
        app.L032y += 1/30
    elif(app.L032y >= 3/4):
        if(app.L032x <= 1):
            app.L032x += 1/30

    #waterShapeL1_34
    if(app.L134y <= 3/4):
        app.L134y += 1/30
    elif(app.L134y > 3/4):
        if(app.L134x <= 1):
            app.L134x += 1/30

    #waterShapeL1_43
    if(app.L143x <= 3/4):
        app.L143x += 1/30
    elif(app.L143x >3/4):
        if(app.L143y < 1):
            app.L143y += 1/30
    
    #waterShapeL2_14
    if(app.L214y <= 3/4):
        app.L214y += 1/30
    elif(app.L214y > 3/4):
        if(app.L214x < 1):
            app.L214x += 1/30

    #waterShapeL2_41
    if(app.L241x <= 3/4):
        app.L241x += 1/30
    elif(app.L241x > 3/4):
        if(app.L241y < 1):
            app.L241y += 1/30

    #waterShapeL3_12
    if(app.L312y <= 3/4):
        app.L312y += 1/30
    elif(app.L312y > 3/4):
        if(app.L312x < 1):
            app.L312x += 1/30

    #waterShapeL3_21
    if(app.L321x <= 3/4):
        app.L321x += 1/30
    elif(app.L321x > 3/4):
        if(app.L321y < 1):
            app.L321y += 1/30

    #waterShapeI1_13 and waterShapeI1_31
    if(app.I1y <=1):
        app.I1y += 1/30

    #waterShapeI0_24 and waterShapeI0_42
    if(app.I0x <= 1):
        app.I0x += 1/30
    
    if(app.waternum < len(app.B)-1):
        app.waternumhelper += 1
    if(app.waternumhelper == 5):
        app.waternum += 1
        app.waternumhelper = 0

#DRAW WATER FUNCTIONS:
def waterShapeL0_23(app, canvas, r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 0):

        canvas.create_polygon(x1, y0 + (1/4 * cellHeight),
                            x1 - (app.L023x * cellWidth), y0 + (1/4 * cellHeight),
                            x1 - (app.L023x * cellWidth), y0 + (app.L023y * cellHeight),
                            x1, y1, fill = "blue4")

        canvas.create_image(x1 - ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL0_32(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 0):

        canvas.create_polygon(x1, y1,
                            x0 + (app.L032x * cellWidth), y1 - (app.L032y * cellHeight),
                            x0 + (1/4 * cellWidth), y1 - (app.L032y * cellHeight),
                            x0 + (1/4 * cellWidth), y1, fill = "blue4")

        canvas.create_image(x1 - ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL1_34(app, canvas, r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 1):

        canvas.create_polygon(x0, y1,
                            x1 - (app.L134x * cellWidth), y1 - (app.L134y * cellHeight),
                            x0 + (3/4*cellWidth), y1 - (app.L134y * cellHeight),
                            x0 + (3/4 * cellWidth), y1, fill = "blue4")

        canvas.create_image(x0 + ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL1_43(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app,r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 1):

        canvas.create_polygon(x0, y0 + (1/4 * cellHeight),
                            x0 + (app.L143x * cellWidth), y0 + (1/4 * cellHeight),
                            x0 + (app.L143x * cellWidth), y0 + (app.L143y * cellHeight),
                            x0, y1, fill = "blue4")
        
        canvas.create_image(x0 + ((1/8) * cellWidth), y1 - ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL2_14(app, canvas, r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 2):

        canvas.create_polygon(x0, y0,
                            x1 - (app.L214x * cellWidth), y0 + (app.L214y * cellHeight),
                            x0 + (3/4 * cellWidth), y0 + (app.L214y * cellHeight),
                            x0 + (3/4 * cellWidth), y0, fill = "blue4")

        canvas.create_image(x0 + ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL2_41(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 2):

        canvas.create_polygon(x0, y0,
                            x0 + (app.L241x * cellWidth), y1 - (app.L241y * cellHeight),
                            x0 + (app.L241x * cellWidth), y1 - (1/4 * cellHeight),
                            x0, y0 + (3/4 * cellHeight), fill = "blue4")

        canvas.create_image(x0 + ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL3_12(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 3):

        canvas.create_polygon(x1, y0,
                            x0 + (app.L312x * cellWidth), y0 + (app.L312y * cellHeight),
                            x0 + (1/4 * cellWidth), y0 + (app.L312y * cellHeight),
                            x0 + (1/4 * cellWidth), y0, fill = "blue4")

        canvas.create_image(x1 - ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeL3_21(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Lshape))and n.shape == 3):

        canvas.create_polygon(x1, y0,
                            x1 - (app.L321x * cellWidth), y1 - (app.L321y * cellHeight),
                            x1 - (app.L321x * cellWidth), y1 - (1/4 * cellHeight),
                            x1, y0 + (3/4 * cellHeight), fill = "blue4")

        canvas.create_image(x1 - ((1/8) * cellWidth), y0 + ((1/8) * cellHeight),
         image=ImageTk.PhotoImage(app.image4))

def waterShapeI0_24(app, canvas, r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app,r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Ishape))and n.shape == 0):

        canvas.create_rectangle(x0, y0 + (1/4 * cellHeight),
                                x0 + (app.I0x * cellWidth), y0 + (3/4 * cellHeight),
                                fill = "blue4")

def waterShapeI0_42(app, canvas, r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app,r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Ishape))and n.shape == 0):

        canvas.create_rectangle(x0 + (app.I0x * cellWidth), y0 + (1/4 * cellHeight),
                                x0, y0 + (3/4 * cellHeight),
                                fill = "blue4")

def waterShapeI1_13(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]

    if((isinstance(n, Ishape))and n.shape == 1):

        canvas.create_rectangle(x0 + (1/4 * cellWidth), y0,
                                x0 + (3/4 * cellWidth), y0 + (app.I1y * cellHeight),
                                fill = "blue4")

def waterShapeI1_31(app, canvas,r, c):
    (x0, y0, x1, y1, cx, cy) = getCellBounds(app, r, c)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    n = app.shapes[r][c]
    if((isinstance(n, Ishape))and n.shape == 1):
        canvas.create_rectangle(x0 + (1/4 * cellWidth), y1 - (app.I1y * cellHeight),
                                x0 + (3/4 * cellWidth), y1,
                                fill = "blue4")

def runWater(app, c):
    runwater = []
    index = 0
    for t in range(len(app.B)):
        i = app.B[t]
        coord = app.usedindeces[index]
        if(i == (2,3)):
            runwater.append(("a", coord[0], coord[1]))
        elif(i == (3,2)):
            runwater.append(("b", coord[0], coord[1]))
        elif(i == (3,4)):
            runwater.append(("c", coord[0], coord[1]))
        elif(i == (4,3)):
            runwater.append(("d", coord[0], coord[1]))
        elif(i == (1,4)):
            runwater.append(("e", coord[0], coord[1]))
        elif(i == (4,1)):
            runwater.append(("f", coord[0], coord[1]))
        elif(i == (1,2)):
            runwater.append(("g", coord[0], coord[1]))
        elif(i == (2,1)):
            runwater.append(("h", coord[0], coord[1]))
        elif(i == (2,4)):
            runwater.append(("i", coord[0], coord[1]))
        elif(i == (4,2)):
            runwater.append(("j", coord[0], coord[1]))
        elif(i == (1,3)):
            runwater.append(("k", coord[0], coord[1]))
        else:
            runwater.append(("l", coord[0], coord[1]))
        index += 1
    return runwater
    
def drawRunWater(app, canvas):
    runwater = runWater(app, canvas)
    for z in runwater:
        if(z[0] == "a"):
            app.a = waterShapeL0_23(app, canvas, z[1], z[2])
        elif(z[0] == "b"):
            app.a = waterShapeL0_32(app, canvas, z[1], z[2])
        elif(z[0] == "c"):
            app.a = waterShapeL1_34(app, canvas, z[1], z[2])
        elif(z[0] == "d"):
            app.a = waterShapeL1_43(app, canvas, z[1], z[2])
        elif(z[0] == "e"):
            app.a = waterShapeL2_14(app, canvas, z[1], z[2])
        elif(z[0] == "f"):
            app.a = waterShapeL2_41(app, canvas, z[1], z[2])
        elif(z[0] == "g"):
            app.a = waterShapeL3_12(app, canvas, z[1], z[2])
        elif(z[0] == "h"):
            app.a = waterShapeL3_21(app, canvas, z[1], z[2])
        elif(z[0] == "i"):
            app.a = waterShapeI0_24(app, canvas, z[1], z[2])
        elif(z[0] == "j"): 
            app.a = waterShapeI0_42(app, canvas, z[1], z[2])
        elif(z[0] == "k"): 
            app.a = waterShapeI1_13(app, canvas, z[1], z[2])
        else:
            app.a = waterShapeI1_31(app, canvas, z[1], z[2])

def drawStart(app, canvas):
    canvas.create_rectangle(0,0,1000,700, fill = "brown")
    canvas.create_text(400, 100, fill = "black", font = "Arial 77" ,text = "OVERFLOW")
    canvas.create_text(400, 150, fill = "white", font = "Arial 20", text = "Select a Level")
    canvas.create_text(400, 175, fill = "white", font = "Arial 20", text = f"Level: {app.level}")
    
    canvas.create_rectangle(100, 200, 250, 280, fill = "green")
    canvas.create_text(150, 225, fill = "black", font = "Arial 20", text = "EASY", anchor = "nw")
    canvas.create_rectangle(325, 200, 475, 280, fill = "yellow")
    canvas.create_text(365, 225, fill = "black",font = "Arial 20", text = "MEDIUM", anchor = "nw")
    canvas.create_rectangle(550, 200, 700, 280, fill = "red")
    canvas.create_text(600, 225, fill = "black",font = "Arial 20", text = "HARD", anchor = "nw")

    canvas.create_rectangle(250,300,550,400, fill = "blue")
    canvas.create_text(350, 330, fill = "white", font = "Arial 30", text = "START", anchor = "nw")

    canvas.create_rectangle(250, 450, 350, 500, fill = "purple")
    canvas.create_text(300, 475, fill = "white", font = "Arial 15", text = "Instructions", anchor = "center")

    canvas.create_rectangle(450, 450, 550, 500, fill = "purple")
    canvas.create_text(500, 475, fill = "white", font = "Arial 15", text = "Backgrounds", anchor = "center")

def drawGrid(app, canvas):
    for grid in app.grid:
        canvas.create_rectangle(grid[0], grid[1], grid[2], grid[3], fill="black")
        cx = grid[4]
        cy = grid[5]
    
    canvas.create_image(35, 340, image=ImageTk.PhotoImage(app.sidesand))
    canvas.create_image(965, 340, image=ImageTk.PhotoImage(app.sidesand))

def drawWaterShop(app, canvas):
    canvas.create_rectangle(0, 0, 1000, 700, fill = "blue4")

    canvas.create_text(500, 100, fill = "white", font = "Arial 40 bold", text = "Background Shop")

    #water 1
    canvas.create_rectangle(200, 200, 450, 450, fill = "black")
    canvas.create_image(325, 325, image=ImageTk.PhotoImage(app.water1display))
    canvas.create_text(325, 500, fill = "white", font = "Arial 30 bold", text = "Pacific")
    canvas.create_text(325, 530, fill = "white", font = "Arial 20", text = "Price: 15 Gems")

    #water 2
    canvas.create_rectangle(550, 200, 800, 450, fill = "black")
    canvas.create_image(675, 325, image=ImageTk.PhotoImage(app.water2display))
    canvas.create_text(675, 500, fill = "white", font = "Arial 30 bold", text = "Atlantic")
    canvas.create_text(675, 530, fill = "white", font = "Arial 20", text = "Price: 30 Gems")
    
    canvas.create_rectangle(900, 20, 970, 60, fill = "black")
    canvas.create_text(935, 40, fill = "white", font = "Arial 15", text = "Home")

    canvas.create_text(500, 600, fill = "White", font = "Arial 20", text = f"{app.bought}")

def drawInstructions(app, canvas):
    canvas.create_rectangle(0, 0, 1000, 700, fill = "purple")
    canvas.create_text(500, 80, fill = "black", font = "Arial 40 bold", text = "Instructions")

    canvas.create_rectangle(900, 20, 970, 60, fill = "black")
    canvas.create_text(935, 40, fill = "white", font = "Arial 15", text = "Home")

    canvas.create_text(500, 150, fill = "white", font = "Arial 20", 
    text = "There are three difficulty levels: Easy, Medium, and Hard.")
    canvas.create_text(500, 190, fill = "white", font = "Arial 20", 
    text = "Select one of these levels before clicking \"Start\".")
    canvas.create_text(500, 230, fill = "white", font = "Arial 20", 
    text = "Each difficulty level contains 10 sublevels.")
    canvas.create_text(500, 270, fill = "white", font = "Arial 20", 
    text = "From the starting tile, make a path to any of the tiles in the last row.")
    canvas.create_text(500, 310, fill = "white", font = "Arial 20", 
    text = "To make a path, rotate the tiles 90 degrees clockwise by clicking on it.")
    canvas.create_text(500, 350, fill = "white", font = "Arial 20", 
    text = "Once you have finished making the path, click the \"r\" key to run the water.")
    canvas.create_text(500, 390, fill = "white", font = "Arial 20", 
    text = "If the water runs through, you earn a gem for every tile used in the path.")
    canvas.create_text(500, 430, fill = "white", font = "Arial 20", 
    text = "You can use these gems to buy other backgrounds in the \"Background Shop\" from the Home page.")
    canvas.create_text(500, 470, fill = "white", font = "Arial 20", 
    text = "If the path is not continuous, the screen will display \"Overflow\".")
    canvas.create_text(500, 510, fill = "white", font = "Arial 20", 
    text = "At any point in the game, you can click to go to the next level.")
    canvas.create_text(500, 550, fill = "white", font = "Arial 20", 
    text = "You can also redo the level if you have won the level or overflowed.")
    canvas.create_text(500, 590, fill = "white", font = "Arial 20", 
    text = "To get a hint, press \"h\".")

    #default background is water0
def drawGridWater0(app, canvas):
    canvas.create_image(500, 35, image=ImageTk.PhotoImage(app.water0))
    canvas.create_image(500, 665, image=ImageTk.PhotoImage(app.water0))

def drawGridWater1(app, canvas):
    canvas.create_image(500, 35, image=ImageTk.PhotoImage(app.water1))
    canvas.create_image(500, 665, image=ImageTk.PhotoImage(app.water1))

def drawGridWater2(app, canvas):
    canvas.create_image(500, 35, image=ImageTk.PhotoImage(app.water2))
    canvas.create_image(500, 665, image=ImageTk.PhotoImage(app.water2))

def drawGridLabels(app, canvas):
    canvas.create_text(10, 10, fill = "orange", font = "Arial 20", text = f"Level Type: {app.level}", anchor = "nw")
    canvas.create_text(300,10, fill = "orange", font = "Arial 20", text = f"Level Number: {app.maplevel + 1}", anchor = "nw")
    canvas.create_text(600,10, fill = "orange", font = "Arial 20", text = f"Gems: {app.gems}", anchor = "nw")

    canvas.create_rectangle(900, 10, 990, 40, fill = "red")
    canvas.create_text(910,15, fill = "yellow", font = "Arial 15", text = "Next Level", anchor = "nw")

    canvas.create_rectangle(800, 10, 880, 40, fill = "red")
    canvas.create_text(815, 15, fill = "yellow", font = "Arial 15", text = "Home", anchor = "nw")

def drawRedo(app, canvas):
    #if it is a win, then create two buttons: redo and next level.
    canvas.create_rectangle(450, 430, 550, 470, fill = "red")
    canvas.create_text(500, 450, fill = "yellow", font = "Arial 20", text = "Redo", anchor = "center")
    canvas.create_rectangle(440, 500, 560, 540, fill = "red")
    canvas.create_text(500, 520, fill = "yellow", font = "Arial 20", text = "Next Level", anchor = "center")
    
def drawHint(app, canvas):

    canvas.create_rectangle(140, 140, 860, 560, fill = "black")
    canvas.create_text(500, 160, fill = "yellow", font = "Arial 20", text = "Hint: ", anchor = "center")
    canvas.create_rectangle(835, 150, 855, 170, fill = "yellow")
    canvas.create_text(845, 157, fill = "black", font = "Arial 20", text = "x", anchor = "center")

    for grid in app.hintGrid:
        canvas.create_rectangle(grid[0], grid[1], grid[2], grid[3], fill="red")
        cx = grid[4]
        cy = grid[5]
    
    i = 0
    for hint in app.hintShapes:
       
        coord = app.hints[i]
        if(isinstance(hint, Lshape)):
            drawShapeHint(app, canvas, hint.shape, coord[2], coord[3])
        if(isinstance(hint, Ishape)):
            drawShape2Hint(app, canvas, hint.shape, coord[2], coord[3])
        i += 1

def drawEnd(app, canvas):
    canvas.create_rectangle(0,0,1000,700, fill = "brown")
    canvas.create_text(500, 250, fill = "black", font = "Arial 50", text = f"Passed the {app.level} Level!")
    canvas.create_text(500, 450, fill = "black", font = "Arial 30", text = f"Total Gems Earned: {app.gems}")
    canvas.create_rectangle(450, 500, 550, 550, fill = "white")
    canvas.create_text(500, 525, fill = "black", font = "Arial 15", text = "Return Home")

def redrawAll(app, canvas):
    drawStart(app, canvas)
    if(app.startGame == True):
        drawGrid(app, canvas)
        if app.background == 0:
            drawGridWater0(app, canvas)
        elif app.background == 1:
            drawGridWater1(app, canvas)
        elif app.background == 2:
            drawGridWater2(app, canvas)
        canvas.create_rectangle(75, 35, 160, 65, fill = "white")
        canvas.create_text(117.5, 50, fill = "black", font = "Arial 15", text = "start here")
        for row in range(app.rows):
            for col in range(app.cols):
                n = app.shapes[row][col]
                (x0, y0, x1, y1, cx, cy) = getCellBounds(app,row, col)
                gridWidth  = app.width - 2*app.margin
                gridHeight = app.height - 2*app.margin
                cellWidth = gridWidth / app.cols
                cellHeight = gridHeight / app.rows
                canvas.create_image(x1 - (0.5 * cellWidth), y1 - (0.5 * cellHeight),
                image=ImageTk.PhotoImage(app.image2))
                if(isinstance(n, Lshape)):
                    drawShape(app, canvas, n.shape, row, col)
                if(isinstance(n, Ishape)):
                    drawShape2(app, canvas, n.shape, row, col)
        drawGridLabels(app, canvas)
    if(app.giveHint == 1 and app.hintPathLegal == False):
        drawHint(app, canvas)
    if(app.hintPathLegal):
        canvas.create_text(500, 340, fill = "black", font = "Arial 40", text = "Path Is Correct!")
    if(app.maplevel >= 9 and app.drawEnd == True):
        drawEnd(app, canvas)
    if(app.drawShop):
        drawWaterShop(app, canvas)
    if(app.drawInstr):
        drawInstructions(app, canvas)        
    if(app.overflow == 1):
        drawRunWater(app, canvas)
        canvas.create_text(500, 350, fill = "yellow", font = "Arial 77", text = "WIN")
        canvas.create_text(600,10, fill = "orange", font = "Arial 20", text = f"Gems: {app.gems}", anchor = "nw")
        drawRedo(app, canvas)
    elif(app.overflow == 2):
        canvas.create_text(500, 350, fill = "yellow", font = "Arial 77", text = "OVERFLOW")
        drawRedo(app, canvas)

runApp(width=1000, height=700)

