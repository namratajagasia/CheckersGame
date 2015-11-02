import gamePlay
import random
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
from gamePlay import getOpponentColor, isAnyMovePossible,\
    isCapturePossibleFromPosition, countPieces
import sys

'''
Simple Greedy just has a simple evaluation function where my coins should be more than my opponent's
A move on the board which maximizes my coins is the best move
'''
color=""
currentPlayerColor =""
opponentPlayerColor=""
deep=0
timeList =[]
def evaluationGreedy(board, color):
    # Evaluation function 1
    # Count how many more pieces I have than the opponent
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value = 0
    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            value = value + 1
        elif board[x][y].upper() == opponentColor.upper():
            value = value - 1
    
    return value

def evaluation(board):
    # Weights are assigned as per the moves forward diagonal vs forward and backward diagonal moves  possible
    #when the piece becomes king more weights are assigned compared to normal piece 
    #print "Considering board"
    global currentPlayerColor    
    global opponentPlayerColor
    value = 0
   
    normalAttack =30
    kingAttack=60
    normalPoint = 1000
    KingPoint = 2000
    currentPiece=0
    opponentPiece=0
    borderPiece=0
    borderList=[(0,1),(0,3),(0,5),(0,7),(1,0),(2,7),(3,7),(4,7),(5,0),(6,7),(7,0),(7,2),(7,4),(7,7)]
    
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if board[x][y]== board[x][y].upper() and  currentPlayerColor ==  currentPlayerColor.upper():#currentKing
           
            if isCapturePossibleFromPosition(board,x,y):
                #capturePossibleValueCurrent+=1.8
                if (x,y) in borderList:
                    value+=borderPiece+kingAttack+KingPoint
                else:
                    value+=kingAttack+KingPoint                 
            else:    
                #noOfCurrentKings=noOfCurrentKings+1.5
                if (x,y) in borderList:
                    value+=borderPiece+KingPoint
                else:    
                    value+=KingPoint
            currentPiece
        elif  board[x][y]== board[x][y].upper() and  opponentPlayerColor ==  opponentPlayerColor.upper():#opponentKing
            
            if isCapturePossibleFromPosition(board,x,y):
                #capturePossibleValueOpponent-=1.8
                value-=(kingAttack+KingPoint)
            else:        
                #noOfOpponentKings=noOfOpponentKings -1.5
                value-=KingPoint
            opponentPiece+=1
        elif  board[x][y].upper() == currentPlayerColor.upper():#current
            
            if isCapturePossibleFromPosition(board,x,y):
                #capturePossibleValueCurrent+=1.8
                if (x,y) in borderList:
                    value+=borderPiece+normalAttack+normalPoint
                else:
                    value+=normalAttack+normalPoint
            else:    
                #noOfCurrent=noOfCurrent+1.3
                if (x,y) in borderList:
                    value+=borderPiece+normalPoint
                else:    
                    value+=normalPoint
            currentPiece+=1   
        elif board[x][y].upper() == opponentPlayerColor.upper():#opponent
            if isCapturePossibleFromPosition(board,x,y):
                #capturePossibleValueOpponent-=1.8
                value-= (normalAttack+normalPoint)
            else:    
                #noOfOpponent= noOfOpponent-1.3
                value-=normalPoint
            opponentPiece+=1
        #value = (((capturePossibleValueCurrent+capturePossibleValueOpponent))+(1*(noOfCurrentKings+noOfOpponentKings))+ (1*(noOfCurrent+noOfOpponent)))
    if opponentPiece!=0:
        return value
    else:
        return value

def nextMove(board, col, time, movesRemaining):
    global deep
    global timeList
    #Assigned global current and  opponent color used to expand nodes and evaluate as per the player
    global currentPlayerColor 
    currentPlayerColor=col
    global opponentPlayerColor
    opponentPlayerColor = getOpponentColor(col)
    moves = getAllPossibleMoves(board, currentPlayerColor)#returns a list of possible moves[] for the current player
    #Trying to find the move where my game has best score
    if len(moves)==1:
        return moves[0]
    timeList.append(time)
    elapsed=timeList[0]-time
    originalTime = elapsed + time
    print "timeList" , timeList
    if(len(timeList)>=2):
        print "secondLast", timeList[-2]
        differenceTime = timeList[-2]-timeList[-1]
    else:
        differenceTime=0    
    print "last",timeList[-1]
    
    best = None
    
    #if time==0 or ((differenceTime*2) >= timeList[-1]) or countPieces(board, currentPlayerColor)<= differenceTime:
            #or time differnce between last and second last 
    if time<=3 or movesRemaining>=time:
        newBoard = deepcopy(board)
        print "calling random move"
        bestMove = randomMove(newBoard,currentPlayerColor)                
    else:        
        for move in moves:  
            newBoard = deepcopy(board)          
            gamePlay.doMove(newBoard,move)#get the possible states
            depth=deep
            
            alpha = -sys.maxint - 1
            beta = sys.maxint           
            print "calling next move" 
            
            moveVal = minimax(newBoard,deep,alpha,beta,True)
                    
                        
            if best == None or moveVal > best:
                bestMove = move
                best = moveVal
        if deep<=7:            
            deep=deep+1
            
    print "increased depth,new depth is ",deep   
    #timeList.append(time)
    print"time list after eval",timeList    
    return bestMove
def randomMove(board,color):
    '''Just play randomly among the possible moves'''
    moves = getAllPossibleMoves(board, color)    
    bestMove = moves[random.randint(0,len(moves) - 1)]
    return bestMove
def minimax(board,depth,alpha,beta,maximizingPlayer):
    #for every alternate player traverse upto depth as specified.
    #Alternately expand the nodes for the min and max player.
    #traverse upto the leaf or until the specified depth is reached
    #Then apply the evaluation function
    #backtrack for each node till the calling node is reached and return.
    #in each step alpha-beta prunning is applied and as per conditions the tree is getting prunned .
    global currentPlayerColor   
    global opponentPlayerColor
    if depth==0 or not isAnyMovePossible(board, currentPlayerColor) or not isAnyMovePossible(board,opponentPlayerColor):
        return evaluation(board) 
    if maximizingPlayer:
        v = -sys.maxint - 1
        moves = getAllPossibleMoves(board, opponentPlayerColor)
        for move in moves:
            newBoard = deepcopy(board)
            gamePlay.doMove(newBoard,move)
            #print "inside max",color
            #color=getOpponentColor(color)
            v = max(v,minimax(newBoard, depth-1, alpha, beta, False))
            alpha = max(alpha,v)
            if beta <= alpha:
                return alpha
        return v
    else:
        v = sys.maxint
        moves = getAllPossibleMoves(board, currentPlayerColor)
        for move in moves:
            newBoard = deepcopy(board)
            gamePlay.doMove(newBoard,move)
            #print "inside min",color
            #color=getOpponentColor(color)
            v = min(v,minimax(newBoard, depth-1, alpha, beta, True))
            beta = min(beta,v)
            if beta <= alpha:
                return beta
        return v
        