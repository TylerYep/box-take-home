import utils
import const
from copy import deepcopy
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral

def find_available_moves(board_obj, player_turn):
    ''' Searches for moves to get out of check. '''
    available_moves = []
    for a in range(const.BOARD_SIZE):
        for b in range(const.BOARD_SIZE):
            # Moves
            piece = board_obj.board[a][b]
            if isinstance(piece, Piece) and piece.team == player_turn:
                for move in piece.get_possible_moves(board_obj.board, piece.position, piece.team, piece.promoted):
                    move_str = 'move ' + piece.position + ' ' + move

                    if board_obj.can_move_piece(piece.position, move, player_turn, True):
                        if simulate_move(deepcopy(board_obj), piece, move, player_turn, True):
                            available_moves.append(move_str + ' promote')

                    if board_obj.can_move_piece(piece.position, move, player_turn, False):
                        if simulate_move(deepcopy(board_obj), piece, move, player_turn, False):
                            available_moves.append(move_str)
            # Drops
            elif piece == '__':
                captures = board_obj.upper_captures if player_turn == 'UPPER' else board_obj.lower_captures
                for pz in captures:
                    pos = utils.get_a1(a, b)
                    drop_str = 'drop ' + str(pz).lower() + ' ' + pos
                    if board_obj.can_drop_piece(player_turn, pz, pos):
                        if simulate_drop(deepcopy(board_obj), player_turn, pz, pos):
                            available_moves.append(drop_str)
    return sorted(available_moves)

def simulate_drop(board_obj, player_turn, pz, move):
    ''' Must pass in a deepcopy of board_obj '''
    board_obj.drop_piece(player_turn, pz, move)
    return not board_obj.king_in_check(player_turn)


def simulate_move(board_obj, pz, move, player_turn, should_promote):
    ''' Must pass in a deepcopy of board_obj '''
    board_obj.move_piece(pz.position, move, player_turn, should_promote)
    return not board_obj.king_in_check(player_turn)

