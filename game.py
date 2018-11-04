import utils
import sys
import const
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral


def main():
    argc = len(sys.argv)
    if argc > 1 and sys.argv[1] == '-f':
        file_name = 'test/initialResponse.in' # = sys.argv[2]
        test_case = utils.parseTestCase(file_name)
        initial_pieces = test_case['initialPieces']
        upper_captures = test_case['upperCaptures']
        lower_captures = test_case['lowerCaptures']
        moves = test_case['moves']

        play_game(initial_pieces, moves)
    elif argc > 1 and sys.argv[1] == '-i':
        test_case = utils.parseTestCase('test/initialMove.in')
        initial_pieces = test_case['initialPieces']
        play_game(initial_pieces, [], True)
    else:
        print('invalid command line arguments')


def init_board(board, initial_pieces):
    for item in initial_pieces:
        piece = item['piece']
        pos = item['position']
        board.set_coord(get_piece(piece, pos))


def play_game(initial_pieces, moves, is_interactive = False):
    board = Board()
    init_board(board, initial_pieces)
    for move in moves:
        move_arr = move.split(' ')
        print(board)
        board.move_piece(move_arr[1], move_arr[2])

    if is_interactive:
        turns = 0
        player_turn = 'lower'
        while turns < const.MAX_MOVES:
            print(board)
            print('Captures UPPER: ', end='')
            for cap in board.upper_captures:
                print(cap, end=' ')
            print('')

            print('Captures lower: ', end='')
            for cap in board.lower_captures:
                print(cap, end=' ')
            print('\n')
            print('>' + player_turn + ': ', end = '')
            move = input()
            print(player_turn + ' player action: ' + move)
            move_arr = move.split(' ')
            valid_move = board.move_piece(move_arr[1], move_arr[2], player_turn)
            if not valid_move:
                print(player_turn + ' player wins. Illegal move.')
                break

            if player_turn == 'lower':
                player_turn = 'UPPER'
            else:
                player_turn = 'lower'


class Board:
    def __init__(self, upper_captures = [], lower_captures = []):
        self.board = [['__' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]
        self.upper_captures = upper_captures
        self.lower_captures = lower_captures

    def verify_player_turn(self, pz, player_turn):
        if player_turn is not None:
            if player_turn == 'lower':
                return pz.is_lower
            elif player_turn == 'UPPER':
                return not pz.is_lower
        return True

    def move_piece(self, pos1, pos2, player_turn = None):
        pz = self.get_piece_at_pos(pos1)
        assert pz is not '__'

        if not self.verify_player_turn(pz, player_turn):
            return False

        if pz.move(pos2):
            pz2 = self.get_piece_at_pos(pos2)
            if pz2 is not '__':
                pass # TODO
            self.set_coord(pz, pos2)
            self.set_coord('__', pos1)
            return True

        print("Error moving piece")
        return False

    def get_piece_at_pos(self, a1):
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


if __name__ == '__main__':
    main()
