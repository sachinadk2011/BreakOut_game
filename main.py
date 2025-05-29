import pygame
import sys
import random
from config import WIDTH, HEIGHT, FPS, WHITE, BLACK, RED, BRICK_COLORS 
from menu import main_menu 
from menu_after_game import post_game_menu
import os
from pathlib import Path


# Initialize pygame
pygame.init()






# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 15
PADDLE_Y = HEIGHT - 40

# Ball
BALL_RADIUS = 10

# Brick
BRICK_ROWS = 10
BRICKS_PER_ROW = 10
BRICK_WIDTH = (WIDTH - (BRICKS_PER_ROW + 1) * 5) / BRICKS_PER_ROW
BRICK_HEIGHT = 20
BRICK_GAP = 5

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Power Breaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Classes
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.x = mouse_x - PADDLE_WIDTH // 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

class Ball:
    def __init__(self, paddle_x, score, selected_mode):
        self.rect = pygame.Rect(paddle_x - BALL_RADIUS, PADDLE_Y - BALL_RADIUS*2, BALL_RADIUS*2, BALL_RADIUS*2)
        self.score = score
        self.selected_mode = selected_mode
        self.prev_rect = self.rect.copy()  # <--- Add this line
        
        self.vel = main_menu_wrapper(self.score, self.selected_mode)# velocity based on current score
        self.min_speed = self.get_min_speed()
        self.current_vel = self.min_speed # mainly for after lives decrease to make ball speed slow for few sec
        self.speed_ramp_start_time = pygame.time.get_ticks()#get the time when ball recreate
        
        #initiall the speed
        self.x_vel = random.choice([-self.vel, self.vel])
        self.y_vel = -self.vel

    def get_min_speed(self):
        if self.selected_mode == "Easy":
            return 2
        elif self.selected_mode == "Medium":
            return 3
        elif self.selected_mode == "Hard":
            return 4
        
    def update(self):
        self.prev_rect = self.rect.copy()  # <--- Track previous position

        # Speed ramps up for 3 seconds after spawn
        elapsed = pygame.time.get_ticks() - self.speed_ramp_start_time
        ramp_time = 5000  # 5 seconds

        if elapsed < ramp_time:
            ratio = elapsed / ramp_time  # 0 to 1
            self.current_speed = self.min_speed + (self.vel - self.min_speed) * ratio
        else:
            self.current_speed = self.vel

         # Update velocity if score has changed (adjust speed dynamically)
        new_vel = main_menu_wrapper(self.score, self.selected_mode)
        if new_vel != self.vel:
            # Maintain direction while changing speed
            self.x_vel = new_vel if self.x_vel > 0 else -new_vel
            self.y_vel = -new_vel if self.y_vel < 0 else new_vel
            self.vel = new_vel
        
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Wall collisions with position reset
        if self.rect.left <= 0:
            self.rect.left = 0
            self.x_vel *= -1
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.x_vel *= -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y_vel *= -1

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), self.rect.center, BALL_RADIUS)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        color = BRICK_COLORS[row % len(BRICK_COLORS)]
        y = 50 + row * (BRICK_HEIGHT + BRICK_GAP)
        for col in range(BRICKS_PER_ROW):
            x = BRICK_GAP + col * (BRICK_WIDTH + BRICK_GAP)
            bricks.append(Brick(x, y, color))
    return bricks

def show_countdown(screen, font, paddle, ball, bricks, lives, score, mode):
    countdown = [3, 2, 1, "Start"]
    count = len(countdown)
    if lives < 3:
        count = 3
    for i in range(count):
        screen.fill(BLACK)

        # Draw bricks
        for brick in bricks:
            brick.draw()

        # Draw paddle
        paddle.draw()

        # Draw ball at its start position
        ball.draw()
        # Draw lives and score
        lives_score_display(screen, font, lives, score,mode )
    
        text = font.render(str(countdown[i]), True, WHITE)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(1000)  # wait 1 second

