"""
A module providing a representation of a chess board. The rules of chess are not implemented - 
this is just a "dumb" board that will let you move pieces around as you like.
"""

from collections import namedtuple
from enum import Enum, auto

from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King
import random

BOARD_SIZE = 8
# TODO check, checkmate, stalemate


class Board:
    """
    A representation of the chess board, and the pieces on it.
    """

    def __init__(self, player, board_state):
        self.current_player = Player.WHITE
        self.board = board_state
        self.last_move = None

    @staticmethod
    def empty():
        return Board(Player.WHITE, Board._create_empty_board())

    @staticmethod
    def at_starting_position():
        return Board(Player.WHITE, Board._create_starting_board())

    @staticmethod
    def _create_empty_board():
        return [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    @staticmethod
    def _create_starting_board():

        # Create an empty board
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Setup the rows of pawns
        board[1] = [Pawn(Player.WHITE) for _ in range(BOARD_SIZE)]
        board[6] = [Pawn(Player.BLACK) for _ in range(BOARD_SIZE)]

        # Setup the rows of pieces
        piece_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board[0] = list(map(lambda piece: piece(Player.WHITE), piece_row))
        board[7] = list(map(lambda piece: piece(Player.BLACK), piece_row))

        return board

    def set_piece(self, square, piece):
        """
        Places the piece at the given position on the board.
        """
        self.board[square.row][square.col] = piece

    def are_squares_empty(self, squares):
        return all(map(lambda s: self.is_square_empty(s), squares))

    def is_square_empty(self, square):
        return self.get_piece(square) is None

    def capture_possible(self, current_position, candidate_position):
        if self.get_piece(current_position).player != self.get_piece(candidate_position).player:
            return True
        return False

    def get_piece(self, square):
        """
        Retrieves the piece from the given square of the board.
        """
        return self.board[square.row][square.col]

    def find_piece(self, piece_to_find):
        """
        Searches for the given piece on the board and returns its square.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is piece_to_find:
                    return Square.at(row, col)
        raise Exception('The supplied piece is not on the board')

    def bot_move(self):
        if self.current_player == Player.BLACK:
            all_moves = []
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    piece_in_square = self.board[row][col]
                    if piece_in_square is None:
                        continue
                    if (piece_in_square.player == Player.BLACK) & (piece_in_square.get_available_moves(self) != []):
                        all_moves.append((piece_in_square, piece_in_square.get_available_moves(self)))
            move = random.choice(all_moves)
            print(move)
            self.move_piece(self.find_piece(move[0]), random.choice(move[1]))

    def move_piece(self, from_square, to_square):
        """
        Moves the piece from the given starting square to the given destination square.
        """
        moving_piece = self.get_piece(from_square)
        if moving_piece is not None and moving_piece.player == self.current_player:
            if isinstance(moving_piece, Pawn) & (to_square.row == 0 or to_square.row == 7):
                moving_piece = Queen(self.current_player)
            self.handle_castling(from_square, to_square, moving_piece)
            en_passant = False
            if isinstance(moving_piece, Pawn):
                self.handle_en_passant(from_square, to_square)
                if (((to_square.row == 3) & (from_square.row == 1))
                        or ((to_square.row == 4) & (from_square.row == 6))):
                    en_passant = True
            self.set_piece(to_square, moving_piece)
            self.set_piece(from_square, None)
            moving_piece.moved = True
            self.last_move = (moving_piece, to_square, en_passant)
            self.current_player = self.current_player.opponent()
            self.bot_move()

    def handle_en_passant(self, from_square, to_square):
        if self.last_move is not None:
            if self.last_move[2] & (self.last_move[1].row == from_square.row):
                if self.last_move[1].col == to_square.col:
                    self.set_piece(self.last_move[1], None)

    def handle_castling(self, from_square, to_square, piece):
        if not isinstance(piece, King):
            return
        if abs(from_square.col - to_square.col) > 1:
            if to_square.col == 2:
                rook = self.get_piece(Square.at(to_square.row, 0))
                self.set_piece(Square.at(to_square.row, 3), rook)
                self.set_piece(Square.at(to_square.row, 0), None)
            else:
                rook = self.get_piece(Square.at(to_square.row, 7))
                self.set_piece(Square.at(to_square.row, 5), rook)
                self.set_piece(Square.at(to_square.row, 7), None)
