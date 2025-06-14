import pygame
from config import WHITE, BLACK, RED
import config

def get_proportional_font():
    # Font size proportional to screen height
    font_size = max(16, int(config.HEIGHT * 0.03))  # 3% of height, min 16
    return pygame.font.SysFont("Arial", font_size)

def lives_score_display_proportional(screen, lives, score, mode):
    font = get_proportional_font()
    # Proportional margins and gap
    left_margin = int(config.WIDTH * 0.015)
    top_margin = int(config.HEIGHT * 0.015)
    gap = int(config.WIDTH * 0.05)
    right_margin = int(config.WIDTH * 0.015)

    # Render UI elements
    lives_label = font.render("Lives: ", True, WHITE)
    heart = '\u2665'
    lives_hearts = font.render(heart * lives, True, RED)
    pause_text = font.render("Pause-p", True, WHITE)
    mode_text = font.render(f"Mode: {mode}", True, WHITE)
    exit_text = font.render("Exit-e", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    # Draw left-aligned info
    x = left_margin
    y = top_margin
    texts = [ pause_text, mode_text, exit_text]
    total_text_width = sum(text.get_width() for text in texts)

    screen.blit(lives_label, (x, y))
    x += lives_label.get_width() 

    # Always clear the hearts area before drawing hearts
    heart_area_width = font.size(heart * 3)[0]  # Enough for max 3 hearts
    heart_area_rect = pygame.Rect(x, y, heart_area_width, lives_label.get_height())
    pygame.draw.rect(screen, BLACK, heart_area_rect)

    if lives > 0:
        screen.blit(lives_hearts, (x, y))
    x += heart_area_width
    # Calculate gap based on remaining space
    # Ensure gap is at least 10 pixels
    gap = max(10,(config.WIDTH - total_text_width - score_text.get_width() - x) // (len(texts) + 1))
    x += gap  # Add initial gap before the first text
    for text in texts:
        screen.blit(text, (x, y))
        x += text.get_width() + gap

    # Draw score at top-right, always visible
    score_x = config.WIDTH - score_text.get_width() - right_margin
    screen.blit(score_text, (score_x, y))



""" 
def lives_score_display(screen, font, lives, score, mode):
    # Margins
    left_margin = 10
    top_margin = 10
    
    right_margin = 10

    # Render UI elements
    lives_label = font.render("Lives: ", True, WHITE)
    heart = '\u2665'
    lives_hearts = font.render(heart * lives, True, RED)
    pause_text = font.render("Pause-p", True, WHITE)
    mode_text = font.render(f"Mode: {mode}", True, WHITE)
    exit_text = font.render("Exit-e", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    heart_area_width = font.size(heart * 3)[0]  # Enough for max 3 hearts

    # Draw left-aligned info
    x = left_margin
    y = top_margin
    texts = [ pause_text, mode_text, exit_text]
    total_text_width = sum(text.get_width() for text in texts)


    screen.blit(lives_label, (x, y))
    x += lives_label.get_width()  

    # Always clear the hearts area before drawing hearts
    heart_area_rect = pygame.Rect(x, y, heart_area_width, lives_label.get_height())
    pygame.draw.rect(screen, BLACK, heart_area_rect)
    if lives > 0:
        screen.blit(lives_hearts, (x, y))
    x += heart_area_width 
    gap = max(10,(WIDTH - total_text_width - score_text.get_width() - x) // (len(texts) + 1))
    x += gap  # Add initial gap before the first text
    for text in texts:
        screen.blit(text, (x, y))
        x += text.get_width() + gap


    # Draw score at top-right, always visible
    score_x = WIDTH - score_text.get_width() - right_margin
    screen.blit(score_text, (score_x, y))
    

 """