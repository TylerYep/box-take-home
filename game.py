import utils
import sys
import const
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral


def main():
    argc = len(sys.argv)
    if argc > 1 and sys.argv[1] == '-f':
        test_case = utils.parseTestCase('test/initialResponse.in')
        initial_pieces = test_case['initialPieces']
        upper_captures = test_case['upperCaptures']
        lower_captures = test_case['lowerCaptures']
        moves = test_case['moves']

        play_game(moves, initial_pieces)
    elif argc > 1 and sys.argv[1] == '-i':
        pass
    else:
        print('invalid command line arguments')


def get_piece(pz, pos):
    PIECE_MAP = dict({
        'k': King, 'b': Bishop,
        'g': GoldGeneral, 's': SilverGeneral,
        'r': Rook, 'p': Pawn
    })
    if len(pz) > 1:
        piece = PIECE_MAP[pz[1].lower()]
        return piece(pos, pz[1].islower(), True)

    piece = PIECE_MAP[pz.lower()]
    return piece(pos, pz.islower(), False)


def init_board(board, initial_pieces):
    for item in initial_pieces:
        piece = item['piece']
        pos = item['position']
        board.set_coord(get_piece(piece, pos))


def play_game(moves, initial_pieces):
    board = Board()
    init_board(board, initial_pieces)
    for move in moves:
        move_arr = move.split(' ')
        print(board)

        board.move_piece(move_arr[1], move_arr[2])

    print(board)


class Board:
    def __init__(self):
        self.board = [['__' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]

    def move_piece(self, pos1, pos2):
        pz = self.get_piece(pos1)
        assert pz is not None
        if pz.move(pos2):
            pz2 = self.get_piece(pos2)
            if pz2 is not '__':
                pass # TODO
            self.set_coord(pz, pos2)
            self.set_coord('__', pos1)
        else:
            print("Error moving piece")

    def get_piece(self, a1):
        if utils.in_bounds(a1):
            x, y = utils.get_coords(a1)
            if isinstance(self.board[x][y], Piece):
                return self.board[x][y]
            else:
                return '__'
        else:
            print("Not in bounds")


    def set_coord(self, piece, a1=None):
        if a1 is None:
            a1 = piece.position
        if utils.in_bounds(a1):
            x, y = utils.get_coords(a1)
            self.board[x][y] = piece
        else:
            print("SET COORD ERROR")

    def __repr__(self):
        ''' Used to distiguish Board objects for logging. '''
        str_board = [['' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                str_board[a][b] = str(self.board[a][b])
        return utils.stringifyBoard(str_board)



if __name__ == '__main__':
    main()
