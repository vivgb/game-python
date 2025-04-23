import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuração da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cartões de Jogo")

# Cores
BACKGROUND_COLOR = (100, 50, 150)  # Fundo roxo
CARD_COLORS = [(160, 90, 210), (220, 140, 90), (120, 200, 120)]  # Cores dos cartões
BORDER_COLOR = (50, 30, 100)  # Cor da borda dos cartões
TEXT_COLOR = (255, 255, 255)

# Fonte
FONT = pygame.font.Font(None, 36)  # Fonte padrão do pygame

# Padrão de fundo (xadrez)
def draw_background():
    TILE_SIZE = 50
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            rect_color = BACKGROUND_COLOR if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0 else (120, 60, 180)
            pygame.draw.rect(SCREEN, rect_color, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Função para desenhar um cartão
def draw_card(x, y, color, title, stats):
    CARD_WIDTH, CARD_HEIGHT = 200, 300
    # Fundo do cartão
    pygame.draw.rect(SCREEN, color, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=15)
    # Borda do cartão
    pygame.draw.rect(SCREEN, BORDER_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), 5, border_radius=15)
    # Texto do título
    title_text = FONT.render(title, True, TEXT_COLOR)
    SCREEN.blit(title_text, (x + CARD_WIDTH // 2 - title_text.get_width() // 2, y + 20))
    # Estatísticas
    stat_text = FONT.render(stats, True, TEXT_COLOR)
    SCREEN.blit(stat_text, (x + CARD_WIDTH // 2 - stat_text.get_width() // 2, y + CARD_HEIGHT - 40))

# Loop principal
def main():
    clock = pygame.time.Clock()

    while True:
        SCREEN.fill((0, 0, 0))  # Limpar a tela
        draw_background()

        # Desenhar os cartões
        draw_card(200, 150, CARD_COLORS[0], "Slime King", "ATK: 7 | DEF: 5")
        draw_card(500, 150, CARD_COLORS[1], "Treasury", "Gold: 10")
        draw_card(800, 150, CARD_COLORS[2], "Toad Knight", "ATK: 3 | DEF: 8")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(30)

main()
