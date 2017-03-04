from ..model.board import FOOD
from ..model.board import SNAKE_HEAD
from ..model.board import SAFE_STATES
from ..model.direction import Direction
from ..model.point import Point

import random
import sys
import math


class MurgatroidController(object):
    def __init__(self, board):
        """Creates a controller of the murgatroid variety
            Args:
                board (Board)
        """
        self.board = board
        self.murgatroid = board.get_murgatroid()
        self.use_safe_bounds = self.murgatroid.health_points > self.murgatroid.hunger_threshold
        self.safe_bounds_ranges = {
            'x': [1, board.width - 2],
            'y': [1, board.height - 2]
        }

    def get_safest_direction(self, direction_map):
        max_weight = 0
        safest_direction = None

        for direction, data in direction_map.iteritems():
            direction_weight = data['weight']
            if direction_weight > max_weight:
                max_weight = direction_weight
                safest_direction = direction

        return safest_direction

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

    def calculate_total_move_weight(self, direction, direction_map):
        def calculate_single_move_weight(point, direction, direction_map):
            safe_directions = self.get_safe_directions(point)
            if safe_directions:
                direction_map[direction]['weight'] += len(safe_up_directions)

            return direction_map

        murgatroid_head = self.murgatroid.head
        adjacent_point = murgatroid_head.increment(direction)
        direction_map[direction] = calculate_single_move_weight(
            adjacent_point,
            direction,
            direction_map[direction],
        )
        direction_map[direction] = calculate_single_move_weight(
            adjacent_point.increment(direction),
            direction,
            direction_map[direction],
        )
        return direction_map

    def get_possible_directions(self):
        """Returns an array of safe directions from murgatroid's current location

            Returns:
                directions (Direction[])

        """
        murgatroid_head = self.murgatroid.head

        # Initialize our direction map with weights
        direction_map = {
            Direction.UP: {'weight': 0},
            Direction.RIGHT: {'weight': 0},
            Direction.DOWN: {'weight': 0},
            Direction.LEFT: {'weight': 0},
        }

        # Calculate the weights of each move from our current position.
        # This takes into account the surrounding points of the points two away from
        # the snake's head in every direction.
        for direction in self.get_safe_directions(murgatroid_head):
            direction_map = self.calculate_total_move_weight(direction, direction_map)
            if direction_map[direction]['weight'] == 0:
                del direction_map[direction]

        for direction in direction_map.iterkeys():
            point = murgatroid_head.increment(direction)
            direction_map[direction]['state'] = self.board.board[point.x][point.y]

        if self.use_safe_bounds and not direction_map:
            # Expand the bounds to the 'outer ring' if we don't have any possible
            # directions after one pass
            self.use_safe_bounds = False
            direction_map = self.get_possible_directions()

        return direction_map

    def get_food_directions(self, directions_map):
        """Returns a safe directions from murgatroid to the closest food

            Returns:
                directions (Direction[])
        """
        if self.murgatroid.health_points >= self.murgatroid.hunger_threshold:
            # Casually go for food if we are next to it and not particularly
            # hungry
            return {
                direction: data
                for direction, data in directions_map.iteritems()
                if data['state'] == FOOD
            }

        food_items = self.board.food_items
        murgatroid_head = self.murgatroid.head

        closest_food = None
        for food_item in food_items:
            food_item_dict = {
                'food': food_item,
                'distance': self.absolute_distance(murgatroid_head, food_item)
            }

            if closest_food is None:
                closest_food = food_item_dict
            else:
                if food_item_dict['distance'] < closest_food['distance']:
                    closest_food = food_item_dict

        food_item = closest_food['food']

        food_map = {}
        if food_item.y < murgatroid_head.y and Direction.UP in directions_map:
            food_map[Direction.UP] = directions_map[Direction.UP]
        elif food_item.y > murgatroid_head.y and Direction.DOWN in directions_map:
            food_map[Direction.DOWN] = directions_map[Direction.DOWN]

        if food_item.x > murgatroid_head.x and Direction.RIGHT in directions_map:
            food_map[Direction.RIGHT] = directions_map[Direction.RIGHT]
        elif food_item.x < murgatroid_head.x and Direction.LEFT in directions_map:
            food_map[Direction.LEFT] = directions_map[Direction.LEFT]

        return food_map

    def get_safe_directions(self, point):
        """Returns an array of safe directions from the provided point
            Args:
                point (Point)

            Returns:
                directions (Direction[])
        """
        directions = []

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
        x_min = self.safe_bounds_ranges['x'][0] if self.use_safe_bounds else 0
        x_max = self.safe_bounds_ranges['x'][1] if self.use_safe_bounds else self.board.width - 1
        y_min = self.safe_bounds_ranges['y'][0] if self.use_safe_bounds else 0
        y_max = self.safe_bounds_ranges['y'][1] if self.use_safe_bounds else self.board.height - 1

        # If outside of bounds, return False
        if any([
            point.x > x_max,
            point.x < x_min,
            point.y > y_max,
            point.y < y_min,
        ]):
            return False

        # If point is next to a snake head, there is a chance that snake will go
        # to the same spot as us in this move.
        # We therefore only want to consider this space safe if we are bigger than
        # that snake. a snake head of a smaller snake consider it a safe space
        adjacent_snake_heads = self.get_adjacent_points(point, SNAKE_HEAD)
        for head in adjacent_snake_heads:
            if self.board.get_snake(head).size > self.murgatroid.size:
                return False

        return self.board.board[point.x][point.y] in SAFE_STATES

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

    def in_outer_ring(self, point):
        return point.x == 0 or point.x == self.board.width - 1 or point.y == 0 \
               or point.y == self.board.height - 1

    def in_absolute_bounds(self, point):
        return 0 <= point.x < self.board.width and 0 <= point.y < self.board.height

    @staticmethod
    def absolute_distance(point1, point2):
        """
        Calculate the distance between two points using the distance formula.
        """
        return math.sqrt( ( point1.x - point2.x )**2 + ( point1.y - point2.y )**2 )
