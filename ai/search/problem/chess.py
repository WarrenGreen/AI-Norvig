from copy import deepcopy

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
    LETTER_RANGE = ["A", "B", "C", "D", "E", "F", "G", "H"]

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
                one_forward_move = f"{loc_letter}{int(loc_number) + 1}"
                if loc_number == 2:
                    two_forward_move = f"{loc_letter}{int(loc_number) + 2}"
            else:
                one_forward_move = f"{loc_letter}{int(loc_number) - 1}"
                if loc_number == Chess.BOARD_SIZE - 1:
                    two_forward_move = f"{loc_letter}{int(loc_number) - 2}"

            one_forward_letter, one_forward_number = one_forward_move
            attack_move_left = f"{chr(ord(one_forward_letter) - 1)}{one_forward_number}"
            attack_move_right = (
                f"{chr(ord(one_forward_letter) + 1)}{one_forward_number}"
            )
            if attack_move_left in state:
                yield attack_move_left

            if attack_move_right in state:
                yield attack_move_right

            if one_forward_move not in state:
                yield one_forward_move
                if two_forward_move and two_forward_move not in state:
                    yield two_forward_move
        elif piece_type == Chess.ROOK:
            moves.update(self._generate_adjacent_moves(state, piece_location))
        elif piece_type == Chess.KING:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    move_letter = chr(ord(loc_letter) + i)
                    move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
                    move_number = int(loc_number) + j
                    move = f"{move_letter}{move_number}"
                    if (
                        0 < move_letter_base <= Chess.BOARD_SIZE
                        and 0 < move_number <= Chess.BOARD_SIZE
                    ):
                        yield move
        elif piece_type == Chess.BISHOP:
            for move in self._generate_diagonal_moves(state, piece_location):
                yield move
        elif piece_type == Chess.QUEEN:
            moves.update(self._generate_adjacent_moves(state, piece_location))
            for move in self._generate_diagonal_moves(state, piece_location):
                yield move
        elif piece_type == Chess.KNIGHT:
            for i, j in Chess.KNIGHT_MOVES:
                move_letter = chr(ord(loc_letter) + i)
                move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
                move_number = int(loc_number) + j
                move = f"{move_letter}{move_number}"
                if (
                    0 < move_letter_base <= Chess.BOARD_SIZE
                    and 0 < move_number <= Chess.BOARD_SIZE
                ):
                    yield move

    def _generate_diagonal_moves(self, state, piece_location):
        loc_letter, loc_number = piece_location
        for i, j in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            move_letter = chr(ord(loc_letter) + i)
            move_letter_base = ord(move_letter) - Chess.LETTER_TO_NUM_BASE
            move_number = int(loc_number) + j
            move = f"{move_letter}{move_number}"
            while (
                0 < move_letter_base <= Chess.BOARD_SIZE
                and 0 < move_number <= Chess.BOARD_SIZE
            ):
                yield move
                if move in state:
                    break

    def _generate_adjacent_moves(self, state, piece_location):
        loc_letter, loc_number = piece_location
        # rows
        row = int(loc_number) + 1
        while row <= Chess.BOARD_SIZE:
            yield f"{loc_letter}{row}"
            if f"{loc_letter}{row}" in state:
                break
            row += 1

        row = int(loc_number) - 1
        while row > 0:
            yield f"{loc_letter}{row}"
            if f"{loc_letter}{row}" in state:
                break
            row -= 1

        # cols
        col = 1
        while col <= Chess.BOARD_SIZE:
            move = f"{chr(ord(loc_letter) + col)}{loc_number}"
            yield move
            if move in state:
                break
            col += 1

        col = -1
        while ord(loc_letter) + col - Chess.LETTER_TO_NUM_BASE > 0:
            move = f"{chr(ord(loc_letter) + col)}{loc_number}"
            yield move
            if move in state:
                break
            col -= 1

    def _generate_player_successors(self, state, player):
        for piece_location, piece in state.items():
            if piece_location == Chess.TURN:
                continue
            piece_player, piece_type = piece
            if piece_player == player:
                for move in self._generate_piece_successors(state, piece_location):
                    yield move, piece

    def generate_successors(self, state):
        for move_loc, piece in self._generate_player_successors(
            state, state[Chess.TURN]
        ):
            new_state = deepcopy(state)
            successor = self._move(new_state, move_loc, piece)
            if not self._in_check(successor, state[Chess.TURN]):
                yield successor

    def _move(self, state, move_loc, piece):
        for board_loc, board_piece in state.items():
            if board_loc == Chess.TURN:
                continue
            if board_piece == piece:
                state.pop(board_loc)
                break

        state[move_loc] = piece
        piece_player, _ = piece
        state[Chess.TURN] = self._opposing_player(piece_player)
        return state

    def _move_in_check(self, state, move, piece):
        piece_player, _ = piece
        new_state = deepcopy(state)
        new_state = self._move(new_state, move, piece)
        return self._in_check(new_state, piece_player)

    def _in_check(self, state, player):
        king_location = self._piece_lookup(state, f"{player}{Chess.KING}")
        for potential_opposing_location, _ in self._generate_player_successors(
            state, self._opposing_player(player)
        ):
            if potential_opposing_location == king_location:
                return True
        return False

    def get_value(self, state):
        # TODO
        pass

    def is_terminal(self, state):
        # Checkmate or Stalemate
        valid_moves_exist = False
        for _ in self.generate_successors(state):
            valid_moves_exist = True
            break
        return not valid_moves_exist

    def _opposing_player(self, player):
        if player == Chess.BLACK:
            return Chess.WHITE
        else:
            return Chess.BLACK

    def _piece_lookup(self, state, search_piece):
        for location, piece in state.items():
            if location == Chess.TURN:
                continue
            if search_piece == piece:
                return location

    def create_start(self):
        state = {
            "A8": f"{Chess.BLACK}{Chess.ROOK}",
            "B8": f"{Chess.BLACK}{Chess.KNIGHT}",
            "C8": f"{Chess.BLACK}{Chess.BISHOP}",
            "D8": f"{Chess.BLACK}{Chess.QUEEN}",
            "E8": f"{Chess.BLACK}{Chess.KING}",
            "F8": f"{Chess.BLACK}{Chess.BISHOP}",
            "G8": f"{Chess.BLACK}{Chess.KNIGHT}",
            "H8": f"{Chess.BLACK}{Chess.ROOK}",
            "A1": f"{Chess.WHITE}{Chess.ROOK}",
            "B1": f"{Chess.WHITE}{Chess.KNIGHT}",
            "C1": f"{Chess.WHITE}{Chess.BISHOP}",
            "D1": f"{Chess.WHITE}{Chess.QUEEN}",
            "E1": f"{Chess.WHITE}{Chess.KING}",
            "F1": f"{Chess.WHITE}{Chess.BISHOP}",
            "G1": f"{Chess.WHITE}{Chess.KNIGHT}",
            "H1": f"{Chess.WHITE}{Chess.ROOK}",
        }

        for board_letter in Chess.LETTER_RANGE:
            state[f"{board_letter}2"] = f"{Chess.WHITE}{Chess.PAWN}"
            state[f"{board_letter}7"] = f"{Chess.BLACK}{Chess.PAWN}"

        state[Chess.TURN] = Chess.WHITE
        return state
