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
