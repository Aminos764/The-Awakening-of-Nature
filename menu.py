import pygame
import sys
import subprocess
pygame.init()


WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Awakening of Nature")

background = pygame.image.load("image/background3.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
TRANSLUCENT_BLUE = (0, 80, 200, 180)
HOVER_BLUE = (0, 140, 255, 220)
SHADOW = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)

try:
    FONT_TITLE = pygame.font.Font("Font/font2.ttf", 72)
    FONT_BUTTON = pygame.font.Font("Font/font2.ttf", 46)
except:
    FONT_TITLE = pygame.font.SysFont(None, 72)
    FONT_BUTTON = pygame.font.SysFont(None, 36)

class Button:
    def __init__(self, text, center_y, action):
        self.text = text
        self.action = action
        self.center_y = center_y
        self.react = pygame.Rect(10, center_y - 30, WIDTH - 20, 60)
        self.width, self.height = 320, 70
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.react.center = (WIDTH // 2, center_y)
        self.rect.center = (WIDTH // 2, center_y)

    def draw(self, win, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = HOVER_BLUE if is_hovered else TRANSLUCENT_BLUE
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius=16)
        win.blit(button_surface, self.rect.topleft)

        text_surf = FONT_BUTTON.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)

        shadow = FONT_BUTTON.render(self.text, True, SHADOW)
        win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        win.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

buttons = [
    Button("Jouer", 320, "play"),
    Button("Options", 420, "options"),
    Button("Quitter", 520, "quit")
]

back_button = Button("Retour", 560, "menu")

option = {
    "volume": 1,
    "fullscreen": False,
    "langage": "Français"
}

current_page = "menu"
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_page == "menu":
        screen.blit(background, (0, 0))

        title = FONT_TITLE.render("The Awakening of Nature", True, WHITE)
        shadow = FONT_TITLE.render("The Awakening of Nature", True, SHADOW)
        screen.blit(shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 103))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for btn in buttons:
            btn.draw(screen, mouse_pos)
            if btn.is_clicked(mouse_pos, mouse_pressed):
                pygame.time.delay(200)
                if btn.action == "play":
                    pygame.quit()
                    subprocess.Popen([sys.executable, "game/game.py"])
                    sys.exit()
                elif btn.action == "options":
                    current_page = "options"
                elif btn.action == "quit":
                    current_page = "quit"
                    running = False
                    

    elif current_page == "options":
        screen.fill(DARK_GRAY)
        title = FONT_TITLE.render("Options", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        back_button.draw(screen, mouse_pos)
        if back_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)
            current_page = "menu"
    pygame.display.flip()

pygame.quit()
sys.exit()
