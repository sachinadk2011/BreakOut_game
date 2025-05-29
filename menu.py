import pygame
import sys
from config import WIDTH, HEIGHT, FPS, WHITE, BLACK, RED , ORANGE, BRICK_COLORS
import random

pygame.init()

CENTER = (WIDTH // 2 - 100, HEIGHT // 2 - 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Power Breaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

class Mode:
    def __init__(self,x,y, text):
        self.text = text
        self.rect = pygame.Rect(x, y, 200, 50)
    
    def draw(self):
        pygame.draw.rect(screen, ORANGE, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class FloatingBrick:
    def __init__(self):
        self.width = random.randint(30, 60)
        self.height = 20
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT)
        self.color = random.choice(BRICK_COLORS)
        self.x_vel = random.choice([-1, 1])
        self.y_vel = random.choice([-1, 1])

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        # Wall collisions
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.x_vel *= -1
        if self.y <= 0 or self.y + self.height >= HEIGHT:
            self.y_vel *= -1

    def draw(self, screen):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surface.fill((*self.color, 80))  # RGBA: last is transparency
        screen.blit(temp_surface, (self.x, self.y))


def mode_menu(modes, current_mode):
    screen.fill(BLACK)
    floating_bricks = [FloatingBrick() for _ in range(30)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for mode in modes:
                    if mode.rect.collidepoint(mouse_pos):
                        print(f"Selected mode: {mode.text}")
                        return mode.text  # Exit the mode menu

        screen.fill(BLACK)
        mode_text = font.render(f"Mode: {current_mode}", True, WHITE)
        screen.blit(mode_text, (10, 10))

        for brick in floating_bricks:
            brick.update()
            brick.draw(screen)

        for mode in modes:
            mode.draw()

        pygame.display.flip()
        clock.tick(FPS)

def main_menu(mode= "Easy"):
    floating_bricks = [FloatingBrick() for _ in range(30)]
    menus = [
        Mode(CENTER[0], CENTER[1], "Start Game"),
        Mode(CENTER[0], CENTER[1] + 100, "Options"),
        Mode(CENTER[0], CENTER[1] + 200, "Exit")
    ]

    modes = [
        Mode(CENTER[0], CENTER[1], "Easy"),
        Mode(CENTER[0], CENTER[1] + 100, "Medium"),
        Mode(CENTER[0], CENTER[1] + 200, "Hard")
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for menu in menus:
                    if menu.rect.collidepoint(mouse_pos):
                        if menu.text == "Exit":
                            pygame.quit()
                            sys.exit()
                        elif menu.text == "Start Game":
                            # Start the game with the selected mode and go to main.py 
                            return mode
                        elif menu.text == "Options":
                            mode = mode_menu(modes, mode)
        screen.fill(BLACK)
        mode_text = font.render(f"Mode: {mode}", True, WHITE)
        screen.blit(mode_text, (10, 10))

        for brick in floating_bricks:
            brick.update()
            brick.draw(screen)

        for menu in menus:
            menu.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()