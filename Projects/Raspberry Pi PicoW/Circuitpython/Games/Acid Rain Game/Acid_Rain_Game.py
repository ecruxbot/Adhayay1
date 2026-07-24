# Acid_Rain_Game.py - Fixed with Y axis inverted
import pygame
import serial
import math
import time
import random

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚖️ Acid_Rain_Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
GRAY = (100, 100, 100)

# Ball
ball_x, ball_y = WIDTH//2, HEIGHT//2
ball_radius = 20
ball_speed = 10

# Game state
score = 0
lives = 3
game_over = False
obstacles = []
obstacle_spawn_rate = 20
obstacle_speed = 4

# --- CALIBRATION ---
class Calibration:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.calibrated = False
        self.samples = 50
        self.sample_count = 0
        self.x_readings = []
        self.y_readings = []
    
    def start(self):
        self.calibrated = False
        self.sample_count = 0
        self.x_readings = []
        self.y_readings = []
        print("🔧 Calibrating... Keep Pico STILL!")
    
    def add_sample(self, x, y):
        self.x_readings.append(x)
        self.y_readings.append(y)
        self.sample_count += 1
        
        if self.sample_count >= self.samples:
            self.offset_x = sum(self.x_readings) / len(self.x_readings)
            self.offset_y = sum(self.y_readings) / len(self.y_readings)
            self.calibrated = True
            print(f"✅ Calibration Done!")
            print(f"   X Offset: {self.offset_x:.2f}")
            print(f"   Y Offset: {self.offset_y:.2f}")
            return True
        return False
    
    def process(self, x, y):
        if self.calibrated:
            return x - self.offset_x, y - self.offset_y
        return x, y

calibration = Calibration()

# --- SERIAL ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    print("="*50)
    print("✅ Connected to Pico!")
    print("⚖️ Acid_Rain_Game Ball Game Started!")
    print("="*50)
    print("")
except Exception as e:
    print(f"❌ Pico not connected: {e}")
    print("Using mouse controls")
    print("")

# Start calibration
calibration.start()

def reset_game():
    global ball_x, ball_y, score, game_over, lives, obstacles
    ball_x, ball_y = WIDTH//2, HEIGHT//2
    score = 0
    game_over = False
    obstacles = []
    lives = 3
    print("🔄 Game Restarted!")

def handle_input():
    global ball_x, ball_y
    
    if ser and ser.in_waiting:
        try:
            while ser.in_waiting:
                data = ser.readline().decode().strip()
                
                if data.startswith("IMU:"):
                    parts = data.split(":")[1].split(",")
                    if len(parts) >= 2:
                        raw_x = float(parts[0])
                        raw_y = float(parts[1])
                        
                        # --- CALIBRATION ---
                        if not calibration.calibrated:
                            calibration.add_sample(raw_x, raw_y)
                            progress = (calibration.sample_count / calibration.samples) * 100
                            print(f"Calibration: {int(progress)}%", end='\r')
                            continue
                        
                        # --- GAME ---
                        x = raw_x - calibration.offset_x
                        y = raw_y - calibration.offset_y
                        
                        # 🔥 FIX: Invert Y axis (UP = negative, DOWN = positive)
                        y = -y
                        
                        # Deadzone
                        deadzone = 0.15
                        if abs(x) < deadzone:
                            x = 0
                        if abs(y) < deadzone:
                            y = 0
                        
                        # Move ball
                        if not game_over:
                            ball_x += x * ball_speed
                            ball_y += y * ball_speed
                            ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))
                            ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))
                
                elif data == "BTN:1":
                    if game_over:
                        reset_game()
                    else:
                        print("🔘 Button Pressed!")
                        
        except Exception as e:
            pass
    
    # Mouse fallback
    if ser is None:
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - ball_x
            dy = mouse_y - ball_y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                ball_x += (dx / dist) * ball_speed * 2
                ball_y += (dy / dist) * ball_speed * 2

def spawn_obstacle():
    if random.randint(1, obstacle_spawn_rate) == 1:
        obstacles.append([random.randint(30, WIDTH-30), -20])

def update_obstacles():
    global game_over, score, lives
    
    for obs in obstacles[:]:
        obs[1] += obstacle_speed
        
        if obs[1] > HEIGHT:
            obstacles.remove(obs)
            score += 5
        
        dx = ball_x - obs[0]
        dy = ball_y - obs[1]
        if math.sqrt(dx*dx + dy*dy) < ball_radius + 15:
            lives -= 1
            obstacles.remove(obs)
            print(f"💥 Hit! Lives: {lives}")
            if lives <= 0:
                game_over = True
                print(f"💀 GAME OVER! Score: {score}")

def check_boundary():
    global lives, game_over, ball_x, ball_y
    
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius or \
       ball_y <= ball_radius or ball_y >= HEIGHT - ball_radius:
        lives -= 1
        print(f"💥 Fell off! Lives: {lives}")
        if lives <= 0:
            game_over = True
            print(f"💀 GAME OVER! Score: {score}")
        else:
            ball_x, ball_y = WIDTH//2, HEIGHT//2

# Main loop
frame_count = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
            if event.key == pygame.K_c:
                calibration.start()
                print("🔄 Re-calibrating...")
    
    handle_input()
    
    if not game_over and calibration.calibrated:
        check_boundary()
        frame_count += 1
        spawn_obstacle()
        update_obstacles()
    
    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT), 3)
    
    # Ball
    color = GREEN if not game_over else RED
    pygame.draw.circle(screen, color, (int(ball_x), int(ball_y)), ball_radius)
    
    # Obstacles
    for obs in obstacles:
        pygame.draw.circle(screen, YELLOW, (int(obs[0]), int(obs[1])), 12)
        pygame.draw.circle(screen, RED, (int(obs[0]), int(obs[1])), 8)
    
    # UI
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Lives: {'❤️' * lives}", True, WHITE), (20, 60))
    
    # Calibration progress
    if not calibration.calibrated:
        progress = (calibration.sample_count / calibration.samples) * 100
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, HEIGHT//2 + 50, 200, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH//2 - 100, HEIGHT//2 + 50, int(progress * 2), 20))
        screen.blit(font.render(f"Calibrating... {int(progress)}%", True, WHITE), 
                   (WIDTH//2 - 70, HEIGHT//2 + 20))
        screen.blit(font.render("Keep Pico STILL!", True, YELLOW), 
                   (WIDTH//2 - 70, HEIGHT//2 + 80))
    
    # Game over
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        screen.blit(font.render("GAME OVER", True, RED), (WIDTH//2 - 70, HEIGHT//2 - 60))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (WIDTH//2 - 50, HEIGHT//2 - 20))
        screen.blit(font.render("Press R or Button to restart", True, WHITE), 
                   (WIDTH//2 - 140, HEIGHT//2 + 30))
    
    pygame.display.flip()
    clock.tick(60)

if ser:
    ser.close()
pygame.quit()
