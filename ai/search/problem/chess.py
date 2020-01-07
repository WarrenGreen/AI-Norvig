from ai.search.problem.problem import Problem


class Chess(Problem):
    """
    State represented as dictionary of board location-piece mappings. Where board
    locations are denoted as a `str` using the standard board denotions. The piece
    representation is a two character `str` where the first character is the player
    color:

        ('W', 'B')

    and the second character is the piece type:

        ('P', 'R', 'N', 'B', 'Q', 'K')

    As well there is a key "turn" with the value being the player color whose turn is
    next.

    """

    TURN = "turn"

    WHITE = "W"
    BLACK = "B"

    PAWN = "P"
    ROOK = "R"
    KING = "K"
    BISHOP = "B"
    QUEEN = "Q"
    KNIGHT = "N"

    BOARD_SIZE = 8

    LETTER_TO_NUM_BASE = ord("A") - 1

    KNIGHT_MOVES = [
        (-1, 2),
        (1, 2),
        (-1, -2),
        (1, 2),
        (-2, -1),
        (-2, 1),
        (2, -1),
        (2, 1),
    ]

    def _generate_piece_successors(self, state, piece_location):
        piece_color, piece_type = state[piece_location]
        loc_letter, loc_number = piece_location
        if piece_color != state[Chess.TURN]:
            return

        moves = set()
        if piece_type == Chess.PAWN:
            one_forward_move = None
            two_forward_move = None
            if piece_color == Chess.WHITE:
                one_forward_move = f"{loc_letter}{loc_number + 1}"
                if loc_number == 2:
                    two_forward_move = f"{loc_letter}{loc_number + 2}"
            else:
                one_forward_move = f"{loc_letter}{loc_number - 1}"
                if loc_number == Chess.BOARD_SIZE - 1:
                    two_forward_move = f"{loc_letter}{loc_number - 2}"

            one_forward_letter, one_forward_number = one_forward_move
            attack_move_left = f"{chr(ord(one_forward_letter)-1)}{one_forward_number}"
            attack_move_right = f"{chr(ord(one_forward_letter)+1)}{one_forward_number}"
            if attack_move_left in state:
                moves.add(attack_move_left)

            if attack_move_right in state:
                moves.add(attack_move_right)

            if one_forward_move not in state:
                moves.add(one_forward_move)
                if two_forward_move and two_forward_move not in state:
                    moves.add(two_forward_move)
        elif piece_type == Chess.ROOK:
            moves.update(self.adjacent_moves(state, piece_location))
        elif piece_type == Chess.KING:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    move_letter = chr(ord(loc_letter) + i)
                    move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
                    move_number = loc_number + j
                    move = f"{move_letter}{move_number}"
                    if (
                        0 < move_letter_base <= Chess.BOARD_SIZE
                        and 0 < move_number <= Chess.BOARD_SIZE
                        and not self.in_check(move)
                    ):
                        moves.add(move)
        elif piece_type == Chess.BISHOP:
            moves.update(self.diagonal_moves(state, piece_location))
        elif piece_type == Chess.QUEEN:
            moves.update(self.adjacent_moves(state, piece_location))
            moves.update(self.diagonal_moves(state, piece_location))
        elif piece_type == Chess.KNIGHT:
            for i, j in Chess.KNIGHT_MOVES:
                move_letter = chr(ord(loc_letter) + i)
                move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
                move_number = loc_number + j
                move = f"{move_letter}{move_number}"
                if (
                    0 < move_letter_base <= Chess.BOARD_SIZE
                    and 0 < move_number <= Chess.BOARD_SIZE
                ):
                    moves.add(move)

        for move in moves:
            yield move

    def in_check(self, state, player):
        # TODO
        return False

    def diagonal_moves(self, state, piece_location):
        loc_letter, loc_number = piece_location
        moves = set()
        for i, j in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            move_letter = chr(ord(loc_letter) + i)
            move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
            move_number = loc_number + j
            move = f"{move_letter}{move_number}"
            while (
                0 < move_letter_base <= Chess.BOARD_SIZE
                and 0 < move_number <= Chess.BOARD_SIZE
            ):
                moves.add(move)
                if move in state:
                    break
        return moves

    def adjacent_moves(self, state, piece_location):
        loc_letter, loc_number = piece_location
        moves = set()
        # rows
        row = loc_number + 1
        while row <= Chess.BOARD_SIZE:
            moves.add(f"{loc_letter}{row}")
            if f"{loc_letter}{row}" in state:
                break
            row += 1

        row = loc_number - 1
        while row > 0:
            moves.add(f"{loc_letter}{row}")
            if f"{loc_letter}{row}" in state:
                break
            row -= 1

        # cols
        col = 1
        while col <= Chess.BOARD_SIZE:
            move = f"{chr(ord(loc_letter) + col)}{loc_number}"
            moves.add(move)
            if move in state:
                break
            col += 1

        col = -1
        while ord(loc_letter) + col - Chess.LETTER_TO_NUM_BASE > 0:
            move = f"{chr(ord(loc_letter) + col)}{loc_number}"
            moves.add(move)
            if move in state:
                break
            col -= 1

        return moves

    def generate_successors(self, state):
        pass

    def get_value(self, state):
        pass

    def is_terminal(self, state):
        pass

    def _piece_lookup(self, state, search_piece):
        for location, piece in state.items():
            if search_piece == piece:
                return location

    def create_start(self):
        pass
