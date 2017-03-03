class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_left_point(self):
        return Point(self.x - 1, self.y)

    def get_right_point(self):
        return Point(self.x + 1, self.y)

    def get_up_point(self):
        return Point(self.x, self.y - 1)

    def get_down_point(self):
        return Point(self.x, self.y + 1)

    def increment(self, direction):
        if direction == direction.UP:
            return self.get_up_point()
        elif direction == direction.DOWN:
            return self.get_down_point()
        elif direction == direction.LEFT:
            return self.get_left_point()
        elif direction == direction.RIGHT:
            return self.get_right_point()

    def __repr__(self):
        return '<Point x=%s, y=%s>' % (self.x, self.y)


    def __eq__(self, point):
        """Returns true if the provided point is equal to self. False otherwise.

            Args:
                Point

            Return:
                bool

        """
        return self.x == point.x and self.y == point.y