def lives_score_display(screen, font, lives, score, mode):
    # Render "Lives:" in white
    lives_label = font.render("Lives: ", True, WHITE)

    
    heart_rect = pygame.Rect(10 + lives_label.get_width(), 10, 100,lives_label.get_height())
    pygame.draw.rect(screen, BLACK, heart_rect)
    # Draw lives and score
    heart = '\u2665'
     
    lives_hearts = font.render(heart * lives, True, RED)
    screen.blit(lives_hearts, (10 + lives_label.get_width(), 10))
    
    mode_text = font.render(f"Mode: {mode}", True, WHITE)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_label, (10, 10))
    screen.blit(mode_text, (WIDTH // 2 -70, 10))
    screen.blit(score_text, (WIDTH - 150, 10))
    


def main_menu_wrapper(score, selected_mode):

    if selected_mode == "Easy":
        # Base speed 2, +1 every 300 points, cap at 4
        return min(2 + score / 300, 4)
    elif selected_mode == "Medium":
        # Base speed 3, +1 every 200 points, cap at 6
        return min(3 + score / 200, 6)
    elif selected_mode == "Hard":
         # Base speed 4, +1 every 200 points, cap at 8
        return min(4 + score / 200, 8)
       
def get_high_score(score, modes):
    base_dir = Path(os.getenv('LOCALAPPDATA', Path.home())) / "Breakout"
    base_dir.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

    filename = base_dir / f'High_score_{modes}.txt'
    

   # Try reading the existing high score
    try:
        with open(filename, 'r') as f:
            high_Score = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        high_Score = 0

    # Update if the new score is higher
    if score > high_Score:
        with open(filename, 'w') as f:
            f.write(str(score))
        return score  # New high score set
    return high_Score  # Return the existing high score
        
        
        


def main():
    selected_mode = main_menu()
    paddle = Paddle()
    score = 0
    lives = 3
    ball = Ball(paddle.rect.centerx, score, selected_mode)
    bricks = create_bricks()
    

    show_countdown(screen, font, paddle, ball, bricks, lives, score, selected_mode)
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        paddle.update()
        ball.update()
        if (ball.prev_rect.bottom <= paddle.rect.top and ball.rect.bottom >= paddle.rect.top):
            if ball.rect.right >= paddle.rect.left and ball.rect.left <= paddle.rect.right:
                ball.y_vel = -abs(ball.y_vel)
                ball.rect.bottom = paddle.rect.top  # Prevent overlap
        elif ball.rect.colliderect(paddle.rect):
            # Ball came from above
            if ball.rect.bottom <= paddle.rect.top + abs(ball.y_vel):
                ball.y_vel = -abs(ball.y_vel)  # bounce up
            # Ball hit from below
            elif ball.rect.top >= paddle.rect.bottom - abs(ball.y_vel):
                ball.y_vel = abs(ball.y_vel)   # bounce down
            # Ball hit the side
            else:
                ball.x_vel *= -1               # reverse horizontal direction


        # Ball and bricks collision
        hit_index = ball.rect.collidelist([b.rect for b in bricks])
        if hit_index != -1:
            hit_brick = bricks.pop(hit_index)
            ball.y_vel *= -1
            score += 10
            ball.score = score  # <-- keep ball's score in sync

        # Ball falls below screen
        if ball.rect.top > HEIGHT:
            lives -= 1
            if lives == 0:
                lives_score_display(screen, font, lives, score, selected_mode)
                

                high_score = get_high_score(score, selected_mode)
                choice = post_game_menu(font,screen,score,high_score, lives)
                if choice == "menu":
                    selected_mode = main_menu(selected_mode)
                    paddle = Paddle()
                    score = 0
                    lives = 3
                    ball = Ball(paddle.rect.centerx, score, selected_mode)
                    bricks = create_bricks()
                    show_countdown(screen, font, paddle, ball, bricks, lives, score, selected_mode)
                    continue  # restart game
                
            else:
                ball = Ball(paddle.rect.centerx, score, selected_mode)  # Reset ball position
                show_countdown(screen, font, paddle, ball, bricks, lives, score, selected_mode)  # Show countdown before next round

        # Clear screen
        screen.fill(BLACK)

        # Draw everything
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        # Display lives and score
        lives_score_display(screen, font, lives, score, selected_mode)
        

        # Check win condition
        if not bricks:
            
            high_score = get_high_score(score, selected_mode)
            choice = post_game_menu(font,screen,score,high_score,lives)
            if choice == "menu":
                selected_mode = main_menu(selected_mode)
                paddle = Paddle()
                score = 0
                lives = 3
                ball = Ball(paddle.rect.centerx, score, selected_mode)
                bricks = create_bricks()
                show_countdown(screen, font, paddle, ball, bricks, lives, score, selected_mode)
                continue  # restart game
        

        pygame.display.flip()

if __name__ == "__main__":
    main()





