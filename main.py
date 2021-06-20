import random

import pygame

# initialize pygame
pygame.init()

img = pygame.image.load("head.png")
down_img = pygame.transform.rotate(pygame.image.load("head.png"), 90)
left_img = pygame.transform.rotate(pygame.image.load("head.png"), 0)
up_img = pygame.transform.rotate(pygame.image.load("head.png"), -90)
right_img = pygame.transform.rotate(pygame.image.load("head.png"), 180)
BODY = pygame.image.load("body.png")
INSECT = pygame.image.load("insect.png")

win = pygame.display.set_mode((600, 600))
interval = 500
score = 0

font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 25)


def your_score(score):
    value = score_font.render("Score: " + str(score), True, [251, 251, 251])
    win.blit(value, [0, 0])


# SNAKE
# cord of snake
snake = [img, BODY, BODY]
snakeX = [100, 132, 164]
snakeY = [100, 100, 100]
snakeX_change = 0
snakeY_change = 0
vel = 32
stop = False
direction = "down"


# draw snake
def draw_snake(x, y, ig):
    win.blit(ig, (snakeX[0], snakeY[0]))
    for i in range(1, len(snake)):
        win.blit(snake[i], (x[i], y[i]))


# direction for each body
def snake_direction(d):
    if d == "left":
        return [-vel, 0]
    elif d == "up":
        return [0, -vel]
    elif d == "right":
        return [vel, 0]
    elif d == "down":
        return [0, vel]


# INSECT
# cords of insect
insectX = random.randint(0, 568)
insectY = random.randint(0, 568)
insect_count = 0


# draw insect
def insect(x, y):
    win.blit(INSECT, (x, y))


# check collision
def isCollide(snake_img, snakeX, snakeY, insectX, insectY):
    snake_mask = pygame.mask.from_surface(snake_img)
    insect_mask = pygame.mask.from_surface(INSECT)

    offset = (snakeX - insectX, snakeY - insectY)

    point = snake_mask.overlap(insect_mask, offset)
    if point:
        return True

    return False


# game loop
run = True
while run:
    win.fill((50, 50, 50))
    pygame.time.wait(interval)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
                img = left_img
            elif event.key == pygame.K_UP and direction != "down":
                direction = "up"
                img = up_img
            elif event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"
                img = right_img
            elif event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
                img = down_img
            elif event.key == pygame.K_SPACE:
                stop = True

    if stop:
        snakeX_change = 0
        snakeY_change = 0

    # draw score
    your_score(score)

    # insect block
    # check collision and prompt new one
    collision = isCollide(img, snakeX[0], snakeY[0], insectX, insectY)
    if collision:
        insectX = random.randint(0, 568)
        insectY = random.randint(0, 568)
        insect_count += 1
        score += 1

    # add body per three insect eaten
    if insect_count == 3:
        insect_count = 0
        snakeX.append(snakeX[len(snake) - 1])
        snakeY.append(snakeX[len(snake) - 1])
        snake.append(BODY)
        interval -= 50

    # winning condition
    if interval == 50:
        stop = True

    # call draw insect function
    insect(insectX, insectY)

    # snake block
    # snake movement
    snakeX_change = snake_direction(direction)[0]
    snakeY_change = snake_direction(direction)[1]
    for i in range(len(snake) - 1, 0, -1):
        snakeX[i] = snakeX[i - 1]
        snakeY[i] = snakeY[i - 1]
    snakeX[0] += snakeX_change
    snakeY[0] += snakeY_change

    # colloid with body
    for x in snake[:-1]:
        if x == snake[0]:
            stop = True

    # making border for snake
    if snakeX[0] < 0 and direction == "left":
        snakeX[0] = 600
    if snakeX[0] > 600 and direction == "right":
        snakeX[0] = 0
    if snakeY[0] < 0 and direction == "up":
        snakeY[0] = 600
    if snakeY[0] > 600 and direction == "down":
        snakeY[0] = 0

    # call draw snake function
    draw_snake(snakeX, snakeY, img)
    pygame.display.update()

pygame.quit()
quit()