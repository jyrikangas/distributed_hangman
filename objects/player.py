""" Player module """

import random
import string

class Player:
    """ Creating class Player """

    def __init__(self, ip_address : str):
        self.ip = ip_address
        self.id = -1
        self.name = ""

    def get_ip(self):
        """ Returning player ip address """
        return self.ip

    def create_name(self,game):
        """ Creating player name """
        characters = string.ascii_letters + string.digits
        name =  ''.join(random.choices(characters, k=10))
        if name in game.playersbyaddress:
            name = name + "1"
        self.name = name
        print(f"Player {self.ip} is named {self.name}")
        return self.name

    def set_name(self, name):
        """ Setting player name """
        self.name = name
