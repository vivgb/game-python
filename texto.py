import pygame, sys

pygame.init()

# Tela
SCREEN = pygame.display.set_mode((1131, 637))
pygame.display.set_caption("Leaderboard")

# Fontes
def get_font(size):
    return pygame.font.Font(None, size)

# Dados para o ranking
ranking = [
    {"name": "KiuMiMiXoa", "trophy": 20000, "reward": "+124.8", "bonus": 192},
    {"name": "Xi Trum", "trophy": 1600, "reward": "+78", "bonus": 120},
    {"name": "Linhhaika", "trophy": 2000, "reward": "+61.29", "bonus": 94.29},
    {"name": "Nabati", "trophy": 1600, "reward": "+28.49", "bonus": 61.29},
    {"name": "Xi Tun", "trophy": 2000, "reward": "+5.66", "bonus": 6.66},
]

# Cores
LILAC_COLOR = (208, 176, 241)  # Lilás claro
TEXT_COLOR = "White"

# Função para desenhar a interface
def draw_interface():
    while True:
        # Fundo
        bg_image = pygame.image.load("assets/fundojogar.png")
        SCREEN.blit(bg_image, (0, 0))
        RANK_MOUSE_POS = pygame.mouse.get_pos()

        # Título
        title = get_font(40).render("LEADERBOARD", True, "White")
        title_rect = title.get_rect(center=(SCREEN.get_width() // 2, 50))
        SCREEN.blit(title, title_rect)

        # Lista de rankings
        rect_width, rect_height = 800, 50  # Retângulos menores
        base_x = (SCREEN.get_width() - rect_width) // 2  # Centralizar horizontalmente
        base_y = (SCREEN.get_height() - (len(ranking) * 60)) // 2  # Centralizar verticalmente
        spacing = 60  # Espaçamento entre retângulos

        for idx, player in enumerate(ranking):
            # Calcular a posição do retângulo
            rect_y = base_y + idx * spacing

            # Desenhar retângulos
            pygame.draw.rect(SCREEN, LILAC_COLOR, (base_x, rect_y, rect_width, rect_height), border_radius=10)

            # Adicionar texto nos retângulos
            player_text = get_font(25).render(
                f"{idx + 1}. {player['name']} | Trophy: {player['trophy']} | Reward: {player['reward']}", 
                True, TEXT_COLOR
            )
            player_text_rect = player_text.get_rect(center=(SCREEN.get_width() // 2, rect_y + rect_height // 2))
            SCREEN.blit(player_text, player_text_rect)

        # Botão Fechar (canto superior direito)
        close_button = get_font(30).render("X", True, "Red")
        close_button_rect = close_button.get_rect(center=(SCREEN.get_width() - 50, 40))
        SCREEN.blit(close_button, close_button_rect)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(RANK_MOUSE_POS):
                    return  # Fecha a interface

        pygame.display.update()

# Testando a interface
draw_interface()
