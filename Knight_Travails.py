''' 
--------------------------------------------------------------
                      Knights Travails
--------------------------------------------------------------
Problem Description:

A Knight from a given position can move to any other position on an 8x8 chessboard.
This program finds the smallest number of moves required for a knight to get
to any end position from a starting position on the chessboard.
'''
from tkinter import *
from tkinter import ttk

#initializes board array with all possible coordinates in the form of tuples (x,y)
# x -> a to h, and y -> 1 to 8
board = [(chr(x//8 + 97),x%8 + 1) for x in range(64)] 

'''
Requires: A tuple in the form of (x,y) where x and y are coordinates on the board.
Effects: Returns a list of all possible legal moves that can be made on the board.
         Will return an empty list if an invalid start position is given
'''
def legalMoves(position): #User Defined Function
    x,y  = ord(position[0]) % 97 + 1, position[1] #Converts a-f to 1-8, use of variables and arithmetic expressions
    possibleMoves = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)] 
    moves  = [(chr(m[0] + x + 96), m[1] + y) for m in possibleMoves] #Use of sequence iteration
    legal = [x for x in moves if x in board]
    return legal

'''
Requires: Two tuples in the form of (x,y) where x and y are coordinates on the board
Effects: Returns a list of possible routes(list of moves) from start to end

The minNumMoves is 7 because the start position is included in the path. 
A knight can get to any square within at least 6 moves
'''
def legalRoutes(start,end):
    routes = []
    def findRoutes(start,end, path, minNumMoves = 7): #Use of if, elif
        if start != end and not(start in path) and len(path) < smallestRouteLength(routes):
            path.append(start)
            moves  = legalMoves(start)
            for x in moves:
                findRoutes(x,end,path,minNumMoves)
            path.pop()
        elif(start == end):
            path.append(start)
            routes.append(path.copy())
            path.pop()
            
    findRoutes(start,end,[])    
    routes = [x for x in routes if len(x) == smallestRouteLength(routes)] #Gets rid of routes that have more than min no. of moves
    return routes

'''
Requires: List of lists that contains positions in the form of a tuple (x,y).
Effects: Returns the shortest list length in routes
'''
def smallestRouteLength(routes):
    y = 7
    for x in routes:
        y = min(y,len(x))
    return y

'''
Requires: List of lists that contains positions in the form of a tuple (x,y).
Effects: Returns a string that will be used to write to a file. Seperates 
each path in routes in new lines.
'''
def formatRouteString(routes):
    formattedRoutes = [[x[0] + str(x[1]) for x in y] for y in routes]
    formattedRoutes = '\n'.join([''.join(x) for x in formattedRoutes])
    return formattedRoutes

def writeRoutes(file, routes): #Use of file output/writing to file
    strRoutes = formatRouteString(routes)
    file = open(file,'w')
    file.write(strRoutes)
    file.close()


def readRoutes(file): #Use of file input/ reading from file
     routes = []
     file = open(file)
     for line in file:
         routes.append(line)
     file.close()
     
     formattedRoutes = []
     for x in routes:
        moves = []
        for y in range(len(x)//2):
            moves.append(x[y*2:y*2 +2])
        formattedRoutes.append(moves)
     return formattedRoutes
     
'''
The following functions are responsible for creating the GUI on the chessboard
'''
def createGUI():
    global routes
    routes = readRoutes("cps109_a1_output.txt")
    
    global routeNo
    routeNo = 0
    
    global moveNo
    moveNo = -1
    
    root = Tk()
    root.title("Knight Moves Explorer")
    global mainframe
    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid()
    ttk.Label(mainframe,text="Moves Explorer",font=('Helvetica', 15, 'italic')).grid(column=0, row=0,columnspan=4)
    ttk.Button(mainframe,text="<",command=routeLeft).grid(column=0,row=1)
    pathLabel = ttk.Label(mainframe,text=f"Route").grid(column=1,row=1,columnspan=2)
    ttk.Button(mainframe,text=">",command=routeRight).grid(column=3,row=1)
    board = ttk.Frame(mainframe,padding=0)
    board.grid(column=0,row=2,columnspan=4)
    global chessframe
    chessframe = Canvas(board,width=400,height=400,background='white')
    for x in range(4):
        for y in range(8):
            if(y%2 == 0):
                chessframe.create_rectangle(x*100 + 50, y*50, x*100 + 100, y*50 +50, fill='black')
            else: #Use of else statement
                chessframe.create_rectangle(x*100, y*50, x*100 + 50, y*50 +50, fill='black')

    chessframe.grid(column=1,row=0,columnspan=8,rowspan=8)
    for x in range(8):
        ttk.Label(board,text=chr(x + 97)).grid(column=x+1,row=10)
        ttk.Label(board,text=str(x + 1)).grid(column=0,row=7-x)
    ttk.Button(mainframe,text="<",command=moveLeft).grid(column=0,row=4)
    moveLabel = ttk.Label(mainframe,text="").grid(column=1,row=4,columnspan=2)
    ttk.Button(mainframe,text=">",command=moveRight).grid(column=3,row=4)
    ttk.Label(mainframe,text='').grid(column=0,row=5,columnspan=4)
    moveRight()
    root.mainloop()
    

def moveLeft():
    global routes
    global routeNo
    global moveNo
    moveNo -= 1
    if moveNo == -1:
        moveNo = len(routes[routeNo]) - 1
    move = routes[routeNo][moveNo]
    updateGUI(routeNo, move)
def moveRight():
    global routes
    global routeNo
    global moveNo
    moveNo += 1
    if moveNo == len(routes[routeNo]):
        moveNo = 0
    move = routes[routeNo][moveNo]
    updateGUI(routeNo, move)
def routeLeft():
    global routes
    global routeNo
    global moveNo
    
    routeNo -= 1
    moveNo = 0
    if routeNo == -1:
        routeNo = len(routes) - 1
    
    move = routes[routeNo][moveNo]
    updateGUI(routeNo, move)
def routeRight():
    global routes
    global routeNo
    global moveNo
    
    routeNo += 1
    moveNo = 0
    if routeNo == len(routes):
        routeNo = 0
        
    move = routes[routeNo][moveNo]
    updateGUI(routeNo, move)

def updateGUI(route, move):
    global knight
    try: #The first updateGUI call will give an error as the knight won't exist, this allows to ignore that first call.
        chessframe.delete(knight)
    except:
        pass
    coord = mapOnBoard(move)
    knight = chessframe.create_text(25 + coord[0],375 - coord[1], anchor='center', text='K', fill='red')
    
    moveLabel = ttk.Label(mainframe,text=f"{move}").grid(column=1,row=4,columnspan=2)
    pathLabel = ttk.Label(mainframe,text=f"Route {route + 1}").grid(column=1,row=1,columnspan=2)
    
def mapOnBoard(move):
    coord = {'a':0,'b':50,'c':100,'d':150,'e':200,'f':250,'g':300,'h':350}
    
    return (coord[move[0]],(int(move[1])-1)*50)


'This function is run when the program is executed'
if __name__ == '__main__':
    
    print('\nKnights Travails') #Use of print statements
    print('Write positions without any spaces or seperators. Ex a1, h3, e7')
    print('Press Q to exit the program')
    while(True): #Use of general iteration
    
     start = input('\nEnter Starting Position: ') #Will take the first two chars
     if(start.lower() == 'q'):
         break
     end = input('Enter Ending Position: ') #Will take the first two chars
     if(end.lower() == 'q'):
         break
     start = (start[0],int(start[1]))
     end = (end[0],int(end[1]))
     if(start not in board or end not in board):
         print('\n Invalid Input')
         continue
     routes = legalRoutes(start, end)
     print('\n----Possible Routes----')
     print(formatRouteString(routes)) # print in the terminal
     writeRoutes('cps109_a1_output.txt',routes)
     createGUI()