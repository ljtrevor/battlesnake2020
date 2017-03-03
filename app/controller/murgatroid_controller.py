from model.direction import Direction


class MurgatroidController(object):
    def __init__(self, board):
        """Creates a controller of the murgatroid variety
            Args:
                board (Board)
        """
        self.board = board
        self.murgatroid = board.get_murgatroid()

    def get_possible_directions(self, point):
        """Returns an array of possible directions from murgatroid

            Args:
                directions (Direction[])
        """
        directions = []
        murgatroid_head = self.murgatroid.head

        # Up
        if self.board.is_safe(murgatroid_head.x, murgatroid_head.y - 1):
            directions.append(Direction.UP)

        # Down
        if self.board.is_safe(murgatroid_head.x, murgatroid_head.y + 1):
            directions.append(Direction.DOWN)

        # Left
        if self.board.is_safe(murgatroid_head.x - 1, murgatroid_head.y):
            directions.append(Direction.LEFT)

        # Right
        if self.board.is_safe(murgatroid_head.x + 1, murgatroid_head.y):
            directions.append(Direction.RIGHT)

        return directions

    def seppuku(self):
        target = Point(self.murgatroid.coords[1].x, self.murgatroid.coords[1].y)

        delta = Point(
            target.x - self.murgatroid.head.x,
            target.y - self.murgatroid.head.y,
        )

        # Switch on the delta to figure out which direction Murgatroid needs
        # to go to kill itself
        if delta.x == 0 and delta.y == -1:
            return Direction.UP
        elif delta.x == 1 and delta.y == 0:
            return Direction.RIGHT
        elif delta.x == 0 and delta.y == 1:
            return Direction.DOWN
        elif delta.x == -1 and delta.y == 0:
            return Direction.LEFT
        else:
            # We shouldn't ever be in a case where the second
            # coord isn't next to the head, but better safe
            # than sorry
            return random.choice(Direction.directions)
