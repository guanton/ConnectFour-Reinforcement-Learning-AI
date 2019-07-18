import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import copy


'''
in this implementation of connect four, we represent the state of the board as
a 7 by 6 numpy array, where red tiles are represented by 1, yellow tiles by -1, and empty tiles by 0.

this state is an attribute of a board, which also has the attribute "red" (a bool that 
tells you whose turn it is). A board is an attribute of a game, which also has the 
attribute "history", which is a set representing all of the board states that have been 
played thus far in the game. After a game has finished, we store every encountered state 
into a dictionary that maps each state to a value. If the value is high, then this state is favourable to red winning.
The reinforcement AI will pick the best move according to this dictionary.
'''

class Game:

    def __init__(self):
        self.history = set()
        self.board = self.Board()  # empty board, red's turn
        self.lastcolplayed = None

    def setBoard(self, board):
        self.board = board

    def updatehistory(self):
        self.history.add(self.board.state.tobytes())  # adds the state of the board (in byte form) to the dictionary

    # plays the corresponding chip (determined by the boolean redTurn)
    # in the corresponding column (col), and it adds that board to the game history accordingly
    def play(self, col, realmove):
        for i in range(6):  # search the column from bottom up for an empty slot
            if self.board.state[col][i] == 0:
                self.lastcolplayed = i
                if self.board.red:
                    if realmove:
                        # print("R", col, i)
                        pass
                    self.board.state[col][i] = 1
                    self.board.red = False
                else:
                    if realmove:
                        # print("B", col, i)
                        pass
                    self.board.state[col][i] = -1
                    self.board.red = True
                if realmove:
                    # play may be called by minimaxAI, which will call it on other board states down the line to
                    # determine its move. In this case, we don't want want to update the history of the game
                    self.updatehistory()
                break
        return

    # determines if the column is playable without altering the board state
    def playable(self, col):
        for i in range(6):
            if self.board.state[col][i] == 0:
                return True
        return False

    """simplistic evaluator for a board. Evaluates end games and returns random number between 0-1 otherwise """
    def evaluatestate(self):
        if self.winner() == 1:
            return float("inf")
        elif self.winner() == -1:
            return float("-inf")
        elif self.winner() == 0:
            return 0
        elif self.winner() is None:
            return random.uniform(0, 1)

    # determines the winner of the game if there is one (1 for red, -1 for black). Returns None if game is ongoing
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
                if np.trace(arr[x:x + 4, y:y + 4]) == 4 or np.trace(np.flipud(arr[x:x + 4, y:y + 4])) == 4:
                    return 1
                elif np.trace(arr[x:x + 4, y:y + 4]) == -4 or np.trace(np.flipud(arr[x:x + 4, y:y + 4])) == -4:
                    return -1

        # draw
        if np.count_nonzero(game.board.state) == 42:
            return 0

        return None

    class Board:

        # constructor creates an empty board, red to move first
        def __init__(self):
            self.red = True
            self.state = np.zeros((7, 6))

        def setstate(self, state):
            self.state = state


class ReinforcementAI:

    # The Reinforcement AI is tethered to a game, and it has access to the dictionary of board states
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
                game_ = copy.deepcopy(self.game)
                next_boards[x] = game_.board.state.tobytes()
            else:
                next_boards[x] = None
        maxscore = float("-inf")
        minscore = float("inf")
        playcolreds = []
        playcolblacks = []
        for x in next_boards:
            # we check if the board state or its mirror state is in the dictionary
            # (mirror states are equivalently valued)
            if next_boards[x] is not None and (next_boards[x] in self.dict
                                               or np.flipud(np.frombuffer(next_boards[x]).reshape((7, 6))).tobytes() in self.dict):
                # if the state isn't in the dictionary, but its mirror image is, set the state to its mirror
                if next_boards[x] not in self.dict:
                    next_boards[x] = np.flipud(np.frombuffer(next_boards[x]).reshape((7, 6))).tobytes()
            else:
                self.dict[next_boards[x]] = 0  # if it is an unencountered state, initialize as 0 in the dictionary
            if maxscore <= self.dict[next_boards[x]]:  # look up the game state in dict to get its value
                maxscore = self.dict[next_boards[x]]
                playcolreds.append(x)
            if minscore >= self.dict[next_boards[x]]:
                minscore = self.dict[next_boards[x]]
                playcolblacks.append(x)
        if self.game.board.red == True:
            return maxscore, random.choice(playcolreds)
            # nextCol = playcolreds[-1]
            # if self.dict[next_boards[nextCol]] > self.dict[next_boards[playcolreds[-2]]]:
            #     return maxscore, nextCol
            # else:
            #     columns = [playcolreds[-2], nextCol]
            #     nextCol = random.choice(columns)
            #     return maxscore, nextCol
        else:
            return minscore, random.choice(playcolblacks)
            # nextCol = playcolblacks[-1]
            # print(self.dict[next_boards[nextCol]])
            # if self.dict[next_boards[nextCol]] < self.dict[next_boards[playcolblacks[-2]]]:
            #     return minscore, nextCol
            # else:
            #     columns = [playcolblacks[-2], nextCol]
            #     nextCol = random.choice(columns)
            #     return minscore, nextCol

