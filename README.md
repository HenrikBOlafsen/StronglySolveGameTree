# For any turn based deterministic game with a game tree small enough to store all possible game states, get all the best moves from all of the game states

The algorithm finds the best moves from all game states (excluding game states with no legal moves). It gets printed and stored in the dict gameStatesBestMoves where each game state has a list of all the best moves from that game state
It also lets you know what game states are a forced win if you play perfectly (this would be all the game states that are scored 1 in the gameStatesScore dict) and from what game states you are forced to lose if your opponent plays perfectly (scored -1 in the gameStatesScore dict). As well as what game states is a forced draw if both players play perfectly (this would be all the game states that are not in the gameStatesScore dict). 

**extra**: The algorithm also lets you know what the longest forced win is, as this will be the last element in the gameStatesScore dict. And you can also find out how many unique game states that exists for your game by getting the length of the dict gameStatesBestMoves. And you can find out how many of the gameStates that are a forced win or forced defeat by getting the length of the gameStatesScore dict. 

This algorithm would work on games like: **Tic-tac-toe, fingers down (chopsticks) and connect 4**
But it would **not** work for games with too large game trees like: chess, go and pente

What makes this algorithm useful is its ease of use for games with small game trees.
All you need to do to make this algorithm work for your game is to modify the function doMove(moveType, gameState), the function evaluateGameState(gameState), the possibleMoveTypes list and the startGameState string like this:

## How to modify the possibleMoveTypes list:

The list should contain all of the possible move types that can be done in the game. For example in the game tic-tac-toe there is 9 possible move types, and these are to put an "x" in any of the 9 squares.
So the possibleMoveTypes list could for example look like this for tic-tac-toe: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]. Or like this: ["topLeft", "topMiddle", "topRight", "middleLeft", "middleMiddle", "middleRight", "bottomLeft", "bottomMiddle", "bottomRight"]

## How to modify the startGameState string:

This string should contain all the necessary information to perfectly represent the game state.
For example in tic-tac-toe startGameState could look like this: **"000000000"**. each "0" represents one square and there is 9 in total.
After a couple of turns the game state would for example look like this: "x00ox0xoo" where there is filled in "x" and "o" in some of the squares

## How to modify doMove(moveType, gameState):

The parameter gameState is a string that contains all of the necessary information to perfectly represent the game state.
While the parameter moveType is a string that tells the function what type of move is to be made from the current gameState.
You need to make it so the function **returns the new game state after the move is executed, or if the moveType is illegal from the current game state then it should return False**.
There are examples further down of what this function could look like for tic-tac-toe and fingers down

## How to modify evaluateGameState(gameState):

The parameter gameState is a string that contains all of the necessary information to perfectly represent the game state.
This function is used to evaluate 
You need to make the function:
**Return -1** if from the current game state the game is finished and the player who had the last move won.
Or **return 1** if from the current game state the game is finished and the player who had the last move lost.
Or **return 0** if from the current game state the game is finished and it was a draw.
Or **return "undecided"** if the game is **not** finished yet from the current game state.
There are examples further down of what this function could look like for tic-tac-toe and fingers down

## **After you have done these modifications to make the algorithm work for your game, then just run ScoreEndMoves.py**

## How the algorithm works: 

Logic for scoring all the game states:
- score of 1 means it is a winning game state, score -1 means it is a losing game state, and if it is not scored the game state is a draw if both players play perfectly
- Start by getting an adjacency list of all the possible game states (How I do this is explained in GetGameAdjacensyList.py)
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

## doMove(moveType, gameState) and evaluateGameState(gameState) examples:

### Tic-tac-toe:
possibleMoveTypes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] #["topLeft", "topMiddle", "topRight", "middleLeft", "middleMiddle", "middleRight", "bottomLeft", "bottomMiddle", "bottomRight"]
startGameState = "000000000" #there are 9 "0" where one each of them represent a different square. "0" will be replaced with "x" and "o" as the games goes on

```
# do the actual move. Return the new game state after the move is executed. If the move is illegal from the current game state then return False.
def doMove(moveType, gameState):

    if evaluateGameState(gameState) != "undecided": 
        return False

    index = int(moveType) - 1
    if(gameState[index]=="0"): #checks if the square is available
        gameState = gameState[:index] + "x" + gameState[index+1:] #puts an "x" on the square
    else:
        return False

    # converts "o" to "x" and "x" to "o" 
    # this makes it so I don't need to keep track of whose turn it is, as it will always be the one with "x" who has the next move
    for i in range(len(gameState)):
        if gameState[i] == "x":
            gameState = gameState[:i] + "o" + gameState[i+1:]
        elif gameState[i] == "o":
            gameState = gameState[:i] + "x" + gameState[i+1:]

    return gameState

# If without having to do any more moves the game state is winning, then return 1. If it's losing return -1.
# If it's a draw then return 0. But if the game is not over yet from the game state then return "undecided"
def evaluateGameState(gameState):
    # checks the rows and columns
    for i in range(3):
        if(gameState[i*3] == "o" and gameState[i*3+1] == "o" and gameState[i*3+2] == "o"):
            return -1
        elif(gameState[i] == "o" and gameState[i+3] == "o" and gameState[i+6] == "o"):
            return -1
    # checks the diagonals
    if(gameState[0] == "o" and gameState[4] == "o" and gameState[8] == "o"):
        return -1
    elif(gameState[6] == "o" and gameState[4] == "o" and gameState[2] == "o"):
        return -1

    availableSpaces = False
    for i in range(len(gameState)):
        if(gameState[i] == "0"):
            availableSpaces = True
    if not availableSpaces:
        return 0

    return "undecided"
```

### Fingers down:
possibleMoveTypes = ["S", "LL", "LH", "HL", "HH"] #[split, use lowest hand on opponent lowest hand, use lowest hand on opponent highest hand, use highest hand on opponent lowest hand, use highest hand on opponent highest hand]
startGameState = "1111" #hand1 hand2 hand3 hand4. The number say how many fingers are on the hand

```
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
```