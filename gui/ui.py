import sys
import random
import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BOARD_SIZE = (950, 750)

WORD = "DISTRIBUTED HANGMAN"  # change this into a list with more items
GUESSED_LETTERS = []

IMAGES = []
game_status = 0
'''for i in range(7):
    image = pygame.image.load((f'assets/hangman{i}.png'))
    IMAGES.append(image)'''

LETTER_BOXES = []
for row in range(2):
    for column in range(13):
        x = ((20 * column) + 80) + (40 * column)
        y = ((20 * row) + 270) + (40 * row) + 330
        box = pygame.Rect(x, y, 40, 40)
        LETTER_BOXES.append(box)

A = 65
LETTER_BUTTONS = []
for index, box in enumerate(LETTER_BOXES):
    letter = chr(A+index)
    button = ([box, letter])
    LETTER_BUTTONS.append(button)

def create_game_board():
    """ Creating game board when game starts """
    board = [0]
    return board

def print_board_in_console():
    """ Printing the game state in console """
    print("printing the board in console")

def game_start_text(turn):
    """ HANGMAN text on top of the window """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 40)
    start_text = "DISTRIBUTED HANGMAN"
    label = text_font.render(start_text, 0, RED)
    return label

def letter_text(letter):
    button_font = pygame.font.Font(pygame.font.get_default_font(), 20)
    label = button_font.render(letter, True, BLACK)
    return label

class UI:
    """ User interface for the game """
    def __init__(self):
        self.board = create_game_board()
        self.game_active = True
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("Distributed Hangman")
    
    def draw_board(self, board):
        """ Drawing the game board in pygame window """
        ''' draw board items here '''
        pygame.display.update()

    def window_top_text(self):
        text_font = pygame.font.Font(pygame.font.get_default_font(), 40)
        start_text = "DISTRIBUTED HANGMAN"
        text = text_font.render(start_text, 0, RED)
        self.screen.blit(text, (200, 15))

    def draw_letter_buttons(self, LETTER_BUTTONS):
        for button, letter in LETTER_BUTTONS:
            button_text = letter_text(letter)
            button_text_rect = button_text.get_rect(center=(button.x + 20, button.y + 20))
            pygame.draw.rect(self.screen, BLACK, button, 2)
            self.screen.blit(button_text, button_text_rect)

    def display_word(self):
        word = ""
        for letter in WORD:
            if letter in GUESSED_LETTERS:
                word += f"{letter}"
            else:
                word += "_ "
        text = letter_text(word)
        self.screen.blit(text, (500, 500))

    def game_loop(self):
        """ Game loop """
        turn = random.choice([1, 2, 3, 4])
        print("starting player:", turn)
        print_board_in_console()  #(self.board)
        pygame.init()
        self.screen.fill(WHITE)
        self.screen.blit(game_start_text(turn), (200, 15))
        self.draw_board(self.board)
        pygame.display.update()

        print("Game started")

        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    for button, letter in LETTER_BUTTONS:
                        if button.collidepoint(clicked_position):
                            print("collision with letter:", letter)
                            GUESSED_LETTERS.append(letter)
                            if letter not in WORD:
                                game_status += 1
                            # implement game end here
                            LETTER_BUTTONS.remove([button, letter])
                #self.screen.blit(IMAGES[game_status], (x, y))  # images for different stages of the game
            self.screen.fill(WHITE)
            self.window_top_text()
            self.display_word()
            self.draw_letter_buttons(LETTER_BUTTONS)
            pygame.display.update()
