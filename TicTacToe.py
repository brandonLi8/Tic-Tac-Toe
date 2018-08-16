from tkinter import * 
import math, random, time, copy

def init(data):
  #set up dimensions
  data.rows,data.cols,data.width,data.height,data.margin = 3,3 ,520,600,20# tix tac toe board is 3x3,set up width of animation and the margin between the board and the edge
  data.box = [20,50,data.width - 20, data. width+30] #this is to make sure you click in bounds
  data.delayToDrawO = 0 #this is to count when the o is drawn
  data.oCenters,data.xCenters  = [],[] # this will be the list of tuples of all the Centers by (row,col
  data.everyBox = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)] # this is everysingle box! (row,col)
  data.drawO = False# permission to draw the 'o' only after a delay
  data.runs = 0 # this is to count how many runs
  data.xWinnner,data.oWinner,data.helpMode,data.isTie = False, False,False,False# will turn True when xWins or oWinsor win help mode is activated
  data.xWins,data.oWins = 0,0 #the number of wins each has
  data.xWinsCount,data.oWinsCount,data.tieCount = False,False, False # this count is needed to make delay the Win or Lose Screen
  data.readyToAddX ,data.readyToAddO = False,False #this is to make sure it only adds one when someone wins
  data.availableToClick = True #this is to make sure there is no spam click
  data.clicked = False

def inarow(data,lis): #this function takes in a list of the centers in tuples of row,col
# it will return True if there is 3 in a row by checking if there are 3 of the same rows, 
#or.if there are 3 of the same cols, or the diagonals
  listOfRows = []
  listOfCols = []
  if len(lis) == 0: # will be faster if you check this first
    return False
  for i in range(len(lis)):
    listOfRows.append(lis[i][0]) #add all of the first item of the tuple, or rows to list of rows
    listOfCols.append(lis[i][1])#add all of the second item of the tuple, or cols to list of rows
  for i in range(len(listOfRows)):
    if listOfRows.count(listOfRows[i]) == 3: #checks if there are 3 of the same rows
      return True
  for i in range(len(listOfCols)):
    if listOfCols.count(listOfCols[i]) == 3:#check if there are 3 of the same cols
      return True
  if ((0,0)in lis) and ((1,1)in lis) and ((2,2)in lis): #check diagnol
        return True
  if ((0,2)in lis) and ((1,1)in lis) and ((2,0)in lis):#check diagnol
      return True
    #we have checked everything, now we can say there isn't 3 in a row
  return False

def mousePressed(event, data): #this moused pressed adds the box that you clicked to xCenters and 
#allows the cpu to go
  x0, y0, x1, y1 = data.box
  data.delayToDrawO = 0 #we need to delay the cpu drawing the 'o'  with this count in Timer Fired

  if (event.x > x0 and event.y > y0 and event.x < x1 and event.y < y1) and data.availableToClick and not(inarow(data,data.oCenters)): #cant click if someone has won
    #if your click was inside the box, you want tell urself that you 
    #want to draw your circle, we add the xCenter to data.xCenters
    if getBox(event.x,event.y,data) in data.everyBox :# if the row/col is still available, clicked is true and remove row/col
      data.clicked = True
      data.everyBox.remove(getBox(event.x,event.y,data))
      data.xCenters.append(tuple(getBox(event.x,event.y,data)))#add it to the x centers
      data.runs += 1 #a run has just happened
      #if you just clicked then you can't spam click until the 'o' has been drawn
      data.availableToClick = False
     
def getBox(x, y, data):# return (row, col) in which (x, y) occurred 
  gridWidth  = data.width - 2*data.margin
  gridHeight = data.height - 2*data.margin
  boxWidth  = gridWidth / data.cols
  boxHeight = gridHeight / data.rows
  row = (y - data.margin) // boxHeight
  col = (x - data.margin) // boxWidth
  return (row, col)

def keyPressed(event, data):#restart and helpmode
  if ( event.keysym == "r" ): #restart    
    copyXWins = data.xWins
    copyOWins = data.oWins#we want to keep the scores
    init(data)
    data.xWins = copyXWins
    data.oWins = copyOWins
  if ( event.keysym == "h" ): #helpmode   
    data.helpMode = not(data.helpMode)

