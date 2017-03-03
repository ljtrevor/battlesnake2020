from model import board
from model.direction import Direction
from model.point import Point

import random
import sys


class MurgatroidController(object):
    def __init__(self, board):
        """Creates a controller of the murgatroid variety
            Args:
                board (Board)
        """
        self.board = board
        self.murgatroid = board.get_murgatroid()
        self.use_safe_bounds = True
        self.safe_bounds_ranges = {
            'x': [1, board.width - 2],
            'y': [1, board.height - 2]
        }

    def get_adjacent_points(self, point, state=None):
        adjacent_points = [
            point.get_left_point(),
            point.get_right_point(),
            point.get_up_point(),
            point.get_down_point(),
        ]
        if not state:
            return adjacent_points

        matching_points = [
            adj
            for adj in adjacent_points
            if self.in_absolute_bounds(adj) and self.board.board[adj.x][adj.y] == state
        ]
        return matching_points

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
        if self.is_safe(point.get_up_point()):
            directions.append(Direction.UP)

        # Down
        if self.is_safe(point.get_down_point()):
            directions.append(Direction.DOWN)

        # Left
        if self.is_safe(point.get_left_point()):
            directions.append(Direction.LEFT)

        # Right
        if self.is_safe(point.get_right_point()):
            directions.append(Direction.RIGHT)

        return directions

    def is_safe(self, point):
        """Returns true if the point is safe. False Otherwise

        Args:
            point (Point)

        Returns:
            bool: True if safe cell. False otherwise.
        """
        x_min, x_max = self.safe_bounds_ranges['x'] if self.use_safe_bounds \
                else 0, self.board.width - 1
        y_min, y_max = self.safe_bounds_ranges['y'] if self.use_safe_bounds \
                else 0, self.board.height - 1

        # If outside of bounds, return False
        if any([
            point.x >= x_max,
            point.x <= x_min,
            point.y >= y_max,
            point.y <= y_min,
        ]):
            return False

        # If point is next to a snake head, there is a chance that snake will go
        # to the same spot as us in this move.
        # We therefore only want to consider this space safe if we are bigger than
        # that snake. a snake head of a smaller snake consider it a safe space
        adjacent_snake_heads = self.get_adjacent_points(point, board.SNAKE_HEAD)
        for head in adjacent_snake_heads:
            if self.board.get_snake(head).size > self.murgatroid.size:
                return False

        return self.board.board[point.x][point.y] in board.SAFE_STATES

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

    def move_edge(self):
        murgatroid_head = self.murgatroid.head

        x_min, x_max = self.safe_bounds_ranges['x']
        y_min, y_max = self.safe_bounds_ranges['y']

        # If not on an edge, start moving towards one
        if not any(
                [murgatroid_head.x in (x_min, x_max),
                 murgatroid_head.y in (y_min, y_max)]):
            edge_distances = [
                (Direction.UP, murgatroid_head.y - y_min),
                (Direction.RIGHT, x_max - murgatroid_head.x),
                (Direction.DOWN, y_max - murgatroid_head.y),
                (Direction.LEFT, murgatroid_head.x - x_min)
            ]
            dist_min = sys.maxint

            # Find the closest edge's index
            for i, d in enumerate(edge_distances):
                if d[1] < dist_min:
                    dist_min = edge_distances[i][1]
                    index = i

            direction = edge_distances[index][0]

        elif murgatroid_head.y == y_min and x_min <= murgatroid_head.x <= x_max - 1:
            direction = Direction.RIGHT
        elif murgatroid_head.x == x_max and y_min <= murgatroid_head.y <= y_max - 1:
            direction = Direction.DOWN
        elif murgatroid_head.y == y_max and x_min + 1 <= murgatroid_head.x <= x_max:
            direction = Direction.LEFT
        else:
            direction = Direction.UP

        return direction

    def in_absolute_bounds(self, point):
        return 0 <= point.x < self.board.width and  0 <= point.y < self.board.height
