import GetGameAdjacencyList

"""
Logic for scoring all the game states:
    - score of 1 means it is a winning game state, score -1 means it is a losing game state, and if it is not scored the game state is a draw if both players play perfectly
    - Start by getting an adjacency list of all the possible game states (How I do this is explained in GetGameAdjacencyList.py)
    - For the game states where the game is over, evaluate those game states with the function evaluateGameState()
    - Go through all the game states without a score and check if they have a child with score. 
      If a child game state is a losing game state, then this game state is a winning game state.
      If all the children game states are winning game states then this game state is a losing game state.
      Otherwise don't score this game state
    - repeat the last step until there is no change in the length of the list gameStatesScore (that means we have accurately scored all the game states)
    
Logic for finding all the best moves from all the game states:
    - Go through each game state
    - If the game state is winning, find which moves are the winning moves (these are moves that result in a new losing game state for the opponent) and add them to the bestMoves list for this game state
    - If the game state is not scored (or scored 0), find which game states that do not result in a new winning game state for the opponent, and add them to the bestMoves list for this game state
    - If there is only losing moves then just add those to the bestMoves list for this game state.
    - The game states that has no legal moves gets deleted from the gameStatesBestMoves list

"""

gameAdj, legalMovesFromGameState = GetGameAdjacencyList.getAdjacencyListOfGame()

gameStates = list(gameAdj)

gameStatesScore = {}

gameStatesBestMoves = {}

# for the game states where the game is over, set the game state to its evaluation
def scoreEndGameStates():
    for gameState in gameStates:
        if(len(gameAdj[gameState]) == 0): # if this game state has no children then it is an end game state
            evaluation = GetGameAdjacencyList.evaluateGameState(gameState)
            if evaluation != 0 and evaluation != "undecided":
                gameStatesScore[gameState] = evaluation

def scoreParentGameStates():
    for gameState in gameStates:
        if(gameState not in gameStatesScore):
            # If the child game state is a losing game state, then this game state is a winning game state
            for child in gameAdj[gameState]:
                if(child in gameStatesScore):
                    if(gameStatesScore[child] == -1):
                        gameStatesScore[gameState] = 1 # winning gameState
                        break
            
            # If all the children game states are winning game states then this game state is a losing game state
            allChildrenWin = True
            for child in gameAdj[gameState]:
                if(child in gameStatesScore):
                    if(gameStatesScore[child] == -1):
                        allChildrenWin = False
                        break
                else:
                    allChildrenWin = False
                    break
            if(allChildrenWin and len(gameAdj[gameState]) != 0):
                gameStatesScore[gameState] = -1 # losing gameState

def scoreAllMoves():
    scoreEndGameStates() #goes through all game states and finds the ones where the game is over, and then it scores these game states based on who won

    oldGameStateScoreLen = 0
    maxDepth = 1000
    i = 0
    while oldGameStateScoreLen != len(gameStatesScore) and i < maxDepth:
        oldGameStateScoreLen = len(gameStatesScore)
        scoreParentGameStates() # scores the parent game states of the already scored game states if one of the players have a forced win from this parent game state
        i += 1

    return gameStatesScore

# for each game state, find the best moves
def findAllBestMoves():
    for gameState in gameStates:
        gameStatesBestMoves[gameState] = findBestMove(gameState);
        if(len(gameStatesBestMoves[gameState]) == 0):
            del gameStatesBestMoves[gameState] # deletes all the game states where the game has ended, and therefore has no legal moves

def findBestMove(gameState):
    bestMoves = []
    # If the game state is winning, find wich moves are the winning moves and add them to the bestMoves list
    for moveType in legalMovesFromGameState[gameState]:
        newGameState = GetGameAdjacencyList.doMove(moveType, gameState)
        if(newGameState in gameStatesScore and gameStatesScore[newGameState] == -1):
            bestMoves.append(moveType)

    # If the game state isn't winning, add all the legal moves that doesn't result in the next move being a winning move to bestMoves
    if(len(bestMoves) == 0):
        for moveType in legalMovesFromGameState[gameState]:
            newGameState = GetGameAdjacencyList.doMove(moveType, gameState)
            if(newGameState not in gameStatesScore):
                bestMoves.append(moveType)

    # If the game state still doesn't have any good moves, then add all the legal moves from the game state to the bestMoves list even though they are losing moves
    if(len(bestMoves) == 0):
        for moveType in legalMovesFromGameState[gameState]:
            bestMoves.append(moveType)
    return bestMoves


scoreAllMoves()
findAllBestMoves()

print("score of game states: 1 is winning, -1 is losing, 0 is draw, if the game state isn't in the dict then it is a draw if both players play perfectly")
print(gameStatesScore)
print("best moves from all game states:")
print(gameStatesBestMoves)