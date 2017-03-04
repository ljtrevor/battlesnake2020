from point import Point


class Snake(object):
    def __init__(self, coords, health_points, snake_id, name, taunt):
        """Creates a Snake instance
            Args:
                coords (Point[]) Array of Point objects'
                health_points (int) Snake health_points
                snake_id (int) Snake id
                name (str) Snake name
                taunt (str) Snake taunt
        """
        self.coords = coords
        self.health_points = health_points
        self.snake_id = snake_id
        self.name = name
        self.taunt = taunt

    @property
    def size(self):
        return len(self.coords)

    @staticmethod
    def from_json(json):
        coords = []
        for coord in json['coords']:
            coords.append(Point(coord[0], coord[1]))
        return Snake(
            coords,
            json['health_points'],
            json['id'],
            json['name'],
            json['taunt']
        )

    @property
    def head(self):
        """Returns the Point of the snake head location

            Returns:
                Point: Snake head Point
        """
        return self.coords[0]


