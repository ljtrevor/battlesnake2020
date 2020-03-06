from point import Point


class Snake(object):
    def __init__(self, coords, health_points, snake_id, name, taunt,
            hunger_threshold=40):
        """Creates a Snake instance
            Args:
                coords (Point[]) Array of Point objects'
                health_points (int) Snake health_points
                snake_id (int) Snake id
                name (str) Snake name
                taunt (str) Snake taunt
                hunger_threshold (int): Hunger threshold
        """
        self.coords = coords
        self.health_points = health_points
        self.snake_id = snake_id
        self.name = name
        self.taunt = taunt
        self.hunger_threshold = hunger_threshold

    @property
    def size(self):
        return len(self.coords)

    @staticmethod
    def from_json(json):
        coords = []
        for coord in json['body']:
            coords.append(Point(coord['x'], coord['y']))
        return Snake(
            coords,
            json['health'],
            json['id'],
            "",
            json['shout']
        )

    @property
    def head(self):
        """Returns the Point of the snake head location

            Returns:
                Point: Snake head Point
        """
        return self.coords[0]


