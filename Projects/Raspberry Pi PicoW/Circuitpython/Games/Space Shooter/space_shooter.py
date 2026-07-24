# shooter.py - Space Shooter Game (No Wrap-Around)
import pygame
import serial
import random
import math

# Setup
pygame.init()
WIDTH, HEIGHT = 1080, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)

# --- GLOBAL VARIABLES ---
player_x = WIDTH//2
player_y = HEIGHT - 80
player_width = 40
player_height = 40
player_speed = 24

bullets = []
bullet_speed = 12
bullet_cooldown = 0
MAX_BULLETS = 10

enemies = []
enemy_spawn_rate = 60
enemy_speed = 5
enemy_size = 25

score = 0
game_over = False
button_held = False
calibration_done = False
calibration_samples = []
calibration_count = 0
CALIBRATION_SAMPLES = 50
offset_x = 0

# --- Serial ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    print("="*50)
    print("✅ Connected to Pico!")
    print("🚀 Space Shooter Started!")
    print("Tilt LEFT/RIGHT to move")
    print("HOLD Button to CONTINUOUS FIRE!")
    print("="*50)
    print("")
    print("🔧 Calibrating... Keep Pico STILL!")
    print(f"   Collecting {CALIBRATION_SAMPLES} samples...")
except Exception as e:
    print(f"❌ Pico not connected: {e}")
    print("Using keyboard controls")

def reset_game():
    global player_x, bullets, enemies, score, game_over, bullet_cooldown
    player_x = WIDTH//2
    bullets = []
    enemies = []
    score = 0
    game_over = False
    bullet_cooldown = 0
    print("🔄 Game Restarted!")

