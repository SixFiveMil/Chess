#!/usr/bin/env python3
"""
Test script for the chess game.
This script runs automated tests to verify the chess game works correctly.
"""

import sys
import os
from chess import ChessBoard, ChessGame, Color, PieceType

def test_initial_setup():
    """Test that the board is set up correctly initially"""
    print("Testing initial board setup...")
    board = ChessBoard()
    
    # Check that pieces are in correct starting positions
    assert board.get_piece(0, 0).piece_type == PieceType.ROOK
    assert board.get_piece(0, 0).color == Color.BLACK
    assert board.get_piece(7, 4).piece_type == PieceType.KING
    assert board.get_piece(7, 4).color == Color.WHITE
    
    # Check that pawns are in correct positions
    for col in range(8):
        assert board.get_piece(1, col).piece_type == PieceType.PAWN
        assert board.get_piece(1, col).color == Color.BLACK
        assert board.get_piece(6, col).piece_type == PieceType.PAWN
        assert board.get_piece(6, col).color == Color.WHITE
    
    print("✓ Initial setup test passed")

def test_pawn_moves():
    """Test basic pawn moves"""
    print("Testing pawn moves...")
    board = ChessBoard()
    
    # Test valid pawn move
    assert board.is_valid_move(6, 4, 4, 4)  # e2 to e4
    assert board.make_move(6, 4, 4, 4)
    assert board.get_piece(4, 4).piece_type == PieceType.PAWN
    assert board.get_piece(6, 4) is None
    
    # Test invalid pawn move (backwards)
    assert not board.is_valid_move(4, 4, 6, 4)
    
    print("✓ Pawn moves test passed")

def test_knight_moves():
    """Test knight moves"""
    print("Testing knight moves...")
    board = ChessBoard()
    
    # Test valid knight move
    assert board.is_valid_move(7, 1, 5, 2)  # b1 to c3
    assert board.make_move(7, 1, 5, 2)
    assert board.get_piece(5, 2).piece_type == PieceType.KNIGHT
    assert board.get_piece(7, 1) is None
    
    # Test invalid knight move
    assert not board.is_valid_move(5, 2, 7, 2)  # Not a knight move
    
    print("✓ Knight moves test passed")

def test_king_moves():
    """Test king moves"""
    print("Testing king moves...")
    board = ChessBoard()
    
    # Move some pieces to clear space around king
    board.make_move(6, 4, 4, 4)  # e2 to e4
    board.make_move(1, 4, 3, 4)  # e7 to e5
    board.make_move(7, 5, 4, 2)  # f1 to c4
    board.make_move(0, 5, 2, 2)  # f8 to c5
    
    # Test valid king move
    assert board.is_valid_move(7, 4, 6, 4)  # e1 to e2
    assert board.make_move(7, 4, 6, 4)
    assert board.get_piece(6, 4).piece_type == PieceType.KING
    assert board.get_piece(7, 4) is None
    
    print("✓ King moves test passed")

def test_check_detection():
    """Test check detection"""
    print("Testing check detection...")
    board = ChessBoard()
    
    # Set up a position where white king is in check
    board.set_piece(7, 4, None)  # Remove white king
    board.set_piece(6, 4, None)  # Remove pawn
    board.set_piece(5, 4, None)  # Remove pawn
    board.set_piece(4, 4, None)  # Remove pawn
    board.set_piece(3, 4, None)  # Remove pawn
    board.set_piece(2, 4, None)  # Remove pawn
    board.set_piece(1, 4, None)  # Remove pawn
    board.set_piece(0, 4, None)  # Remove black king
    
    # Place white king and black queen
    board.set_piece(4, 4, board.Piece(Color.WHITE, PieceType.KING))
    board.set_piece(4, 0, board.Piece(Color.BLACK, PieceType.QUEEN))
    
    # White king should be in check
    assert board.is_in_check(Color.WHITE)
    
    print("✓ Check detection test passed")

def test_move_validation():
    """Test move validation"""
    print("Testing move validation...")
    board = ChessBoard()
    
    # Test that you can't move opponent's pieces
    assert not board.is_valid_move(0, 0, 1, 0)  # Try to move black rook on white's turn
    
    # Test that you can't move to same position
    assert not board.is_valid_move(7, 0, 7, 0)
    
    # Test that you can't capture your own pieces
    assert not board.is_valid_move(7, 0, 7, 1)  # Try to capture own knight
    
    print("✓ Move validation test passed")

def test_game_flow():
    """Test basic game flow"""
    print("Testing game flow...")
    game = ChessGame()
    
    # Test move parsing
    move = game.parse_move("e2e4")
    assert move == (6, 4, 4, 4)
    
    # Test invalid move parsing
    assert game.parse_move("invalid") is None
    assert game.parse_move("e2e9") is None  # Invalid square
    
    print("✓ Game flow test passed")

def run_all_tests():
    """Run all tests"""
    print("Running Chess Game Tests")
    print("=" * 40)
    
    try:
        test_initial_setup()
        test_pawn_moves()
        test_knight_moves()
        test_king_moves()
        test_check_detection()
        test_move_validation()
        test_game_flow()
        
        print("=" * 40)
        print("✓ All tests passed! Chess game is working correctly.")
        return True
        
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)