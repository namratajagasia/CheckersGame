import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
from gamePlay import getOpponentColor, isAnyMovePossible
import sys

'''
Simple Greedy just has a simple evaluation function where my coins should be more than my opponent's
A move on the board which maximizes my coins is the best move
'''
color=""
currentPlayerColor =""
opponentPlayerColor=""
def evaluation(board):
    global currentPlayerColor    
    global opponentPlayerColor
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == currentPlayerColor.upper():
            value = value + 1
        elif board[x][y].upper() == opponentPlayerColor.upper():
            value = value - 1
    
    return value

def evaluation1(board):
    global currentPlayerColor    
    global opponentPlayerColor
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        
        if board[x][y]== board[x][y].upper() and  currentPlayerColor ==  currentPlayerColor.upper():
            value = value + 5
        elif board[x][y].upper() == currentPlayerColor.upper():
            value = value + 3
        elif board[x][y]== board[x][y].upper() and  opponentPlayerColor ==  opponentPlayerColor.upper(): 
            value = value - 5      
        elif board[x][y].upper() == opponentPlayerColor.upper():
            value = value - 3
    
    return value

def nextMove(board, col, time, movesRemaining):
   
    #print "player color",color
    global currentPlayerColor 
    currentPlayerColor=col
    global opponentPlayerColor
    opponentPlayerColor = getOpponentColor(col)
    moves = getAllPossibleMoves(board, currentPlayerColor)#returns a list of possible moves[]
    #Trying to find the move where I have best score
    best = None
    for move in moves:
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)#get the possible states
        depth=5
        alpha = -sys.maxint - 1
        beta = sys.maxint
        moveVal = minimax(newBoard,depth,alpha,beta,True) #we cal minimax to evaluate
        if best == None or moveVal > best:
            bestMove = move
            best = moveVal
    return bestMove

def minimax(board,depth,alpha,beta,maximizingPlayer):
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
        