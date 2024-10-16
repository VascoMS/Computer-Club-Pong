import pygame
from random import randint


pygame.init()
BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2]).convert()

        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def serve(self, player):
        if player == 1:
            self.vel_x = randint(3, 5)
            self.vel_y = randint(-3, 3)
        if player == 2:
            self.vel_x = randint(-5, -3)
            self.vel_y = randint(-3, 3)

    def paddle_bounce(self):
        self.vel_y = randint(-3, 3)
        if self.vel_x < 0:
            self.rect.x += self.rect.width 
            self.vel_x = randint(4,8)
        else:
            self.rect.x -= self.rect.width
            self.vel_x = randint(-8,-4)

    def wall_bounce(self):
        self.vel_y = -self.vel_y

    def collided(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def spawn(self, paddle, start):
        if start == 1:
            self.rect.x = paddle.rect.x + paddle.rect.width * 2
            self.rect.y = paddle.rect.y + paddle.rect.height // 2
        elif start == 2:
            self.rect.x = paddle.rect.x - paddle.rect.width * 2
            self.rect.y = paddle.rect.y + paddle.rect.height // 2
        self.vel_x = 0
        self.vel_y = 0
