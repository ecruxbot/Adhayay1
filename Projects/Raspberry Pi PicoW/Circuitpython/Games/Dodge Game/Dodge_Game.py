# Dodge Game
import pygame
import serial
import random
import math

# Setup
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎪 Dodge Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
PURPLE = (150, 50, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
PINK = (255, 50, 150)
CYAN = (50, 255, 255)

# --- GAME VARIABLES ---
player_x = WIDTH//2
player_y = HEIGHT//2
player_size = 25
player_speed = 30

obstacles = []
obstacle_spawn_rate = 30
obstacle_speed = 3
obstacle_types = ['circle', 'square', 'triangle', 'star']

score = 0
lives = 3
level = 1
game_over = False
invincible = False
invincible_timer = 0
combo = 0

# Powerups
powerups = []
powerup_spawn_rate = 200

# --- CALIBRATION ---
calibration_done = False
calibration_samples_x = []
calibration_samples_y = []
calibration_count = 0
CALIBRATION_SAMPLES = 50
offset_x = 0
offset_y = 0

# --- SERIAL ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    print("="*50)
    print("✅ Connected to Pico!")
    print("🎪 Dodge Game Started!")
    print("Tilt Pico to move player")
    print("Dodge obstacles to survive!")
    print("Collect powerups for bonus!")
    print("="*50)
    print("")
    print("🔧 Calibrating... Keep Pico STILL!")
    print(f"   Collecting {CALIBRATION_SAMPLES} samples...")
except Exception as e:
    print(f"❌ Pico not connected: {e}")
    print("Using mouse controls")

def reset_game():
    global player_x, player_y, obstacles, powerups, score, lives, level, game_over, combo
    player_x, player_y = WIDTH//2, HEIGHT//2
    obstacles = []
    powerups = []
    score = 0
    lives = 3
    level = 1
    game_over = False
    combo = 0
    print("🔄 Game Reset!")

def create_obstacle():
    # Random position (from edges)
    side = random.choice(['top', 'bottom', 'left', 'right'])
    
    if side == 'top':
        x = random.randint(0, WIDTH)
        y = -30
        dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        dy = random.uniform(1, 3)
    elif side == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT + 30
        dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        dy = -random.uniform(1, 3)
    elif side == 'left':
        x = -30
        y = random.randint(0, HEIGHT)
        dx = random.uniform(1, 3)
        dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    else:  # right
        x = WIDTH + 30
        y = random.randint(0, HEIGHT)
        dx = -random.uniform(1, 3)
        dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    
    size = random.randint(15, 35)
    color = random.choice([RED, YELLOW, ORANGE, PURPLE, PINK, CYAN])
    shape = random.choice(obstacle_types)
    
    obstacles.append([x, y, dx, dy, size, color, shape])

def create_powerup():
    x = random.randint(50, WIDTH-50)
    y = random.randint(50, HEIGHT-50)
    types = ['shield', 'speed', 'slow', 'life']
    p_type = random.choice(types)
    powerups.append([x, y, p_type, 0])  # [x, y, type, timer]

def update_obstacles():
    global game_over, score, lives, level, combo, invincible, invincible_timer
    
    for obs in obstacles[:]:
        obs[0] += obs[2] * obstacle_speed * (1 + level * 0.1)
        obs[1] += obs[3] * obstacle_speed * (1 + level * 0.1)
        
        # Remove if off screen
        if obs[0] < -50 or obs[0] > WIDTH + 50 or obs[1] < -50 or obs[1] > HEIGHT + 50:
            obstacles.remove(obs)
            score += 2
            combo += 1
            continue
        
        # Collision with player
        dx = obs[0] - player_x
        dy = obs[1] - player_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < obs[4] + player_size and not invincible:
            lives -= 1
            combo = 0
            obstacles.remove(obs)
            print(f"💥 Hit! Lives: {lives}")
            
            # Invincibility
            invincible = True
            invincible_timer = 60  # 1 second
            
            if lives <= 0:
                game_over = True
                print(f"💀 GAME OVER! Score: {score}")

def update_powerups():
    global lives, player_speed, obstacle_speed, score
    
    for powerup in powerups[:]:
        powerup[3] += 1  # Timer
        
        # Auto remove after 5 seconds
        if powerup[3] > 300:
            powerups.remove(powerup)
            continue
        
        # Collision with player
        dx = powerup[0] - player_x
        dy = powerup[1] - player_y
        if math.sqrt(dx*dx + dy*dy) < 20 + player_size:
            if powerup[2] == 'life':
                lives += 1
                print(f"❤️ +1 Life! Lives: {lives}")
            elif powerup[2] == 'shield':
                invincible = True
                invincible_timer = 120  # 2 seconds
                print("🛡️ Shield Active!")
            elif powerup[2] == 'speed':
                player_speed = 8
                print("💨 Speed Boost!")
            elif powerup[2] == 'slow':
                obstacle_speed = 1
                print("🐢 Slow Motion!")
            
            powerups.remove(powerup)
            score += 5

def update_timers():
    global invincible, invincible_timer, player_speed, obstacle_speed
    
    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0:
            invincible = False
            print("🛡️ Shield expired")
    
    # Reset speed boosts
    if player_speed > 5:
        player_speed -= 0.1
        if player_speed < 5:
            player_speed = 5
    
    if obstacle_speed < 3:
        obstacle_speed += 0.05
        if obstacle_speed > 3:
            obstacle_speed = 3

def handle_input():
    global player_x, player_y, calibration_done, calibration_count, offset_x, offset_y
    
    if ser and ser.in_waiting:
        try:
            while ser.in_waiting:
                data = ser.readline().decode().strip()
                
                if data.startswith("IMU:"):
                    parts = data.split(":")[1].split(",")
                    if len(parts) >= 2:
                        raw_x = float(parts[0])
                        raw_y = float(parts[1])
                        
                        if not calibration_done:
                            calibration_samples_x.append(raw_x)
                            calibration_samples_y.append(raw_y)
                            calibration_count += 1
                            progress = (calibration_count / CALIBRATION_SAMPLES) * 100
                            print(f"Calibration: {int(progress)}%", end='\r')
                            
                            if calibration_count >= CALIBRATION_SAMPLES:
                                offset_x = sum(calibration_samples_x) / len(calibration_samples_x)
                                offset_y = sum(calibration_samples_y) / len(calibration_samples_y)
                                calibration_done = True
                                print(f"\n✅ Calibration Done!")
                                print("🎮 Game Starting...\n")
                            continue
                        
                        x = raw_x - offset_x
                        y = raw_y - offset_y
                        
                        # Invert Y
                        y = -y
                        
                        if abs(x) < 0.15:
                            x = 0
                        if abs(y) < 0.15:
                            y = 0
                        
                        if not game_over and calibration_done:
                            new_x = player_x + x * player_speed
                            new_y = player_y + y * player_speed
                            
                            # Keep on screen
                            new_x = max(player_size, min(WIDTH - player_size, new_x))
                            new_y = max(player_size, min(HEIGHT - player_size, new_y))
                            
                            player_x = new_x
                            player_y = new_y
                
                elif data == "BTN:1":
                    if game_over:
                        reset_game()
                    else:
                        # Reset position to center
                        player_x, player_y = WIDTH//2, HEIGHT//2
                        print("📍 Reset to center!")
                        
        except Exception as e:
            pass
    
    # Keyboard fallback
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = max(player_size, player_x - player_speed)
    if keys[pygame.K_RIGHT]:
        player_x = min(WIDTH - player_size, player_x + player_speed)
    if keys[pygame.K_UP]:
        player_y = max(player_size, player_y - player_speed)
    if keys[pygame.K_DOWN]:
        player_y = min(HEIGHT - player_size, player_y + player_speed)
    
    if keys[pygame.K_r] and game_over:
        reset_game()

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
                calibration_done = False
                calibration_count = 0
                calibration_samples_x = []
                calibration_samples_y = []
                print("🔧 Re-calibrating... Keep Pico STILL!")
    
    handle_input()
    
    if not game_over and calibration_done:
        # Spawn obstacles
        if frame_count % max(10, obstacle_spawn_rate - level * 2) == 0:
            create_obstacle()
            # Spawn more obstacles at higher levels
            if level > 3 and frame_count % 20 == 0:
                create_obstacle()
        
        # Spawn powerups
        if frame_count % max(100, powerup_spawn_rate - level * 10) == 0:
            create_powerup()
        
        update_obstacles()
        update_powerups()
        update_timers()
        
        # Level up
        if score > 0 and score % 30 == 0:
            new_level = score // 30 + 1
            if new_level > level:
                level = new_level
                print(f"⬆️ Level {level}!")
        
        frame_count += 1
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw grid
    for i in range(0, WIDTH, 50):
        pygame.draw.line(screen, DARK_GRAY, (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 50):
        pygame.draw.line(screen, DARK_GRAY, (0, i), (WIDTH, i), 1)
    
    # Draw player
    if invincible:
        # Blinking effect
        if frame_count % 6 < 3:
            color = CYAN
        else:
            color = BLUE
    else:
        color = BLUE
    
    pygame.draw.circle(screen, color, (int(player_x), int(player_y)), player_size)
    pygame.draw.circle(screen, WHITE, (int(player_x), int(player_y)), player_size, 2)
    
    # Player eyes
    pygame.draw.circle(screen, WHITE, (int(player_x-8), int(player_y-5)), 5)
    pygame.draw.circle(screen, WHITE, (int(player_x+8), int(player_y-5)), 5)
    pygame.draw.circle(screen, BLACK, (int(player_x-8), int(player_y-5)), 2)
    pygame.draw.circle(screen, BLACK, (int(player_x+8), int(player_y-5)), 2)
    
    # Draw obstacles
    for obs in obstacles:
        color = obs[5]
        x, y = int(obs[0]), int(obs[1])
        size = obs[4]
        
        if obs[6] == 'circle':
            pygame.draw.circle(screen, color, (x, y), size)
            pygame.draw.circle(screen, WHITE, (x, y), size, 2)
        elif obs[6] == 'square':
            pygame.draw.rect(screen, color, (x-size//2, y-size//2, size, size))
            pygame.draw.rect(screen, WHITE, (x-size//2, y-size//2, size, size), 2)
        elif obs[6] == 'triangle':
            points = [(x, y-size//2), (x-size//2, y+size//2), (x+size//2, y+size//2)]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
        else:  # star
            for i in range(5):
                angle = i * 72 - 90
                angle_rad = math.radians(angle)
                x1 = x + size * math.cos(angle_rad)
                y1 = y + size * math.sin(angle_rad)
                x2 = x + size//2 * math.cos(angle_rad + math.radians(36))
                y2 = y + size//2 * math.sin(angle_rad + math.radians(36))
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)
    
    # Draw powerups
    for powerup in powerups:
        x, y = int(powerup[0]), int(powerup[1])
        p_type = powerup[2]
        
        if p_type == 'life':
            pygame.draw.circle(screen, RED, (x, y), 15)
            pygame.draw.circle(screen, WHITE, (x, y), 15, 2)
            heart = font.render("❤️", True, WHITE)
            screen.blit(heart, (x-10, y-15))
        elif p_type == 'shield':
            pygame.draw.circle(screen, CYAN, (x, y), 15)
            pygame.draw.circle(screen, WHITE, (x, y), 15, 2)
            shield = font.render("🛡️", True, WHITE)
            screen.blit(shield, (x-10, y-15))
        elif p_type == 'speed':
            pygame.draw.circle(screen, YELLOW, (x, y), 15)
            pygame.draw.circle(screen, WHITE, (x, y), 15, 2)
            speed = font.render("💨", True, WHITE)
            screen.blit(speed, (x-10, y-15))
        elif p_type == 'slow':
            pygame.draw.circle(screen, PURPLE, (x, y), 15)
            pygame.draw.circle(screen, WHITE, (x, y), 15, 2)
            slow = font.render("🐢", True, WHITE)
            screen.blit(slow, (x-10, y-15))
    
    # UI
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Lives: {'❤️' * lives}", True, RED), (20, 60))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (20, 100))
    screen.blit(font.render(f"Combo: {combo}", True, WHITE), (20, 140))
    
    if invincible:
        screen.blit(font.render("🛡️ SHIELD", True, CYAN), (20, 180))
    
    if calibration_done:
        status = "Pico: ✅"
    else:
        status = "Pico: 🔧 Calibrating..."
    screen.blit(font.render(status, True, WHITE), (WIDTH - 150, 20))
    
    hint = "Tilt to move | Button = Reset to center"
    screen.blit(font.render(hint, True, GRAY), (WIDTH//2 - 150, HEIGHT - 30))
    
    # Calibration progress
    if not calibration_done:
        progress = (calibration_count / CALIBRATION_SAMPLES) * 100
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
        
        game_over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        
        level_text = font.render(f"Level Reached: {level}", True, WHITE)
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 + 20))
        
        restart_text = font.render("Press R or Button to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.flip()
    clock.tick(60)

if ser:
    ser.close()
pygame.quit()
