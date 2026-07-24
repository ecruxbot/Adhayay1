# pong.py - Pong Game with Tilt Control
import pygame
import serial
import math
import random

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Pong - Tilt Control")
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
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# --- GAME VARIABLES ---
# Player (Left paddle)
player_y = HEIGHT//2 - 60
player_width = 20
player_height = 120
player_speed = 6

# Computer (Right paddle)
computer_y = HEIGHT//2 - 60
computer_speed = 4

# Ball
ball_x = WIDTH//2
ball_y = HEIGHT//2
ball_size = 15
ball_speed_x = 5
ball_speed_y = 5
ball_start_x = 5
ball_start_y = 5

# Score
player_score = 0
computer_score = 0
win_score = 5

# --- CALIBRATION ---
calibration_done = False
calibration_samples = []
calibration_count = 0
CALIBRATION_SAMPLES = 50
offset_y = 0

# --- SERIAL ---
ser = None
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    ser.reset_input_buffer()
    print("="*50)
    print("✅ Connected to Pico!")
    print("🏓 Pong Game Started!")
    print("Tilt UP/DOWN to move paddle")
    print("First to 5 wins!")
    print("Press Button or R to restart")
    print("="*50)
    print("")
    print("🔧 Calibrating... Keep Pico STILL!")
    print(f"   Collecting {CALIBRATION_SAMPLES} samples...")
except Exception as e:
    print(f"❌ Pico not connected: {e}")
    print("Using keyboard controls")

def reset_game():
    global player_y, computer_y, ball_x, ball_y, ball_speed_x, ball_speed_y
    global player_score, computer_score, game_over
    player_y = HEIGHT//2 - 60
    computer_y = HEIGHT//2 - 60
    ball_x = WIDTH//2
    ball_y = HEIGHT//2
    ball_speed_x = ball_start_x * random.choice([-1, 1])
    ball_speed_y = ball_start_y * random.choice([-1, 1])
    player_score = 0
    computer_score = 0
    game_over = False
    print("🔄 Game Reset!")

def reset_round():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH//2
    ball_y = HEIGHT//2
    ball_speed_x = ball_start_x * random.choice([-1, 1])
    ball_speed_y = ball_start_y * random.choice([-1, 1])

def handle_input():
    global player_y, calibration_done, calibration_count, offset_y
    
    if ser and ser.in_waiting:
        try:
            while ser.in_waiting:
                data = ser.readline().decode().strip()
                
                if data.startswith("IMU:"):
                    parts = data.split(":")[1].split(",")
                    if len(parts) >= 2:
                        raw_y = float(parts[1])
                        
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
                        
                        y = raw_y - offset_y
                        
                        # 🔥 Invert Y (UP = negative, DOWN = positive)
                        y = -y
                        
                        if abs(y) < 0.15:
                            y = 0
                        
                        # Move player paddle
                        if not game_over:
                            player_y += y * player_speed
                            player_y = max(0, min(HEIGHT - player_height, player_y))
                
                elif data == "BTN:1":
                    if game_over:
                        reset_game()
                    else:
                        print("🔘 Button Pressed!")
                        
        except Exception as e:
            pass
    
    # Keyboard fallback
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
        player_y = max(0, player_y)
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        player_y = min(HEIGHT - player_height, player_y)
    
    if keys[pygame.K_r] and game_over:
        reset_game()

def update_computer():
    global computer_y
    
    # Simple AI - follow ball with some delay
    target_y = ball_y - player_height//2
    diff = target_y - computer_y
    
    if abs(diff) > 20:
        if diff > 0:
            computer_y += computer_speed
        else:
            computer_y -= computer_speed
    
    computer_y = max(0, min(HEIGHT - player_height, computer_y))

