import sys
import random
import pygame
import asyncio
from objects.player import Player

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BOARD_SIZE = (950, 750)

IMAGES = []
#game_status = 0
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

INPUT_IP = pygame.Rect(200, 200, 140, 32) 
IP = ''

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
        self.board = [0]
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

    def join_game_input(self, INPUT_IP, IP="", active=False):
        text_font = pygame.font.Font(pygame.font.get_default_font(), 40)

        color_active = pygame.Color('lightskyblue3') 

        color_passive = pygame.Color('chartreuse4') 
        if active:
            color = color_active
        else:
            color = color_passive

        text = text_font.render(IP, True, BLACK)
        pygame.draw.rect(self.screen, color, INPUT_IP) 
        INPUT_IP.w = max(100, text.get_width()+10) 
        
        self.screen.blit(text,INPUT_IP)
        



    def draw_letter_buttons(self, LETTER_BUTTONS):
        for button, letter in LETTER_BUTTONS:
            button_text = letter_text(letter)
            button_text_rect = button_text.get_rect(center=(button.x + 20, button.y + 20))
            pygame.draw.rect(self.screen, BLACK, button, 2)
            self.screen.blit(button_text, button_text_rect)

    def display_word(self, game):
        word = ""
        for letter in game.get_word():
            if letter in game.get_guessed_letters():
                word += f"{letter}"
            else:
                word += "_ "
        text = letter_text(word)
        self.screen.blit(text, (500, 500))

    async def game_loop(self, communication, game):
        """ Game loop """
        
        turn = random.choice([1, 2, 3, 4])
        print("starting player:", turn)
        print_board_in_console()  #(self.board)
        pygame.init()
        self.screen.fill(WHITE)
        self.screen.blit(game_start_text(turn), (200, 15))
        self.draw_board(self.board)
        pygame.display.update()
        IP= ""
        active = False
        
        print("Game started")

        while self.game_active:
            await asyncio.sleep(0.001)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    for button, letter in LETTER_BUTTONS:
                        if (button.collidepoint(clicked_position)): #  and (game.turnorder[game.turnorder[game.turn]] == 1)):
                            print("collision with letter:", letter)
                            # kutsu game.guess letter. palauttaa true/false
                            game.guess_letter(letter)
                            await communication.guess(letter)
                            
                            # jos true, tee jotain napille
                            LETTER_BUTTONS.remove([button, letter])
                            

                    if INPUT_IP.collidepoint(event.pos): 
                        active = True
                    else: 
                        active = False

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_BACKSPACE: 
                        IP = IP[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(f"enter {IP}")

                        await communication.initiate_connection(IP)
                        #TODO: handle error!
                        game.add_player(Player(IP, len(game.players) + 1))
                        
                    else: 
                        IP += event.unicode
                #self.screen.blit(IMAGES[game_status], (x, y))  # images for different stages of the game
            self.screen.fill(WHITE)
            self.window_top_text()

            self.display_word(game)
            self.draw_letter_buttons(LETTER_BUTTONS)
            self.join_game_input(INPUT_IP, IP, active)
            pygame.display.update()
