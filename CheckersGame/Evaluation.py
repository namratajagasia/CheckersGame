import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
from gamePlay import getOpponentColor, isAnyMovePossible, isCapturePossible,\
    isCapturePossibleFromPosition, countPieces, canMoveToPosition
import sys
color=""
currentPlayerColor =""
opponentPlayerColor=""
'''
For the depth
the moves remaining and the time factor varies the depth of the tree 
For the evaluation function
Count of pieces of the current player is used to determine 
which stage ie initial ,middle or last
respective strategies to use and the weights assigned for different evaluation functions 
 
'''
def canMoveToMyPosition(board, x1, y1, x2, y2):
    # Check whether (x1,y1) can move to (x2,y2) in one move (plain or capture)
    
    if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > 7 or y1 > 7 or x2 > 7 or y2 > 7:
        return False
        
    color = board[x1][y1]
    if color == ' ':
        return False
    if board[x2][y2] != ' ':
        return False
    x1_x2 = abs(x1-x2)
    y1_y2 = abs(y1-y2)
    if x1_x2 != 1 and x1_x2 != 2:
        return False
    if x1_x2 != y1_y2:
        return False
    if color == 'w' and x2 > x1:    # White men cannot move down
        return False
    if color == 'r' and x2 < x1:    # Red men cannot move up
        return False
    if x1_x2 == 2: # It could be a capture move
        if board[(x1+x2)/2][(y1+y2)/2].lower() == opponentPlayerColor.lower():
            # Middle piece must be opponent
            return False
    return True
def isMyCapturePossibleFromPosition(board, x, y):
    # Returns whether (x,y) piece can make a capture at this time
    
    opponent = getOpponentColor(board[x][y])
    # Check whether a jump possible to all four directions    
    if canMoveToMyPosition(board, x, y, x-2, y-2) == True:#top left diagonal leaving 1
        return True    
    if canMoveToMyPosition(board, x, y, x-2, y+2) == True:#bottom left
        return True    
    if canMoveToMyPosition(board, x, y, x+2, y-2) == True:#right top
        return True    
    if canMoveToMyPosition(board, x, y, x+2, y+2) == True:#right bottom
        return True    
            
    return False
def evaluation1(board):
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
def evaluationMovingToCenter(board):
    '''
    its a good practice to move the coins in the center of the game at opening
    '''
    value = 0
    
    for pos in [14,15,16]:
        xy = gamePlay.serialToGrid(pos)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == currentPlayerColor.upper() and currentPlayerColor.upper()== 'R' :
            value = value+1
    for pos in [17,18,19]:
        xy = gamePlay.serialToGrid(pos)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == currentPlayerColor.upper() and currentPlayerColor.upper()== 'W' :
            value = value+1        
    return value
def evaluationMovingToDefense(board):
    '''
    after the pieces have come to the center and hopefully after some attack trying to move to the defense locations
    '''
    value = 0
    for pos in [12,13]:
        xy = gamePlay.serialToGrid(pos)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == currentPlayerColor.upper() and currentPlayerColor.upper()== 'R' :
            value = value+1
    for pos in [20,21]:
        xy = gamePlay.serialToGrid(pos)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == currentPlayerColor.upper() and currentPlayerColor.upper()== 'W' :
            value = value+1        
    return value
def evaluationMakingItKing(board):
    '''
    numbers of kings wrt to opponents kings
    '''
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
    if board[x][y]== board[x][y].upper() and  currentPlayerColor ==  currentPlayerColor.upper():   
        value = value+1
    elif board[x][y]== board[x][y].upper() and  opponentPlayerColor ==  opponentPlayerColor.upper():
        value = value+1
    return value    
        
def evaluationColorVsOpposite(board):
    '''number of pieces compared to opponents'''
    global currentPlayerColor    
    global opponentPlayerColor
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        
        if board[x][y].upper() == currentPlayerColor.upper():  
            value = value+1
        elif board[x][y].upper() == opponentPlayerColor.upper():
            value = value - 1    
    return value

