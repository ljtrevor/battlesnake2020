from snake import Snake
from point import Point

MURGATROID = u'murgatroid'
EMPTY = u'empty'
FOOD = u'food'
SNAKE_HEAD = u'snake_head'
SNAKE_BODY = u'snake_body'
SAFE_STATES = [FOOD, EMPTY]


class Board(object):
    def __init__(self, game_id, height, width, turn, snakes, food_items, you):
        """Creates a Board instance
            Args:
                game_id (int)
                height (int)
                width (int)
                turn (int)
                snakes (Snake[])
                food_items (Food[])
                you (Snake)
        """
        self.game_id = game_id
        self.height = height
        self.width = width
        self.turn = turn
        self.snakes = snakes
        self.food_items = food_items
        self.you = you

        # Populate board
        self.board = [
            [EMPTY for _ in range(width)]
            for _ in range(height)
        ]

        # Populate food
        for food in food_items:
            self.board[food.x][food.y] = FOOD

        # Populate snakes
        for snake in snakes:
            coords = snake.coords

            # Set the coordinates of the head
            head = coords[0]
            self.board[head.x][head.y] = SNAKE_HEAD

            # Set the coordinates of the body
            for coord in coords[1:]:
                self.board[coord.x][coord.y] = SNAKE_BODY

        murgatroid_coords = self.you.coords
        for coord in murgatroid_coords:
            self.board[coord.x][coord.y] = MURGATROID


    @staticmethod
    def from_json(json):
        """Creates a Board instance from the provided json

        Args:
            json (Array)

        Returns:
            Board: Board instance
        """
        snakes = []
        for snake in json['board']['snakes']:
            snakes.append(Snake.from_json(snake))

        food_items = []
        for food in json['board']['food']:
            food_items.append(Point(food['x'], food['y']))

        you = Snake.from_json(json['you'])

        return Board(
            json['game']['id'],
            json['board']['height'],
            json['board']['width'],
            json['board']['turn'],
            snakes,
            food_items,
            you
        )

    def get_murgatroid(self):
        """
        Find and returns the one, the only, the great Murgatroid

        Returns:
            Snake|None: Returns murgatroid if can be found. None otherwise.
        """

        return self.you

    def get_snake(self, point):
        """Returns a Snake at a given point if exists. None otherwise.

        Returns:
            Snake|None
        """
        for snake in self.snakes:
            for coord in snake.coords:
                if coord == point:
                    return snake

        return None
