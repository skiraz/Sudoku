import pygame


class square():
    def __init__(self, window, position, area, value=0, color="white"):
        self.FONT = pygame.font.SysFont('Arial', 35)
        self.position = position
        self.border_rect = pygame.Rect(self.position, area)
        self.border_color = "black"
        self.box = pygame.Rect(position, area)
        self.box_color = color
        self.window = window
        self.wrong = 0
        self.value = value
        self.font = (0, 0, 0)

    def draw(self):
        pygame.draw.rect(self.window, self.box_color, self.box)
        self.num = self.FONT.render(str(self.value), True, self.font)
        
        if self.value:
            self.window.blit(
                self.num, (self.box.center[0]-self.num.get_width()/2, self.box.center[1]-self.num.get_height()/2))

        pygame.draw.rect(self.window, self.border_color, self.border_rect, (1))