#the logic behind timer Fired is hard
#this function is the delay behind everything
def timerFired(data): #this function could be done better
  if (data.clicked): #you only want to count after you've clicked
      data.delayToDrawO += 1
  if (data.delayToDrawO == 10): 
      data.drawO = True
  if (inarow(data,data.xCenters)): #you only want to count after win
    data.xWinsCount += 1
  if (data.xWinsCount == 10): 
    data.xWinnner = True 
    data.readyToAddX = True
  if inarow(data,data.oCenters) :
    data.oWinsCount += 1
  if (data.oWinsCount == 10): 
    data.oWinner= True 
    data.readyToAddO = True
  if (data.runs == 9) and (inarow(data,data.xCenters) == False):
    data.tieCount += 1
  if (data.tieCount == 10):
    data.isTie = True
 
def getBoxBounds(row, col, data): # returns (x0, y0, x1, y1) corners/bounding box of given box in grid
  gridWidth  = data.width - 2*data.margin 
  gridHeight = data.height - 2*data.margin 
  columnWidth = gridWidth / data.cols
  rowHeight = gridHeight / data.rows
  x0 = data.margin + col * columnWidth
  x1 = data.margin + (col+1) * columnWidth
  y0 = data.margin + row * rowHeight + 15
  y1 = data.margin + (row+1) * rowHeight + 15
  return (x0, y0, x1, y1)
    
def helpMode(canvas,data): #lol extremely painful
  canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60")    
  canvas.create_text(data.width/2 +4.5 ,data.height/8-20,text = "Help Mode!", font=('Comic Sans MS', '70', 'bold italic'),fill = "black")
  canvas.create_text(data.width/2 ,data.height/8-20,text = "Help Mode!", font=('Comic Sans MS', '70', 'bold italic'),fill = "purple")
  canvas.create_text(data.width/2 ,data.height/2+30,text = "Get 3 in a row \n \nto win! Your score will be on the top \n\nright of the board. When entering \n\nhelp mode the progress will be saved. \n\nWhen restarting your score\n\n will be saved. Good Luck!", font=('Comic Sans MS', '20', 'bold italic'),fill = "black")
  canvas.create_rectangle(60+270, data.height/2+100-200-60, 110+270, data.height/2+150-200-60,fill="grey80",outline="grey6",width = 2)
  canvas.create_text(75+270,data.height/2+115-200-60,text = "h",font = ('Comic Sans MS', '13', 'bold italic'))
  canvas.create_line(85+270,data.height/2+125-200-60,85+270,data.height/2+125-200+45-60)
  canvas.create_text(95+270,data.height/2+110-200+60-60,text = "help/ \n exit help",font = ('Comic Sans MS', '13', 'bold italic'))
  canvas.create_rectangle(260, data.height/2+100-200-60, 310,  data.height/2+150-200-60,fill="grey80",outline="grey6",width = 2)
  canvas.create_text(270,data.height/2+115-200-60,text = "r",font = ('Comic Sans MS', '13', 'bold italic'))
  canvas.create_line(265,data.height/2+125-200-60,246,data.height/2+125-200+45-60)
  canvas.create_text(240,data.height/2+110-200+60-60,text = "restart",font = ('Comic Sans MS', '13', 'bold italic'))

def drawGrid(canvas,data):
  canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60") 
  for row in range(data.rows):
    for col in range(data.cols):
      (x0, y0, x1, y1) = getBoxBounds(row, col, data)
      canvas.create_rectangle(x0, y0, x1, y1,fill='grey90',width = 7)

def convertRowColToCoordinates(data,row1,col1): #this is hardcoded
  if col1 == 0 :
    x2 = data.margin + (data.width-2*data.margin)/6
  if col1 == 1 : 
    x2 = (data.width-2*data.margin)/2 + data.margin
  if col1 == 2 :
    x2 = (data.width - 2*data.margin) - ((data.width - 2*data.margin) / 6) + data.margin
  if row1 == 0 :
    y2 = data.margin + (data.width-2*data.margin)/6 +25
  if row1 == 1 : 
    y2 = (data.width-2*data.margin)/2 + data.margin + 50
  if row1 == 2 :
    y2 = (data.width - 2*data.margin) - ((data.width - 2*data.margin) / 6) + data.margin + 80
  return (x2,y2)

