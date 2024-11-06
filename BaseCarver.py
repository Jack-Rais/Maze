from BaseCreator import BaseCreator
from BaseCell import Cell
import random

class BaseCarver(BaseCreator):


    def __init__(self, lenght_grid):
        super().__init__(lenght_grid)

    
    def __has_neighbours(self, node, care_visited = False):

        '''
        
        Args:
            care_visited: if the nodes are visited use True, else False.
        
        '''

        if care_visited:

            cells = [
                getattr(node, x) for x in [
                    'right', 'left', 'down', 'up'
                ] if not getattr(node, x, None) is None and \
                    getattr(getattr(node, x, None), 'visited', False)
            ]

            return cells
        
        cells = [
            (getattr(node, x), x) for x in [
                'right', 'left', 'down', 'up'
            ] if not getattr(node, x, None) is None and \
                not getattr(getattr(node, x, None), 'visited', False)
        ]

        return cells
    

    def get_idx(self, idx:tuple) -> Cell:

        if not (self.lenght_grid - 1 >= idx[0] >= 0 or \
            self.lenght_grid - 1 >= idx[1] >= 0):

            raise ValueError(f"Index {idx} is out of range for max: {self.lenght_grid - 1}")
        
        stack = [(self.root, None)]

        while len(stack) != 0:

            current_node = stack.pop(0)[0]
            setattr(current_node, 'visited', True)

            if current_node.idx[0] == idx[0] and \
                current_node.idx[1] == idx[1]:
                return current_node
            
            else:
                stack.extend(self.__has_neighbours(current_node, False))



    def set_non_visited(self):

        cells = [self.root]
        setattr(self.root, 'visited', False)

        while True:

            for _ in range(len(cells)):
                current = cells.pop(0)

                visited = self.__has_neighbours(current, True)
                [setattr(x, 'visited', False) for x in visited]
                cells.extend(visited)

            if len(cells) == 0:
                break

    
    def depth_first_search(self):

        opposite = {
                    'left': 'right',
                    'right': 'left',
                    'up': 'down',
                    'down': 'up'
                }

        setattr(self.root, 'visited', True)
        stack = [self.root]

        while len(stack) != 0:

            current = stack.pop(0)
            neighbours = self.__has_neighbours(current, False)

            if len(neighbours) != 0:
                stack.append(current)

                chosen_cell, idx_chosen = random.choice(neighbours)

                setattr(current, f'wall_{idx_chosen}', False)
                setattr(chosen_cell, f'wall_{opposite[idx_chosen]}', False)

                setattr(chosen_cell, 'visited', True)
                #stack.append(chosen_cell)
                stack.insert(0, chosen_cell)

            else:
                yield current
    