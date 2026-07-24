# car_game.py - Fixed button restart (final)
import pygame
import serial
import random
import sys
import os
import time

# Game setup
pygame.init()
WIDTH, HEIGHT = 800, 600
LANE_WIDTH, LANE_COUNT = 140, 3
CAR_WIDTH, CAR_HEIGHT = 80, 150
SCROLL_SPEED = 4
SPAWN_RATE = 90

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load images
def load_image(name, default_color, size):
    try:
        img = pygame.image.load(os.path.join(name))
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill(default_color)
        return surf

player_img = load_image('player_car.png', GREEN, (CAR_WIDTH, CAR_HEIGHT))
enemy_imgs = [
    load_image('enemy_car1.png', RED, (CAR_WIDTH, CAR_HEIGHT)),
    load_image('enemy_car2.png', RED, (CAR_WIDTH, CAR_HEIGHT)),
    load_image('enemy_car3.png', RED, (CAR_WIDTH, CAR_HEIGHT))
]

class Car:
    def __init__(self, lane, is_player=False):
        self.lane = lane
        self.x = WIDTH//2 - (LANE_COUNT*LANE_WIDTH)//2 + lane*LANE_WIDTH + (LANE_WIDTH-CAR_WIDTH)//2
        self.y = HEIGHT - CAR_HEIGHT - 20 if is_player else -CAR_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)
        self.is_player = is_player
        self.image = player_img if is_player else random.choice(enemy_imgs)
    
    def move(self, target_lane):
        self.lane = target_lane
        self.x = WIDTH//2 - (LANE_COUNT*LANE_WIDTH)//2 + target_lane*LANE_WIDTH + (LANE_WIDTH-CAR_WIDTH)//2
        self.rect.x = self.x

# --- Game State ---
player = Car(1, True)
enemies = []
score = 0
game_over = False
current_lane = 1

# --- Tilt Controller ---
class TiltController:
    def __init__(self):
        self.last_direction = ""
        self.cooldown = 0
        self.MIN_COOLDOWN = 20
        self.THRESHOLD = 0.6
        self.CENTER_DEADZONE = 0.4
    
    def process(self, x_value):
        if self.cooldown > 0:
            self.cooldown -= 1
        
        if self.cooldown > 0:
            return None
        
        if x_value < -self.THRESHOLD:
            if self.last_direction != "left":
                self.last_direction = "left"
                self.cooldown = self.MIN_COOLDOWN
                return "left"
        elif x_value > self.THRESHOLD:
            if self.last_direction != "right":
                self.last_direction = "right"
                self.cooldown = self.MIN_COOLDOWN
                return "right"
        else:
            if -self.CENTER_DEADZONE < x_value < self.CENTER_DEADZONE:
                self.last_direction = ""
        
        return None

tilt = TiltController()

# --- RESET FUNCTION ---
def reset_game():
    global player, enemies, score, game_over, current_lane, tilt
    player = Car(1, True)
    enemies = []
    score = 0
    game_over = False
    current_lane = 1
    tilt.last_direction = ""
    tilt.cooldown = 0
    print("🔄 Game Restarted!")

# --- CONNECT TO PICO ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    time.sleep(0.5)
    print("="*50)
    print("✅ Connected to Pico on COM3!")
    print("🎮 Car Racing Game Started!")
    print("Tilt LEFT/RIGHT to move car")
    print("Press Button or R to Restart")
    print("="*50)
    print("")
except Exception as e:
    print(f"❌ Could not connect to COM3: {e}")
    print("Using keyboard controls (← → arrows)")
    print("Press R to restart")
    print("")

def handle_input():
    global current_lane, game_over
    
    # Read from Pico
    if ser and ser.in_waiting:
        try:
            data = ser.readline().decode().strip()
            
            if data:
                # Debug - print all data
                # print(f"📥 {data}")
                pass
            
            # Process IMU data
            if data.startswith("IMU:"):
                parts = data.split(":")[1].split(",")
                if len(parts) >= 2:
                    x = float(parts[0])
                    
                    # Only move if game not over
                    if not game_over:
                        direction = tilt.process(x)
                        
                        if direction == "left" and current_lane > 0:
                            current_lane -= 1
                            print(f"⬅️ Left - Lane: {current_lane}")
                        elif direction == "right" and current_lane < 2:
                            current_lane += 1
                            print(f"➡️ Right - Lane: {current_lane}")
            
            # Process Button - ALWAYS check, regardless of game state
            elif data == "BTN:1":
                print("🔘 Button Pressed!")
                
                # Restart ALWAYS works, even if game is NOT over (for testing)
                # But we want restart only when game over
                if game_over:
                    reset_game()
                else:
                    print("   (Game not over, no restart)")
                    
        except Exception as e:
            print(f"Serial error: {e}")
            pass
    
    # Keyboard controls
    keys = pygame.key.get_pressed()
    
    # Left/Right
    if not game_over:
        if keys[pygame.K_LEFT] and current_lane > 0:
            if not hasattr(handle_input, 'key_cooldown'):
                handle_input.key_cooldown = 0
            if handle_input.key_cooldown == 0:
                current_lane -= 1
                handle_input.key_cooldown = 10
        if keys[pygame.K_RIGHT] and current_lane < 2:
            if not hasattr(handle_input, 'key_cooldown'):
                handle_input.key_cooldown = 0
            if handle_input.key_cooldown == 0:
                current_lane += 1
                handle_input.key_cooldown = 10
        
        if hasattr(handle_input, 'key_cooldown') and handle_input.key_cooldown > 0:
            handle_input.key_cooldown -= 1

def check_collision():
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            return True
    return False

# Main loop
frame_count = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # R key for restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
    
    # Update game
    if not game_over:
        handle_input()
        player.move(current_lane)
        
        frame_count += 1
        if frame_count % SPAWN_RATE == 0:
            enemies.append(Car(random.randint(0, 2)))
        
        for enemy in enemies[:]:
            enemy.y += SCROLL_SPEED
            enemy.rect.y = enemy.y
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 5
        
        game_over = check_collision()
        if game_over:
            print(f"💥 GAME OVER! Score: {score}")
            print("Press Button or R to restart")
    else:
        # Even when game over, keep reading serial for button
        handle_input()
    
    # Drawing
    screen.fill(BLACK)
    
    road_left = WIDTH//2 - (LANE_COUNT*LANE_WIDTH)//2
    pygame.draw.rect(screen, GRAY, (road_left, 0, LANE_COUNT*LANE_WIDTH, HEIGHT))
    for i in range(LANE_COUNT + 1):
        pygame.draw.line(screen, WHITE, (road_left + i*LANE_WIDTH, 0), 
                         (road_left + i*LANE_WIDTH, HEIGHT), 2)
    
    for enemy in enemies:
        screen.blit(enemy.image, (enemy.x, enemy.y))
    screen.blit(player.image, (player.x, player.y))
    
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Lane: {current_lane}", True, WHITE), (WIDTH - 120, 20))
    
    # Status
    if ser:
        status = "Pico: ✅"
    else:
        status = "Pico: ❌"
    screen.blit(font.render(status, True, WHITE), (WIDTH - 120, 50))
    
    if game_over:
        screen.blit(font.render("GAME OVER - Press R or Button to restart", True, WHITE), 
                   (WIDTH//2 - 200, HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

if ser:
    ser.close()
pygame.quit()