def drawAllX(canvas,data):
  for i in range(len(data.xCenters)):
    if data.xCenters != []:
      size = 100
      hypo = (size)/2 #trig!!! 
      (row1,col1) = data.xCenters[i]
      (x2,y2) = convertRowColToCoordinates(data,row1,col1)
      canvas.create_line(x2-(hypo/math.sqrt(2)),y2 -(hypo/math.sqrt(2)),x2+(hypo/math.sqrt(2)),y2 +(hypo/math.sqrt(2)),width=5,fill = "blue")
      canvas.create_line(x2-(hypo/math.sqrt(2)),y2 +(hypo/math.sqrt(2)),x2+(hypo/math.sqrt(2)),y2 -(hypo/math.sqrt(2)),width=5,fill = "blue")

def drawAllO(canvas,data):
  for i in range(len(data.oCenters)):
    if (data.oCenters != []) :
      (row2,col2) = data.oCenters[i]
      (x,y) = convertRowColToCoordinates(data,row2,col2)
      r = 60 #radius
      canvas.create_oval(x-r, y-r, x+r, y+r,fill = 'grey90',width = 5,outline = "red"  )

def drawText(canvas,data): # this is all the text
  canvas.create_text(data.width/2,12,text="Brandon's Tic Tac Toe", font=('Comic Sans MS', '20', 'bold italic'))
  canvas.create_text(data.width/2,25, text="Press 'r' to restart", font=('Comic Sans MS', '10', 'bold italic'))
  canvas.create_text(data.width/4 - 60,12,text="X:   " + str(data.xWins), font=('Comic Sans MS', '20', 'bold italic'),fill = "blue")
  canvas.create_text(3*data.width/4 + 60,12,text="O:   " + str(data.oWins), font=('Comic Sans MS', '20', 'bold italic'),fill = "red")
  if data.xWinnner:
    canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60")
    canvas.create_text(data.width/2+3, data.height/2-80,text="YOU WIN!!!", font=('Comic Sans MS', '60', 'bold italic'),fill = "black")
    canvas.create_text(data.width/2, data.height/2,text="GAME OVER", font=('Comic Sans MS', '60', 'bold italic'),)
    canvas.create_text(data.width/2, data.height/2 + 80,text="press 'r' to restart", font=('Comic Sans MS', '20', 'bold italic'))
    canvas.create_text(data.width/4 - 60,data.height/2 + 120, text="X:  " + str(data.xWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "blue")
    canvas.create_text(3*data.width/4 + 60,data.height/2 + 120, text="O:  " + str(data.oWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "red" )
  if data.oWinner:
    canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60")
    canvas.create_text(data.width/2+3, data.height/2-80,text="You Lose", font=('Comic Sans MS', '60', 'bold italic'),fill = "black")
    canvas.create_text(data.width/2, data.height/2,text="GAME OVER", font=('Comic Sans MS', '60', 'bold italic'),)
    canvas.create_text(data.width/2, data.height/2 + 80,text="press 'r' to restart", font=('Comic Sans MS', '20', 'bold italic'))
    canvas.create_text(data.width/4 - 60,data.height/2 + 120, text="X:  " + str(data.xWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "blue")
    canvas.create_text(3*data.width/4 + 60,data.height/2 + 120, text="O:  " + str(data.oWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "red" )
    
  if data.isTie :
    canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60")
    canvas.create_text(data.width/2+3, data.height/2-80,text="Tie!", font=('Comic Sans MS', '60', 'bold italic'),fill = "black")
    canvas.create_text(data.width/2, data.height/2,text="GAME OVER", font=('Comic Sans MS', '60', 'bold italic'),)
    canvas.create_text(data.width/2, data.height/2 + 80,text="press 'r' to restart", font=('Comic Sans MS', '20', 'bold italic'))
    canvas.create_text(data.width/4 - 60,data.height/2 + 120, text="X:  " + str(data.xWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "blue")
    canvas.create_text(3*data.width/4 + 60,data.height/2 + 120, text="O:  " + str(data.oWins), font=('Comic Sans MS', '40', 'bold italic'),fill = "red" )

def addScore(data):#add the score whens someone wins, this was challenging to only add
#only once
  if data.readyToAddX:
    data.xWins+= 1
    data.readyToAddX = False
  if data.readyToAddO:
    data.oWins+= 1
    data.readyToAddO = False 
def addCurrentOtoCenter(current,data): 
  data.oCenters.append(current)
  data.runs +=1
  data.everyBox.remove(current)
  data.clicked = False 
  data.drawO = False
  data.delayToDrawO = 0
  data.availableToClick = True
def checkWin(data):
  current = -1
  everyBox =[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]#modifying while looping, 
  #i just decided to loop through every box even if filled
  #even though it is slightly slower
  for i in range(0,len(everyBox)):#how thid works:I make a copy of the oCenters
  # just in case, then I add the current, and check if that will win the game. if not
  # check the next one,if at one works, it will return True, otherwise False
    o = copy.deepcopy(data.oCenters)#just in case
    current = everyBox[i]
    o.append(current)         
    if (inarow(data,o)) and (current in data.everyBox)  and (o.count(current) != 0):#double check
      addCurrentOtoCenter(current,data)
      return True
  return False
def checkBlock(data):#same thing as check win but this time we see if we can block
  current = -1
  everyBox =[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]#modifying while looping, 
  #i just decided to loop through every box even if filled
  #even though it is slightly slower
  for i in range(0,len(everyBox)):#how thid works:I make a copy of the oCenters
  # just in case, then I add the current, and check if that will win the game. if not
  # check the next one,if at one works, it will return True, otherwise False
    x = copy.deepcopy(data.xCenters)#just in case

    current = everyBox[i]
    x.append(current)       
    if (inarow(data,x) == True) and (current in data.everyBox) and (x.count(current) != 2):
      addCurrentOtoCenter(current,data)
      return True
  return False
def AI(data):#this function makes the decision behnd where to draw to O
#it prioritizes winning the game first, so if you can win, it will. Otherwize, it will check
#to prevent the player from winning, by seeing if it can block a 3 in a row. If there are no chances for
#these two, if will pick a random one
  current = 0
  if (data.clicked and data.drawO):#if we've clicked and we have permission to draw the 'o' then we will add an o to the list
    if (data.everyBox != [])and not(data.xWinnner):#don't add anything if x has already won or if there is nothing left
      if checkWin(data):
        return True #make sure the function ends
      if checkBlock(data):
        return True
      else:#nothing available , pick random
        while current not in data.everyBox:#double check available
          current = random.choice(data.everyBox)
        addCurrentOtoCenter(current,data)

def redrawAll(canvas, data):  
    drawGrid(canvas,data)#always draw the box and the 3x3 grid
    drawAllX(canvas,data)#draw all the x's in xCenters
    drawAllO(canvas,data)#draw all the o's in xCenters
    addScore(data)
    AI(data)
    drawText(canvas,data)
    if data.helpMode: helpMode(canvas,data)

def run(width=300, height=300):
  def redrawAllWrapper(canvas, data):
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, data.width, data.height,fill='white', width=0)
    redrawAll(canvas, data)
    canvas.update()    
  def mousePressedWrapper(event, canvas, data):
    mousePressed(event, data)
    redrawAllWrapper(canvas, data)
  def keyPressedWrapper(event, canvas, data):
    keyPressed(event, data)
    redrawAllWrapper(canvas, data)
  def timerFiredWrapper(canvas, data):
    timerFired(data)
    redrawAllWrapper(canvas, data)# pause, then call timerFired again
    canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
   # Set up data and call init
  class Struct(object): pass
  data = Struct()
  data.width = width
  data.height = height
  data.timerDelay = 100 # milliseconds
  root = Tk()
  init(data)
  # create the root and the canvas
  canvas = Canvas(root, width=data.width, height=data.height)
  canvas.pack()
  # set up events
  root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, data))
  root.bind("<Key>", lambda event:keyPressedWrapper(event, canvas, data))
  timerFiredWrapper(canvas, data)
  # and launch the app
  root.mainloop()  # blocks until window is closed
  print("bye!")
run(300, 300)