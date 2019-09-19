"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def get_moves_in_direction(self, board, direction):
        valid_moves = []
        distance = 1
        start_position = board.find_piece(self)

        while True:
            move_vector = (direction[0] * distance, direction[1] * distance)
            candidate_position = start_position.translate_by(move_vector)
            if candidate_position.is_on_board():
                if board.is_square_empty(candidate_position):
                    valid_moves.append(candidate_position)
                    distance += 1
                elif board.capture_possible(start_position, candidate_position):
                    valid_moves.append(candidate_position)
                    break
                else:
                    break
            else:
                break
        return valid_moves


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """
    def is_at_start_position(self, current_square):
        if (((self.player == Player.WHITE) & (current_square.row == 1)) |
                ((self.player == Player.BLACK) & (current_square.row == 6))):
            return True
        return False

    def get_available_moves(self, board):
        moves = []
        start_square = board.find_piece(self)
        direction = 1 if self.player == Player.WHITE else -1
        candidate_square = Square.at(start_square.row + direction, start_square.col)
        if candidate_square.is_on_board():
            # move 1
            if board.is_square_empty(candidate_square):
                moves.append(Square.at(candidate_square.row, candidate_square.col))
                # move 2
                candidate_square = Square.at(candidate_square.row + direction, candidate_square.col)
                if self.is_at_start_position(start_square):
                    if candidate_square.is_on_board() & board.is_square_empty(candidate_square):
                        moves.append(Square.at(candidate_square.row, candidate_square.col))
            # capture
        candidate_square = Square.at(start_square.row + direction, start_square.col + 1)
        moves += self.check_diagonal(board, start_square, candidate_square)
        candidate_square = Square.at(start_square.row + direction, start_square.col - 1)
        moves += self.check_diagonal(board, start_square, candidate_square)
        return moves

    @staticmethod
    def check_diagonal(board, start_square, candidate_square):
        moves = []
        if candidate_square.is_on_board():
            if not board.is_square_empty(candidate_square):
                if board.capture_possible(start_square, candidate_square):
                    moves.append(Square.at(candidate_square.row, candidate_square.col))
        return moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """
    def get_available_moves(self, board):
        moves = self.get_fs_moves(board)
        moves += self.get_bs_moves(board)
        return moves

    def get_fs_moves(self, board):
        up = (1, 1)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, -1)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_bs_moves(self, board):
        right = (-1, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (1, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        moves = self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_vertical_moves(self, board):
        up = (1, 0)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, 0)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_horizontal_moves(self, board):
        right = (0, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (0, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves


class Queen(Piece):
    """
    A class representing a chess queen.
    """
    def get_available_moves(self, board):
        moves = self.get_fs_moves(board)
        moves += self.get_bs_moves(board)
        moves += self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_fs_moves(self, board):
        up = (1, 1)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, -1)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_bs_moves(self, board):
        right = (-1, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (1, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves

    def get_vertical_moves(self, board):
        up = (1, 0)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, 0)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_horizontal_moves(self, board):
        right = (0, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (0, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        moves = self.get_fs_moves(board)
        moves += self.get_bs_moves(board)
        moves += self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_fs_moves(self, board):
        up = (1, 1)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, -1)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_bs_moves(self, board):
        right = (-1, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (1, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves

    def get_vertical_moves(self, board):
        up = (1, 0)
        up_moves = self.get_moves_in_direction(board, up)
        down = (-1, 0)
        down_moves = self.get_moves_in_direction(board, down)
        return up_moves + down_moves

    def get_horizontal_moves(self, board):
        right = (0, 1)
        up_moves = self.get_moves_in_direction(board, right)
        left = (0, -1)
        down_moves = self.get_moves_in_direction(board, left)
        return up_moves + down_moves

    def get_moves_in_direction(self, board, direction):
        valid_moves = []
        distance = 1
        start_position = board.find_piece(self)

        move_vector = (direction[0] * distance, direction[1] * distance)
        candidate_position = start_position.translate_by(move_vector)
        if candidate_position.is_on_board():
            if board.is_square_empty(candidate_position):
                valid_moves.append(candidate_position)
            elif board.capture_possible(start_position, candidate_position):
                valid_moves.append(candidate_position)
        return valid_moves

