import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 832
WINDOW_HEIGHT = 832
VIEWPORT_WIDTH = 25
VIEWPORT_HEIGHT = 25
CHAR_WIDTH = 32
CHAR_HEIGHT = 32
FPS = 60
MOVE_DELAY = 0.1  # Delay in seconds between movements
CLAW_MOVE_DELAY = 0.05  # Delay in seconds between claw movements

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font settings
FONT_SIZE = 32
font = pygame.font.SysFont('Consolas', FONT_SIZE)

# Create the Pygame window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('MV Retos GameDev: Gancho!')

# Calculate character positions
start_x = WINDOW_WIDTH // 2 - (VIEWPORT_WIDTH // 2 * CHAR_WIDTH) - (CHAR_WIDTH // 2)
start_y = WINDOW_HEIGHT // 2 - (VIEWPORT_HEIGHT // 2 * CHAR_HEIGHT) - (CHAR_HEIGHT // 2)

# Character settings
character = '@'
char_x = VIEWPORT_WIDTH // 2
char_y = VIEWPORT_HEIGHT // 2

# Load the level from a text file
def load_level(filename):
    with open(filename, 'r') as file:
        level_data = [line.strip() for line in file.readlines()]
    return level_data

# Function to draw the ASCII level
def draw_level(level_data, claw_positions=None, claw_direction=None):
    window.fill(BLACK)
    
    for y in range(len(level_data)):
        for x in range(len(level_data[y])):
            char = level_data[y][x]
            color = WHITE if char != '·' else RED
            window.blit(font.render(char, True, color), (start_x + x * CHAR_WIDTH, start_y + y * CHAR_HEIGHT))
    
    # Draw the character
    window.blit(font.render(character, True, WHITE), (start_x + char_x * CHAR_WIDTH, start_y + char_y * CHAR_HEIGHT))

    # Draw the claw if it is being thrown
    if claw_positions:
        for i, pos in enumerate(claw_positions):
            claw_char = '*' if i == len(claw_positions) - 1 else ('|' if claw_direction in [(0, -1), (0, 1)] else '-')
            window.blit(font.render(claw_char, True, WHITE), (start_x + pos[0] * CHAR_WIDTH, start_y + pos[1] * CHAR_HEIGHT))

# Function to check if a move is valid
def is_valid_move(x, y, level_data):
    if level_data[y][x] in['#', 'X']:
        return False
    return True

# Function to handle the claw mechanic with animation
def handle_claw(direction, char_x, char_y, level_data):
    dx, dy = direction
    claw_positions = []
    for i in range(1, 7):
        new_x = char_x + dx * i
        new_y = char_y + dy * i
        claw_positions.append((new_x, new_y))
        draw_level(level_data, claw_positions, direction)
        pygame.display.flip()
        pygame.time.delay(int(CLAW_MOVE_DELAY * 1000))  # Delay to show the claw animation
        
        if 0 <= new_x < len(level_data[0]) and 0 <= new_y < len(level_data):
            if level_data[new_y][new_x] == 'X':
                return new_x - dx, new_y - dy
            elif level_data[new_y][new_x] == '#':
                break
    return char_x, char_y

# Function to move the character step-by-step
def move_character_to(target_x, target_y, level_data):
    global char_x, char_y
    while char_x != target_x or char_y != target_y:
        if char_x < target_x:
            char_x += 1
        elif char_x > target_x:
            char_x -= 1
        if char_y < target_y:
            char_y += 1
        elif char_y > target_y:
            char_y -= 1
        
        draw_level(level_data)
        pygame.display.flip()
        pygame.time.delay(int(MOVE_DELAY * 1000))

# Main game loop
def main():
    global char_x, char_y
    clock = pygame.time.Clock()
    level_data = load_level('level.txt')
    last_move_time = time.time()
    
    while True:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        new_x, new_y = char_x, char_y
        moved = False

        if level_data[char_y][char_x] == '·':
            print("Game Over: You fell into a hole!")
            char_x = VIEWPORT_WIDTH // 2
            char_y = VIEWPORT_HEIGHT // 2

        if keys[pygame.K_SPACE]:
            if keys[pygame.K_UP]:
                new_x, new_y = handle_claw((0, -1), char_x, char_y, level_data)
                moved = True
            elif keys[pygame.K_DOWN]:
                new_x, new_y = handle_claw((0, 1), char_x, char_y, level_data)
                moved = True
            elif keys[pygame.K_LEFT]:
                new_x, new_y = handle_claw((-1, 0), char_x, char_y, level_data)
                moved = True
            elif keys[pygame.K_RIGHT]:
                new_x, new_y = handle_claw((1, 0), char_x, char_y, level_data)
                moved = True
            if moved:
                move_character_to(new_x, new_y, level_data)
        else:
            if current_time - last_move_time > MOVE_DELAY:
                if keys[pygame.K_UP]:
                    new_y -= 1
                    moved = True
                elif keys[pygame.K_DOWN]:
                    new_y += 1
                    moved = True
                elif keys[pygame.K_LEFT]:
                    new_x -= 1
                    moved = True
                elif keys[pygame.K_RIGHT]:
                    new_x += 1
                    moved = True
                
                if moved and is_valid_move(new_x, new_y, level_data):
                    char_x, char_y = new_x, new_y
                    last_move_time = current_time
        
        draw_level(level_data)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
