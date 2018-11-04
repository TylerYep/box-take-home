import utils
import const

class Piece:
    def __init__(self, position, is_lower, promoted=False):
        self.position = position
        self.is_lower = is_lower
        self.name = 'Piece'
        self.promoted = False

    def move(self, new_a1):
        possible = self.get_possible_moves(self.position, self.is_lower, self.promoted)
        print(self.name, possible)

        if new_a1 in possible:
            self.position = new_a1
            # update all other pieces
            return True

        return False

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        return '__'


class King(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'King'

    def is_in_check(self):
        return False

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        x, y = utils.get_coords(position)

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if utils.in_bounds(new_pos) and not (i == 0 and j == 0): # and not player_in_check
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.promoted: s = '+'
        if self.is_lower:
            return s + 'k'
        return s + 'K'


class Pawn(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'Pawn'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= GoldGeneral.get_possible_moves(position, is_lower, False)
        x, y = utils.get_coords(position)
        new_pos = utils.get_a1(x, y - 1)
        if is_lower:
            new_pos = utils.get_a1(x, y + 1)
        if utils.in_bounds(new_pos):
            possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.promoted: s = '+'
        if self.is_lower:
            return s + 'p'
        return s + 'P'


class Rook(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'Rook'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= King.get_possible_moves(position, is_lower, False)
        x, y = utils.get_coords(position)
        for i in range(-const.BOARD_SIZE, const.BOARD_SIZE):
            new_pos = utils.get_a1(x + i, y)
            if utils.in_bounds(new_pos):
                possible_moves.add(new_pos)
            new_pos = utils.get_a1(x, y + i)
            if utils.in_bounds(new_pos):
                possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.promoted: s = '+'
        if self.is_lower:
            return s + 'r'
        return s + 'R'


class Bishop(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'Bishop'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= King.get_possible_moves(position, is_lower, False)
        x, y = utils.get_coords(position)
        for i in range(-const.BOARD_SIZE, const.BOARD_SIZE):
            new_pos = utils.get_a1(x + i, y + i)
            if utils.in_bounds(new_pos):
                possible_moves.add(new_pos)
            new_pos = utils.get_a1(x + i, y - i)
            if utils.in_bounds(new_pos):
                possible_moves.add(new_pos)
        return possible_moves


    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.promoted: s = '+'
        if self.is_lower:
            return s + 'b'
        return s + 'B'


class SilverGeneral(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'SilverGeneral'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= GoldGeneral.get_possible_moves(position, is_lower, False)
        x, y = utils.get_coords(position)

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if utils.in_bounds(new_pos) and not (i == 0 and j == 0) \
                and not (i == -1 and j == 0) and not (i == 1 and j == 0) \
                and not (i == 0 and j == -1): # and not player_in_check
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.promoted: s = '+'
        if self.is_lower:
            return s + 's'
        return s + 'S'


class GoldGeneral(Piece):
    def __init__(self, position, is_lower, promoted=False):
        super().__init__(position, is_lower)
        self.name = 'GoldGeneral'

    @staticmethod
    def get_possible_moves(position, is_lower, promoted):
        possible_moves = set()
        x, y = utils.get_coords(position)

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if utils.in_bounds(new_pos) and not (i == -1 and j == -1) \
                and not (i == 1 and j == -1): # and not player_in_check
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = '_'
        if self.is_lower:
            return s + 'g'
        return s + 'G'
