import utils
import sys
import const
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral
from board import Board

def main():
    argc = len(sys.argv)
    if argc > 1 and sys.argv[1] == '-f':
        file_name = sys.argv[2]
        test_case = utils.parseTestCase(file_name)
        play_game(test_case, False)

    elif argc > 1 and sys.argv[1] == '-i':
        test_case = utils.parseTestCase('tests/initialMove.in')
        play_game(test_case, True)

    else:
        print('Invalid command line arguments')


def execute_command(board, move, player_turn, verbose = True):
    move_arr = move.split(' ')
    if verbose: print(board)
    if move_arr[0] == 'move':
        should_promote = False
        if len(move_arr) > 3 and move_arr[3] == 'promote':
            should_promote = True
        pos1 = move_arr[1]
        pos2 = move_arr[2]
        valid_move = board.move_piece(pos1, pos2, player_turn, should_promote)
        return valid_move

    elif move_arr[0] == 'drop':
        piece = move_arr[1]
        pos = move_arr[2]
        valid_move = board.drop_piece(piece, pos)
        return valid_move


def output_game_state(board):
    print(board)
    print('Captures UPPER: ', end='')
    for cap in board.upper_captures:
        print(cap, end=' ')
    print('')

    print('Captures lower: ', end='')
    for cap in board.lower_captures:
        print(cap, end=' ')
    print('\n')



def execute_file(board, moves):
    assert len(moves) != 0
    # print(moves)                                                # TODO
    valid_move = True
    turns = 0
    player_turn = ''
    for move in moves:
        player_turn = 'lower' if turns % 2 == 0 else 'UPPER'
        valid_move = execute_command(board, move, player_turn, False)
        turns += 1

    print(player_turn + ' player action: ' + moves[-1])
    output_game_state(board)

    player_turn = 'lower' if turns % 2 == 0 else 'UPPER'
    if not valid_move:
        print(player_turn + ' player wins.  Illegal move.')
    else:
        print(player_turn + '> ')


def play_game(test_case, is_interactive):
    board = Board(test_case['initialPieces'], test_case['upperCaptures'], test_case['lowerCaptures'])

    if is_interactive:
        execute_interactive(board)
    else: # is file_name
        execute_file(board, test_case['moves'])




def execute_interactive(board):
    turns = 0
    player_turn = 'lower' if turns % 2 == 0 else 'UPPER'

    while turns < const.MAX_MOVES:
        output_game_state(board)

        print(player_turn + '> ', end = '')
        move = input()

        print(player_turn + ' player action: ' + move)

        move_arr = move.split(' ')
        valid_move = board.move_piece(move_arr[1], move_arr[2], player_turn)
        if not valid_move:
            print(player_turn + ' player wins. Illegal move.')
            break

        player_turn = 'lower' if turns % 2 == 0 else 'UPPER'

    print(board)



if __name__ == '__main__':
    main()
