"""
how explore(gamestate) works:

start by giving explore() the startGameState as a parameter

it then creates a node for this game state in the game tree adjacency list, and creates
edges from this game state to all the game states that can be reached from the current gamestate with only 1 move (using the function findLegalMoves(gameState)).
then it goes through all of the edges (child game states) and if that game state is not in adj yet then call explore() with the child game state as parameter

the adjacency list of all game states is structured like this:
adj[<gameState>] = [<childGameState1>, <childGameState2>, ...]
gameState and childGameState is a string wich contains all the neccesary information about the game state
for the game FingersDown it looks like this: "1214"  ("hand1 hand2 hand3 hand4")
where hand1 and hand2 (in ascending order based on hand value) is the hands of the player whose turn it is, and hand3 and hand4 (also in ascending order) is the other player's hands

for example:
adj["1111"] = ["1211"]
adj["1211"] = ["1212", "1312"]
and so on...

"""

possibleMoveTypes = ["S", "LL", "LH", "HL", "HH"] # [split, use lowest hand on opponent lowest hand, use lowest hand on opponent highest hand, use highest hand on opponent lowest hand, use highest hand on opponent highest hand]
startGameState = "1111" # hand1 hand2 hand3 hand4. The number say how many fingers are on the hand

def getAdjacencyListOfGame():
    adj = {}
    adjMoveIDs = {}
    return explore(startGameState, adj, adjMoveIDs)

def explore(gameState, adj, adjMoveIDs):

    adj[gameState], adjMoveIDs[gameState] = findLegalMoves(gameState)

    for move in adj[gameState]:
        if move not in adj:
            adj, adjMoveIDs, = explore(move, adj, adjMoveIDs,)

    return [adj, adjMoveIDs]

# do the actual move. Return the new game state after the move is executed. If the move is illegal from the current game state then return False.
def doMove(moveType, gameState):

    hand1 = gameState[0]
    hand2 = gameState[1]
    hand3 = gameState[2]
    hand4 = gameState[3]

    attackWithHand = attackHand = split = 0

    # checks wether the move is legal. If it's not then return False
    if(moveType == possibleMoveTypes[0] and (((hand1 == "2" or hand1 == "4") and hand2 == "0") or ((hand2 == "2" or hand2 == "4") and hand1 == "0"))):
        split = 1
    elif(moveType == possibleMoveTypes[1] and hand1 != "0" and hand3 != "0"):
        attackWithHand = 1
        attackHand = 1
    elif(moveType == possibleMoveTypes[2] and (hand1 != "0" and hand4 != "0")):
        attackWithHand = 1
        attackHand = 2
    elif(moveType == possibleMoveTypes[3] and (hand2 != "0" and hand3 != "0")):
        attackWithHand = 2
        attackHand = 1
    elif(moveType == possibleMoveTypes[4] and hand2 != "0" and hand4 != "0"):
        attackWithHand = 2
        attackHand = 2
    else:
        return False

    # calculate result of move
    if (split == 1):
        if((hand1 == "2" or hand1 == "4")  and hand2 == "0"):
            hand1 = str(int(int(hand1) / 2))
            hand2 = hand1
        elif(hand1 == "0" and (hand2 == "2" or hand2 == "4")):
            hand1 = str(int(int(hand2) / 2))
            hand2 = hand1
    else:
        if (attackWithHand == 1 and attackHand == 1):
            hand3 = str((int(hand3) + int(hand1)) % 5)
        elif (attackWithHand == 1):
            hand4 = str((int(hand4) + int(hand1)) % 5)
        elif (attackHand == 1):
            hand3 = str((int(hand3) + int(hand2)) % 5)
        else:
            hand4 = str((int(hand4) + int(hand2)) % 5)

    # make hand1 and hand2 be in ascending order, same with hand3 and hand4 (to remove symetrical game states, for example: "1231" is the same as "1213" in this game)
    if(hand1>hand2): hand1, hand2 = hand2, hand1
    if(hand3>hand4): hand3, hand4 = hand4, hand3

    # reverse/swap/switch hands 
    # this makes it so I don't need to keep track of whose turn it is, as it will always be the one with the first two hands who has the next move
    hand1, hand3 = hand3, hand1
    hand2, hand4 = hand4, hand2

    newGameState = hand1 + hand2 + hand3 + hand4

    return newGameState

# If without having to do any more moves the game state is winning, then return 1. If it's losing return -1.
# If it's a draw then return 0. But if the game is not over yet from the game state then return "undecided"
def evaluateGameState(gameState):
    if(gameState[0] == "0" and gameState[1] == "0"): return -1

    return "undecided"

# this function returns a list of all the game states you can reach from the current game state
def findLegalMoves(gameState):
    legalMoves = []
    legalNewGameStates = []

    for x in possibleMoveTypes:
        newGameState = doMove(x, gameState)
        if newGameState != False: 
            legalMoves.append(x)
            if(newGameState not in legalNewGameStates): 
                legalNewGameStates.append(newGameState)
    
    return [legalNewGameStates, legalMoves]