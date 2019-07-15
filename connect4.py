import numpy as np
import matplotlib.pyplot as plt
import pickle
from sets import set
import random


'''
in this implementation of connect four, we represent the state of the board as
a 7 by 6 numpy array (game), where red tiles are represented by 1, yellow tiles by -1, and empty tiles by 0.
'''


class Game:

    def __init__(self, history=Set([])):
        self.history = history
        self.board = self.Board()

    def getboard(self):
        return self.board

    def updatehistory(self):
        self.history.add(self.board.state)

    # plays the corresponding chip (determined by the boolean redTurn)
    # in the corresponding column (col), and it adds that board to the game history accordingly

    def play(col, realmove):
        for i in range(6):
            if self.board.state[col][i]==0:
                if self.red:
                    self.board.state[col][i] = 1
                    self.red = False
                else:
                    self.board.state[col][i] = -1
                    self.red = True
                if realmove:
                    self.updatehistory()
                break
        return False

    class Board:

        # constructor creates an empty board
        def __init__(self, red=true, state=np.zeros((7, 6))):
            self.red = red  # boolean denoting red starts
            self.state = state





def newgame() :
    f = open("C:\\Users\\Pengfei\\Desktop\\C4dict.pickle", 'rb')
    dict = pickle.load(f) #set the dictionary to what has been saved
    game = Game()




'''this method is used for finding the next possible boardstates of a given boardstate '''
def playCol(game, col, redTurn):
    for i in range(6):
        if game[col][i]==0:
            if redTurn:
                game[col][i]=1
                redTurn = False
            else:
                game[col][i] = -1
                redTurn = True
        break
    return game


#determines if the given column is playable (not full)
def playable(game, col):

    for i in range(6):
        if game[col][i]==0:
            return True;
    return False;

#retuns whether the game is over as its first output
#and if so, returns the winner (1, -1)

def winner(game):

    #hcheck
    for x in range(4):
        for y in range(6):
            if game[x:x+4,y].sum()==4:
                return 1
            elif game[x:x+4,y].sum()==-4:
                return -1

    #vcheck
    for x in range(7):
        for y in range(3):
            if game[x, y:y+4].sum() == 4:
                return 1
            elif game[x, y:y+4].sum() == -4:
                return -1

    #rdcheck
    for x in range(4):
        for y in range(3):
            if np.trace(game[x:x+4, y:y+4])==4 or np.trace(np.fliplr(game[x:x+4, y:y+4]))==4:
                return 1
            elif np.trace(game[x:x+4, y:y+4])==-4 or np.trace(np.fliplr(game[x:x+4, y:y+4]))==-4:
                return -1

    if np.count_nonzero(game)==42:
        return 0

    return None

'''returns a column (0-6) as next move'''
def generate_move(game, dict, redTurn):
    next_boards = []
    for x in range(7):
        if playable(game, x):
            next_boards.append(play(game, col, ))





        columns = [0, 1, 2, 3, 4, 5, 6]
        checker = False
        while checker == False:
            nextCol=random.choice(columns)
            if playable(game, nextCol):
                checker = True
        return




'''A boardstate is deemed to be positive if it was played in a game that black ended up winning'''
def endgame(game, history, dict):
    if winner(game) != None:  # game is over
        if winner(game) == 1:  # red won
            for h in history:
                if h in dict:
                    dict[h] += -1
                else:
                    dict[h] = -1
        elif winner(game) == -1:  # black won
            for h in history:
                if h in dict:
                    dict[h] += 1
                else:
                    dict[h] = 1
        elif winner(game) == 0:  # draw
            for h in history:
                if h in dict:
                    dict[h] += -.1
                else:
                    dict[h] = -.1
    f = open('C:\\Users\\Pengfei\\Desktop\\C4dict.pickle', 'wb')
    pickle.dump(dict, f)
    f.close()





if __name__ == "__main__":
    game = newgame()[0]
    dict = newgame()[1]













