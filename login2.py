import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1131, 637
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Login")

# Fonte
FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT = pygame.font.SysFont("Arial", 18)
FONT_LOGIN = pygame.font.SysFont("Arial", 25)

# Paleta de cores
ACTIVE_COLOR = (220, 180, 255)
INACTIVE_COLOR = (240, 230, 250)
BORDER_COLOR = (200, 100, 255)
TEXT_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 150, 255)
BUTTON_HOVER_COLOR = (170, 120, 230)

# Função para redimensionar ícones
def resize_icon(image, max_width, max_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    if original_width > original_height:
        new_width = min(max_width, original_width)
        new_height = new_width / aspect_ratio
    else:
        new_height = min(max_height, original_height)
        new_width = new_height * aspect_ratio
    return pygame.transform.scale(image, (int(new_width), int(new_height)))

# Carregar imagens
user_icon = resize_icon(pygame.image.load("assets/login_icon.png"), 80, 80)
password_icon = resize_icon(pygame.image.load("assets/senha_icon.png"), 80, 80)
login_background = pygame.transform.scale(pygame.image.load("assets/login_fundo.gif"), (SCREEN_WIDTH, SCREEN_HEIGHT))
create_account_background = pygame.transform.scale(pygame.image.load("assets/criar_conta.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Função para a tela de login
def login_screen():


    email_text = ""
    password_text = ""
    active_email = False
    active_password = False
    input_rect_width = 300
    input_rect_height = 40
    
    FONT_SMALL = pygame.font.SysFont("Arial", 16)
    FONT = pygame.font.SysFont("Arial", 20)
    create_account_text = "Criar conta"
    create_account_text = "Criar conta"
    create_account_color = (255, 255, 255)  # Branco
    create_account_hover_color = (128, 128, 128)  # Azul escuro ao passar o mouse
    
        # Paleta de cores
    bg_color = (240, 230, 250)  # Fundo lilás suave
    border_color = (200, 100, 255)  # Borda roxa clara
    text_color = (50, 50, 50)  # Preto para o texto
    button_color = (200, 150, 255)  # Botão lilás suave
    button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
    active_color = (220, 180, 255)  # Caixa ativa
    inactive_color = bg_color  # Caixa inativa


    start_button_rect = pygame.Rect(
        (SCREEN.get_width() - 150) // 2,  # Centraliza horizontalmente
        SCREEN.get_height() // 2 + 100,  # Abaixo da caixa de texto
        150, 40
    )

    
    email_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2,  # Centraliza no eixo X
        SCREEN_HEIGHT // 2 - 100,  # Ajuste vertical para o campo de e-mail
        input_rect_width,
        input_rect_height
    )

    password_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2,  # Centraliza no eixo X
        SCREEN_HEIGHT // 2 - 30,  # Ajuste vertical para o campo de senha
        input_rect_width,
        input_rect_height
    )
    # Retângulo para o texto "Criar conta"
    create_account_surface = FONT_SMALL.render(create_account_text, True, create_account_color)
    create_account_rect = create_account_surface.get_rect(
        center=(SCREEN_WIDTH // 2, password_rect.y + password_rect.height + 30)
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_email = True
                    active_password = False
                elif password_rect.collidepoint(event.pos):
                    active_email = False
                    active_password = True
                elif create_account_rect.collidepoint(event.pos):
                    return "create_account"

            if event.type == pygame.KEYDOWN:
                if active_email:
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        # Verifica o comprimento do texto renderizado
                        text_width = FONT.size(email_text + event.unicode)[0]
                        if text_width < email_rect.width - 20:  # 20 para margem interna
                            email_text += event.unicode
                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        text_width = FONT.size(password_text + event.unicode)[0]
                        if text_width < password_rect.width - 20:
                            password_text += event.unicode
                    

        SCREEN.blit(login_background, (0, 0))
        
        # Caixa de e-mail
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_email else INACTIVE_COLOR, email_rect, border_radius=10)
        pygame.draw.rect(SCREEN, BORDER_COLOR, email_rect, 2, border_radius=5)

        # Caixa de senha
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_password else INACTIVE_COLOR, password_rect, border_radius=10)
        pygame.draw.rect(SCREEN, BORDER_COLOR, password_rect, 2, border_radius=5)

        # Renderizar textos das caixas
        email_surface = FONT.render(email_text or "Digite seu usuário", True, TEXT_COLOR)
        password_surface = FONT.render("*" * len(password_text) or "Digite sua senha", True, TEXT_COLOR)
       
        # Ajuste para centralizar os ícones verticalmente na caixa de texto
        icon_margin = -20  # Distância horizontal entre o ícone e o início da caixa de texto
        icon_center_offset = (input_rect_height - user_icon.get_height()) // 2

        # Ícone de usuário na caixa de texto do e-mail
        SCREEN.blit(user_icon, (email_rect.x + icon_margin, email_rect.y + icon_center_offset))
        # Ajuste o texto do e-mail para não sobrepor o ícone
        SCREEN.blit(email_surface, (email_rect.x + user_icon.get_width() + 2 * icon_margin, email_rect.y + 10))

        # Ícone de senha na caixa de texto de senha
        SCREEN.blit(password_icon, (password_rect.x + icon_margin, password_rect.y + icon_center_offset))
        # Ajuste o texto da senha para não sobrepor o ícone
        SCREEN.blit(password_surface, (password_rect.x + password_icon.get_width() + 2 * icon_margin, password_rect.y + 10))
        

        # Botão de começar jogo        
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT.render("Login", True, text_color)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)
        

        # Renderizar texto "Criar conta"
        mouse_pos = pygame.mouse.get_pos()
        current_color = create_account_hover_color if create_account_rect.collidepoint(mouse_pos) else create_account_color
        create_account_surface = FONT_SMALL.render(create_account_text, True, current_color)
        SCREEN.blit(create_account_surface, create_account_rect.topleft)


        pygame.display.flip()

