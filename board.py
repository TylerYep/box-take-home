import utils
import const
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral

class Board:
    def __init__(self, initial_pieces, upper_captures = [], lower_captures = []):
        self.board = [['__' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]
        self.upper_captures = upper_captures
        self.lower_captures = lower_captures
        for item in initial_pieces:
            piece = item['piece']
            pos = item['position']
            self.set_coord(self.get_piece_from_map(piece, pos))

    def is_pos_in_check(a1, opposing_team):
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if piece.is_lower == opposing_team:
                    if a1 in piece.get_possible_moves(piece.position, piece.is_lower, piece.promoted):
                        return True
        return False

    def get_piece_from_map(self, pz, pos):
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

    def verify_player_turn(self, pz, player_turn):
        if player_turn is not None:
            if player_turn == 'lower':
                return pz.is_lower
            elif player_turn == 'UPPER':
                return not pz.is_lower
        return True

    def move_piece(self, pos1, pos2, player_turn, should_promote = False):
        pz = self.get_piece_at_pos(pos1)
        if pz is not '__' and pz.move(pos2):
            if not self.verify_player_turn(pz, player_turn):
                return False

            pz2 = self.get_piece_at_pos(pos2)

            if pz2 is not '__':
                if pz2.is_lower == pz.is_lower:
                    return False

                if player_turn == 'lower':
                    self.lower_captures.append(str(pz2)[1].lower())
                elif player_turn == 'UPPER':
                    self.upper_captures.append(str(pz2)[1].upper())

            self.set_coord(pz, pos2)
            self.set_coord('__', pos1)
            return True

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