def update_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global player_score, computer_score, game_over
    
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Wall collision (top/bottom)
    if ball_y <= ball_size or ball_y >= HEIGHT - ball_size:
        ball_speed_y = -ball_speed_y
    
    # Player paddle collision (left)
    if ball_x - ball_size <= player_width and player_y <= ball_y <= player_y + player_height:
        if ball_speed_x < 0:
            ball_speed_x = -ball_speed_x
            # Add some angle based on where ball hits paddle
            hit_pos = (ball_y - player_y) / player_height  # 0 to 1
            ball_speed_y = (hit_pos - 0.5) * 8
            print("🏓 Player hit!")
    
    # Computer paddle collision (right)
    if ball_x + ball_size >= WIDTH - player_width and computer_y <= ball_y <= computer_y + player_height:
        if ball_speed_x > 0:
            ball_speed_x = -ball_speed_x
            hit_pos = (ball_y - computer_y) / player_height
            ball_speed_y = (hit_pos - 0.5) * 8
            print("🏓 Computer hit!")
    
    # Score
    if ball_x < 0:
        computer_score += 1
        print(f"💻 Computer scores! {player_score}-{computer_score}")
        reset_round()
    
    if ball_x > WIDTH:
        player_score += 1
        print(f"👤 Player scores! {player_score}-{computer_score}")
        reset_round()
    
    # Check win
    if player_score >= win_score:
        game_over = True
        print(f"🏆 YOU WIN! {player_score}-{computer_score}")
    elif computer_score >= win_score:
        game_over = True
        print(f"💻 COMPUTER WINS! {player_score}-{computer_score}")

# Main loop
game_over = False
running = True
frame_count = 0

# Initial ball direction
ball_speed_x = ball_start_x * random.choice([-1, 1])
ball_speed_y = ball_start_y * random.choice([-1, 1])

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
    
    if not game_over and calibration_done:
        update_computer()
        update_ball()
        frame_count += 1
    
    # Drawing
    screen.fill(BLACK)
    
    # Center line
    for i in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 2, i, 4, 15))
    
    # Center circle
    pygame.draw.circle(screen, GRAY, (WIDTH//2, HEIGHT//2), 60, 2)
    
    # Player paddle (Left)
    pygame.draw.rect(screen, BLUE, (0, player_y, player_width, player_height))
    pygame.draw.rect(screen, WHITE, (0, player_y, player_width, player_height), 2)
    
    # Computer paddle (Right)
    pygame.draw.rect(screen, RED, (WIDTH - player_width, computer_y, player_width, player_height))
    pygame.draw.rect(screen, WHITE, (WIDTH - player_width, computer_y, player_width, player_height), 2)
    
    # Ball
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_size)
    # Ball glow
    for i in range(3):
        radius = ball_size + i * 4
        pygame.draw.circle(screen, (100, 100, 100, 50), (int(ball_x), int(ball_y)), radius, 1)
    
    # Score
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (WIDTH//2 - 80, 30))
    
    computer_text = font.render(str(computer_score), True, WHITE)
    screen.blit(computer_text, (WIDTH//2 + 60, 30))
    
    # VS text
    vs_text = font.render("VS", True, GRAY)
    screen.blit(vs_text, (WIDTH//2 - 20, 30))
    
    # Pico status
    if calibration_done:
        status = "Pico: ✅"
    else:
        status = "Pico: 🔧 Calibrating..."
    screen.blit(font.render(status, True, WHITE), (WIDTH - 150, 20))
    
    # Controls hint
    hint = "Tilt UP/DOWN to move paddle"
    screen.blit(font.render(hint, True, GRAY), (WIDTH//2 - 130, HEIGHT - 30))
    
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
        
        if player_score > computer_score:
            win_text = "🏆 YOU WIN!"
            color = GREEN
        else:
            win_text = "💻 COMPUTER WINS!"
            color = RED
        
        game_over_text = big_font.render(win_text, True, color)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        
        score_text = font.render(f"{player_score} - {computer_score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        
        restart_text = font.render("Press R or Button to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    
    pygame.display.flip()
    clock.tick(60)

if ser:
    ser.close()
pygame.quit()