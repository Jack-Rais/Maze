from BaseCarver import BaseCarver
from BaseCell import Cell
from typing import Generator, Literal
import pygame

class BaseViewer(BaseCarver):


    def __init__(self, lenght_grid):
        super().__init__(lenght_grid)

    
    def __draw_box(self, screen:pygame.surface.Surface,
                         box:Cell,
                         length:float,
                         line_color:tuple = (0, 255, 0)) -> None:
        
        rect = pygame.Rect(
            box.idx[0] * length,
            box.idx[1] * length,
            length,
            length
        )

        rect_surface = pygame.Surface((length, length), pygame.SRCALPHA)
        rect_surface.fill((0, 255, 0, 128))

        screen.blit(rect_surface, rect.topleft)

        # Left wall
        if box.wall_left:

            pygame.draw.line(
                screen,
                line_color,
                (0, box.idx[1] * length),
                (0, (box.idx[1] + 1) * length),
                width = 3
            )

        # Down wall
        if box.wall_down:

            pygame.draw.line(
                screen,
                line_color,
                (box.idx[0] * length, 0),
                ((box.idx[0] + 1) * length, 0),
                width = 3
            )

        # Up wall
        if box.wall_up:
            pygame.draw.line(
                screen,
                line_color,
                (box.idx[0] * length, (box.idx[1] + 1) * length),
                ((box.idx[0] + 1) * length, (box.idx[1] + 1) * length),
                width = 3
            )


        # Right wall
        if box.wall_right:
            pygame.draw.line(
                screen,
                line_color,
                ((box.idx[0] + 1) * length, box.idx[1] * length),
                ((box.idx[0] + 1) * length, (box.idx[1] + 1) * length),
                width = 3
            )

    
    def draw_creation(self, screen:pygame.surface.Surface) -> Generator[Cell, None, None]:

        length = screen.get_width() / self.lenght_grid

        for box in self.create():

            self.__draw_box(screen, box, length)
            yield box

    
    def draw_carving(self, screen:pygame.surface.Surface) -> Generator[Cell, None, None]:

        length = screen.get_width() / self.lenght_grid

        for box in self.depth_first_search():

            self.__draw_box(screen, box, length)
            yield box

    def draw_boxes(self, screen:pygame.surface.Surface,
                         boxes:list[Cell],
                         last_box = False) -> Generator[Cell, None, None]:
        
        length = screen.get_width() / self.lenght_grid
        pointer_pos = pygame.surface.Surface((length, length), masks=pygame.SRCALPHA)
        pointer_pos.fill((0, 255, 0, 200))

        last = boxes[-1]

        for box in boxes:
            
            self.__draw_box(screen, box, length)

            if box == last and not last_box:
                screen.blit(pointer_pos, (box.idx[0] * length, box.idx[1] * length))

            yield box

    def draw_all(self, screen:pygame.surface.Surface) -> Generator[Cell, None, None]:
        
        length = screen.get_width() / self.lenght_grid
        pointer_pos = pygame.surface.Surface((length, length), masks=pygame.SRCALPHA)
        pointer_pos.fill((0, 255, 0, 200))

        boxes = []
        generator = self.depth_first_search()

        while True:

            boxes.append(next(generator))

            for box in boxes:
                self.__draw_box(screen, box, length)

            try:
                last = boxes[-1]
                screen.blit(pointer_pos, (last.idx[0] * length, last.idx[1] * length))

            except Exception:
                break

            yield last

            