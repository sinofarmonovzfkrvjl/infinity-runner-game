import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Multiple Borders with Gaps")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player settings
playerW = 20
playerH = 20

# Game state
playerX = 100
playerY = 50
score = 0

# Helper functions
def player(x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, playerW, playerH))

def border(gap_start, gap_end, y):
    pygame.draw.line(screen, (255, 0, 0), (0, y), (gap_start, y), 10)
    pygame.draw.line(screen, (255, 0, 0), (gap_end, y), (800, y), 10)

def generate_borders():
    new_borders = []
    for y in range(100, 600, 100):  # 100px spacing
        gap_start = random.randint(100, 600)
        gap_end = gap_start + 100
        new_borders.append({"gap_start": gap_start, "gap_end": gap_end, "y": y, "passed": False})
    return new_borders

def player_hits_any_border(x, y, w, h):
    for b in borders:
        y_pos = b["y"]
        if y_pos - 5 < y + h and y < y_pos + 5:
            if x + w < b["gap_start"] or x > b["gap_end"]:
                return True
    return False

def reset_game():
    global playerX, playerY, score, borders
    playerX = 100
    playerY = 50
    borders = generate_borders()

# Initialize first set of borders
borders = generate_borders()

# Game loop
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    newX = playerX
    newY = playerY

    if keys[pygame.K_w]:
        newY -= 3
    if keys[pygame.K_s]:
        newY += 3
    if keys[pygame.K_a]:
        newX -= 3
    if keys[pygame.K_d]:
        newX += 3

    newX = max(0, min(800 - playerW, newX))
    newY = max(0, min(600 - playerH, newY))

    if not player_hits_any_border(newX, newY, playerW, playerH):
        playerX = newX
        playerY = newY

    # Check for score increase
    for b in borders:
        if not b["passed"]:
            if playerY > b["y"]:
                if playerX + playerW > b["gap_start"] and playerX < b["gap_end"]:
                    b["passed"] = True
                    score += 1

    # Check if player passed the last border's gap
    last_border = borders[-1]
    if playerY > last_border["y"] + 10:
        if playerX + playerW > last_border["gap_start"] and playerX < last_border["gap_end"]:
            reset_game()

    # Draw
    player(playerX, playerY)
    for b in borders:
        border(b["gap_start"], b["gap_end"], b["y"])

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
