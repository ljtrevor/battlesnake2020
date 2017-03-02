class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, point):
        """Returns true if the provided point is equal to self. False otherwise.

            Args:
                Point

            Return:
                bool

        """
        return self.x == point.x and self.y == point.y
