from keyboard import KEY_DOWN, read_event, unhook_all
from time import sleep
from maze import (
    Maze,
)
from mazegenerator import (
    MazeGenerator,
)
from player import (
    Player,
)
from renderer import (
    Renderer,
)


class GameManager:
    """Класс для описания логики игры."""

    def __init__(self) -> None:
        """Инициализация процесса игры с начальными значениями.

        Attributes:
            self.renderer: Объект для отрисовки.
            self.levels_order: Порядок уровней сложности.
            self.current_maze: Текущий лабиринт.
            self.current_player: Текущий игрок.
            self.current_level_index: Индекс текущего уровня (0, 1 или 2).
        """

        self.renderer = Renderer()
        self.levels_order = ["Легкий", "Средний", "Сложный"]
        self.current_maze = None
        self.current_player = None
        self.current_level_index = 0

    @staticmethod
    def generate_maze_for_level(level_name) -> list[str]:
        """Генерирует лабиринт для указанного уровня.

        Args:
            level_name: Название уровня.

        Returns:
            Список с символами лабиринта.
        """

        level_sizes = {
            "Легкий": (15, 11),
            "Средний": (21, 15),
            "Сложный": (31, 21)
        }

        width, height = level_sizes[level_name]
        maze_data = MazeGenerator.generate_maze(width, height)

        return maze_data

    def run(self) -> None:
        """Запуск главного цикла игры."""

        running = True

        while running:
            self.renderer.render_menu()

            menuchoice = input("Выберите вариант: ")
            match menuchoice:
                case '1':
                    self.select_level()
                case '2':
                    self.renderer.render_instructions()
                case '3':
                    print("Игра успешно завершена!")

                    running = False
                case _:
                    print('Выберите корректный номер из меню!')
                    sleep(1)

    def select_level(self) -> None:
        """Обработка выбора уровня."""

        while True:
            self.renderer.render_level_selection()

            levelchoice = input("Выберите уровень: ").strip()
            match levelchoice:
                case '1':
                    self.current_level_index = 0
                    self.play_levels_from_current()
                case '2':
                    self.current_level_index = 1
                    self.play_levels_from_current()
                case '3':
                    self.current_level_index = 2
                    self.play_levels_from_current()
                case '4':
                    return
                case _:
                    print('Выберите корректный номер!')
                    sleep(1)

    def play_levels_from_current(self) -> None:
        """Запускает последовательное прохождение уровней, начиная с текущего."""

        while self.current_level_index < len(self.levels_order):
            level_name = self.levels_order[self.current_level_index]

            # Генерируем новый лабиринт для этого уровня
            maze_data = self.generate_maze_for_level(level_name)
            self.current_maze = Maze(level_name, maze_data)

            result = self.start_game(level_name)

            match result:
                case "next":
                    self.current_level_index += 1
                case "menu":
                    return
                case "restart":
                    # Переиграть текущий уровень(уже с новым лабиринтом).
                    continue
                case "restart_all":
                    self.current_level_index = 0
                    continue

    def start_game(self, level_name) -> str:
        """Запуск игры выбранного уровня.

        Args:
            level_name: Название запускаемого уровня.

        Returns:
            "next" - перейти к следующему уровню
            "menu" - вернуться в меню
            "restart" - переиграть уровень
            "restart_all" - начать все заново
        """

        self.current_player = Player(
            self.current_maze.start_x,
            self.current_maze.start_y
        )

        unhook_all()

        print(f"\nУровень: {level_name}\n" +
              "\nИспользуйте стрелки для движения. Нажмите ENTER чтобы начать...")

        # Ждем нажатия ENTER
        input()

        while True:
            # Очищаем и рисуем текущее состояние
            self.renderer.render_game(self.current_maze, self.current_player)

            # Проверка, достиг ли игрок выхода
            if self.current_player.has_reached_exit(self.current_maze):
                # Проверка, последний ли это уровень
                last_level = len(self.levels_order) - 1
                is_last_level = (self.current_level_index == last_level)

                # Показываем экран завершения уровня
                action = self.renderer.render_level_complete(
                    self.current_maze,
                    is_last_level
                )

                return action

            # Ждем нажатия клавиши(keyboard)
            event = read_event()

            if event.name == 'esc' and event.event_type == KEY_DOWN:
                return "menu"

            direction_map = {
                'up': 'up',
                'down': 'down',
                'left': 'left',
                'right': 'right'
            }

            # Нажата стрелка
            if event.name in direction_map and event.event_type == KEY_DOWN:
                self.current_player.move(direction_map[event.name], self.current_maze)