# Função para a tela de criação de conta
def create_account_screen():
    input_rect_width = 300
    input_rect_height = 40
    name_text = ""
    email_text = ""
    password_text = ""
    confirm_password_text = ""
    active_name = False
    active_email = False
    active_password = False
    active_confirm_password = False

    name_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 190, input_rect_width,input_rect_height)
    email_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 120, input_rect_width,input_rect_height)
    password_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 50, input_rect_width,input_rect_height)
    confirm_password_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 + 20, input_rect_width,input_rect_height)

    FONT_HEADER = pygame.font.Font(None, 36)  # Ajuste o tamanho conforme necessário
    header_color = (106, 13, 173)  # Cor roxa

        # Paleta de cores
    bg_color = (240, 230, 250)  # Fundo lilás suave
    border_color = (200, 100, 255)  # Borda roxa clara
    text_color = (50, 50, 50)  # Preto para o texto
    button_color = (200, 150, 255)  # Botão lilás suave
    button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
    active_color = (220, 180, 255)  # Caixa ativa
    inactive_color = bg_color  # Caixa inativa


    start_button_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 250,
        SCREEN_HEIGHT // 2 + 100,  # Abaixo do campo de senha
        200,50
    )
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(event.pos):
                    active_name = True
                    active_email = active_password = active_confirm_password = False
                elif email_rect.collidepoint(event.pos):
                    active_email = True
                    active_name = active_password = active_confirm_password = False
                elif password_rect.collidepoint(event.pos):
                    active_password = True
                    active_name = active_email = active_confirm_password = False
                elif confirm_password_rect.collidepoint(event.pos):
                    active_confirm_password = True
                    active_name = active_email = active_password = False
                    
            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        # Verifica o comprimento do texto renderizado
                        text_width = FONT.size(name_text + event.unicode)[0]
                        if text_width < name_rect.width - 20:  # 20 para espaçamento interno
                            name_text += event.unicode
                elif active_email:
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        text_width = FONT.size(email_text + event.unicode)[0]
                        if text_width < email_rect.width - 20:
                            email_text += event.unicode
                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        text_width = FONT.size(password_text + event.unicode)[0]
                        if text_width < password_rect.width - 20:
                            password_text += event.unicode
                elif active_confirm_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                    else:
                        text_width = FONT.size(confirm_password_text + event.unicode)[0]
                        if text_width < confirm_password_rect.width - 20:
                            confirm_password_text += event.unicode


        SCREEN.blit(create_account_background, (0, 0))
        
        # Renderizar o texto "Criação de conta" no canto superior direito
        header_text = FONT_HEADER.render("Criação de conta", True, header_color)
        header_rect = header_text.get_rect()
        header_rect.topright = (SCREEN_WIDTH - 300, 50)  # 10px de margem
        SCREEN.blit(header_text, header_rect)

        
        #caixa de novo
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_name else INACTIVE_COLOR, name_rect,border_radius=5)
        pygame.draw.rect(SCREEN, BORDER_COLOR, name_rect, 2,border_radius=5)
        
        #caixa de email
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_email else INACTIVE_COLOR, email_rect,border_radius=5)
        pygame.draw.rect(SCREEN, BORDER_COLOR, email_rect, 2,border_radius=5)
        
        #caixa de senha
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_password else INACTIVE_COLOR, password_rect,border_radius=5)
        pygame.draw.rect(SCREEN, BORDER_COLOR, password_rect, 2,border_radius=5)
        
        #caixa de confirmação de senha
        pygame.draw.rect(SCREEN, ACTIVE_COLOR if active_confirm_password else INACTIVE_COLOR, confirm_password_rect,border_radius=5)
        pygame.draw.rect(SCREEN, BORDER_COLOR, confirm_password_rect, 2,border_radius=5)

        name_surface = FONT.render(name_text or "Nome", True, TEXT_COLOR)
        email_surface = FONT.render(email_text or "Usuário", True, TEXT_COLOR)
        password_surface = FONT.render("*" * len(password_text) or "Senha", True, TEXT_COLOR)
        confirm_password_surface = FONT.render("*" * len(confirm_password_text) or "Confirmar Senha", True, TEXT_COLOR)
        # Botão de começar jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT_LOGIN.render("Criar", True, text_color)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)

        SCREEN.blit(name_surface, (name_rect.x + 10, name_rect.y + 10))
        SCREEN.blit(email_surface, (email_rect.x + 10, email_rect.y + 10))
        SCREEN.blit(password_surface, (password_rect.x + 10, password_rect.y + 10))
        SCREEN.blit(confirm_password_surface, (confirm_password_rect.x + 10, confirm_password_rect.y + 10))

        pygame.display.flip()

# Loop principal
current_screen = "login"
while True:
    if current_screen == "login":
        current_screen = login_screen()
    elif current_screen == "create_account":
        create_account_screen()
        current_screen = "login"
