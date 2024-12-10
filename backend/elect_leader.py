import asyncio
import random
class Decisions():

    def __init__(self):
        self.playerstates = {}
        self.playerrolls = {}

    async def decide_order(self, communication, game):
        #send message to all players to elect leader
        print("Deciding order")
        await communication.send_info({'Command': 'Election'})

        asyncio.sleep(3)
        await communication.send_info({'Command': 'Ready'})
        #await ready
        print("awaiting ready")
        while True:
            await asyncio.sleep(1)
            if len(self.playerstates) == len(game.players):
                print("all players ready")
                break
        
        #after all players are ready, or 30 s have passed, start
        randomint = random.randint(1, 10000)
        #send random number between 1 and 10000
        print(f"sending random number {randomint}")
        await communication.send_info({'Command': 'ElectionRoll', 'roll': randomint})

        #check who has the largest number
        while True:
            await asyncio.sleep(1)
            if len(self.playerrolls) == len(game.players):
                print("all players have rolled")
                break
        print(self.playerrolls)
        sort = self.playerrolls.items().sort(key=lambda x: x[1])
        print(sort)
        print()
        game.turnorder = [player[0] for player in sort]
        #tiebreaker based on ip

        #send turn order to all players
        print("sending turn order")
        await communication.send_info({'Command': 'TurnOrder', 'turnorder': game.turnorder})
        print("turn order sent")

