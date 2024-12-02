
class Game:
    def __init__(self):
        self.guessed_letters = []
        self.game_status = 0
        self.WORD = "DISTRIBUTED HANGMAN"  # change this into a list with more items
        self.board = [0]
        
    def guess_letter(self, letter):
        self.guessed_letters.append(letter)
    
    def get_word(self):
        return self.WORD
    
    def get_guessed_letters(self):
        return self.guessed_letters
    


