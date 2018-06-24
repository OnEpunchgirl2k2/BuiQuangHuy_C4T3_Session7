import pygame
import random
from pygame.locals import *

width = 960
height = 500
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")

RED = (255, 0, 0)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
fps = 200
fps_clock = pygame.time.Clock()

class Food:
    def __init__(self, x, y, r):
        self.r = r
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.circle(display_surf, RED, (self.x, self.y), self.r)

class Snake:
    def __init__(self, x, y, r):
        self.r = r
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.circle(display_surf, BLACK, (self.x, self.y), self.r)
    def move(self, dx, dy, speed):
        self.x += dx * speed
        self.y += dy * speed
    def follow(self, i, snake_body, list_dx, list_dy):
        a = snake_body[0].x
        b = snake_body[0].y
        for k in range(i+1, 0, -1):
            if k == 1:
                a -= list_dx[1]
                b -= list_dy[1]
            else:
                a -= list_dx[k*self.r*4]*self.r*2
                b -= list_dy[k*self.r*4]*self.r*2
        self.x = a
        self.y = b
    def hit_wall(self, dx, dy):
        if self.x + dx <= 0 or self.x + dx >= 960 - self.r:
            return 1
        elif self.y + dy <= 0 or self.y + dy >= 540 - self.r:
            return 2
        else:
            return 0
    def through_wall(self, hit_wall):
        if hit_wall == 1:
            self.x = abs((960 - 2 * self.r) - self.x)
        elif hit_wall == 2:
            self.y = abs((540 - 2 * self.r) - self.y)
    def eat_food(self, dx, dy, food):
        if food.x - self.r < self.x + dx < food.x + self.r and \
                food.y - self.r < self.y + dy < food.y + self.r:
            return True
        else:
            return False
    def grow(self, snake_list):
        snake_list.insert(0, self)
    def hit_self(self, snake_list):
        for i in range(4, len(snake_list)):
            if snake_list[i].x - self.r < self.x < snake_list[i].x + self.r and \
                snake_list[i].y - self.r < self.y < snake_list[i].y + self.r:
                return True

class Game:
    def __init__(self, food, snake_body, speed, r):
        self.food = food
        self.snake_body = snake_body
        self.speed = speed
        self.r = r
    def draw_arena(self):
        display_surf.fill(WHITE)
        self.food.draw()
        for i in range(len(self.snake_body)):
            self.snake_body[i].draw()
    def update(self, list_dx, list_dy, r):
        for i in range(len(self.snake_body)):
            if self.snake_body[i].hit_wall(list_dx[i], list_dy[i]) == 1 or 2:
                self.snake_body[i].through_wall(self.snake_body[i].hit_wall(list_dx[i], list_dy[i]))
            if self.snake_body[0].eat_food(list_dx[0], list_dy[0], self.food):
                if list_dx[0] == 1:
                    Snake(self.snake_body[0].x + 2*self.r, self.snake_body[0].y, self.r).grow(self.snake_body)
                elif list_dx[0] == -1:
                    Snake(self.snake_body[0].x - 2*self.r, self.snake_body[0].y, self.r).grow(self.snake_body)
                elif list_dy[0] == 1:
                    Snake(self.snake_body[0].x, self.snake_body[0].y + 2*self.r, self.r).grow(self.snake_body)
                elif list_dy[0] == -1:
                    Snake(self.snake_body[0].x, self.snake_body[0].y - 2*self.r, self.r).grow(self.snake_body)
                del self.food
                self.food = Food(random.randrange(r, width - r), random.randrange(r, height - r), r)
            self.snake_body[i].follow(i, self.snake_body, list_dx, list_dy)
        self.snake_body[0].move(list_dx[0], list_dy[0], self.speed)



def main():
    pygame.init()
    speed = 2
    r = 10
    food = Food(random.randrange(r, width - r), random.randrange(r, height - r), r)
    snake_body = [Snake(random.randrange(r, width - r), random.randrange(r, height - r), r)]
    list_dx = [1]
    list_dy = [0]
    game = Game(food, snake_body, speed, r)
    end = False
    no_action = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == KEYDOWN and event.key == K_a and list_dx[0] != 1:
                list_dx.insert(0, -1)
                list_dy.insert(0, 0)
            elif event.type == KEYDOWN and event.key == K_d and list_dx[0] != -1:
                list_dx.insert(0, 1)
                list_dy.insert(0, 0)
            elif event.type == KEYDOWN and event.key == K_w and list_dy[0] != 1:
                list_dx.insert(0, 0)
                list_dy.insert(0, -1)
            elif event.type == KEYDOWN and event.key == K_s and list_dy[0] != -1:
                list_dx.insert(0, 0)
                list_dy.insert(0, 1)
            else:
                no_action = True
        if no_action:
            list_dx.insert(1, list_dx[0])
            list_dy.insert(1, list_dy[0])
        if snake_body[0].hit_self(snake_body):
            end = True
        if end == True:
            break
        game.draw_arena()
        game.update(list_dx, list_dy, r)
        pygame.display.update()
        fps_clock.tick(fps)

if __name__ ==  '__main__':
    main()



