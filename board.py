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

    def king_in_check(self, player_turn):
        ''' Returns False is player is not in check. '''
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if isinstance(piece, King) and piece.team == player_turn:
                    if self.pos_in_check(utils.get_a1(a, b), player_turn):
                        return True
        return False

    def find_available_moves(self, player_turn):
        available_moves = []
        # Moves
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if isinstance(piece, Piece) and piece.team == player_turn:
                    pass
                    # for move in get_all_moves(): # TODO
                    # simulate_move()
                    #     if not self.pos_in_check(a1, player_turn):
                    #         available_moves.append(move)
        # Drops

        return available_moves

    def pos_in_check(self, a1, player_turn):
        opposing_team = 'lower' if player_turn == 'UPPER' else 'UPPER'
        for a in range(const.BOARD_SIZE):
            for b in range(const.BOARD_SIZE):
                piece = self.board[a][b]
                if isinstance(piece, Piece) and piece.team == opposing_team:
                    if a1 in piece.get_possible_moves(self.board, piece.position, piece.team, piece.promoted):
                        return True
        return False

    def get_piece_from_map(self, pz, pos):
        if len(pz) > 1:
            piece = const.PIECE_MAP[pz[1].lower()]
            return piece(pos, 'lower' if pz[1].islower() else 'UPPER', True)

        piece = const.PIECE_MAP[pz.lower()]
        return piece(pos, 'lower' if pz.islower() else 'UPPER', False)

    def verify_player_turn(self, pz, player_turn):
        if player_turn is not None:
            return player_turn == pz.team
        return True

    def move_piece(self, pos1, pos2, player_turn, should_promote = False):
        ''' Return True if move was successful '''
        pz = self.get_piece_at_pos(pos1)
        if isinstance(pz, Pawn) and ((player_turn == 'UPPER' and utils.get_coords(pos2)[1] == 0) or \
            (player_turn == 'lower' and utils.get_coords(pos2)[1] == const.BOARD_SIZE - 1)):
            should_promote = True

        if pz is not '__' and pz.move(self.board, pos2):
            if not self.verify_player_turn(pz, player_turn):
                return False

            if should_promote:
                if pz.promoted or isinstance(pz, King) or isinstance(pz, GoldGeneral):
                    return False

                if (player_turn == 'UPPER' and utils.get_coords(pos2)[1] == 0) or \
                    (player_turn == 'lower' and utils.get_coords(pos2)[1] == const.BOARD_SIZE - 1) or \
                    (player_turn == 'UPPER' and utils.get_coords(pos1)[1] == 0) or \
                        (player_turn == 'lower' and utils.get_coords(pos1)[1] == const.BOARD_SIZE - 1):
                    pz.promoted = True
                else:
                    return False

            pz2 = self.get_piece_at_pos(pos2)
            if pz2 is not '__':
                if pz2.team == pz.team:
                    return False
                if player_turn == 'lower':
                    self.lower_captures.append(str(pz2)[1].lower())
                elif player_turn == 'UPPER':
                    self.upper_captures.append(str(pz2)[1].upper())

            self.set_coord(pz, pos2)
            self.set_coord('__', pos1)
            return True
        return False

    def drop_piece(self, player_turn, piece, pos):
        ''' Return True if move was successful '''
        piece_name = str(piece)
        if len(piece_name) > 1:
            piece_name = piece_name[1]

        # Cannot place Pawn in promotion zone or in same row as another Pawn.
        if piece_name.lower() == 'p':
            if ((player_turn == 'UPPER' and utils.get_coords(pos)[1] == 0) or \
                (player_turn == 'lower' and utils.get_coords(pos)[1] == const.BOARD_SIZE - 1)):
                return False
            else:
                x, y = utils.get_coords(pos)
                for j in range(const.BOARD_SIZE):
                    if isinstance(self.board[x][j], Pawn) and self.board[x][j].team == player_turn:
                        return False

        # Only drop pieces in empty spaces
        if self.get_piece_at_pos(pos) == '__':
            if player_turn == 'UPPER':
                for i in range(len(self.upper_captures)):
                    if self.upper_captures[i].lower() == piece_name.lower():
                        new_piece = const.PIECE_MAP[piece_name](pos, player_turn)
                        self.set_coord(new_piece, pos)
                        del self.upper_captures[i]
                        return True

            elif player_turn == 'lower':
                for i in range(len(self.lower_captures)):
                    if self.lower_captures[i] == piece_name:
                        new_piece = const.PIECE_MAP[piece_name](pos, player_turn)
                        self.set_coord(new_piece, pos)
                        del self.lower_captures[i]
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
            return False

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
