# ConnectFour-Reinforcement-Learning-AI

While the minimax algorithm for an AI Connect Four player literally examines future board states in order to determine its next move, another approach is to use
the board histories of past games as an indicator for the player's success in the current game. We may store these board histories as a 
dictionary where the keys are 7 by 6 numpy arrays (in byte format) that represent the board and the values are numerical scores that denote how correlated that board state is to
the maximizing player (w/l/o/g assume red) winning the game. As the number of games that we take into account grows, the dictionary will get bigger and become a better predictor of the outcome of the game given a board state.

With the dictionary, all that remains to be done is to select the column that produces the best board state for the AI player. I chose python primarily because of pickling being far superior to equivalents in Java for storing and reading objects from a file.

I am currently building the dictionary by playing two AIs against each other hundreds of thousands of times. Once I am done preliminary testing, I will add functionality that supports interactive Human vs AI games
