from config import  WHITE, ORANGE
import config
import pygame
import sys



def post_game_menu(font,screen,score,high_score,lives):
    while True:
        
        if lives>0:
            text = "You Win!"
        else:
            text = "Game Over"
        game_over_text = font.render(text, True, WHITE)
        Your_score = font.render(f"Your Score: {score}", True, WHITE)
        High_score_text = font.render(f"Best score: {high_score}", True, WHITE)
        menu_text = font.render("Press M to return to Menu", True, ORANGE)
        quit_text = font.render("Press Q to Quit", True, ORANGE)

        # Blit texts onto screen
        screen.blit(game_over_text, (config.WIDTH// 2 - 50, config.HEIGHT // 2 - 25))
        screen.blit(Your_score, (config.WIDTH// 2 - 50, config.HEIGHT // 2 ))
        screen.blit(High_score_text, (config.WIDTH// 2 - 50, config.HEIGHT // 2 + 25))
        screen.blit(menu_text, (config.WIDTH// 2 - menu_text.get_width() // 2, config.HEIGHT // 2 + 60))
        screen.blit(quit_text, (config.WIDTH// 2 - quit_text.get_width() // 2, config.HEIGHT // 2 + 100))

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
                else:
                    break                   

def pause_menu(screen, font):
    while True:
        paused_text = font.render("Game Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, ORANGE)
        menu_text = font.render("Press M to return to Menu", True, ORANGE)
        quit_text = font.render("Press E to Exit", True, ORANGE)
        screen.blit(paused_text, (config.WIDTH // 2 - paused_text.get_width() // 2, config.HEIGHT // 2 - 30))
        screen.blit(resume_text, (config.WIDTH // 2 - resume_text.get_width() // 2, config.HEIGHT // 2 + 10))
        screen.blit(menu_text, (config.WIDTH// 2 - menu_text.get_width() // 2, config.HEIGHT // 2 + 50))
        screen.blit(quit_text, (config.WIDTH// 2 - quit_text.get_width() // 2, config.HEIGHT // 2 + 90))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "resume" # resume
                elif event.key == pygame.K_m:
                    return "menu"
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
                else:
                    break               

