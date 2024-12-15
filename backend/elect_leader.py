""" Leader election module """

import asyncio
import random
import os

class Decisions():
    """ Decisions class """

    def __init__(self):
        self.playerstates = {}
        self.playerrolls = {}

    async def decide_order(self, communication, game):
        """ Send message to all players to elect leader """
        print("Deciding order")
        await communication.send_info({'Command': 'Election'})

        """
        #await ready
        print("awaiting ready")
        while True:
            print(game.playerstates)
            await communication.send_info({'Command': 'Ready'})
            if len(game.playerstates) == len(game.players)-1:
                print("all players ready")
                break
        """
        #after all players are ready, or 30 s have passed, start
        randomint = random.randint(1, 10000)
        game.playerrolls[os.getenv('HOST')] = randomint
        for _ in range(15):
            #send random number between 1 and 10000
            print(f"sending random number {randomint}")
            await communication.send_info({'Command': 'ElectionRoll', 'roll': randomint})

            #check who has the largest number
            await asyncio.sleep(1)
        while True:
            await asyncio.sleep(1)
            if len(game.playerrolls) == len(game.players):
                print("all players have rolled")
                break
        print(game.playerrolls)
        sort = sorted(game.playerrolls.items(), key=lambda x: x[1], reverse=True)
        print(sort)
        print()
        game.turnorder = [player[0] for player in sort]
        #tiebreaker based on ip

        #send turn order to all players
        print("sending turn order")
        await communication.send_info({'Command': 'TurnOrder', 'turnorder': game.turnorder})
        print("turn order sent")
