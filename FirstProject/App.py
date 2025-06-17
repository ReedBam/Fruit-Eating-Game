import pygame
import random
import math

background_color = (135, 206, 250)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Fruit Eating Game")
font = pygame.font.SysFont(None, 70)
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (100, 100))
player_x, player_y = 50, 500
sound = pygame.mixer.Sound("victory.mp3")
sound2 = pygame.mixer.Sound("Eating.mp3")

# Create fruits with positions, target positions, and timers
fruits = []
for _ in range(5):
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color != background_color:
            break
    x = random.randint(0, 750)
    y = random.randint(100, 550)
    rect = pygame.Rect(x, y, 50, 50)
    fruits.append({
        "rect": rect,
        "color": color,
        "target": [x, y],
        "last_target_time": pygame.time.get_ticks()
    })

move_cooldown_end_time = 0  # Movement cooldown tracker

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_fruits():
    for fruit in fruits:
        pygame.draw.rect(screen, fruit["color"], fruit["rect"])

def move_toward(fruit, speed, player_rect):
    x, y = fruit["rect"].topleft
    tx, ty = fruit["target"]
    dx, dy = tx - x, ty - y
    dist = math.hypot(dx, dy)

    if dist < speed or dist == 0:
        fruit["rect"].topleft = fruit["target"]
        return

    dx, dy = dx / dist, dy / dist
    next_x = x + int(dx * speed)
    next_y = y + int(dy * speed)
    next_rect = pygame.Rect(next_x, next_y, fruit["rect"].width, fruit["rect"].height)

    if next_rect.colliderect(player_rect):
        # Pick a new safe target immediately
        while True:
            new_x = random.randint(0, 750)
            new_y = random.randint(100, 550)
            new_rect = pygame.Rect(new_x, new_y, fruit["rect"].width, fruit["rect"].height)
            if not new_rect.colliderect(player_rect):
                fruit["target"] = [new_x, new_y]
                fruit["last_target_time"] = pygame.time.get_ticks()
                break
        return  # skip movement this frame

    fruit["rect"].x = next_x
    fruit["rect"].y = next_y

running = True
while running:
    current_time = pygame.time.get_ticks()
    num_fruits = len(fruits)
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Only allow player movement if cooldown is over
    if pygame.mouse.get_pressed()[0] and current_time >= move_cooldown_end_time:
        player_x, player_y = pygame.mouse.get_pos()

    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())

    for fruit in fruits[:]:
        if player_rect.colliderect(fruit["rect"]):
            fruits.remove(fruit)
            sound2.play()
            move_cooldown_end_time = current_time + 1000  # 1 second cooldown
            continue

        if fruit["rect"].topleft == tuple(fruit["target"]):
            if current_time - fruit["last_target_time"] >= 1000:
                while True:
                    new_x = random.randint(0, 750)
                    new_y = random.randint(100, 550)
                    new_rect = pygame.Rect(new_x, new_y, fruit["rect"].width, fruit["rect"].height)
                    if not new_rect.colliderect(player_rect):
                        fruit["target"] = [new_x, new_y]
                        fruit["last_target_time"] = current_time
                        break

        move_toward(fruit, speed=2, player_rect=player_rect)

    draw_fruits()
    draw_player(player_x, player_y)

    pygame.display.update()

    if num_fruits == 0:
        text_surface = font.render("You won! You ate all the fruit!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 400))  # center the text
        screen.blit(text_surface, text_rect.topleft)
        sound.play()
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        exit()

pygame.quit()
