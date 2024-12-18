import sys
import asyncio
import time
import pygame


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BOARD_SIZE = (950, 750)
GAME = None
IMAGES = []
for i in range(8):
    image = pygame.image.load((f'assets/hangman_image_{i}.jpg'))
    IMAGES.append(image)

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

INPUT_IP = pygame.Rect(500, 200, 140, 32)
IP = ''

def game_start_text():
    """ Drawing DISTRIBUTED HANGMAN text on top of the window """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 40)
    start_text = "DISTRIBUTED HANGMAN"
    label = text_font.render(start_text, 0, RED)
    # add text informing which player starts the game?
    return label

def letter_text(letter):
    """ Drawing letters which are placed in letter boxes """
    button_font = pygame.font.Font(pygame.font.get_default_font(), 20)
    label = button_font.render(letter, True, BLACK)
    return label


class UI:
    """ User interface for the game """
    def __init__(self):
        self.game_active = True
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("Distributed Hangman")

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
        """ Drawing letter buttons on the screen """
        for button, letter in LETTER_BUTTONS:
            if letter not in GAME.guessed_letters:
                button_text = letter_text(letter)
                button_text_rect = button_text.get_rect(center=(button.x + 20, button.y + 20))
                pygame.draw.rect(self.screen, BLACK, button, 2)
                self.screen.blit(button_text, button_text_rect)

    def display_wrong_guesses(self, image_index):
        """ Displaying wrong guesses """
        if image_index > 6:
            image_index = 6
        text_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = f"Wrong guesses: {image_index}/6"
        label = text_font.render(text, 0, BLACK)
        self.screen.blit(label, (500, 300))

    def draw_player_won_text(self):
        """ Drawing YOU WON when all letters guessed correct """
        text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text = "YOU WON!!!"
        label = text_font.render(text, 0, RED)
        self.screen.blit(label, (500, 400))
        pygame.display.update()
        time.sleep(3)

    def draw_game_over_text(self):
        """ Drawing text GAME OVER when game ends """
        text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text = "GAME OVER"
        label = text_font.render(text, 0, RED)
        self.screen.blit(label, (500, 400))
        pygame.display.update()

    async def guess_loop(self, event, communication, game):
        global all_letters_found
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_position = event.pos
            for button, letter in LETTER_BUTTONS:
                if (button.collidepoint(clicked_position)): 
                    correct_guess = game.guess_letter(letter) 
                    print("correct_guess:", correct_guess)
                    all_letters_found = True
                    for char in game.get_word():
                        if char == " ":
                            continue
                        if char not in game.get_guessed_letters():
                            all_letters_found = False
                    print("all_letters_found in the end:", all_letters_found)
                    await communication.guess(letter)
                    await communication.state()


    def display_word(self, game):
        """ Displaying the guessed word on the screen """
        word = ""
        for letter in game.get_word():
            if letter in game.get_guessed_letters():
                word += f"{letter}"
            elif letter == " ":
                word += "  "
            else:
                word += "_ "
        text = letter_text(word)
        self.screen.blit(text, (500, 500))

    async def game_loop(self, communication, game):
        """ Game loop """
        pygame.init()
        self.screen.fill(WHITE)
        self.screen.blit(game_start_text(), (200, 15))
        pygame.display.update()
        global GAME
        GAME = game
        IP= ""
        active = False
        global all_letters_found
        all_letters_found = False
        game_started = False
        print("Game started")

        while self.game_active:
            await asyncio.sleep(0.001)
            if game.wrong_guesses == 6:
                print("6 wrong_guesses, game over")
                self.draw_game_over_text()
                game.wrong_guesses += 1
            if all_letters_found:
                self.draw_player_won_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if INPUT_IP.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    if game_started:
                        print(f"round {game.round} turn {game.turn} player {game.turnorder[game.turn]}")
                    if game_started and game.turnorder[game.turn] == game.playersbyaddress[communication.host].name:
                        await self.guess_loop(event, communication, game)

                # Loop for entering IP address to connect to. If 'start' is entered, the 'ready' message is sent to other players
                # if all players are ready, the game starts.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        IP = IP[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(f"enter {IP}")
                        if IP == "start":
                            game_started = True
                            await communication.decide_order(game)
                            turn = game.turnorder[0]
                            print("starting player:", turn)
                            break
                        await communication.initiate_connection(IP)
                        #TODO: handle error!

                    else: 
                        IP += event.unicode

            self.screen.fill(WHITE)
            self.window_top_text()
            self.screen.blit(IMAGES[game.wrong_guesses], (50, 140))

            self.display_wrong_guesses(game.wrong_guesses)
            self.display_word(game)
            self.draw_letter_buttons(LETTER_BUTTONS)
            self.join_game_input(INPUT_IP, IP, active)
            pygame.display.update()
