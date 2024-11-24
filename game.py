# start the game by writing in console: python3 game.py
from backend import communication_node
import asyncio

from gui.ui import UI

async def main():
    
    await UI().game_loop(communication_node)
    

if __name__ == "__main__":
    asyncio.run(main())