def evaluationAttackFunction(board):
    '''
    number of pieces the board can capture
    '''
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if isCapturePossibleFromPosition(board, x, y):
            if board[x][y].upper() == currentPlayerColor.upper():  
                value = value+1
            elif board[x][y].upper() == opponentPlayerColor.upper():
                value = value - 1
    return value         
def evaluationCanBeAttacked(board):
    '''
    current player can be attacked
    '''  
    value = 0
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if isMyCapturePossibleFromPosition(board, x, y):
            value = -100
    return value   

def nextMove(board, col, time, movesRemaining):
   
    #print "player color",color
    global currentPlayerColor 
    currentPlayerColor=col
    global opponentPlayerColor
    opponentPlayerColor = getOpponentColor(col)
    moves = getAllPossibleMoves(board, currentPlayerColor)
    
    '''If there is only 1 move possible no need to evaluate just return that moves'''
    if len(moves)==1:
        return moves[0]
    else:
        best = None
        for move in moves:
            newBoard = deepcopy(board)
            gamePlay.doMove(newBoard,move)       
            alpha = -sys.maxint - 1
            beta = sys.maxint
            '''
            Time and moves remaining are few based on the simple greedy evaluation of the board 
            '''
            if time < 5 or (movesRemaining)<4:
                moveVal = evaluation1(newBoard)
                     
            else:  
                 
                '''
                #if moves remaing are very few we donot go too deep
                '''
                if (movesRemaining/2)<30:
                    moveVal = minimax(newBoard,3,alpha,beta,True)
                    '''inital moves'''    
                elif movesRemaining>140:
                    #start of the game heuristics handles the opening so dont need to go to deep
                    moveVal = minimax(newBoard,3,alpha,beta,True)              
                else:
                    '''last moves'''
                    if time < 5:
                        moveVal = minimax(newBoard,1,alpha,beta,True)
                    elif time<18:
                        moveVal = minimax(newBoard,3,alpha,beta,True)
                    elif time<23:
                        moveVal = minimax(newBoard,5,alpha,beta,True)        
                    elif time<28:
                        moveVal = minimax(newBoard,7,alpha,beta,True)
                        '''middle moves'''    
                    else:
                        moveVal = minimax(newBoard,5,alpha,beta,True)   
            
            #moveVal = minimax(newBoard,depth,alpha,beta,True) #we cal minimax to evaluate
            if best == None or moveVal > best:
                bestMove = move
                best = moveVal
        return bestMove

def minimax(board,depth,alpha,beta,maximizingPlayer):
    global currentPlayerColor 
   
    global opponentPlayerColor
    if depth==0 or not isAnyMovePossible(board, currentPlayerColor) or not isAnyMovePossible(board,opponentPlayerColor):
        if countPieces(board,currentPlayerColor)>7:
            '''
            initial stage and opening moves trying to focus on center and attack
            '''
            return (0.75 * evaluationMovingToCenter(board))+ (0.20 * evaluationAttackFunction(board))+(0.5*evaluationColorVsOpposite(board))
        
        elif countPieces(board,currentPlayerColor)>=6 :
            '''
            middle stage have to be defensive And would also need to be attacktive
            ''' 
            return (0.75 * evaluationMovingToDefense(board))+ (0.15 * evaluationAttackFunction(board))+(0.5*evaluationColorVsOpposite(board)+(0.5*evaluationMakingItKing(board)))
        elif countPieces(board,currentPlayerColor)>4 :
            '''
            middle stage have to be get in center amd attack
             
            '''  
            return (0.20 * evaluationMovingToCenter(board))+ (0.70 * evaluationAttackFunction(board))+(0.5*evaluationColorVsOpposite(board)+(0.5*evaluationMakingItKing(board))+evaluationCanBeAttacked(board))
        else:
            '''
            when 4 or less than four pieces are remaining
            '''   
            return (0.50 * evaluationAttackFunction(board))+(0.30*evaluationColorVsOpposite(board)+(0.20*evaluationMovingToDefense(board))+evaluationCanBeAttacked(board))      
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
        