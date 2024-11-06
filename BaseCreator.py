from BaseCell import Cell
from typing import Generator

class BaseCreator:


    def __init__(self, lenght_grid):

        self.lenght_grid = lenght_grid
        self.start = None

    @property
    def root(self):
        
        if self.start is None:
            raise ValueError(f"Before using {self}.root call {self}.create")
        
        return self.start


    def __get_idx(self, idx:tuple, stack:list[list]) -> Cell:
        x, y = idx

        if isinstance(stack[x][y], Cell):
            return stack[x][y]
        
        else:
            current_node = Cell(idx)
            stack[x][y] = current_node
            return current_node


    def create_node(self, idx:tuple, 
                          current_node:Cell, 
                          stack:list[list], 
                          coming_from:str,
                          back_to:str):

        node = self.__get_idx(idx, stack)

        setattr(node, back_to, current_node)
        setattr(current_node, coming_from, node)
        

    def create(self) -> Generator[Cell, None, None]:

        stack:list[list[Cell]] = [[(x, y) for x in range(self.lenght_grid)] for y in range(self.lenght_grid)]
        copy:list[list[Cell]] = [[y for y in x.copy()] for x in stack.copy()]

        for y, row in enumerate(copy):
            for x, idx in enumerate(row):

                current_node = self.__get_idx(idx, stack)

                if 0 <= current_node.idx[0] + 1 < self.lenght_grid:

                    self.create_node(
                        (x + 1, y),
                        current_node,
                        stack,
                        'right',
                        'left'
                    )

                if 0 <= current_node.idx[0] - 1 < self.lenght_grid:

                    self.create_node(
                        (x - 1, y),
                        current_node,
                        stack,
                        'left',
                        'right'
                    )

                if 0 <= current_node.idx[1] + 1 < self.lenght_grid:

                    self.create_node(
                        (x, y + 1),
                        current_node,
                        stack,
                        'up',
                        'down'
                    )

                if 0 <= current_node.idx[1] - 1 < self.lenght_grid:

                    self.create_node(
                        (x, y - 1),
                        current_node,
                        stack,
                        'down',
                        'up'
                    )

                if (x, y) == (0, 0):
                    self.start = current_node
                    current_node.wall_down = False

                if (x, y) == (self.lenght_grid - 1, self.lenght_grid - 1):
                    current_node.wall_up = False

                yield current_node