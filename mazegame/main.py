from time import sleep
from game_manager import (
    GameManager,
)


def main() -> None:
    """Запуск игры."""

    print('Loading...')
    sleep(2)

    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
