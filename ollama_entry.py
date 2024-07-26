import sys

from dotenv import load_dotenv
from eval.game import Game, Player1, Player2
from loguru import logger
import logging

logger.remove()
logger.add(sys.stdout, level="INFO")
logging.getLogger('httpx').setLevel(logging.WARNING)  # suppress httpx logs from ollama package HTTP API calls

load_dotenv()


def main():
    # Environment Settings

    game = Game(
        render=True,
        save_game=True,
        player_1=Player1(
            nickname="Baby",
            model="ollama:qwen:14b-chat-v1.5-fp16",
            # model="ollama:mistral",
        ),
        player_2=Player2(
            nickname="Daddy",
            model="ollama:qwen:14b-chat-v1.5-fp16",
            # model="ollama:mistral",
        ),
    )

    game.run()
    return 0


if __name__ == "__main__":
    main()
