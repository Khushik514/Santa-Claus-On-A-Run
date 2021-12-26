import pygame
import random
import time

pygame.init()
pygame.font.init()
pressed = None
HEIGHT = 750
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
font = pygame.font.SysFont('Comic Sans MS', 35)
pygame.display.set_caption('Santa Claus On a Run')
max_score = 0
SANTA_CLAUS = pygame.image.load('santa_claus.png')
SANTA_CLAUS_WIDTH, SANTA_CLAUS_HEIGHT = SANTA_CLAUS.get_size()
SANTA_CLAUS = pygame.transform.scale(
    SANTA_CLAUS, (SANTA_CLAUS_WIDTH // 2, SANTA_CLAUS_HEIGHT // 2))
SANTA_CLAUS_y = HEIGHT / 2
score = 0
present_images = [
    pygame.image.load('present1.png'),
    pygame.image.load('present2.png')
] * 10
PRESENT_WIDTH, PRESENT_HEIGHT = present_images[0].get_size()
present_images = [
    pygame.transform.scale(present, (PRESENT_WIDTH // 2, PRESENT_HEIGHT // 2))
    for present in present_images
]
PRESENT_SPEED = 0.5
PRESENT_index = 0
presents = []
uped = False
for i in range(5):
    presents.append([[WIDTH + PRESENT_WIDTH,
                      random.randint(0, HEIGHT)],
                     random.choice(present_images), PRESENT_SPEED])

flakes = []
for i in range(30):
    flakes.append([[random.randint(0, WIDTH),
                    random.randint(0, HEIGHT)],
                   random.randint(2, 8)])

while True:
    screen.fill((0, 0, 0))
    i = 0
    for flake in flakes:
        pygame.draw.circle(screen, (255, 255, 255), flake[0], flake[1])
        flake[0][1] += 1
        if flake[0][1] > HEIGHT + flake[1] * 2:
            flake[0][1] = 0 - flake[1] * 2
        flakes[i] = flake
        i += 1

    screen.blit(SANTA_CLAUS, (0, SANTA_CLAUS_y))

    present = presents[PRESENT_index]
    screen.blit(present[1], present[0])
    present[0][0] -= present[2]
    if present[0][0] < 0 - PRESENT_WIDTH / 2:
        score -= 1
        present[0][0] = WIDTH + PRESENT_WIDTH
        present[0][1] = random.randint(0, HEIGHT)
        if PRESENT_index < len(presents) - 1:
            PRESENT_index += 1
        else:
            PRESENT_index = 0
    present[2] = PRESENT_SPEED
    presents[PRESENT_index] = present

    SANTA_CLAUS_rect = SANTA_CLAUS.get_rect()
    SANTA_CLAUS_rect.x = 0
    SANTA_CLAUS_rect.y = SANTA_CLAUS_y

    PRESENT_rect = present[1].get_rect()
    PRESENT_rect.x = present[0][0]
    PRESENT_rect.y = present[0][1]

    present[2] = PRESENT_SPEED

    if SANTA_CLAUS_rect.colliderect(PRESENT_rect):
        score += 1
        uped = False
        if not uped:
            PRESENT_SPEED += 0.1
            uped = True
        present[0][0] = WIDTH + PRESENT_WIDTH
        present[0][1] = random.randint(0, HEIGHT)
        if PRESENT_index < len(presents) - 1:
            PRESENT_index += 1
        else:
            PRESENT_index = 0
        presents[PRESENT_index] = present
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            pressed = event.key
        elif event.type == pygame.KEYUP:
            pressed = None
    if pressed == pygame.K_UP:
        if SANTA_CLAUS_y > 0:
            SANTA_CLAUS_y -= 1
    elif pressed == pygame.K_DOWN:
        if SANTA_CLAUS_y < HEIGHT - SANTA_CLAUS_HEIGHT / 2:
            SANTA_CLAUS_y += 1
    max_score = max(score, max_score)
    score_text = font.render('Score: ' + str(score), False, (255, 255, 255))
    screen.blit(score_text, (WIDTH / 2, 0))
    if score < 0:
        text = font.render(
            "Game Over! You highest collected gifts were " + str(max_score), True,
            (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(5)
        quit()
    pygame.display.flip()