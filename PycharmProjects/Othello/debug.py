import random
import math
import numpy

#### Othello Shell
#### P. White 2016-2018
# Sophia Wang's code 2/9/18


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N + E, S + E, N + W, S + W
DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)
OPP_DIRECTIONS = {N: S, S: N, E: W, W: E, SE: NW, NW: SE, SW: NE, NE: SW}
PLAYERS = {BLACK: "Black", WHITE: "White"}
CORNERS = [11, 18, 81, 88]
CORNER_DIRECTIONS = {11: (E, S, SE), 18: (W, S, SW), 81: (N, E, NE), 88: (N, W, NW)}


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
        # self.player = p
        self.move = m
        self.score = s

    def __repr__(self):
        # return self.board
        return self.board

    def __lt__(self, other):
        return self.score < other.score


class Strategy():
    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        board = "?" * 10 + ("?" + "." * 8 + "?") * 8 + "?" * 10
        board = self.replace_square(board, WHITE, 44)
        board = self.replace_square(board, WHITE, 55)
        board = self.replace_square(board, BLACK, 45)
        board = self.replace_square(board, BLACK, 54)

        return board

    def get_pretty_board(self, board):  # checked
        """Get a string representation of the board."""
        values = [x for x in board]
        values = numpy.array(values).reshape(10, 10)
        return values

    def print_pretty_board(self, board):  # checked
        board = self.get_pretty_board(board)
        for line in board:
            print("  ".join(line))

    def opponent(self, player):
        """Get player's opponent."""
        if player is BLACK: return WHITE
        if player is WHITE: return BLACK
        return None

    def find_match(self, board, player, square, direction):  # checked
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        position = square + direction
        opp = self.opponent(player)
        assert opp is not None
        while position in range(11, 89) and board[position] is opp:
            position = position + direction
            if board[position] == player:
                return position
        return None

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        pass

    def replace_square(self, board, player, square):
        return board[:square] + player + board[square + 1:]

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        for dir in DIRECTIONS:
            match = self.find_match(board, player, move, dir)
            if match is not None:
                for x in range(move, match, dir):
                    board = self.replace_square(board, player, x)

        return board

    def pieces_on_board(self, board, player):
        return [x for x in range(11, 89) if board[x] is player]

    def remove_corners(self, moves, corner):
        if corner in moves and len(moves) > 1:
            moves.remove(corner)
        return moves

    def get_valid_moves(self, board, player):  # checked
        """Get a list of all legal moves for player."""
        moves = []

        for square in [x for x in range(11, 89) if board[x] is EMPTY]:
            # if square==11: topleft= 1
            # if square==19: topright= 2
            # if square==81: bottomleft= 3
            # if square==91: bottomright= 4
            for dir in DIRECTIONS:
                if board[square + dir] == self.opponent(player):
                    match = self.find_match(board, player, square, dir)
                    if match is not None and square not in moves:
                        moves.append(square)
        # squarecorners = {topleft: [12, 14], topright: [18, 29], bottomleft: [71, 82], bottomright: [88, 79]}

        for c in [22, 28, 72, 77]:  # diagonal corners
            self.remove_corners(moves, c)
        # for x in [topleft, topright, bottomleft, bottomright]:
        #     if type(x)==int:
        #         for m in squarecorners[x]:
        #             self.remove_corners(moves, m)
        # for c in [12,14,18,29,71,82,88,79]:
        #    self.remove_corners(moves,c)
        return moves

    def has_any_valid_moves(self, board, player):
        return len(self.get_valid_moves(board, player)) > 0

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = self.opponent(prev_player)
        if self.has_any_valid_moves(board, opp): return opp
        if self.has_any_valid_moves(board, prev_player): return prev_player
        return None

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        return len(self.pieces_on_board(board, BLACK)) - len(self.pieces_on_board(board, WHITE))

    def stability(self, board, move, player, status, prev_move,
                  prev_player):  #rewards how many levels it stays the same color
        pass


    def mob_stability_weighted_score(self, board, player=BLACK, prev_move=None, prev_player=BLACK):
        matrix = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 120, -30, 20, 5, 5, 20, -30, 120, 0,
            0, -30, -80, -5, -5, -5, -5, -80, -30, 0,
            0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
            0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
            0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
            0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
            0, -30, -80, -5, -5, -5, -5, -80, -30, 0,
            0, 120, -30, 20, 5, 5, 20, -30, 120, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        score = 0
        board_pieces = [x for x in range(11, 89) if board[x] is not EMPTY]
        for corner in CORNERS:
            for dir in CORNER_DIRECTIONS:
                if board[corner] is BLACK:
                    matrix[corner] = 10
                    corner += dir
        for b in board_pieces:
            if board[b] is BLACK:
                score += self.stability(board, b, BLACK)
                score += matrix[b]
            else:
                score -= self.stability(board, b, WHITE)
                score -= matrix[b]

        return score

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
    def alphabeta_search(self, node, player, alpha, beta, depth, prev_move=None):
        best = {BLACK: max, WHITE: min}
        board = node.board
        if depth == 0:
            node.score = self.mob_stability_weighted_score(board, prev_move)
            return node
        my_moves = self.get_valid_moves(board, player)
        children = []

        for corner in CORNERS:
            if corner in my_moves:
                next_board = self.make_move(board, player, corner)
                next_player = self.next_player(next_board, player)
                if next_player is None:  # is winning board
                    c = Node(next_board, corner, s=1000 * self.score(next_board))
                    children.append(c)
                else:
                    c = Node(next_board, corner)
                    c.score = self.alphabeta_search(c, next_player, alpha, beta, depth=depth - 1).score
                    children.append(c)
        if len(children) > 0:
            winner = best[player](children)
            node.score = winner.score
            return winner

        for move in my_moves:
            next_board = self.make_move(board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:  # is winning board
                c = Node(next_board, move, s=1000 * self.score(next_board))
                children.append(c)
            else:
                c = Node(next_board, move)
                c.score = self.alphabeta_search(c, next_player, alpha, beta, depth=depth - 1).score
                children.append(c)
            if player is BLACK:
                alpha = max(alpha, c.score)
            if player is WHITE:
                beta = min(beta, c.score)
            if alpha >= beta:
                break
        winner = best[player](children)
        node.score = winner.score
        return winner

    def alphabeta_strategy(self, board, player, depth=3):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move

        move = self.alphabeta_search(Node(board), player, -1000000, 1000000, depth=1).move
        return move

    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while (True):
            board = "".join(board)
            best_move.value = self.alphabeta_strategy(board, player)
            depth += 1

    standard_strategy = alphabeta_strategy


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
        strategy = {BLACK: black.standard_strategy, WHITE: white.minmax_strategy}
        print(ref.get_pretty_board(board))
        tic = time.clock()
        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)
        toc = time.clock()
        print("Time %i" % (toc - tic))
        print(strategy)
        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))




if __name__ == "__main__":
    game = ParallelPlayer(1)
    game = StandardPlayer()
    # game.play()
    s = Strategy()
    b = s.get_starting_board()
    b = b[:35] + BLACK + b[36:]
    b = b[:45] + BLACK + b[46:]
    b = b[:55] + WHITE + b[56:]
    # s.print_pretty_board(b)
    # rint(s.find_match(b, WHITE, 55, N))
    sp = StandardPlayer()
    sp.play()
