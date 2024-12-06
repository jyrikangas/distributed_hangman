
class Player:
    def __init__(self, ip_address : str, playerid : int):
        self.ip = ip_address
        self.id = playerid

    def get_ip(self):
        return self.ip