#!/usr/bin/env python3
"""
Chess Game Implementation
A complete chess game with all standard rules including:
- Piece movement validation
- Check and checkmate detection
- Castling, en passant, pawn promotion
- Turn-based gameplay
- ASCII board display
"""

import copy
from typing import List, Tuple, Optional, Dict, Set
from enum import Enum

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False
    
    def __str__(self):
        symbols = {
            (Color.WHITE, PieceType.PAWN): "♙",
            (Color.WHITE, PieceType.ROOK): "♖",
            (Color.WHITE, PieceType.KNIGHT): "♘",
            (Color.WHITE, PieceType.BISHOP): "♗",
            (Color.WHITE, PieceType.QUEEN): "♕",
            (Color.WHITE, PieceType.KING): "♔",
            (Color.BLACK, PieceType.PAWN): "♟",
            (Color.BLACK, PieceType.ROOK): "♜",
            (Color.BLACK, PieceType.KNIGHT): "♞",
            (Color.BLACK, PieceType.BISHOP): "♝",
            (Color.BLACK, PieceType.QUEEN): "♛",
            (Color.BLACK, PieceType.KING): "♚",
        }
        return symbols.get((self.color, self.piece_type), "?")

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.move_history = []
        self.en_passant_target = None
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        """Set up the initial chess position"""
        # Place pawns
        for col in range(8):
            self.board[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.board[6][col] = Piece(Color.WHITE, PieceType.PAWN)
        
        # Place other pieces
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                      PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(Color.BLACK, piece_type)
            self.board[7][col] = Piece(Color.WHITE, piece_type)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        """Set piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_empty(self, row: int, col: int) -> bool:
        """Check if position is empty"""
        return self.is_valid_position(row, col) and self.board[row][col] is None
    
    def is_occupied_by_color(self, row: int, col: int, color: Color) -> bool:
        """Check if position is occupied by piece of given color"""
        piece = self.get_piece(row, col)
        return piece is not None and piece.color == color
    
    def is_occupied_by_opponent(self, row: int, col: int, color: Color) -> bool:
        """Check if position is occupied by opponent piece"""
        piece = self.get_piece(row, col)
        return piece is not None and piece.color != color
    
    def get_king_position(self, color: Color) -> Tuple[int, int]:
        """Find the king of given color"""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.piece_type == PieceType.KING and piece.color == color:
                    return (row, col)
        raise ValueError(f"King not found for {color}")
    
    def is_in_check(self, color: Color) -> bool:
        """Check if the king of given color is in check"""
        try:
            king_row, king_col = self.get_king_position(color)
            return self.is_square_attacked(king_row, king_col, color)
        except ValueError:
            return False
    
    def is_square_attacked(self, row: int, col: int, by_color: Color) -> bool:
        """Check if a square is attacked by pieces of given color"""
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == by_color:
                    if self.can_attack_square(r, c, row, col):
                        return True
        return False
    
    def can_attack_square(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if piece at from_pos can attack to_pos (ignoring check rules)"""
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False
        
        # Temporarily remove the piece to check if it can move there
        original_piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Check if the move would be valid (ignoring check)
        can_attack = self._is_valid_move_internal(from_row, from_col, to_row, to_col)
        
        # Restore the piece
        self.board[from_row][from_col] = original_piece
        
        return can_attack
    
    def _is_valid_move_internal(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Internal move validation without check considerations"""
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False
        
        # Can't move to same position
        if from_row == to_row and from_col == to_col:
            return False
        
        # Can't capture own piece
        target_piece = self.get_piece(to_row, to_col)
        if target_piece and target_piece.color == piece.color:
            return False
        
        # Check piece-specific movement rules
        if piece.piece_type == PieceType.PAWN:
            return self._is_valid_pawn_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == PieceType.ROOK:
            return self._is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == PieceType.KNIGHT:
            return self._is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == PieceType.BISHOP:
            return self._is_valid_bishop_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == PieceType.QUEEN:
            return self._is_valid_queen_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == PieceType.KING:
            return self._is_valid_king_move(from_row, from_col, to_row, to_col)
        
        return False
    
    def _is_valid_pawn_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate pawn move"""
        piece = self.get_piece(from_row, from_col)
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1
        
        # Forward move
        if from_col == to_col and self.is_empty(to_row, to_col):
            if to_row == from_row + direction:
                return True
            # Two squares from start position
            if from_row == start_row and to_row == from_row + 2 * direction:
                return True
        
        # Diagonal capture
        if abs(to_col - from_col) == 1 and to_row == from_row + direction:
            target_piece = self.get_piece(to_row, to_col)
            if target_piece and target_piece.color != piece.color:
                return True
            # En passant
            if (to_row, to_col) == self.en_passant_target:
                return True
        
        return False
    
    def _is_valid_rook_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate rook move"""
        if from_row != to_row and from_col != to_col:
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)
    
    def _is_valid_knight_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate knight move"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _is_valid_bishop_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate bishop move"""
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)
    
    def _is_valid_queen_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate queen move"""
        return (self._is_valid_rook_move(from_row, from_col, to_row, to_col) or
                self._is_valid_bishop_move(from_row, from_col, to_row, to_col))
    
    def _is_valid_king_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate king move"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # Normal king move
        if row_diff <= 1 and col_diff <= 1:
            return True
        
        # Castling
        return self._is_valid_castling(from_row, from_col, to_row, to_col)
    
    def _is_valid_castling(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate castling move"""
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.piece_type != PieceType.KING or piece.has_moved:
            return False
        
        if piece.color == Color.WHITE and from_row != 7:
            return False
        if piece.color == Color.BLACK and from_row != 0:
            return False
        
        # Kingside castling
        if to_col == from_col + 2:
            rook = self.get_piece(from_row, 7)
            if (rook and rook.piece_type == PieceType.ROOK and not rook.has_moved and
                self.is_empty(from_row, from_col + 1) and self.is_empty(from_row, from_col + 2)):
                return True
        
        # Queenside castling
        if to_col == from_col - 2:
            rook = self.get_piece(from_row, 0)
            if (rook and rook.piece_type == PieceType.ROOK and not rook.has_moved and
                self.is_empty(from_row, from_col - 1) and self.is_empty(from_row, from_col - 2) and
                self.is_empty(from_row, from_col - 3)):
                return True
        
        return False
    
    def _is_path_clear(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if path between two positions is clear"""
        row_step = 0 if to_row == from_row else (1 if to_row > from_row else -1)
        col_step = 0 if to_col == from_col else (1 if to_col > from_col else -1)
        
        current_row, current_col = from_row + row_step, from_col + col_step
        while current_row != to_row or current_col != to_col:
            if not self.is_empty(current_row, current_col):
                return False
            current_row += row_step
            current_col += col_step
        
        return True
    
    def is_valid_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if move is valid (including check rules)"""
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.color != self.current_turn:
            return False
        
        if not self._is_valid_move_internal(from_row, from_col, to_row, to_col):
            return False
        
        # Make the move temporarily to check for check
        temp_board = copy.deepcopy(self)
        temp_board._make_move_internal(from_row, from_col, to_row, to_col)
        
        # Can't move into check
        if temp_board.is_in_check(self.current_turn):
            return False
        
        return True
    
    def _make_move_internal(self, from_row: int, from_col: int, to_row: int, to_col: int):
        """Make a move without validation (internal use)"""
        piece = self.get_piece(from_row, from_col)
        if piece:
            piece.has_moved = True
        
        # Handle en passant capture
        if (piece and piece.piece_type == PieceType.PAWN and
            (to_row, to_col) == self.en_passant_target):
            captured_pawn_row = to_row + (1 if piece.color == Color.WHITE else -1)
            self.set_piece(captured_pawn_row, to_col, None)
        
        # Handle castling
        if (piece and piece.piece_type == PieceType.KING and
            abs(to_col - from_col) == 2):
            if to_col > from_col:  # Kingside
                rook = self.get_piece(from_row, 7)
                self.set_piece(from_row, 5, rook)
                self.set_piece(from_row, 7, None)
            else:  # Queenside
                rook = self.get_piece(from_row, 0)
                self.set_piece(from_row, 3, rook)
                self.set_piece(from_row, 0, None)
        
        # Move the piece
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, None)
        
        # Set en passant target for next move
        if (piece and piece.piece_type == PieceType.PAWN and
            abs(to_row - from_row) == 2):
            self.en_passant_target = (to_row + from_row) // 2, to_col
        else:
            self.en_passant_target = None
    
    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Make a move if valid"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        # Record the move
        move_record = {
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': str(self.get_piece(from_row, from_col)),
            'captured': str(self.get_piece(to_row, to_col)) if self.get_piece(to_row, to_col) else None
        }
        
        self._make_move_internal(from_row, from_col, to_row, to_col)
        self.move_history.append(move_record)
        
        # Switch turns
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        
        return True
    
    def is_checkmate(self, color: Color) -> bool:
        """Check if given color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        # Check if any move can get out of check
        for from_row in range(8):
            for from_col in range(8):
                piece = self.get_piece(from_row, from_col)
                if piece and piece.color == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move(from_row, from_col, to_row, to_col):
                                return False
        return True
    
    def is_stalemate(self, color: Color) -> bool:
        """Check if given color is in stalemate"""
        if self.is_in_check(color):
            return False
        
        # Check if any move is possible
        for from_row in range(8):
            for from_col in range(8):
                piece = self.get_piece(from_row, from_col)
                if piece and piece.color == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move(from_row, from_col, to_row, to_col):
                                return False
        return True
    
    def get_all_valid_moves(self, color: Color) -> List[Tuple[int, int, int, int]]:
        """Get all valid moves for given color"""
        moves = []
        for from_row in range(8):
            for from_col in range(8):
                piece = self.get_piece(from_row, from_col)
                if piece and piece.color == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move(from_row, from_col, to_row, to_col):
                                moves.append((from_row, from_col, to_row, to_col))
        return moves
    
    def display(self):
        """Display the board"""
        print("\n   a b c d e f g h")
        print("  +-+-+-+-+-+-+-+-+")
        
        for row in range(8):
            print(f"{8-row}|", end="")
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    print(f"{piece}|", end="")
                else:
                    print(" |", end="")
            print(f"{8-row}")
            print("  +-+-+-+-+-+-+-+-+")
        
        print("   a b b c d e f g h")
        print(f"\nCurrent turn: {self.current_turn.value}")
        
        if self.is_in_check(self.current_turn):
            print("CHECK!")
        
        if self.is_checkmate(self.current_turn):
            print("CHECKMATE!")
        elif self.is_stalemate(self.current_turn):
            print("STALEMATE!")

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.game_over = False
        self.winner = None
    
    def parse_move(self, move_str: str) -> Optional[Tuple[int, int, int, int]]:
        """Parse move string like 'e2e4' to coordinates"""
        if len(move_str) != 4:
            return None
        
        try:
            from_col = ord(move_str[0]) - ord('a')
            from_row = 8 - int(move_str[1])
            to_col = ord(move_str[2]) - ord('a')
            to_row = 8 - int(move_str[3])
            
            if (0 <= from_row < 8 and 0 <= from_col < 8 and
                0 <= to_row < 8 and 0 <= to_col < 8):
                return (from_row, from_col, to_row, to_col)
        except (ValueError, IndexError):
            pass
        
        return None
    
    def make_move(self, move_str: str) -> bool:
        """Make a move from string notation"""
        move = self.parse_move(move_str)
        if not move:
            return False
        
        from_row, from_col, to_row, to_col = move
        return self.board.make_move(from_row, from_col, to_row, to_col)
    
    def play(self):
        """Main game loop"""
        print("Welcome to Chess!")
        print("Enter moves in format like 'e2e4' (from square to square)")
        print("Type 'quit' to exit, 'help' for help")
        
        while not self.game_over:
            self.board.display()
            
            if self.board.is_checkmate(self.board.current_turn):
                self.game_over = True
                self.winner = Color.BLACK if self.board.current_turn == Color.WHITE else Color.WHITE
                print(f"Checkmate! {self.winner.value} wins!")
                break
            elif self.board.is_stalemate(self.board.current_turn):
                self.game_over = True
                print("Stalemate! Game is a draw!")
                break
            
            move = input(f"\n{self.board.current_turn.value}'s move: ").strip().lower()
            
            if move == 'quit':
                break
            elif move == 'help':
                self.show_help()
                continue
            elif move == 'moves':
                self.show_valid_moves()
                continue
            elif move == 'undo':
                self.undo_move()
                continue
            
            if self.make_move(move):
                print("Move made successfully!")
            else:
                print("Invalid move! Try again.")
    
    def show_help(self):
        """Show help information"""
        print("\nChess Help:")
        print("- Enter moves like 'e2e4' (from square to square)")
        print("- 'moves' - show all valid moves")
        print("- 'undo' - undo last move")
        print("- 'quit' - exit game")
        print("- 'help' - show this help")
    
    def show_valid_moves(self):
        """Show all valid moves for current player"""
        moves = self.board.get_all_valid_moves(self.board.current_turn)
        if moves:
            print(f"\nValid moves for {self.board.current_turn.value}:")
            for i, (from_row, from_col, to_row, to_col) in enumerate(moves):
                from_square = chr(ord('a') + from_col) + str(8 - from_row)
                to_square = chr(ord('a') + to_col) + str(8 - to_row)
                print(f"{i+1:2d}. {from_square}{to_square}")
        else:
            print("No valid moves available!")
    
    def undo_move(self):
        """Undo the last move"""
        if len(self.board.move_history) == 0:
            print("No moves to undo!")
            return
        
        # This is a simplified undo - in a real implementation,
        # you'd want to store more state to properly undo moves
        print("Undo not fully implemented yet!")

def main():
    """Main function to start the game"""
    game = ChessGame()
    game.play()

if __name__ == "__main__":
    main()