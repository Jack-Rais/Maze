

class Cell:

    def __init__(self, pos:tuple,
                       left = None,
                       right = None,
                       up = None,
                       down = None):

        self.idx = pos

        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.wall_left = True
        self.wall_right = True
        self.wall_up = True
        self.wall_down = True

        self.visited = None

    def __repr__(self):
        return f"{self.idx}"