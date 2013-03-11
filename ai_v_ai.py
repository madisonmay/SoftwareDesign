import tictactoe, ankur
import sys

def unpack(b):
    l = [1,2,3,4,5,6,7,8,9]
    for elem in b['x']: l.remove(elem)
    for elem in b['o']: l.remove(elem)
    return {' ':l,'x':b['x'],'o':b['o']}

def printboard(board):
    nboard = unpack(board)
    for j in range(3):
        for i in range(1+3*j,4+3*j):
            if i in nboard[' ']: sys.stdout.write('- ')
            if i in nboard['x']: sys.stdout.write('x ')
            if i in nboard['o']: sys.stdout.write('o ')
        print()
    print()


if __name__ == "__main__":
    board = {'X': [], 'O': []}
    for i in range(4):
        board = tictactoe.play(board, 'x')
        board = ankur.play(board, 'o')



