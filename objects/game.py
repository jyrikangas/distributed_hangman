import random
from objects.player import Player
class Game:
    def __init__(self):
        self.guessed_letters = []
        self.game_status = 0
        self.WORD = "DISTRIBUTED HANGMAN"  # This should be changed at the start of the game
        self.board = [0]
        # which round / how many guesses made
        self.round = 0
        # turn order as a list of player ids
        self.turnorder = []
        self.turn = 0
        self.players = []
        
    def guess_letter(self, letter):
        self.guessed_letters.append(letter)
        
        #increment game state
        self.round += 1
        self.turn += 1
        if self.turn == len(self.players):
            self.turn = 0
        print(f"round {self.round}: Player {self.turn} guessed {letter}")
        
    
    def get_word(self):
        return self.WORD
    
    def get_guessed_letters(self):
        return self.guessed_letters
    
    #takes a list of players and decides the turn order
    def decide_turnorder(self):
        self.turnorder = [player.id for player in self.players]
        random.shuffle(self.turnorder)
        
        return self.turnorder
    
    def add_player(self, player : Player):
        self.players.append(player)
        
    def as_JSON(self):
        return {
            "guessed_letters": self.guessed_letters,
            "game_status": self.game_status,
            "WORD": self.WORD,
            "board": self.board,
            "round": self.round,
            "turnorder": self.turnorder,
            "turn": self.turn,
            "players": [player.__dict__ for player in self.players]
        }

