from point import Point

class Snake:
    def __init__(self, coords, health_points, id, name, taunt):
        """Creates a Snake instance
            Args:
                coords (Point[]) Array of Point objects'
                health_points (int) Snake health_points
                id (int) Snake ID
                name (str) Snake name
                taunt (str) Snake taunt
        """
        self.coords = coords
        self.health_points = health_points
        self.id = id
        self.name = name
        self.taunt = taunt

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


    def get_head(self):
        """Returns the Point of the snake head location

            Returns:
                Point: Snake head Point
        """
        return Point(self.coords[0].x, self.coords[0].y)

