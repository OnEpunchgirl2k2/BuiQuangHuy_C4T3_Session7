import pygame
from pygame.locals import *

width = 960
height = 600
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG PAN")

WHITE = (255, 225, 225)
fps = 200
fps_clock = pygame.time.Clock()
3
class Paddle:
    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.rect(display_surf, WHITE, (self.x, self.y, self.w, self.h))
    def move(self, pos):
        self.y = pos[1] - self.h/2
        if self.y < 0:
            self.y = 0
        if self.y > height - self.h:
            self.y = height - self.h

class AutoPaddle(Paddle):
    def __init__(self, w, h, x, y, speed):
        super().__init__(w, h, x, y)
        self.speed = speed
    def move(self, ball):
        self.y = ball.y - self.h/2
        if self.y < 0:
            self.y = 0
        if self.y > height - self.h:
            self.y = height - self.h


class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.dir_x = 1.2
        self.dir_y = 1
    def draw(self):
        pygame.draw.rect(display_surf, WHITE, (self.x, self.y, self.w, self.h))
    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.speed += 0.0005
    def bounce(self, axis):
        if axis == 'x':
            self.dir_y *= -1
        elif axis == 'y':
            self.dir_x *= -1
    def HitCeiling(self):
        if self.y <= 0:
            return True
        else:
            return False
    def HitFloor(self):
        if self.y >= height - self.h:
            return True
        else:
            return False
    def HitPaddle(self, paddle):
        if paddle.y - self.h <= self.y <= paddle.y + paddle.h and\
                self.x <= paddle.x + paddle.w:
            return True
        else:
            return False
    def HitAutoPaddle(self, AutoPaddle):
        if AutoPaddle.y - self.h <= self.y <= AutoPaddle.y + AutoPaddle.h and \
                self.x >= AutoPaddle.x - self.w:
            return True
        else:
            return False
    def HitWall(self):
        if self.x <= 0 or self.x >= width - self.w:
            return True
        else:
            return False

class ScoreBoard:
    def __init__(self, x, y, score, size):
        self.x = x
        self.y = y
        self.score = score
        self.size = size
        self.font = pygame.font.Font(None, self.size)
    def display(self):
        display_score = self.font.render("Score: " + str(self.score), True, WHITE)
        display_surf.blit(display_score, (self.x, self.y))



class Game:
    def __init__(self, ball, paddle, autoPaddle, scoreBoard, speed):
        self.speed = speed
        self.ball = ball
        self.paddle = paddle
        self.autoPaddle = autoPaddle
        self.scoreBoard = scoreBoard
    def draw_arena(self):
        display_surf.fill((30, 225, 60))
        pygame.draw.line(display_surf, WHITE, (width/2, 0), (width/2, height), 5)
        pygame.draw.circle(display_surf, WHITE, (int(width/2), int(height/2)), 120, 5)
        self.paddle.draw()
        self.ball.draw()
        self.autoPaddle.draw()
        self.scoreBoard.display()
    def update(self, pos):
        if self.ball.HitCeiling() or self.ball.HitFloor():
            self.ball.bounce('x')
        if self.ball.HitPaddle(self.paddle):
            self.ball.bounce('y')
            self.scoreBoard.score += 1
        if self.ball.HitAutoPaddle(self.autoPaddle):
            self.ball.bounce('y')
        if self.ball.HitWall():
            self.ball.bounce('y')
            self.scoreBoard.score -= 1
        self.ball.move()
        self.paddle.move(pos)
        self.autoPaddle.move(self.ball)

def Main():
    speeed = 1.5
    pygame.init()
    ball = Ball(width/2, height/2, 10, 10, speeed)
    paddle = Paddle(10, 120, 0, height/2)
    autoPaddle = AutoPaddle(10, 120, width - 10, height/2, speeed)
    scoreBoard = ScoreBoard(150, 20, 0, 20)
    game = Game(ball, paddle, autoPaddle, scoreBoard, speeed)
    mousePos = [10, 10]
    flag = False
    while True:
            if scoreBoard.score <= -1:
                Ball.speed = 0
                font = pygame.font.Font(None, 100)
                display_result = font.render("Game over!", True, (225, 0, 0))
                display_surf.blit(display_result, (width / 2 - 180, height / 2 - 45))
                pygame.display.update()
                break

            for event in pygame.event.get():
                    if event.type == QUIT:
                        flag = True
                    if flag:
                        quit()
                    if event.type == MOUSEMOTION:
                        mousePos = pygame.mouse.get_pos()
            game.draw_arena()
            game.update(mousePos)
            pygame.display.update()
            fps_clock.tick(fps)

if __name__ ==  '__main__':
    Main()






