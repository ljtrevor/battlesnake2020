class Direction:
    UP = u'up'
    RIGHT = u'right'
    DOWN = u'down'
    LEFT = u'left'

    @property
    def directions(self):
        return [
            self.UP,
            self.RIGHT,
            self.DOWN,
            self.LEFT,
        ]
