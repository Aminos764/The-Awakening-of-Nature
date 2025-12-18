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
DARK_GRAY = (40, 40, 40)

try:
    FONT_TITLE = pygame.font.Font("Font/font2.ttf", 72)
    FONT_BUTTON = pygame.font.Font("Font/font2.ttf", 46)
except:
    FONT_TITLE = pygame.font.SysFont(None, 72)
    FONT_BUTTON = pygame.font.SysFont(None, 36)

texts = {
    "Français": {
        "play": "Jouer",
        "options": "Options",
        "quit": "Quitter"
    },
    "English": {
        "play": "Play",
        "options": "Options",
        "quit": "Quit"
    }
}

option = {
    "fullscreen": False,
    "langage": "Français"
}

class Button:
    def __init__(self, text, center_y, action):
        self.text = text
        self.action = action
        self.width, self.height = 420, 70
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (WIDTH // 2, center_y)

    def draw(self, win, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = HOVER_BLUE if hovered else TRANSLUCENT_BLUE
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, self.width, self.height), border_radius=16)
        win.blit(surf, self.rect.topleft)
        shadow = FONT_BUTTON.render(self.text, True, SHADOW)
        text = FONT_BUTTON.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        win.blit(text, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

def create_menu_buttons():
    lang = option["langage"]
    return [
        Button(texts[lang]["play"], 320, "play"),
        Button(texts[lang]["options"], 420, "options"),
        Button(texts[lang]["quit"], 520, "quit")
    ]

buttons = create_menu_buttons()
language_button = Button("", 300, "language")
fullscreen_button = Button("", 380, "fullscreen")
back_button = Button("Retour", 560, "menu")

current_page = "menu"
clock = pygame.time.Clock()
running = True

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
                    running = False

    elif current_page == "options":
        screen.fill(DARK_GRAY)

        title = FONT_TITLE.render("Options", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        if option["langage"] == "Français":
            language_button.text = "Langue : Français"
        else:
            language_button.text = "Language : English"

        if option["fullscreen"]:
            fullscreen_button.text = "Plein écran : Activé"
        else:
            fullscreen_button.text = "Plein écran : Désactivé"

        back_button.text = "Retour"

        language_button.draw(screen, mouse_pos)
        fullscreen_button.draw(screen, mouse_pos)
        back_button.draw(screen, mouse_pos)

        if language_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)
            if option["langage"] == "Français":
                option["langage"] = "English"
            else:
                option["langage"] = "Français"
            buttons = create_menu_buttons()

        if fullscreen_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)
            if option["fullscreen"]:
                option["fullscreen"] = False
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            else:
                option["fullscreen"] = True
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

        if back_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)
            current_page = "menu"

    pygame.display.flip()

pygame.quit()
sys.exit()

