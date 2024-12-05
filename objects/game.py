import random
from objects.player import Player
class Game:
    def __init__(self):
        self.guessed_letters = []
        self.game_status = 0
        self.WORD = "DISTRIBUTED HANGMAN"  # change this into a list with more items
        self.board = [0]
        # which turn / how many guesses made
        self.turn = 0
        # turn order as a list of player ids
        self.turnorder = []
        self.players = []
        
    def guess_letter(self, letter):
        self.guessed_letters.append(letter)
    
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

