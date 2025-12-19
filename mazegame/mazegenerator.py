from random import shuffle


class MazeGenerator:
    """Класс для автогенерации лабиринтов."""

    @staticmethod
    def generate_maze(width: int, height: int) -> list[str]:
        """Генерация лабиринта алгоритмом Recursive Backtracking.

        Args:
            width: Ширина лабиринта(нечетное число для корректной работы алгоритма).
            height: Высота лабиринта(нечетное число для корректной работы алгоритма).

        Returns:
            Список строк, где каждая строка - ряд лабиринта.Символы: '█' - стена, ' ' - проход, '📕' - старт, '📗' -
            выход.
        """

        # Инициализация сетки (1 - стена, 0 - проход, изначально - все это стены).
        grid = [[1 for _ in range(width)] for _ in range(height)]

        # Начальная точка
        start_x, start_y = 1, 1

        # Рекурсивная генерация
        MazeGenerator._recursive_backtracking(grid, start_x, start_y, width, height)

        grid[1][1] = 0  # Старт
        grid[height - 2][width - 2] = 0  # Выход

        # Преобразуем в строки.
        result = []
        for y in range(height):
            row = []
            for x in range(width):
                if x == 1 and y == 1:
                    row.append('📕')
                elif x == width - 2 and y == height - 2:
                    row.append('📗')
                elif grid[y][x] == 1:
                    row.append('█')
                else:
                    row.append(' ')
            result.append(''.join(row))

        return result

    @staticmethod
    def _recursive_backtracking(grid: list[list[int]], x: int, y: int, width: int, height: int) -> None:
        """Рекурсивный алгоритм генерации лабиринта.

        Args:
            grid: Двумерный массив, представляющий лабиринт (1-стена, 0-проход).
            x: Текущая x-координата.
            y: Текущая y-координата.
            width: Ширина лабиринта.
            height: Высота лабиринта.
        """

        grid[y][x] = 0

        # Направления движения (шаг 2 - для создания коридоров)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

        # Случайный порядок
        shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Проверка границ (по 1 клетке для внешних стен)
            x_in_range = 1 <= nx < width - 1
            y_in_range = 1 <= ny < height - 1

            if x_in_range and y_in_range and grid[ny][nx] == 1:
                # Убираем стену между текущей и следующей ячейкой
                grid[y + dy // 2][x + dx // 2] = 0

                MazeGenerator._recursive_backtracking(grid, nx, ny, width, height)
