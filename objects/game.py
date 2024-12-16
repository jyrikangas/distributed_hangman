import random
from gui.ui import LETTER_BUTTONS
from objects.player import Player

class Game:
    def __init__(self):
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.WORD = "DISTRIBUTED HANGMAN"
        # which round / how many guesses made
        self.round = 0
        # turn order as a list of player ids
        self.turnorder = []
        self.turn = 0
        self.players = []
        self.playersbyaddress = {}

    def guess_letter(self, letter):
        self.guessed_letters.append(letter)

        #increment game state
        self.round += 1
        self.turn += 1
        if self.turn == len(self.players):
            self.turn = 0
        print(f"round {self.round}: Player {self.turn} guessed {letter}")
        for index, item in enumerate(LETTER_BUTTONS):
            if letter == item[1]:
                del LETTER_BUTTONS[index]
                break
        if letter in self.WORD:
            return True
        self.wrong_guesses += 1
        return False

    def get_word(self):
        return self.WORD

    def get_guessed_letters(self):
        return self.guessed_letters


    def add_player(self, player : Player):
        self.playersbyaddress[player.ip] = player
        self.players.append(player)

    def update_name(self, ip, name):
        self.playersbyaddress[ip].set_name(name)
        self.players = list(self.playersbyaddress.values())


    def as_JSON(self):
        return {
            "guessed_letters": self.guessed_letters,
            "game_status": self.wrong_guesses,
            "WORD": self.WORD,
            "round": self.round,
            "turnorder": self.turnorder,
            "turn": self.turn,
            "players": [player.__dict__ for player in self.players],
        }

    def set_state(self, state):
        self.guessed_letters = state["guessed_letters"]
        self.wrong_guesses = state["game_status"]
        # self.wordlist = ["DISTRIBUTED HANGMAN", "UNIVERSITY OF HELSINKI", "SUOMI FINLAND"]
        self.WORD = state["WORD"]  # e.g. self.wordlist[random.randint(0,2)]
        # which round / how many guesses made
        self.round = state["round"]
        # turn order as a list of player ids
        self.turnorder = state["turnorder"]
        self.turn = state["turn"]

    def get_round(self):
        return self.round

    def get_players(self):
        return self.players
