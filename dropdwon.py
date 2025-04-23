import pygame
import sys

pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dropdown em Pygame")

# Cores
LAVANDA = (230, 230, 230)
ROXO = (128,0,120)
ROXO_CLARO = (200, 150, 255)
ROXO_ESCURO = (75, 0, 130)
LAVANDA_1 = (220, 180, 255)
BRANCO = (255,255,255)
# Fonte
FONT = pygame.font.Font(None, 36)

class Dropdown:
    def __init__(self, x, y, width, height, options, default="Selecione"):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = default
        self.is_open = False
        self.option_rects = [
            pygame.Rect(x, y + (i + 1) * height, width, height) for i in range(len(options))
        ]

    def draw(self, screen):
        # Caixa principal
        pygame.draw.rect(screen, ROXO_CLARO, self.rect, border_radius=5)
        pygame.draw.rect(screen, ROXO, self.rect, 2, border_radius=5)

        # Texto da seleção atual
        text_surface = FONT.render(self.selected, True, ROXO)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        if self.is_open:
            for i, rect in enumerate(self.option_rects):
                pygame.draw.rect(screen, LAVANDA_1, rect)
                pygame.draw.rect(screen, ROXO, rect, 1)
                option_text = FONT.render(self.options[i], True, ROXO)
                screen.blit(option_text, (rect.x + 10, rect.y + (rect.height - option_text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open  # Alterna entre aberto/fechado
            elif self.is_open:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = self.options[i]
                        self.is_open = False
                        break
                else:
                    self.is_open = False  # Fecha o dropdown se clicar fora das opções

# Exemplo de uso
dropdown = Dropdown(200, 150, 200, 40, ["Inglês", "Português", "Espanhol"])

def main():
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(LAVANDA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            dropdown.handle_event(event)

        dropdown.draw(SCREEN)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
