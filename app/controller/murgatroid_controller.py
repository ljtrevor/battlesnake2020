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




