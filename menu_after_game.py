from config import WIDTH, HEIGHT, WHITE, ORANGE
import pygame
import sys



def post_game_menu(font,screen,score,high_score,lives):
    while True:
        
        if lives>0:
            text = "You Win!"
        text = "Game Over"
        game_over_text = font.render(text, True, WHITE)
        Your_score = font.render(f"Your Score: {score}", True, WHITE)
        High_score_text = font.render(f"Best score: {high_score}", True, WHITE)
        menu_text = font.render("Press M to return to Menu", True, ORANGE)
        quit_text = font.render("Press Q to Quit", True, ORANGE)

        # Blit texts onto screen
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 25))
        screen.blit(Your_score, (WIDTH // 2 - 50, HEIGHT // 2 ))
        screen.blit(High_score_text, (WIDTH // 2 - 50, HEIGHT // 2 + 25))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return "menu"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()