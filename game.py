import utils
import sys
import const
from pieces import King, Piece, Pawn, Bishop, Rook, SilverGeneral, GoldGeneral
from board import Board, find_available_moves

def main():
    argc = len(sys.argv)
    if argc > 1 and sys.argv[1] == '-f':
        file_name = sys.argv[2]
        test_case = utils.parseTestCase(file_name)
        board = Board(test_case['initialPieces'], test_case['upperCaptures'], test_case['lowerCaptures'])

        play_game_file(board, test_case['moves'])

    elif argc > 1 and sys.argv[1] == '-i':
        test_case = utils.parseTestCase('tests/initialMove.in')
        board = Board(test_case['initialPieces'], test_case['upperCaptures'], test_case['lowerCaptures'])
        play_game_interactive(board)

    else:
        print('Invalid command line arguments')


def execute_command(board, move, player_turn, verbose = True):
    ''' Takes any command and manipulated the given board.
        - move (with promote)
        - drop
    '''
    move_arr = move.split(' ')
    if verbose: print(board)
    if move_arr[0] == 'move':
        should_promote = False
        if len(move_arr) > 3 and move_arr[3] == 'promote':
            should_promote = True
        pos1 = move_arr[1]
        pos2 = move_arr[2]
        if board.can_move_piece(pos1, pos2, player_turn, should_promote):
            board.move_piece(pos1, pos2, player_turn, should_promote)
            return True

    elif move_arr[0] == 'drop':
        piece = move_arr[1]
        pos = move_arr[2]
        valid_move = board.drop_piece(player_turn, piece, pos)
        return valid_move

    return False


def output_game_state(board):
    ''' Outputs game state as specified in the spec. '''
    print(board)
    print('Captures UPPER: ', end='')
    for cap in board.upper_captures:
        print(cap, end=' ')
    print('')

    print('Captures lower: ', end='')
    for cap in board.lower_captures:
        print(cap, end=' ')
    print('\n')


def play_game_file(board, moves):
    ''' Plays game automatically using specified moves. '''

    assert len(moves) != 0
    # print(moves)
    valid_move = True
    turns = 0
    player_turn = ''
    for move in moves:
        player_turn = 'lower' if turns % 2 == 0 else 'UPPER'
        valid_move = execute_command(board, move, player_turn, False) #TODO
        turns += 1
        if turns >= const.MAX_MOVES * 2: break
        if not valid_move: break

    print(player_turn + ' player action: ' + move)
    output_game_state(board)
    player_turn = 'lower' if turns % 2 == 0 else 'UPPER'
    if turns >= const.MAX_MOVES * 2:
        print('Tie game.  Too many moves.')
    elif not valid_move:
        print(player_turn + ' player wins.  Illegal move.')
    else:
        if board.king_in_check(player_turn):
            available_moves = find_available_moves(board, player_turn)
            if available_moves:
                print(player_turn + ' player is in check!')
                print('Available moves: ')
                for move in available_moves:
                    print(move)
            else:
                print(player_turn + ' Checkmate!')

        print(player_turn + '> ')


def play_game_interactive(board):
    ''' Plays game interactively using a turn-based system. '''

    turns = 0
    player_turn = 'lower'

    while turns < const.MAX_MOVES * 2:
        output_game_state(board)

        # available_moves = board.find_checks(player_turn)
        # if available_moves:
        #     print(player_turn + ' player is in check!')
        #     print('Available moves: ')
        #     for move in available_moves:
        #         print(move)

        print(player_turn + '> ', end = '')
        move = input()
        print(player_turn + ' player action: ' + move)

        player_turn = 'lower' if turns % 2 == 0 else 'UPPER'
        valid_move = execute_command(board, move, player_turn, False)
        turns += 1
        player_turn = 'lower' if turns % 2 == 0 else 'UPPER'

        if not valid_move:
            print(player_turn + ' player wins. Illegal move.')
            break
    print('Tie game.  Too many moves.')


if __name__ == '__main__':
    main()
