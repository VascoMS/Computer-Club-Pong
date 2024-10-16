import pygame

pygame.init()
BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.score = 0

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels

    def respawn(self, position):
        self.rect.y = position

