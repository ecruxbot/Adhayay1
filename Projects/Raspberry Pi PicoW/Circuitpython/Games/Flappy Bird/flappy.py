# flappy.py - Flappy Bird with Tilt Control
import pygame
import serial
import random
import math

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐦 Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)

# --- GLOBAL VARIABLES ---
bird_x = 150
bird_y = HEIGHT//2
bird_radius = 20
bird_vel = 0
gravity = 0.5
flap_strength = -8
MAX_VEL = 10

pipes = []
pipe_width = 60
pipe_gap = 180
pipe_speed = 4
pipe_spawn_rate = 90

score = 0
best_score = 0
game_over = False

# --- Calibration ---
calibration_done = False
calibration_samples = []
calibration_count = 0
CALIBRATION_SAMPLES = 50
offset_y = 0

# --- Serial ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    print("="*50)
    print("✅ Connected to Pico!")
    print("🐦 Flappy Bird Started!")
    print("Tilt UP/DOWN to control bird")
    print("Press Button or R to restart")
    print("="*50)
    print("")
    print("🔧 Calibrating... Keep Pico STILL!")
    print(f"   Collecting {CALIBRATION_SAMPLES} samples...")
except Exception as e:
    print(f"❌ Pico not connected: {e}")
    print("Using keyboard controls")

def reset_game():
    global bird_y, bird_vel, pipes, score, game_over
    bird_y = HEIGHT//2
    bird_vel = 0
    pipes = []
    score = 0
    game_over = False
    print("🔄 Game Restarted!")

def handle_input():
    global bird_vel, calibration_done, calibration_count, offset_y
    
    if ser and ser.in_waiting:
        try:
            while ser.in_waiting:
                data = ser.readline().decode().strip()
                
                if data.startswith("IMU:"):
                    parts = data.split(":")[1].split(",")
                    if len(parts) >= 2:
                        raw_y = float(parts[1])
                        
                        # --- CALIBRATION ---
                        if not calibration_done:
                            calibration_samples.append(raw_y)
                            calibration_count += 1
                            progress = (calibration_count / CALIBRATION_SAMPLES) * 100
                            print(f"Calibration: {int(progress)}%", end='\r')
                            
                            if calibration_count >= CALIBRATION_SAMPLES:
                                offset_y = sum(calibration_samples) / len(calibration_samples)
                                calibration_done = True
                                print(f"\n✅ Calibration Done! Offset: {offset_y:.2f}")
                                print("🎮 Game Starting...\n")
                            continue
                        
                        # --- NORMAL GAME ---
                        y = raw_y - offset_y
                        
                        # Deadzone
                        if abs(y) < 0.15:
                            y = 0
                        
                        # 🔥 Control bird with tilt
                        if not game_over:
                            if y < -0.3:  # Tilt UP = Flap
                                bird_vel = flap_strength
                            elif y > 0.3:  # Tilt DOWN = Dive
                                bird_vel = 3
                
                elif data == "BTN:1":
                    if game_over:
                        reset_game()
                    else:
                        # Flap on button press
                        if not game_over:
                            bird_vel = flap_strength
                            print("🦅 Flap!")
                        
        except Exception as e:
            pass
    
    # Keyboard fallback
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not game_over:
        bird_vel = flap_strength
    if keys[pygame.K_DOWN] and not game_over:
        bird_vel = 3
    if keys[pygame.K_SPACE] and not game_over:
        bird_vel = flap_strength

def update_bird():
    global bird_y, bird_vel, game_over
    
    if not game_over:
        bird_vel += gravity
        bird_vel = max(-MAX_VEL, min(MAX_VEL, bird_vel))
        bird_y += bird_vel
        
        # Ground/ceiling collision
        if bird_y < bird_radius:
            bird_y = bird_radius
            bird_vel = 0
        elif bird_y > HEIGHT - bird_radius:
            game_over = True
            print(f"💀 GAME OVER! Score: {score}")

def spawn_pipe():
    if random.randint(1, pipe_spawn_rate) == 1:
        height = random.randint(100, HEIGHT - pipe_gap - 100)
        pipes.append([WIDTH, height])

def update_pipes():
    global game_over, score, best_score
    
    for pipe in pipes[:]:
        pipe[0] -= pipe_speed
        
        if pipe[0] < -pipe_width:
            pipes.remove(pipe)
            score += 1
            print(f"🎯 Score: {score}")
            if score > best_score:
                best_score = score
        
        # Collision
        if not game_over:
            if bird_x + bird_radius > pipe[0] and bird_x - bird_radius < pipe[0] + pipe_width:
                if bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap:
                    game_over = True
                    print(f"💀 GAME OVER! Score: {score}")

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
                calibration_samples = []
                print("🔧 Re-calibrating... Keep Pico STILL!")
    
    handle_input()
    
    if calibration_done:
        update_bird()
        spawn_pipe()
        update_pipes()
        frame_count += 1
    
    # Drawing
    screen.fill(BLACK)
    
    # Sky gradient
    for i in range(HEIGHT):
        color = (0, 0, 50 + i // 3)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
    
    # Clouds
    cloud_x = (frame_count * 0.2) % WIDTH
    for i in range(5):
        cx = (cloud_x + i * 200) % WIDTH
        cy = 100 + i * 50
        pygame.draw.ellipse(screen, (100, 100, 150), (cx, cy, 120, 40))
        pygame.draw.ellipse(screen, (100, 100, 150), (cx+30, cy-20, 80, 40))
    
    # Pipes
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
        pygame.draw.rect(screen, (0, 150, 0), (pipe[0]-10, pipe[1]-30, pipe_width+20, 30))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap))
        pygame.draw.rect(screen, (0, 150, 0), (pipe[0]-10, pipe[1] + pipe_gap, pipe_width+20, 30))
    
    # Bird
    color = YELLOW if not game_over else RED
    pygame.draw.circle(screen, color, (int(bird_x), int(bird_y)), bird_radius)
    # Eye
    pygame.draw.circle(screen, WHITE, (int(bird_x+8), int(bird_y-5)), 6)
    pygame.draw.circle(screen, BLACK, (int(bird_x+10), int(bird_y-5)), 3)
    # Beak
    pygame.draw.polygon(screen, ORANGE, [
        (int(bird_x+18), int(bird_y)),
        (int(bird_x+28), int(bird_y+5)),
        (int(bird_x+18), int(bird_y+10))
    ])
    
    # UI
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Best: {best_score}", True, WHITE), (20, 70))
    
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
        hint = "Tilt UP = Flap, Tilt DOWN = Dive"
        screen.blit(font.render(hint, True, GRAY), (WIDTH//2 - 130, HEIGHT - 30))
    
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