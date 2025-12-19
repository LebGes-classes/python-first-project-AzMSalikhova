class Player:
    """Класс для описания действий пользователя"""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Инициализация координатов пользователя и кол-ва пройденных шагов.

        Args:
            start_x: Начальная точка по оси x.
            start_y: Начальная точка по оси y.

        Attributes:
            self.x: Текущая x-координата игрока.
            self.y: Текущая y-координата игрока.
        """

        self.x = start_x
        self.y = start_y

    def move(self, direction: str, maze) -> bool:
        """Метод для перемещения игрока в лабиринте.

        Args:
            direction: Направление(задается через стрелки).
            maze: Объект лабиринта для проверки возможности перемещения.

        Returns:
            True, если перемещение успешно выполнено,
            False - иначе.
        """

        new_x, new_y = self.x, self.y

        match direction:
            case 'up':
                new_y -= 1
            case 'down':
                new_y += 1
            case 'left':
                new_x -= 1
            case 'right':
                new_x += 1
            case _:
                return False

        if not maze.is_wall(new_x, new_y):
            self.x, self.y = new_x, new_y

            return True

        return False

    def has_reached_exit(self, maze) -> bool:
        """Метод проверяет, достиг ли игрок выхода.

        Args:
            maze: Объект лабиринта для проверки выхода.

        Returns:
            True, если текущие координаты игрока совпадают с координатами выхода,
            False - иначе.
        """

        return maze.is_exit(self.x, self.y)
