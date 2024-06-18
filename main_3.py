import time
import pygame
import chess
import csv
import sys
import math

arromode = None

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640  # Adjusted to a more practical size for a chessboard
DIM = 8
SQ_SIZE = WIDTH // DIM
MAX_FPS = 15
IMAGES = {}


def sleeep():
    sleeptime = 1
    skip_delay = False
    arromode = False
    start_time = time.time()
    while time.time() - start_time < sleeptime:  # 1-second delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    skip_delay = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if skip_delay:
            break



# Load images
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"assets/images/imgs-80px/{piece}.png"), (SQ_SIZE, SQ_SIZE))

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Draw board
def draw_board(screen, player):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[((r + c) % 2)]
            if player == "Black":
                # Invert the coordinates for Black
                pygame.draw.rect(screen, color, pygame.Rect((DIM - 1 - c) * SQ_SIZE, (DIM - 1 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw pieces on the board
def draw_pieces(screen, board, player):
    piece_to_image = {
        'P': 'wp', 'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK',
        'p': 'bp', 'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK'
    }
    for r in range(DIM):
        for c in range(DIM):
            piece = board.piece_at(chess.square(c, 7 - r))
            if piece:
                piece_image = IMAGES[piece_to_image[piece.symbol()]]
                if player == "Black":
                    # Invert the coordinates for Black
                    screen.blit(piece_image, pygame.Rect((DIM - 1 - c) * SQ_SIZE, (DIM - 1 - (7 - r)) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(piece_image, pygame.Rect(c * SQ_SIZE, (7 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def create_puzzle_dictionary(puzzle):
    return {
        'PUZZLE_CODE': puzzle[0],
        'PUZZLE_FEN': puzzle[1],
        'FIRST_MOVE': puzzle[2].split(),
        'FIRST_PUZZLE_MOVE': 'White' if puzzle[1].split()[-5] == 'w' else 'Black',
        'PUZZLE_RATING': puzzle[3],
        'PUZZLE_URL': puzzle[8]
    }


import math


def draw_arrows(screen, move, player):
    start_square = move.from_square
    end_square = move.to_square

    print(player)

    start_col = chess.square_file(start_square)
    start_row = chess.square_rank(start_square)
    end_col = chess.square_file(end_square)
    end_row = chess.square_rank(end_square)


    if player == "White":
        start_col, end_col = start_col, end_col
        start_row, end_row = start_row,end_row
    else:
        start_col, end_col = 7-start_col, 7-end_col
        start_row, end_row = 7-start_row, 7-end_row


    start_pos = (start_col * SQ_SIZE + SQ_SIZE // 2, start_row * SQ_SIZE + SQ_SIZE // 2)
    end_pos = (end_col * SQ_SIZE + SQ_SIZE // 2, end_row * SQ_SIZE + SQ_SIZE // 2)

    pygame.draw.line(screen, pygame.Color("green"), start_pos, end_pos, 15)

    # Draw arrowhead
    arrow_size = 30
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

    left_wing = (end_pos[0] + arrow_size * math.cos(angle + math.radians(150)),
                 end_pos[1] + arrow_size * math.sin(angle + math.radians(150)))
    right_wing = (end_pos[0] + arrow_size * math.cos(angle - math.radians(150)),
                  end_pos[1] + arrow_size * math.sin(angle - math.radians(150)))

    pygame.draw.polygon(screen, pygame.Color("green"), [end_pos, left_wing, right_wing])

load_images()



def main():
    global arromode
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.k_a:
                arromode = True



    with open('lichess_puzzles.csv') as puzzles_csv:
        puzzles = list(csv.reader(puzzles_csv))



    for puzzle in puzzles:
        puz = create_puzzle_dictionary(puzzle)
        puzzle_fen = puz["PUZZLE_FEN"]
        board = chess.Board(puzzle_fen)
        player = puz["FIRST_PUZZLE_MOVE"]


        move = chess.Move.from_uci(puz["FIRST_MOVE"][0])
        board.push(move)

        draw_board(screen, player)
        draw_arrows(screen, move, player)
        draw_pieces(screen, board, player)
        pygame.display.flip()

        if arromode:
            moves = puz["FIRST_MOVE"]
            for move in moves[1:]:
                move = chess.Move.from_uci(move)
                board.push(move)
                draw_arrows(screen, move, player)


        sleeep()  # Adjusted sleep time for better visualization

        moves = puz["FIRST_MOVE"]
        for move in moves[1:]:
            move = chess.Move.from_uci(move)
            board.push(move)

            draw_board(screen, player)
            draw_arrows(screen, move, player)
            draw_pieces(screen, board, player)
            pygame.display.flip()
            sleeep()  # Adjusted sleep time for better visualization

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
