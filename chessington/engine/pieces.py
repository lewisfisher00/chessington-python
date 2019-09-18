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

    def is_at_edge_of_board(self, square):
        if ((self.player == Player.WHITE) & (square.row == 7)) | ((self.player == Player.BLACK) & (square.row == 0)):
            return True
        return False


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
        current_square = board.find_piece(self)
        direction = 1 if self.player == Player.WHITE else -1
        next_square = Square.at(current_square.row + direction, current_square.col)
        # check edge
        if self.is_at_edge_of_board(current_square):
            return moves
        # move 1
        if board.is_square_empty(next_square):
            moves.append(Square.at(next_square.row, current_square.col))
            second_square = Square.at(next_square.row + direction, next_square.col)
            # move 2
            if (self.is_at_start_position(current_square)) & (board.is_square_empty(second_square)):
                moves.append(Square.at(second_square.row, current_square.col))
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
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []