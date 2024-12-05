# start the game by writing in console: python3 game.py
from backend import communication_node
import asyncio

from gui.ui import UI
from objects.game import Game


async def main():
    game = Game()
    await asyncio.gather(communication_node.main(game),UI().game_loop(communication_node, game))
    

if __name__ == "__main__":
    asyncio.run(main())
