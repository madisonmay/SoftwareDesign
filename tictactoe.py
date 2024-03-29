import random
import os
from copy import deepcopy
import itertools


"""Note that this implementation of tic-tac-toe takes a performance hit because of deepcopy,
and should probably be optimized to only use inplace methods as opposed to return copies of objects.
For normal gameplay, this isn't a concern.

Also, code may be unnecessarily complex because of my choice to try OOP for this problem"""

class Board():
    """
    Board representation: arranged to map to numpad

         |     |
      7  |  8  |  9
    _____|_____|_____
         |     |
      4  |  5  |  6
    _____|_____|_____
         |     |
      1  |  2  |  3
         |     |
    """
    def __init__(self, board=False):
        if board:
            self.board = board
        else:
            self.board =  [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def printBoard(self):
        """Composes board and prints"""
        empty_row = " "*5+"|" + " "*5 + "|" + " "*5
        bottom_row = "_"*5+"|" + "_"*5 + "|" + "_"*5
        board = self.board

        def data_row(row):
            return "  %s  |  %s  |  %s  " %(row[0], row[1], row[2])

        os.system('clear')
        for row in board[:-1]:
            print(empty_row)
            print(data_row(row))
            print(bottom_row)
        print(empty_row)
        print(data_row(board[-1]))
        print(empty_row)
        print('')


    def fill(self, position, symbol):
        """Fill a position on the board"""
        self.board[2 - (position - 1) // 3][(position - 1) % 3] = symbol

    def filled(self, position, symbol):
        """Return new board with position filled"""
        board = Board(deepcopy(self.board))
        board.board[2 - (position - 1) // 3][(position - 1) % 3] = symbol
        return board

    def position(self, position):
        """Converts from input to board position"""
        return self.board[2 - (position - 1) // 3][(position - 1) % 3]

    def open_positions(self):
        """Returns a list of open positions"""
        res = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    res.append((2-i)*3 + j + 1)
        return res

    def rearranged(self, b):
        """Converts the two diagonals into rows"""
        return [[b[0][0], b[1][1], b[2][2]], [b[0][2], b[1][1], b[2][0]]]


    def rows(self):
        """Return rows, columns, and diagonals in row format"""
        rows = []
        for row in self.board:
            rows.append(row)
        for col in zip(*self.board):
            rows.append(col)
        for diagonal in self.rearranged(self.board):
            rows.append(diagonal)
        return rows

    def win(self):
        """Checks to see if any win condition has been fulfilled"""
        for row in self.rows():
            if (len(set([e for e in row])) == 1 and row[0] != ' '):
                return True
        return False

    def tie(self):
        """Checks for the presence of unfilled boxes"""
        for row in self.board:
            for element in row:
                if element == ' ':
                    return False
        if not (self.win()):
            return True
        return False

    def successors(self, symbol):
        """Generates a list of successors to a state"""
        l = []
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] == ' ' and not self.game_over()):
                    board = Board(deepcopy(self.board))
                    board.board[i][j] = symbol
                    l.append(board)
        return l

    def win_count(self, player_symbol):
        """Counts number of plays that would produce a win"""
        count = 0
        for s in self.successors(player_symbol):
            if s.win():
                count += 1
        return count

    def first_move(self, player_symbol):
        """Play in the corner if possible"""
        empty = True
        for row in self.board:
            for element in row:
                if element != ' ':
                    empty = False
        if empty:
            board = Board(deepcopy(self.board))
            board.board[0][0] = player_symbol
            return board

        return False


    def can_win(self, player_symbol):
        """Checks to see if player can win"""
        for s in self.successors(player_symbol):
            if s.win():
                return s
        return False

    def can_lose(self, player_symbol):
        """Checks to see if player will lose if a certain move is not made"""
        symbols = ['O', 'X']
        for s in symbols:
            if s != player_symbol:
                opponent_symbol = s

        opponent_moves = self.successors(opponent_symbol)
        moves = self.successors(player_symbol)
        for i in range(len(opponent_moves)):
            if opponent_moves[i].win():
                return moves[i]

        return False

    def fork(self, player_symbol):
        """Checks for fork possibilities"""
        symbols = ['O', 'X']
        for s in symbols:
            if s != player_symbol:
                opponent_symbol = s

        for state in self.successors(player_symbol):
            if state.win_count(player_symbol) >= 2:
                return state
        return False

    def block_fork(self, player_symbol):
        """If possible, blocks an opponents fork"""
        symbols = ['O', 'X']
        for s in symbols:
            if s != player_symbol:
                opponent_symbol = s

        opponent_moves = self.successors(opponent_symbol)
        moves = self.successors(player_symbol)


        #force an opponent to block
        for i in range(len(opponent_moves)):
            if opponent_moves[i].win_count(opponent_symbol) >= 2:
                for i in range(len(moves)):
                    if moves[i].win_count(player_symbol) >= 1:
                        block_attempt = moves[i].can_lose(opponent_symbol)
                        if block_attempt.win_count(opponent_symbol) <= 1:
                            return moves[i]

        #play where they would move to create a fork
        for i in range(len(opponent_moves)):
            if opponent_moves[i].win_count(opponent_symbol) >= 2:
                return moves[i]

        return False

    def center(self, player_symbol):
        """If the center is open, play in that space"""
        for s in self.successors(player_symbol):
            if s.board[1][1] == player_symbol:
                return s
        return False

    def opposite_corner(self, player_symbol):
        """If a corner is open opposite the other players piece, play there."""
        symbols = ['O', 'X']
        for s in symbols:
            if s != player_symbol:
                opponent_symbol = s

        corner_index = [0, 2]
        for position in itertools.permutations(corner_index):
            if self.board[position[0]][position[1]] == opponent_symbol:
                if self.board[position[1]][position[0]] == ' ':
                    board = Board(deepcopy(self.board))
                    board.board[position[1]][position[0]] = player_symbol
                    return board
        return False

    def corner(self, player_symbol):
        """Play in a corner if open"""
        symbols = ['O', 'X']
        for s in symbols:
            if s != player_symbol:
                opponent_symbol = s

        corner_index = [0, 2]
        for position in itertools.permutations(corner_index):
            if self.board[position[0]][position[1]] == ' ':
                board = Board(deepcopy(self.board))
                board.board[position[0]][position[1]] = player_symbol
                return board
        return False

    def game_over(self):
        """Checks for any fulfilled end_game conditions"""
        return self.tie() or self.win()

    def out(self):
        """Conversion for playing other ai"""
        d = {'x': [], 'o': []}
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != ' ':
                    d[self.board[i][j].lower()].append(i*3 + j + 1)
        return d

    def data_in(self, board):
        """Conversion for playing other ai"""
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        for k in board.keys():
            for v in board[k]:
                self.board[(v-1)//3][(v-1)%3] = k.upper()
        self.printBoard()

    def ai_move(self, player):
        """AI Move Method"""
        first_move = self.first_move(player.symbol)
        win = self.can_win(player.symbol)
        lose = self.can_lose(player.symbol)
        fork = self.fork(player.symbol)
        block_fork = self.block_fork(player.symbol)
        center = self.center(player.symbol)
        opposite_corner = self.opposite_corner(player.symbol)
        corner = self.corner(player.symbol)
        if first_move: return first_move
        elif win: return win
        elif lose: return lose
        elif fork: return fork
        elif block_fork: return block_fork
        elif center: return center
        elif opposite_corner: return opposite_corner
        elif corner: return corner
        else:
            position = random.choice(self.open_positions())
            return self.filled(position, player.symbol)

class Player():
    """Player class"""
    def __init__(self, name, symbol, monkey=False, ai=False):
        self.name = name
        self.symbol = symbol.upper()
        self.monkey = monkey
        self.ai = ai


class TicTacToe():
    """Game class"""
    def __init__(self, players):
        """Takes a list of players as its only argument"""
        self.board = Board();
        symbols = ['O', 'X']
        player_list = []
        for i in range(2):
            if players[i].lower() == "monkey":
                player_list.append(Player(players[i], symbols[i], monkey=True))
            elif players[i].lower() == "ai":
                player_list.append(Player(players[i], symbols[i], ai=True))
                # self.tree = self.gen_tree()
            else:
                player_list.append(Player(players[i], symbols[i]))
        self.players = player_list

    def game_over(self):
        """Ends the game"""
        return self.board.game_over()

    def move(self, player):
        """Handles moves for all player types"""

        """Player Type Monkey"""
        if player.monkey:
            position = random.choice(self.open_positions())
            self.board.fill(position, player.symbol)

        elif player.ai:
            self.board = self.board.ai_move(player)

        else:

            try:
                position = int(input("\nWhere do you want to move, %s? Use the numpad to select a position.\n" % (player.name)).strip())
                if 1 <= position <= 9:
                    if self.board.position(position) == ' ':
                        self.board.fill(position, player.symbol)
                    else:
                        self.printBoard()
                        print("That location has already been filled.  Try a different location...")
                        self.move(player)

            except:
                self.printBoard()
                print("Please enter a number between 1 and 9")
                self.move(player)
        self.printBoard()


    def open_positions(self):
        """Returns a list of open positions in the game"""
        return self.board.open_positions()

    def printBoard(self):
        """Prints the game board"""
        self.board.printBoard()

    def start(self):
        """Main game loop"""
        player_num = random.randint(0, 1)
        while not self.game_over():
            player = self.players[player_num]
            self.move(player)
            player_num = 1 - player_num
        player_num = 1 - player_num
        self.end(player_num)

    def end(self, player_num):
        """Executed upon game end condition"""
        self.printBoard()
        if not self.board.tie():
            print('%s wins!' % (self.players[player_num].name))
            if self.players[player_num].name == "AI":
                try:
                    global wins
                    wins += 1
                except:
                    pass
        else:
            try:
                print("It's a tie!")
                global ties
                ties += 1
            except:
                pass


def play(board_in, you):
    """Play method for competing against other ai's"""
    new_board = Board()
    new_board.data_in(board_in)
    new_board.printBoard();
    player = Player('Madison', you, ai=True)
    print(new_board.board)
    print('Before')
    new_board = new_board.ai_move(player)
    print(new_board.board)
    print('After')
    return new_board.out()

if __name__ == '__main__':
    game = TicTacToe(['AI', 'Madison'])
    game.start()
    # """Code for testing AI"""
    # ties = 0
    # wins = 0
    # for i in range(100):
    #     """Specifying 'Monkey' will yield a random player, 'AI' will yield a computer player,
    #     and any other string will create a human player"""
    #     game = TicTacToe(['AI', 'Monkey'])
    #     game.start()
    # os.system('clear')
    # print("Wins: " + str(wins) + "/" + str(i+1))
    # print("Ties: " + str(ties) + "/" + str(i+1))
    # print("Losses: " + str(i+1-wins-ties) + "/" + str(i+1))

