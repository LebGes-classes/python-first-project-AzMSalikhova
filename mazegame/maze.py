class Maze:
    """Класс для представления лабиринта."""

    def __init__(self, level_name: str, maze_data: list[str]) -> None:
        """Инициализация лабиринта.

        Args:
            level_name: Название уровня сложности.
            maze_data: Лабиринт определенного уровня.

        Attributes:
            level_name: Название уровня.
            self.grid: Двумерный массив символов, представляющий лабиринт.
            start_x, start_y: Координаты стартовой позиции.
            exit_x, exit_y: Координаты выхода.
        """

        self.level_name = level_name
        self.grid = [list(row) for row in maze_data]
        self.start_x, self.start_y = self._find_position('📕')
        self.exit_x, self.exit_y = self._find_position('📗')

    def _find_position(self, symbol: str) -> tuple[int, int]:
        """Нахождение координатов символа в лабиринте.

        Args:
            symbol: Символ для поиска.

        Returns:
            Кортеж с координатами символа((0, 0) - символ не найден).
        """

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == symbol:

                    return x, y

        return 0, 0

    def is_wall(self, x: int, y: int) -> bool:
        """Проверка, является ли символ стеной.

        Args:
            x: Координата по оси x.
            y: Координата по оси y.

        Returns:
            True, если символ - это строка или символ за пределами лабиринта,
            False - иначе.
        """

        if y < 0 or y >= len(self.grid):

            return True
        if x < 0 or x >= len(self.grid[y]):

            return True

        return self.grid[y][x] == '█'

    def is_exit(self, x: int, y: int) -> bool:
        """Проверка, является ли символ выходом.

        Args:
            x: Координата по оси x.
            y: Координата по оси y.

        Returns:
            True, если заданные координаты совпадают с координатами выхода,
            False - иначе.
        """

        return x == self.exit_x and y == self.exit_y

    def get_width(self) -> int:
        """Геттер для лабиринта.

        Returns:
            Ширина лабиринта.
        """

        return len(self.grid[0]) if self.grid else 0

    def get_height(self) -> int:
        """Геттер для лабиринта.

        Returns:
            Длина лабиринта.
        """

        return len(self.grid)

    def get_size_info(self) -> str:
        """Возвращает информацию о размере лабиринта.

        Returns:
            Строка в формате "ширина x высота".
        """

        return f"{self.get_width()} x {self.get_height()}"