def handle_input():
    global player_x, bullet_cooldown, button_held
    global calibration_done, calibration_count, offset_x
    
    if ser and ser.in_waiting:
        try:
            while ser.in_waiting:
                data = ser.readline().decode().strip()
                
                if data.startswith("IMU:"):
                    parts = data.split(":")[1].split(",")
                    if len(parts) >= 2:
                        raw_x = float(parts[0])
                        
                        # --- CALIBRATION PHASE ---
                        if not calibration_done:
                            calibration_samples.append(raw_x)
                            calibration_count += 1
                            progress = (calibration_count / CALIBRATION_SAMPLES) * 100
                            print(f"Calibration: {int(progress)}%", end='\r')
                            
                            if calibration_count >= CALIBRATION_SAMPLES:
                                offset_x = sum(calibration_samples) / len(calibration_samples)
                                calibration_done = True
                                print(f"\n✅ Calibration Done! Offset: {offset_x:.2f}")
                                print("🎮 Game Starting...\n")
                            continue
                        
                        # --- NORMAL GAME ---
                        x = raw_x - offset_x
                        
                        # Deadzone
                        if abs(x) < 0.15:
                            x = 0
                        
                        # Move player (NO WRAP-AROUND)
                        if not game_over:
                            player_x += x * player_speed
                            # 🔥 Keep player on screen
                            player_x = max(player_width//2, min(WIDTH - player_width//2, player_x))
                
                # Button hold for continuous fire
                elif data == "BTN_HOLD":
                    button_held = True
                    if not game_over and calibration_done:
                        if bullet_cooldown <= 0 and len(bullets) < MAX_BULLETS:
                            bullets.append([player_x, player_y - player_height//2])
                            bullet_cooldown = 5
                
                elif data == "BTN:1":
                    if game_over:
                        reset_game()
                    else:
                        if calibration_done and bullet_cooldown <= 0 and len(bullets) < MAX_BULLETS:
                            bullets.append([player_x, player_y - player_height//2])
                            bullet_cooldown = 5
                            print("🔥 Pew!")
                
                elif data == "BTN:0":
                    button_held = False
                        
        except Exception as e:
            pass
    
    # Keyboard fallback
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_x = max(player_width//2, player_x)  # 🔥 Left boundary
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_x = min(WIDTH - player_width//2, player_x)  # 🔥 Right boundary
    
    if keys[pygame.K_SPACE] and not game_over and calibration_done:
        if bullet_cooldown <= 0 and len(bullets) < MAX_BULLETS:
            bullets.append([player_x, player_y - player_height//2])
            bullet_cooldown = 5
    
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

def spawn_enemy():
    if random.randint(1, enemy_spawn_rate) == 1:
        x = random.randint(enemy_size, WIDTH - enemy_size)
        enemies.append([x, -enemy_size, random.choice([1, -1])])

def update_enemies():
    global game_over, score
    
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        
        enemy[0] += enemy[2] * 0.5
        if enemy[0] < enemy_size or enemy[0] > WIDTH - enemy_size:
            enemy[2] = -enemy[2]
        
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            score += 5
        
        dx = enemy[0] - player_x
        dy = enemy[1] - player_y
        if math.sqrt(dx*dx + dy*dy) < enemy_size + player_width//2:
            enemies.remove(enemy)
            game_over = True
            print(f"💀 GAME OVER! Score: {score}")

def update_bullets():
    global score
    
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
            continue
        
        for enemy in enemies[:]:
            dx = bullet[0] - enemy[0]
            dy = bullet[1] - enemy[1]
            if math.sqrt(dx*dx + dy*dy) < enemy_size + 5:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                print(f"🎯 Hit! Score: {score}")
                break

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
                # Re-calibrate
                calibration_done = False
                calibration_count = 0
                calibration_samples = []
                print("🔧 Re-calibrating... Keep Pico STILL!")
    
    handle_input()
    
    if calibration_done and not game_over:
        spawn_enemy()
        update_bullets()
        update_enemies()
        frame_count += 1
    
    # Drawing
    screen.fill(BLACK)
    
    # Stars
    for i in range(50):
        x = (i * 37 + frame_count) % WIDTH
        y = (i * 53 + frame_count * 2) % HEIGHT
        pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    # Player (single position - no wrap)
    pygame.draw.polygon(screen, GREEN, [
        (player_x, player_y - player_height//2),
        (player_x - player_width//2, player_y + player_height//2),
        (player_x + player_width//2, player_y + player_height//2)
    ])
    pygame.draw.polygon(screen, BLUE, [
        (player_x, player_y - player_height//2 + 5),
        (player_x - player_width//4, player_y),
        (player_x + player_width//4, player_y)
    ])
    
    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet[0]-3, bullet[1]-8, 6, 16))
        pygame.draw.rect(screen, ORANGE, (bullet[0]-1, bullet[1]-8, 2, 16))
    
    # Enemies
    for enemy in enemies:
        color = RED if enemy[1] > 100 else ORANGE
        pygame.draw.circle(screen, color, (int(enemy[0]), int(enemy[1])), enemy_size)
        pygame.draw.circle(screen, YELLOW, (int(enemy[0]), int(enemy[1])), enemy_size//2)
        pygame.draw.circle(screen, WHITE, (int(enemy[0]-8), int(enemy[1]-5)), 5)
        pygame.draw.circle(screen, WHITE, (int(enemy[0]+8), int(enemy[1]-5)), 5)
        pygame.draw.circle(screen, BLACK, (int(enemy[0]-8), int(enemy[1]-5)), 2)
        pygame.draw.circle(screen, BLACK, (int(enemy[0]+8), int(enemy[1]-5)), 2)
    
    # UI
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Bullets: {len(bullets)}/{MAX_BULLETS}", True, WHITE), (20, 60))
    
    if calibration_done:
        status = "Pico: ✅"
    else:
        status = "Pico: 🔧 Calibrating..."
    screen.blit(font.render(status, True, WHITE), (WIDTH - 150, 20))
    
    # Calibration progress
    if not calibration_done:
        progress = (calibration_count / CALIBRATION_SAMPLES) * 100
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, HEIGHT//2 + 50, 200, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH//2 - 100, HEIGHT//2 + 50, int(progress * 2), 20))
        screen.blit(font.render(f"Calibrating... {int(progress)}%", True, WHITE), 
                   (WIDTH//2 - 70, HEIGHT//2 + 20))
        screen.blit(font.render("Keep Pico STILL!", True, YELLOW), 
                   (WIDTH//2 - 70, HEIGHT//2 + 80))
    else:
        hint = "HOLD Button = Continuous Fire"
        screen.blit(font.render(hint, True, GRAY), (WIDTH//2 - 100, HEIGHT - 30))
    
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
        
        restart_text = font.render("Press R or Button to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    
    pygame.display.flip()
    clock.tick(60)

if ser:
    ser.close()
pygame.quit()