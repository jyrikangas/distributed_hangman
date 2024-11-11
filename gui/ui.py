import sys
import random
import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BOARD_SIZE = (950, 750)

def create_game_board():
    """ Creating game board when game starts """
    board = [0]
    return board

def print_board_in_console():
    """ Printing the game state in console """
    print("printing the board in console")

def game_start_text(turn):
    """ HANGMAN text on top of the window """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
    start_text = "HANGMAN"
    label = text_font.render(start_text, 0, YELLOW)
    return label

class UI:
    """ User interface for the game """
    def __init__(self):
        self.board = create_game_board()
        self.game_active = True
        self.screen = pygame.display.set_mode(BOARD_SIZE)
    
    def draw_board(self, board):
        """ Drawing the game board in pygame window """
        ''' draw board items here '''
        pygame.display.update()

    def game_loop(self):
        """ Game loop """
        turn = random.choice([1, 2, 3, 4])
        print("starting player:", turn)
        print_board_in_console()  #(self.board)
        pygame.init()
        self.screen.blit(game_start_text(turn), (300, 15))
        self.draw_board(self.board)
        pygame.display.update()

        print("Game started")

        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    ''' mouse action comes here '''
                pygame.display.update()
