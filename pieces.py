import utils

class Piece:
    def __init__(self, position, team, promoted=False):
        self.position = position
        self.team = team
        self.name = 'Piece'
        self.promoted = False

    def move(self, board, new_a1):
        possible = self.get_possible_moves(board, self.position, self.team, self.promoted)
        if new_a1 in possible:
            self.position = new_a1
            return True

        return False

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        return '__'


class King(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'King'

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        possible_moves = set()
        x, y = utils.get_coords(position)

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if utils.in_bounds(new_pos) and not (i == 0 and j == 0):
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.promoted: s = '+'
        if self.team == 'lower':
            return s + 'k'
        return s + 'K'


class Pawn(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'Pawn'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        if promoted:
            return GoldGeneral.get_possible_moves(board, position, team, False)

        possible_moves = set()
        x, y = utils.get_coords(position)

        new_pos = utils.get_a1(x, y + 1)
        if team == 'UPPER':
            new_pos = utils.get_a1(x, y - 1)
        if utils.in_bounds(new_pos):
            possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.promoted: s = '+'
        if self.team == 'lower':
            return s + 'p'
        return s + 'P'


class Rook(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'Rook'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= King.get_possible_moves(board, position, team, False)

        x, y = utils.get_coords(position)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x + i, y)
            if utils.in_bounds(new_pos):
                pz = board[x+i][y]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x, y + i)
            if utils.in_bounds(new_pos):
                pz = board[x][y+i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x - i, y)
            if utils.in_bounds(new_pos):
                pz = board[x-i][y]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x, y - i)
            if utils.in_bounds(new_pos):
                pz = board[x][y-i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.promoted: s = '+'
        if self.team == 'lower':
            return s + 'r'
        return s + 'R'


class Bishop(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'Bishop'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        possible_moves = set()
        if promoted:
            possible_moves |= King.get_possible_moves(board, position, team, False)
        x, y = utils.get_coords(position)

        for i in range(1, len(board)):
            new_pos = utils.get_a1(x + i, y + i)
            if utils.in_bounds(new_pos):
                pz = board[x+i][y+i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)

        for i in range(1, len(board)):
            new_pos = utils.get_a1(x - i, y + i)
            if utils.in_bounds(new_pos):
                pz = board[x-i][y+i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x + i, y - i)
            if utils.in_bounds(new_pos):
                pz = board[x+i][y-i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        for i in range(1, len(board)):
            new_pos = utils.get_a1(x - i, y - i)
            if utils.in_bounds(new_pos):
                pz = board[x-i][y-i]
                if pz != '__':
                    if pz.team != team:
                        possible_moves.add(new_pos)
                    break
                else:
                    possible_moves.add(new_pos)
        return possible_moves


    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.promoted: s = '+'
        if self.team == 'lower':
            return s + 'b'
        return s + 'B'


class SilverGeneral(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'SilverGeneral'
        self.promoted = promoted

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        if promoted:
            return GoldGeneral.get_possible_moves(board, position, team, False)

        possible_moves = set()
        x, y = utils.get_coords(position)

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if team == 'UPPER':
                    new_pos = utils.get_a1(x + i, y - j)

                if utils.in_bounds(new_pos) and not (i == 0 and j == 0) \
                and not (i == -1 and j == 0) and not (i == 1 and j == 0) \
                and not (i == 0 and j == -1):
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.promoted: s = '+'
        if self.team == 'lower':
            return s + 's'
        return s + 'S'


class GoldGeneral(Piece):
    def __init__(self, position, team, promoted=False):
        super().__init__(position, team)
        self.name = 'GoldGeneral'

    @staticmethod
    def get_possible_moves(board, position, team, promoted):
        possible_moves = set()
        x, y = utils.get_coords(position)
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = utils.get_a1(x + i, y + j)
                if team == 'UPPER':
                    new_pos = utils.get_a1(x + i, y - j)

                if utils.in_bounds(new_pos) and not (i == 0 and j == 0) \
                and not (i == -1 and j == -1) and not (i == 1 and j == -1):
                    possible_moves.add(new_pos)
        return possible_moves

    def __repr__(self):
        ''' Used to distiguish Piece objects for logging. '''
        s = ' '
        if self.team == 'lower':
            return s + 'g'
        return s + 'G'
