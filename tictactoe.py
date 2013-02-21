class Board():
    """Board representation"""
    def __init__(self):
        self.board = [[' '] * 3, [' '] * 3, [' '] * 3]

    def printBoard(self):
        for i in range(3):
            print self.board[i]
        print

    def fill(self, position, symbol):
        self.board[2 - (position - 1) / 3][(position - 1) % 3] = symbol

if __name__ == '__main__':
    board = Board()
    board.printBoard()
    board.fill(9, 'x')
    board.printBoard()