class Board:
    def __init__(self, initial_pieces, upper_captures = [], lower_captures = []):
        self.board = [['__' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]
        self.upper_captures = upper_captures
        self.lower_captures = lower_captures
        for item in initial_pieces:
            piece = item['piece']
            pos = item['position']
            self.set_coord(self.get_piece_from_map(piece, pos))

    def king_in_check(self, player_turn):
        ''' Returns True is player's King is currently in check. '''
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if isinstance(piece, King) and piece.team == player_turn:
                    if self.pos_in_check(utils.get_a1(a, b), player_turn):
                        return True
        return False

    def pos_in_check(self, a1, player_turn):
        ''' Returns True is a given position is in check (aka can be taken by an opponent's piece). '''
        opposing_team = 'lower' if player_turn == 'UPPER' else 'UPPER'
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if isinstance(piece, Piece) and piece.team == opposing_team:
                    if a1 in piece.get_possible_moves(self.board, piece.position, piece.team, piece.promoted):
                        return True
        return False

    def get_piece_from_map(self, pz, pos):
        ''' Returns constructor for a piece object. '''
        if len(pz) > 1:
            piece = const.PIECE_MAP[pz[1].lower()]
            return piece(pos, 'lower' if pz[1].islower() else 'UPPER', True)
        piece = const.PIECE_MAP[pz.lower()]
        return piece(pos, 'lower' if pz.islower() else 'UPPER', False)

    def verify_player_turn(self, pz, player_turn):
        ''' Returns True if the piece belongs to the given player. '''
        if player_turn is not None:
            return player_turn == pz.team
        return True

    def should_promote_pawn(self, pz, player_turn, pos2):
        return isinstance(pz, Pawn) and ((player_turn == 'UPPER' and utils.get_coords(pos2)[1] == 0) or \
                (player_turn == 'lower' and utils.get_coords(pos2)[1] == const.BOARD_SIZE - 1))

    def move_piece(self, pos1, pos2, player_turn, should_promote = False):
        '''
        Expects a valid move.
        - Updates board.captures
        - Updates board positions
        '''
        pz = self.get_piece_at_pos(pos1)
        if should_promote or self.should_promote_pawn(pz, player_turn, pos2):
            pz.promoted = True
        pz2 = self.get_piece_at_pos(pos2)
        if pz2 is not '__':
            if player_turn == 'lower':
                self.lower_captures.append(str(pz2)[1].lower())
            elif player_turn == 'UPPER':
                self.upper_captures.append(str(pz2)[1].upper())

        pz.position = pos2
        self.set_coord(pz, pos2)
        self.set_coord('__', pos1)

    def can_move_piece(self, pos1, pos2, player_turn, should_promote = False):
        ''' Return True if move is valid.
            Verifies:
            - Correct player's turn,
            - Promotion is valid (especailly for pawns)
            - Piece is on last row to be promoted
        '''
        pz = self.get_piece_at_pos(pos1)
        if pz is not '__' and pz.can_move(self.board, pos2):
            if not self.verify_player_turn(pz, player_turn):
                return False

            if isinstance(pz, King) and self.pos_in_check(pos2, player_turn):
                return False

            if should_promote or self.should_promote_pawn(pz, player_turn, pos2):
                if pz.promoted or isinstance(pz, King) or isinstance(pz, GoldGeneral):
                    return False

                if not((player_turn == 'UPPER' and utils.get_coords(pos2)[1] == 0) or \
                    (player_turn == 'lower' and utils.get_coords(pos2)[1] == const.BOARD_SIZE - 1) or \
                    (player_turn == 'UPPER' and utils.get_coords(pos1)[1] == 0) or \
                    (player_turn == 'lower' and utils.get_coords(pos1)[1] == const.BOARD_SIZE - 1)):
                    return False

            pz2 = self.get_piece_at_pos(pos2)
            if pz2 is not '__' and pz2.team == pz.team:
                return False

            return True

        return False

    def can_drop_piece(self, player_turn, piece, pos):
        ''' Return True if drop is possible. '''
        piece_name = str(piece)
        if len(piece_name) > 1:
            piece_name = piece_name[1]

        # Cannot place Pawn in promotion zone or in same row as another Pawn.
        if piece_name.lower() == 'p':
            if ((player_turn == 'UPPER' and utils.get_coords(pos)[1] == 0) or \
                (player_turn == 'lower' and utils.get_coords(pos)[1] == const.BOARD_SIZE - 1)):
                return False

            x, y = utils.get_coords(pos)
            for j in range(const.BOARD_SIZE):
                if isinstance(self.board[x][j], Pawn) and self.board[x][j].team == player_turn:
                    return False

            board_obj = deepcopy(self)
            board_obj.drop_piece(player_turn, piece_name, pos)
            other_player = utils.get_other_player(player_turn)
            if board_obj.king_in_check(other_player) and not find_available_moves(board_obj, other_player):
                return False

        # Only drop pieces in empty spaces
        if self.get_piece_at_pos(pos) == '__':
            if player_turn == 'UPPER':
                for i in range(len(self.upper_captures)):
                    if self.upper_captures[i].lower() == piece_name.lower():
                        return True

            elif player_turn == 'lower':
                for i in range(len(self.lower_captures)):
                    if self.lower_captures[i] == piece_name:
                        return True
        return False

    def drop_piece(self, player_turn, piece, pos):
        ''' Drops piece in specified location. Assumes location is valid. '''
        piece_name = str(piece)
        if len(piece_name) > 1:
            piece_name = piece_name[1]

        new_piece = const.PIECE_MAP[piece_name.lower()](pos, player_turn)
        self.set_coord(new_piece, pos)

        if player_turn == 'UPPER':
            for i in range(len(self.upper_captures)):
                if self.upper_captures[i].lower() == piece_name.lower():
                    del self.upper_captures[i]
                    break
        else:
            for i in range(len(self.lower_captures)):
                if self.lower_captures[i] == piece_name:
                    del self.lower_captures[i]
                    break

    def get_piece_at_pos(self, a1):
        ''' Returns piece object at an a1 location. '''
        if utils.in_bounds(a1):
            x, y = utils.get_coords(a1)
            if isinstance(self.board[x][y], Piece):
                return self.board[x][y]
            else:
                return '__'
        else:
            print("Coordinate not in bounds.")
            return False

    def set_coord(self, piece, a1=None):
        ''' Sets coordinate of a piece. If a1 is None, defaults to piece.position. '''
        if a1 is None:
            a1 = piece.position
        if utils.in_bounds(a1):
            x, y = utils.get_coords(a1)
            self.board[x][y] = piece
        else:
            print("Error setting coordinate.")

    def __repr__(self):
        ''' Used to distiguish Board objects for logging. '''
        str_board = [['' for _ in range(const.BOARD_SIZE)] for _ in range(const.BOARD_SIZE)]
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                str_board[a][b] = str(self.board[a][b])
        return utils.stringifyBoard(str_board)
