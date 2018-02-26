import random
import math
import numpy

#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N,S,E,W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N,NE,E,SE,S,SW,W,NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}

########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################
class Node:
    def __init__(self, b, m=None, s=None):
        # self.name= tempname
        self.board = b
        self.children = []
        #self.player = p
        self.move= m
        self.score = s

    def __repr__(self):
        # return self.board
        return self.board

    def __lt__(self, other):
        return self.score<other.score


class Strategy():

    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        board= "?"*10+("?"+ "."*8+ "?")*8+ "?"*10
        board= self.replace_square(board, WHITE, 44)
        board =self.replace_square(board, WHITE, 55)
        board =self.replace_square(board, BLACK, 45)
        board =self.replace_square(board, BLACK, 54)

        return board

    def get_pretty_board(self, board): #checked
        """Get a string representation of the board."""
        values = [x for x in board]
        values = numpy.array(values).reshape(10, 10)
        return values

    def print_pretty_board(self, board): #checked
        board= self.get_pretty_board(board)
        for line in board:
            print("  ".join(line))

    def opponent(self, player): #checked
        """Get player's opponent."""
        if player==BLACK: return WHITE
        if player==WHITE: return BLACK

        return None

    def find_match(self, board, player, square, direction): #checked
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        counter_square= square
        opp=self.opponent(player)

        counter_square += direction
        while board[counter_square] is opp:
            counter_square += direction
            if board[counter_square] is player:
                return square
        return None

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        valid_moves= self.get_valid_moves(board, player)
        return move in valid_moves

    def replace_square(self, board, player, square):
        return board[:square]+player+board[square+1:]

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        assert self.is_move_valid(board, player, move) is True
        pairs=set()
        for dir in DIRECTIONS:
            m= self.find_match(board, player, move, dir)
            if m is not None and (m,dir) not in pairs:
                pairs.add((m, dir))
        print(pairs)
        assert(len(pairs)>0)
        for match in pairs:
            end, dir= match[0], match[1]
            square = move
            board = self.replace_square(board, player, square)
            while square is not end:
                square+= dir
                board=self.replace_square(board, player, square)
        #self.print_pretty_board(board)
        return board


    def pieces_on_board(self, board, player): #checked
        pieces=set()
        for x in range(11,89):
            if board[x]== player:
                pieces.add(x)
        return pieces

    def get_valid_moves(self, board, player): #checked
        """Get a list of all legal moves for player."""
        matches= []
        #for square in self.pieces_on_board(board, player):
        for square in [x for x in range(0,100) if board[x] is EMPTY]:
            for dir in DIRECTIONS:
                val = self.find_match(board, player, square, dir)
                if val is not None and val not in matches:
                    matches.append(val)

        return matches

    def has_any_valid_moves(self, board, player):
        return len(self.get_valid_moves(board, player))>0

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.has_any_valid_moves(board, self.opponent(prev_player)): return self.opponent(prev_player)
        if self.has_any_valid_moves(board, prev_player): return prev_player
        return None

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        return len(self.pieces_on_board(board, BLACK))- len(self.pieces_on_board(board, WHITE))

    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        return self.next_player(board, player) is None

    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################

    def minmax_search(self, node, player, depth=5):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        best={BLACK:max, WHITE: min}
        board= node.board
        if depth== 0:
            node.score= self.score(board, player)
            return node
        my_moves= self.get_valid_moves(board, player)
        children=[]
        if len(my_moves)<=0:
            print(player)
            print(my_moves)
        for move in my_moves:
            next_board= self.make_move(board, player, move)
            next_player= self.next_player(board, player)
            if next_player is None: #is winning board
                c= Node(next_board, move, s= 1000*self.score(next_board))
                children.append(c)
            else:
                c= Node(next_board, move)
                c.score = self.minmax_search(c, next_player, depth=depth-1).score
                children.append(c)
        winner = best[player](children)
        node.score= winner.score
        return winner

    def minmax_strategy(self, board, player, depth=5):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        return self.minmax_search(Node(board), player, 2).move
    
    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while(True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.random_strategy(board, player)
            depth += 1

    standard_strategy = minmax_strategy


###############################################
# The main game-playing code
# You can probably run this without modification
################################################
import time
from multiprocessing import Value, Process
import os, signal
silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.minmax_strategy, WHITE: white.minmax_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board)>0 else "White"))



#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():

    def __init__(self, time_limit = 5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        print("Playing Parallel Game")
        strategy = lambda who: self.black.random_strategy if who == BLACK else self.white.random_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent:print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))

if __name__ == "__main__":
    game =  ParallelPlayer(1)
    game = StandardPlayer()
    game.play()

    s = Strategy()
    b = s.get_starting_board()
    b = b[:35] + BLACK + b[36:]
    b = b[:45] + BLACK + b[46:]
    b = b[:55] + WHITE + b[56:]
    # s.print_pretty_board(b)
    # rint(s.find_match(b, WHITE, 55, N))

    sp = StandardPlayer()
    sp.play()
