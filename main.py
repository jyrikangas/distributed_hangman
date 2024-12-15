""" Main module of the game """

import asyncio
from backend import communication_node

from gui.ui import UI
from objects.game import Game

async def main():
    """ Main function """
    game = Game()
    await asyncio.gather(communication_node.main(game),UI().game_loop(communication_node, game))

if __name__ == "__main__":
    asyncio.run(main())
