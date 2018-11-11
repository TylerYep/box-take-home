import os
import const

def get_other_player(player):
    ''' Returns other player, lower or upper. '''
    return 'lower' if player == 'UPPER' else 'UPPER'

def get_coords(a1):
    ''' a1 is the move, given as a letter and a number. '''
    letter, number = a1
    x = ord(letter) - ord('a')
    y = int(number) - 1
    return x, y


def get_a1(x, y):
    ''' Converts an x,y coordinate into a1 format. '''
    a = chr(ord('a') + x)
    num = int(y) + 1
    if num <= 0 or num > const.BOARD_SIZE or \
        ord(a) < ord('a') or ord(a) >= ord('a') + const.BOARD_SIZE: return None
    return str(a) + str(num)


def in_bounds(a1):
    ''' Returns true if the given a1 coordinate is in bounds. Defaults true when a1 = None. '''
    if a1 is None: return False
    x, y = get_coords(a1)
    return x >= 0 and x < const.BOARD_SIZE and y >= 0 and y < const.BOARD_SIZE


def stringifyBoard(board):
    ''' Converts board to string. '''
    s = ''
    for row in range(len(board) - 1, -1, -1):
        s += '' + str(row + 1) + ' |'
        for col in range(0, len(board[row])):
            s += _stringifySquare(board[col][row])
        s += os.linesep
    s += '    a  b  c  d  e' + os.linesep
    return s


def _stringifySquare(sq):
    if type(sq) is not str or len(sq) > 2:
        raise ValueError('Board must be an array of strings like "", "P", or "+P"')

    if len(sq) == 0:
        return '__|'
    if len(sq) == 1:
        return ' ' + sq + '|'
    if len(sq) == 2:
        return sq + '|'


def parseTestCase(path):
    f = open(path)
    line = f.readline()
    initialBoardState = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initialBoardState.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upperCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lowerCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initialBoardState, upperCaptures=upperCaptures, lowerCaptures=lowerCaptures, moves=moves)
