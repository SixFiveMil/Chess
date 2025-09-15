# Chess Game

A complete, feature-rich chess game implementation in Python with full standard chess rules.

## Features

### Core Gameplay
- **Complete Chess Rules**: All standard chess rules implemented
- **Turn-based Gameplay**: White and black players alternate turns
- **Move Validation**: Comprehensive move validation for all pieces
- **ASCII Board Display**: Clean, readable board visualization with Unicode chess pieces

### Advanced Features
- **Check Detection**: Automatically detects when a king is in check
- **Checkmate Detection**: Game ends when checkmate is achieved
- **Stalemate Detection**: Handles stalemate situations
- **Castling**: Both kingside and queenside castling
- **En Passant**: Pawn capture en passant
- **Pawn Promotion**: Automatic promotion to queen (can be extended)
- **Move History**: Tracks all moves made during the game

### User Interface
- **Interactive Commands**:
  - `e2e4` - Make a move (from square to square)
  - `moves` - Show all valid moves for current player
  - `undo` - Undo last move (basic implementation)
  - `help` - Show help information
  - `quit` - Exit the game

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Running the Game
```bash
# Clone the repository
git clone https://github.com/SixFiveMil/Chess.git
cd Chess

# Run the chess game
python chess.py
```

## How to Play

1. **Start the game**: Run `python chess.py`
2. **Make moves**: Enter moves in algebraic notation (e.g., `e2e4`)
3. **View valid moves**: Type `moves` to see all possible moves
4. **Get help**: Type `help` for command reference
5. **Exit**: Type `quit` to end the game

### Move Notation
- **Format**: `from_square` + `to_square` (e.g., `e2e4`)
- **Squares**: Use standard chess notation (a1-h8)
- **Examples**:
  - `e2e4` - Move pawn from e2 to e4
  - `g1f3` - Move knight from g1 to f3
  - `e1g1` - Kingside castling

## Game Rules Implemented

### Piece Movement
- **Pawn**: Forward movement, diagonal capture, two-square initial move, en passant
- **Rook**: Horizontal and vertical movement
- **Knight**: L-shaped movement (2+1 squares)
- **Bishop**: Diagonal movement
- **Queen**: Combines rook and bishop movement
- **King**: One square in any direction, castling

### Special Rules
- **Castling**: Both kingside and queenside castling when conditions are met
- **En Passant**: Pawn capture en passant
- **Check**: Automatic detection and prevention of moves that put own king in check
- **Checkmate**: Game ends when king is in checkmate
- **Stalemate**: Game ends in draw when no legal moves available

## Code Structure

### Main Classes
- **`Piece`**: Represents individual chess pieces with color and type
- **`ChessBoard`**: Manages the 8x8 board state and piece positions
- **`ChessGame`**: Handles game flow, user input, and game logic

### Key Methods
- **`is_valid_move()`**: Validates if a move is legal
- **`make_move()`**: Executes a valid move
- **`is_in_check()`**: Checks if a king is in check
- **`is_checkmate()`**: Determines if the game is in checkmate
- **`display()`**: Shows the current board state

## Example Game Session

```
Welcome to Chess!
Enter moves in format like 'e2e4' (from square to square)
Type 'quit' to exit, 'help' for help

   a b c d e f g h
  +-+-+-+-+-+-+-+-+
8|♜|♞|♝|♛|♚|♝|♞|♜|8
  +-+-+-+-+-+-+-+-+
7|♟|♟|♟|♟|♟|♟|♟|♟|7
  +-+-+-+-+-+-+-+-+
6| | | | | | | | |6
  +-+-+-+-+-+-+-+-+
5| | | | | | | | |5
  +-+-+-+-+-+-+-+-+
4| | | | | | | | |4
  +-+-+-+-+-+-+-+-+
3| | | | | | | | |3
  +-+-+-+-+-+-+-+-+
2|♙|♙|♙|♙|♙|♙|♙|♙|2
  +-+-+-+-+-+-+-+-+
1|♖|♘|♗|♕|♔|♗|♘|♖|1
  +-+-+-+-+-+-+-+-+
   a b c d e f g h

Current turn: white

white's move: e2e4
Move made successfully!
```

## Extending the Game

### Adding Features
- **AI Player**: Implement computer opponent using minimax algorithm
- **Move Notation**: Add algebraic notation support
- **Game Saving**: Save/load games to/from files
- **Time Controls**: Add chess clocks
- **Network Play**: Multiplayer over network

### Customization
- **Piece Symbols**: Modify Unicode symbols in `Piece.__str__()`
- **Board Display**: Customize `ChessBoard.display()` method
- **Move Input**: Extend `ChessGame.parse_move()` for different notations

## Technical Details

### Performance
- **Move Generation**: Efficient O(1) move validation for most pieces
- **Check Detection**: O(n) where n is number of pieces
- **Memory Usage**: Minimal memory footprint with efficient data structures

### Code Quality
- **Type Hints**: Full type annotations for better code clarity
- **Error Handling**: Comprehensive input validation and error messages
- **Modular Design**: Clean separation of concerns between classes
- **Documentation**: Extensive docstrings and comments

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Future Enhancements

- [ ] AI opponent with different difficulty levels
- [ ] Graphical user interface (GUI)
- [ ] Network multiplayer support
- [ ] Tournament mode
- [ ] Opening book database
- [ ] Endgame tablebase support
- [ ] Mobile app version