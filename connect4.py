import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import copy


'''
in this implementation of connect four, we represent the state of the board as
a 7 by 6 numpy array, where red tiles are represented by 1, yellow tiles by -1, and empty tiles by 0.

this state is an attribute of a board, which also has the attribute "red" (a bool that 
tells you whose turn it is). A board is also a characteristic of a game, which also has the 
attribute "history", which is a set representing all of the board states that have been 
played thus far in the game. We store every encountered state into a dictionary that maps each
state to a value. If the value is high, then this state is favourable to red winning.
'''


class Game:

    def __init__(self, history=set()):
        self.history = history
        self.board = self.Board()

    def setBoard(self, board):
        self.board = board

    def getboard(self):
        return self.board

    def updatehistory(self):
        self.history.add(self.board.state.tobytes())

    # plays the corresponding chip (determined by the boolean redTurn)
    # in the corresponding column (col), and it adds that board to the game history accordingly

    def play(self, col, realmove):
        for i in range(6):
            if self.getboard().getstate()[col][i] == 0:
                if self.board.red:
                    if realmove:
                        print("R", col, i)
                    self.board.state[col][i] = 1
                    self.board.red = False
                else:
                    if realmove:
                        print("B", col, i)
                    self.board.state[col][i] = -1
                    self.board.red = True
                if realmove:
                    self.updatehistory()
                break
        return

    # determines if the column is playable without altering the board state
    def playable(self, col):

        for i in range(6):
            if self.board.state[col][i] == 0:
                return True
        return False

    # determines the winner of the game if there is one (1 for red, -1 for black)
    def winner(self):

        arr = self.board.state
        # horizontal check
        for x in range(4):
            for y in range(6):
                if arr[x:x + 4, y].sum() == 4:
                    return 1
                elif arr[x:x + 4, y].sum() == -4:
                    return -1

        # vertical check
        for x in range(7):
            for y in range(3):
                if arr[x, y:y + 4].sum() == 4:
                    return 1
                elif arr[x, y:y + 4].sum() == -4:
                    return -1

        # diagonal checks
        for x in range(4):
            for y in range(3):
                if np.trace(arr[x:x + 4, y:y + 4]) == 4 or np.trace(np.fliplr(arr[x:x + 4, y:y + 4])) == 4:
                    return 1
                elif np.trace(arr[x:x + 4, y:y + 4]) == -4 or np.trace(np.fliplr(arr[x:x + 4, y:y + 4])) == -4:
                    return -1

        # draw
        if np.count_nonzero(game) == 42:
            return 0

        return False

    class Board:

        # constructor creates an empty board
        def __init__(self, red=True, state=np.zeros((7, 6))):
            self.red = red  # boolean denoting red starts
            self.state = state

        def setstate(self, state):
            self.state = state

        def getstate(self):
            return self.state

        def setred(self, red):
            self.red = red



class ReinforcementAI:

    def __init__(self, game, dict):
        self.game = game
        self.dict = dict

    # returns a column (0-6) as next move
    def generate_move(self):
        return self.evaluate_board()[1]

    def evaluate_board(self):
        next_boards = {}
        for x in range(7):
            if self.game.playable(x):
                game_=copy.deepcopy(self.game)
                next_boards[x] = game_.getboard().getstate().tobytes();
        indict = False
        maxscore = float("-inf")
        minscore = float("inf")
        for x in next_boards:
            if next_boards[x] in self.dict:
                indict = True
                if maxscore < self.dict[next_boards[x]]:  # look up the game state in dict to get its value
                    maxscore = self.dict[next_boards[x]]
                    playcolred = x
                if minscore > self.dict[next_boards[x]]:
                    minscore = self.dict[next_boards[x]]
                    playcolblack = x
        if indict == True:
            if self.game.board.red == True:
                return maxscore, playcolred
            else:
                return minscore, playcolblack
        else:
            columns = [0, 1, 2, 3, 4, 5, 6]
            checker = False
            while checker == False:
                nextCol=random.choice(columns)
                if self.game.playable(nextCol):
                    checker = True
            return 0, nextCol


if __name__ == "__main__":
    f = open("C:\\Users\\Pengfei\\Desktop\\C4dict.pickle", 'rb')
    dict = pickle.load(f)  # set the dictionary to what has been saved on file
    game = Game()
    reinforcementAI1 = ReinforcementAI(game, dict)
    reinforcementAI2 = ReinforcementAI(game, dict)
    while not game.winner():
        game.play(reinforcementAI1.generate_move(), True)
        if not game.winner():
            game.play(reinforcementAI2.generate_move(), True)

    if game.winner() == 1:
        print("red won!")
        for h in game.history:
            if h in dict:
                dict[h] += -1
            else:
                dict[h] = -1
    elif game.winner() == -1:  # black won
        print("black won!")
        for h in game.history:
            if h in dict:
                dict[h] += 1
            else:
                dict[h] = 1
    elif game.winner() == 0:  # draw
        print("draw!")
        for h in game.history:
            if h in dict:
                dict[h] += -.1
            else:
                dict[h] = -.1
    f = open("C:\\Users\\Pengfei\\Desktop\\C4dict.pickle", 'wb')
    pickle.dump(dict, f)
    print(len(dict))
    f.close()
















