import pprint

from snake import Snake
from point import Point

class Board:
    MURGATROID = u'murgatroid'
    EMPTY = u'empty'
    FOOD = u'food'
    HEAD = u'head'
    SNAKE_HEAD = u'snake_head'
    SNAKE_BODY = u'snake_body'
    SAFE = [FOOD, EMPTY]

    def __init__(self, game_id, height, width, turn, snakes, food):
        """Creates a Board instance
            Args:
                game_id (int)
                height (int)
                width (int)
                turn (int)
                snakes (Snake[])
                food (Food[])
        """
        self.game_id = game_id
        self.height = height
        self.width = width
        self.turn = turn
        self.snakes = snakes
        self.food = food

        # Populate board
        self.board = [
            [self.EMPTY for _ in range(width)]
            for _ in range(height)
        ]

        # Populate food
        for foodItem in food:
            self.board[foodItem.x][foodItem.y] = self.FOOD

        # Populate snakes
        for snake in snakes:
            coords = snake.coords

            if snake.name == self.MURGATROID:
                for coord in coords:
                    self.board[coord.x][coord.y] = self.MURGATROID
            else:
                # Set the coordinates of the head
                head = coords[0]
                self.board[head.x][head.y] = self.SNAKE_HEAD

            # Set the coordinates of the body
            for coord in coords[1:]:
                self.board[coord.x][coord.y] = self.SNAKE_BODY

    @staticmethod
    def from_json(json):
        """Creates a Board instance from the provided json

        Args:
            json (Array)

        Returns:
            Board: Board instance
        """
        snakes = []
        for snake in json['snakes']:
            snakes.append(Snake.from_json(snake))

        foods = []
        for food in json['food']:
            foods.append(Point(food[0], food[1]))

        return Board(
            json['game_id'],
            json['height'],
            json['width'],
            json['turn'],
            snakes,
            foods
        )

    def get_murgatroid(self):
        """
        Find and returns the one, the only, the great Murgatroid

        Returns:
            Snake|None: Returns murgatroid if can be found. None otherwise.


        """
        for snake in self.snakes:
            if snake.name == self.MURGATROID:
                return snake

        return None

    def get_snake(self, point):
        """Returns a Snake at a given point if exists. None otherwise.

        Returns:
            Snake|None
        """
        for snake in self.snakes:
            for coord in snake.coords:
                if coord.x == point.x and coord.y == point.y:
                    return snake

        return None

    def is_safe(self, point):
        """Returns true if the point is safe. False Otherwise

        Args:
            point (Point)

        Returns:
            bool: True if safe cell. False otherwise.
        """
        murgatroid = self.get_murgatroid()

        for snake in self.snakes:
            if snake.get_head() == point:
                if len(murgatroid.coords) > len(snake.coords):
                    return True

        return self.board[point.x][point.x] in self.SAFE



