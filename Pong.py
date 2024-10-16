# Pong.py
import pygame
from paddle import Paddle
from ball import Ball

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 700, 500

PLAYER_1 = 1
PLAYER_2 = 2

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.running = True
        self.serving = True
        self.current = PLAYER_1
        self.player_1_points = 0
        self.player_2_points = 0

        self.left_paddle = Paddle(WHITE, 10, 50)
        self.left_paddle.rect.x = 20
        self.left_paddle.rect.y = 200

        self.right_paddle = Paddle(WHITE, 10, 50)
        self.right_paddle.rect.x = 670
        self.right_paddle.rect.y = 200

        self.ball = Ball(WHITE, 5)
        self.ball.spawn(self.left_paddle, PLAYER_1)

        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.left_paddle, self.right_paddle, self.ball)

    def reset_paddles(self):
        self.left_paddle.respawn(200)
        self.right_paddle.respawn(200)

    def update_points(self):
        if self.ball.rect.x <= 0:
            self.player_2_points += 1
            return True
        elif self.ball.rect.x + self.ball.rect.width >= WIDTH:
            self.player_1_points += 1
            return True
        return False

    def get_next_server(self):
        return PLAYER_2 if (self.player_1_points + self.player_2_points) % 2 == 0 else PLAYER_1
    
    def handle_input(self, keys):
        paddle_move = 5
        if not self.serving:
            if keys[pygame.K_w] and self.left_paddle.rect.y > 0:
                self.left_paddle.move_up(paddle_move)
            if keys[pygame.K_s] and self.left_paddle.rect.y < HEIGHT - self.left_paddle.rect.height:
                self.left_paddle.move_down(paddle_move)
            if keys[pygame.K_UP] and self.right_paddle.rect.y > 0:
                self.right_paddle.move_up(paddle_move)
            if keys[pygame.K_DOWN] and self.right_paddle.rect.y < HEIGHT - self.right_paddle.rect.height:
                self.right_paddle.move_down(paddle_move)

    def display_scores(self, font):
        text1 = font.render(str(self.player_1_points), True, WHITE)
        text2 = font.render(str(self.player_2_points), True, WHITE)
        screen.blit(text1, (250, 10))
        screen.blit(text2, (420, 10))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.handle_input(keys)

            if self.ball.rect.y <= 0 or self.ball.rect.y + self.ball.rect.height > HEIGHT:
                self.ball.wall_bounce()

            if self.ball.collided(self.left_paddle) or self.ball.collided(self.right_paddle):
                self.ball.paddle_bounce()

            self.all_sprites_list.update()

            screen.fill(BLACK)
            pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
            self.all_sprites_list.draw(screen)

            # Display scores
            font = pygame.font.Font(None, 74)
            self.display_scores(font)

            if self.update_points():
                self.reset_paddles()
                self.current = self.get_next_server()
                self.ball.spawn(self.left_paddle if self.current == PLAYER_1 else self.right_paddle, self.current)
                self.serving = True

            if keys[pygame.K_SPACE] and self.serving:
                self.serving = False
                self.ball.serve(self.current)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    Game().run()
