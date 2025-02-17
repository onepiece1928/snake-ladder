import pygame
import random
import os
import time

# Set up audio driver (for Windows sound issues)
os.environ['SDL_AUDIODRIVER'] = 'directsound'

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load board image
board_img = pygame.image.load("board.png")
board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))

# Load Sounds
dice_sound = pygame.mixer.Sound("dice_roll.mp3")
snake_sound = pygame.mixer.Sound("snake_bite.mp3")
ladder_sound = pygame.mixer.Sound("ladder_climb.mp3")
move_sound = pygame.mixer.Sound("player_move.mp3")
win_sound = pygame.mixer.Sound("win_sound.mp3")  # Add a winning sound

# Set Volume
dice_sound.set_volume(1.0)
snake_sound.set_volume(1.0)
ladder_sound.set_volume(1.0)
move_sound.set_volume(1.0)
win_sound.set_volume(1.0)

# Font
font = pygame.font.Font(None, 50)

# Dice values and player positions
dice_values = [1, 1]
player_positions = [1, 1]  # Start at position 1
current_player = 0  # 0 for Player 1, 1 for Player 2
game_over = False

# Snakes and Ladders (Based on board image)
snakes = {17: 13, 52: 29, 57: 40, 62: 22, 88: 18, 95: 51, 97: 79}
ladders = {3: 21, 8: 30, 28: 84, 58: 77, 75: 86, 80: 99, 90: 91}

# Dice roll function
def roll_dice():
    return random.randint(1, 6)

# Convert board position to (x, y) coordinates
def get_position(pos):
    row = (pos - 1) // 10
    col = (pos - 1) % 10
    if row % 2 == 1:
        col = 9 - col  # Reverse direction every alternate row
    x = col * (WIDTH // 10) + 30
    y = HEIGHT - (row + 1) * (HEIGHT // 10) + 30
    return x, y

# Function to display winner message
def display_winner(player):
    screen.fill(WHITE)
    text = font.render(f"🎉 Player {player} Wins! 🎉", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    win_sound.play()  # Play winning sound
    time.sleep(3)  # Pause for 3 seconds before closing
    pygame.quit()
    exit()

# Main game loop   
running = True
while running:
    screen.fill(WHITE)
    screen.blit(board_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                dice_values[current_player] = roll_dice()
                dice_sound.play()  # 🎲 Play dice roll sound
                
                new_position = player_positions[current_player] + dice_values[current_player]

                # Update window title with dice roll
                pygame.display.set_caption(f"Snakes and Ladders - P1 Dice: {dice_values[0]} | P2 Dice: {dice_values[1]}")

                # Check if move is valid
                if new_position <= 100:
                    player_positions[current_player] = new_position
                    move_sound.play()  # 🎵 Play player move sound

                    # Check for snakes or ladders
                    if new_position in snakes:
                        snake_sound.play()  # 🐍 Play snake sound
                        print(f"Player {current_player + 1} got bitten by a snake! Moving from {new_position} to {snakes[new_position]}")
                        player_positions[current_player] = snakes[new_position]
                    elif new_position in ladders:
                        ladder_sound.play()  # 🪜 Play ladder sound
                        print(f"Player {current_player + 1} climbed a ladder! Moving from {new_position} to {ladders[new_position]}")
                        player_positions[current_player] = ladders[new_position]

                    # Check for win condition
                    if player_positions[current_player] == 100:
                        print(f"🎉 Player {current_player + 1} wins! 🎉")
                        game_over = True
                        display_winner(current_player + 1)

                    # Switch turn
                    current_player = 1 - current_player

    # Draw players
    for i in range(2):
        x, y = get_position(player_positions[i])
        color = RED if i == 0 else BLUE
        pygame.draw.circle(screen, color, (x, y), 15)

    pygame.display.flip()

pygame.quit()
