import pygame
import chess
import os
import chess.pgn

# Initialize pygame
pygame.init()

# Set up main display
board_size = 640
square_size = board_size // 8
window_width = board_size + 200  # Total width for board and notation
window_height = board_size
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Chess')

# Set up notation display window
notation_width = 200
notation_height = board_size
notation_window = pygame.Surface((notation_width, notation_height))
notation_window.fill(pygame.Color('white'))  # Fill with white initially

# Initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 18)

def load_pieces():
    pieces = {}
    for color in ['black', 'white']:
        for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
            piece_name = f'{color}_{piece}'
            image = pygame.image.load(os.path.join('assets', 'images', 'imgs-80px', f'{piece_name}.png'))
            pieces[piece_name] = pygame.transform.scale(image, (square_size, square_size))
    return pieces

pieces = load_pieces()

# Map chess pieces to image names
piece_to_name = {
    'p': 'black_pawn',
    'r': 'black_rook',
    'n': 'black_knight',
    'b': 'black_bishop',
    'q': 'black_queen',
    'k': 'black_king',
    'P': 'white_pawn',
    'R': 'white_rook',
    'N': 'white_knight',
    'B': 'white_bishop',
    'Q': 'white_queen',
    'K': 'white_king'
}

# Draw the board
def draw_board(last_move, board):
    colors = [pygame.Color(235, 235, 208), pygame.Color(119, 148, 85)]
    highlight_color = pygame.Color(186, 202, 68)
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            pygame.draw.rect(window, color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))

    if last_move:
        from_square = last_move.from_square
        to_square = last_move.to_square
        from_x = chess.square_file(from_square)
        from_y = 7 - chess.square_rank(from_square)
        to_x = chess.square_file(to_square)
        to_y = 7 - chess.square_rank(to_square)

        pygame.draw.rect(window, highlight_color,
                         pygame.Rect(from_x * square_size, from_y * square_size, square_size, square_size))
        pygame.draw.rect(window, highlight_color,
                         pygame.Rect(to_x * square_size, to_y * square_size, square_size, square_size))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_name = piece_to_name[piece.symbol()]
            piece_image = pieces[piece_name]
            x = chess.square_file(square)
            y = 7 - chess.square_rank(square)
            window.blit(piece_image, (x * square_size, y * square_size))


def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x = mouse_pos[0] // square_size
    y = 7 - (mouse_pos[1] // square_size)
    return chess.square(x, y)


# Display move notation in separate window
def display_move_notation(game):
    notation_window.fill(pygame.Color('white'))
    text_height = 20
    move_list = list(game.mainline_moves())
    move_strings = []
    for idx, move in enumerate(move_list):
        move_strings.append(f'{idx + 1}. {move.uci()}')

    for idx, move_string in enumerate(move_strings):
        text_surface = font.render(move_string, True, pygame.Color('black'))
        notation_window.blit(text_surface, (10, idx * text_height))

    window.blit(notation_window, (board_size, 0))  # Blit notation window next to the board

    pygame.display.flip()


# Main game loop
def main():
    game = chess.pgn.Game()  # Start a new game
    board = game.board()
    selected_square = None
    last_move = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square_under_mouse()
                piece = board.piece_at(square)
                if selected_square is None:
                    if piece and piece.color == (board.turn):
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        game = game.add_main_variation(move)
                        last_move = move
                        display_move_notation(game)  # Update move notation window
                    selected_square = None

        window.fill(pygame.Color('white'))  # Clear main window
        draw_board(last_move, board)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