class minimaxAI:

    # each minimaxAI is tethered to a game
    def __init__(self, game):
        self.game = game

    def generate_move_minimax(self):
        if self.game.board.red:
            return self.minimax(game, 3, True, float("-inf"), float("inf"))[1]
        else:
            return self.minimax(game, 3, False, float("-inf"), float("inf"))[1]

    """first output is the minimax score, second output is the column played to achieve that score"""
    def minimax(self, g, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or (g.winner() is not None):  # base case
            return g.evaluatestate(), g.lastcolplayed
        col = -1
        if maximizingPlayer:
            value = float("-inf")
            for i in range(7):
                g_ = copy.deepcopy(g)
                if g_.playable(i):
                    g_.play(i, False)
                    currval = self.minimax(g_, depth-1, False, alpha, beta)[0]
                    if value <= currval:
                        value = currval
                        col = i
                    alpha = max(alpha, currval)
                    if beta <= alpha:
                        break
            return value, col
        else:
            value = float("inf")
            for i in range(7):
                g_ = copy.deepcopy(g)
                if g_.playable(i):
                    g_.play(i, False)
                    currval = self.minimax(g_, depth - 1, True, alpha, beta)[0]
                    if value >= currval:
                        value = currval
                        col = i
                    beta = min(beta, currval)
                    if beta <= alpha:
                        break
            return value, col



if __name__ == "__main__":
    n = 100
    w = 0
    f = open("C:\\Users\\Pengfei\\Desktop\\C4dict.pickle", 'rb')
    dict = pickle.load(f)  # set the dictionary to what has been saved on file
    for z in range(n):
        game = Game()
        AI1 = ReinforcementAI(game, dict)  # player 1
        AI2 = minimaxAI(game)  # player 2
        while game.winner() is None:

            game.play(AI1.generate_move(), True)
            # print(game.board.state)
            # col = int(input('What column'))
            # if game.playable(col):
            #     game.play(col, True)
            # if game.winner() is None:
            #     game.play(reinforcementAI2.generate_move(), True)
            game.play(AI2.generate_move_minimax(), True)
            # print(game.board.state)

        if game.winner() == 1:
            w = w+1
            print("red won!")
            for h in game.history:
                if h in dict or np.flipud(np.frombuffer(h).reshape((7, 6))).tobytes() in dict:
                    if h not in dict:
                        h = np.flipud(np.frombuffer(h).reshape((7, 6))).tobytes()
                    dict[h] += 1
                else:
                    dict[h] = 1
        elif game.winner() == -1:  # black won
            print("black won!")
            for h in game.history:
                if h in dict or np.flipud(np.frombuffer(h).reshape((7, 6))).tobytes() in dict:
                    if h not in dict:
                        h = np.flipud(np.frombuffer(h).reshape((7, 6))).tobytes()
                    dict[h] += -1
                else:
                    dict[h] = -1
        elif game.winner() == 0:  # draw

            print("draw!")

        print(len(dict))
        f = open("C:\\Users\\Pengfei\\Desktop\\C4dict.pickle", 'wb')
        pickle.dump(dict, f)
        f.close()
    print(w / n)

















