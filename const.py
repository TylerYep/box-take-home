from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral

BOARD_SIZE = 5
MAX_MOVES = 200

PIECE_MAP = dict({
    'k': King, 'b': Bishop,
    'g': GoldGeneral, 's': SilverGeneral,
    'r': Rook, 'p': Pawn
})
