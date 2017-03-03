from model.direction import Direction
from model.point import Point

import random


class MurgatroidController(object):
    def __init__(self, board):
        """Creates a controller of the murgatroid variety
            Args:
                board (Board)
        """
        self.board = board
        self.murgatroid = board.get_murgatroid()

    def get_possible_directions(self):
        """Returns an array of safe directions from murgatroid's current location

            Returns:
                directions (Direction[])

        """
        murgatroid_head = self.murgatroid.head

        # Get safe directions from current point
        cur_safe_directions = self.get_safe_directions(murgatroid_head)

        look_ahead_directions_map = {}
        for direction in cur_safe_directions:
            if direction == Direction.UP:
                num_safe_up_directions = \
                    len(self.get_safe_directions(murgatroid_head.get_up_point()))
                look_ahead_directions_map[Direction.UP] = num_safe_up_directions
            elif direction == Direction.DOWN:
                num_safe_down_directions = \
                    len(self.get_safe_directions(murgatroid_head.get_down_point()))
                look_ahead_directions_map[Direction.DOWN] = num_safe_down_directions
            elif direction == Direction.LEFT:
                num_safe_left_directions = \
                    len(self.get_safe_directions(murgatroid_head.get_left_point()))
                look_ahead_directions_map[Direction.LEFT] = num_safe_left_directions
            elif direction == Direction.RIGHT:
                num_safe_right_directions = \
                    len(self.get_safe_directions(murgatroid_head.get_right_point()))
                look_ahead_directions_map[Direction.RIGHT] = num_safe_right_directions
        print look_ahead_directions_map

    def get_safe_directions(self, point):
        """Returns an array of safe directions from the provided point
            Args:
                point (Point)

            Returns:
                directions (Direction[])
        """
        directions = []
        murgatroid_head = self.murgatroid.head

        # Up
        if self.board.is_safe(point.get_up_point()):
            directions.append(Direction.UP)

        # Down
        if self.board.is_safe(point.get_down_point()):
            directions.append(Direction.DOWN)

        # Left
        if self.board.is_safe(point.get_left_point()):
            directions.append(Direction.LEFT)

        # Right
        if self.board.is_safe(point.get_right_point()):
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
            # If somehow we're trapped on the first turn where we just have our
            # head and no other spaces with snake coordinates, just go in a
            # random direction
            return random.choice([
                Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT,
            ])
