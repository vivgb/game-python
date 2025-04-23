import pygame

# Inicializar o Pygame
pygame.init()

# Variáveis de estado para a tela de login
login_email_text = ""  
login_password_text = ""



# Placeholders
email_placeholder = "Digite seu usuário"
password_placeholder = "Digite sua senha"

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1131, 637
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Login")

# icon do usuario
user_icon = pygame.image.load("assets/login_icon.png")
user_icon = pygame.transform.scale(user_icon, (60, 60))  # Ajuste de tamanho, se necessário


# Carregar a imagem do ícone
user_icon = pygame.image.load("assets/login_icon.png")
password_icon = pygame.image.load("assets/senha_icon.png")

# Ajuste de tamanho mantendo a proporção

# Fonte para o texto "Criar conta"
FONT_SMALL = pygame.font.SysFont("Arial", 16)
create_account_text = "Criar conta"
create_account_color = (255, 255, 255)  # Branco
create_account_hover_color = (128, 128, 128)  # Azul escuro ao passar o mouse

# Configurações das caixas de texto
input_rect_width = 300
input_rect_height = 40

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

# Função para a tela de criação de conta
def handle_text_input(event, active_field, text_value, max_length, valid_chars):
    """Função para lidar com entrada de texto."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            active_field = False
        elif event.key == pygame.K_BACKSPACE:
            text_value = text_value[:-1]
        else:
            if len(text_value) < max_length and event.unicode in valid_chars:
                text_value += event.unicode
    return active_field, text_value

def render_input_boxes():
    """Renderizar caixas de entrada na tela."""
    # Caixa de texto - E-mail
    # Caixa de texto - E-mail
    email_color = active_color if active_email else inactive_color
    pygame.draw.rect(SCREEN, email_color, email_rect, border_radius=5)
    pygame.draw.rect(SCREEN, border_color, email_rect, 2, border_radius=5)
    if email_text == "" and not active_email:
        email_surface = FONT.render(email_placeholder, True, (150, 150, 150))  # Placeholder em cinza
    else:
        email_surface = FONT.render(email_text, True, (50, 50, 50))
    
    password_color = active_color if active_password else inactive_color
    pygame.draw.rect(SCREEN, password_color, password_rect, border_radius=5)
    pygame.draw.rect(SCREEN, border_color, password_rect, 2, border_radius=5)
    if password_text == "" and not active_password:
        password_surface = FONT.render(password_placeholder, True, (150, 150, 150))  # Placeholder em cinza
    else:
        password_display = "*" * len(password_text)  # Exibir senha como "*"
        password_surface = FONT.render(password_display, True, (50, 50, 50))
    
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

def create_account_screen():

    """Função para a tela de criação de conta."""
    global active_email, active_password, active_name, active_confirm_password
    # Variáveis de estado para a tela de criação de conta
    create_account_email_text = ""
    create_account_password_text = ""
    create_account_name_text = ""
    create_account_confirm_password_text = ""

    active_name = False
    active_confirm_password = False
    name_text = ""
    confirm_password_text = ""

    name_text = ""
    confirm_password_text = ""
    
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
    
    # Imagem de fundo
    background = pygame.image.load("assets/criar_conta.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Criação de retângulos específicos para esta função
    create_account_name_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 200,
        SCREEN_HEIGHT // 2 - 190,  # Acima do campo de e-mail
        input_rect_width,
        input_rect_height
    )
    
    create_account_email_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 200,
        SCREEN_HEIGHT // 2 - 120,
        input_rect_width,
        input_rect_height
    )
    
    create_account_password_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 200,
        SCREEN_HEIGHT // 2 - 50,
        input_rect_width,
        input_rect_height
    )
    
    create_account_confirm_password_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 200,
        SCREEN_HEIGHT // 2 + 20,  # Abaixo do campo de senha
        input_rect_width,
        input_rect_height
    )
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        
            # Detectar clique nas caixas de texto
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_name = create_account_name_rect.collidepoint(event.pos)
                active_email = create_account_email_rect.collidepoint(event.pos)
                active_password = create_account_password_rect.collidepoint(event.pos)
                active_confirm_password = create_account_confirm_password_rect.collidepoint(event.pos)

            if active_name:
                active_name, create_account_name_text = handle_text_input(
                    event, active_name, create_account_name_text, 30, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
            elif active_email:
                active_email, create_account_email_text = handle_text_input(
                    event, active_email, create_account_email_text, 30, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._-")
            elif active_password:
                active_password, create_account_password_text = handle_text_input(
                    event, active_password, create_account_password_text, 30, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            elif active_confirm_password:
                active_confirm_password, create_account_confirm_password_text = handle_text_input(
                    event, active_confirm_password, create_account_confirm_password_text, 30, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

        # Renderizar fundo
        SCREEN.blit(background, (0, 0))
        
        # Renderizar o texto "Criação de conta" no canto superior direito
        header_text = FONT_HEADER.render("Criação de conta", True, header_color)
        header_rect = header_text.get_rect()
        header_rect.topright = (SCREEN_WIDTH - 300, 50)  # 10px de margem
        SCREEN.blit(header_text, header_rect)

            
        # Renderizar caixas de texto específicas desta função
        email_color = active_color if active_email else inactive_color
        pygame.draw.rect(SCREEN, email_color, create_account_email_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, create_account_email_rect, 2, border_radius=5)
        if email_text == "" and not active_email:
            email_surface = FONT.render(email_placeholder, True, (150, 150, 150))  # Placeholder em cinza
        else:
            email_surface = FONT.render(email_text, True, (50, 50, 50))
        
        # Renderizar caixas de texto específicas desta função
        # Nome
        name_color = active_color if active_name else inactive_color
        pygame.draw.rect(SCREEN, name_color, create_account_name_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, create_account_name_rect, 2, border_radius=5)
        name_surface = FONT.render(name_text if name_text else "Nome", True, (50, 50, 50) if name_text else (150, 150, 150))
        SCREEN.blit(name_surface, (create_account_name_rect.x + 10, create_account_name_rect.y + 10))

        # Email
        email_color = active_color if active_email else inactive_color
        pygame.draw.rect(SCREEN, email_color, create_account_email_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, create_account_email_rect, 2, border_radius=5)
        email_surface = FONT.render(email_text if email_text else "Usuário", True, (50, 50, 50) if email_text else (150, 150, 150))
        SCREEN.blit(email_surface, (create_account_email_rect.x + 10, create_account_email_rect.y + 10))
        
        # Senha
        password_color = active_color if active_password else inactive_color
        pygame.draw.rect(SCREEN, password_color, create_account_password_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, create_account_password_rect, 2, border_radius=5)
        password_display = "*" * len(password_text)
        password_surface = FONT.render(password_display if password_text else "Senha", True, (50, 50, 50) if password_text else (150, 150, 150))
        SCREEN.blit(password_surface, (create_account_password_rect.x + 10, create_account_password_rect.y + 10))

        # Confirmar Senha
        confirm_password_color = active_color if active_confirm_password else inactive_color
        pygame.draw.rect(SCREEN, confirm_password_color, create_account_confirm_password_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, create_account_confirm_password_rect, 2, border_radius=5)
        confirm_password_display = "*" * len(confirm_password_text)
        confirm_password_surface = FONT.render(confirm_password_display if confirm_password_text else "Confirmar Senha", True, (50, 50, 50) if confirm_password_text else (150, 150, 150))
        SCREEN.blit(confirm_password_surface, (create_account_confirm_password_rect.x + 10, create_account_confirm_password_rect.y + 10))

        
        # Botão de começar jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT_LOGIN.render("Criar", True, text_color)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)
        
        pygame.display.flip()

        
# Redimensionar as imagens do ícone
def resize_icon(image, max_width, max_height):
    # Obter as dimensões originais da imagem
    original_width, original_height = image.get_size()

    # Calcular a proporção de largura/altura
    aspect_ratio = original_width / original_height

    # Ajustar a largura ou altura, mantendo a proporção
    if original_width > original_height:
        # Ajustar a largura, calcular altura proporcional
        new_width = min(max_width, original_width)
        new_height = new_width / aspect_ratio
    else:
        # Ajustar a altura, calcular largura proporcional
        new_height = min(max_height, original_height)
        new_width = new_height * aspect_ratio

    # Redimensionar a imagem com as novas dimensões
    return pygame.transform.scale(image, (int(new_width), int(new_height)))

user_icon = resize_icon(user_icon, 80, 80)  # Ajuste para se encaixar em 60x60, mantendo a proporção
password_icon = resize_icon(password_icon, 80, 80)  # Ajuste para se encaixar em 60x60, mantendo a proporção


# Imagem de fundo
background = pygame.image.load("assets/login_fundo.gif")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Paleta de cores (tons de roxo)
active_color = (220, 180, 255)  # Roxo claro (ativo)
inactive_color = (240, 230, 250)  # Roxo escuro (inativo)
border_color = (200, 100, 255)  # Roxo mais escuro
button_color = (200, 150, 255)  # Roxo do botão
button_text_color = (255, 255, 255)  # Branco para o texto do botão

# Fonte
FONT = pygame.font.SysFont("Arial", 18)
FONT_LOGIN = pygame.font.SysFont("Arial", 25)

# Configurações das caixas de texto
input_rect_width = 300
input_rect_height = 40

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

# Configurações do botão
#button_width, button_height = 200, 50
#button_rect = pygame.Rect(
    #(SCREEN_WIDTH - button_width) // 2,
    #SCREEN_HEIGHT // 2 + 100,
    #button_width,
    #button_height
#)

    # Paleta de cores
bg_color = (240, 230, 250)  # Fundo lilás suave
border_color = (200, 100, 255)  # Borda roxa clara
text_color = (50, 50, 50)  # Preto para o texto
button_color = (200, 150, 255)  # Botão lilás suave
button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
active_color = (220, 180, 255)  # Caixa ativa
inactive_color = bg_color  # Caixa inativa


start_button_rect = pygame.Rect(
        (SCREEN.get_width() - 200) // 2,  # Centraliza horizontalmente
        SCREEN.get_height() // 2 + 100,  # Abaixo da caixa de texto
        200, 50
    )

# Variáveis de estado
email_text = ""  # Texto digitado no campo de e-mail
password_text = ""  # Texto digitado no campo de senha
active_email = False  # Indica se a caixa de texto de e-mail está ativa
active_password = False  # Indica se a caixa de texto de senha está ativa


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verifica cliques nas caixas de texto
        if event.type == pygame.MOUSEBUTTONDOWN:
            if email_rect.collidepoint(event.pos):
                active_email = True
                active_password = False
            elif password_rect.collidepoint(event.pos):
                active_email = False
                active_password = True
            elif create_account_rect.collidepoint(event.pos):
                create_account_screen()  # Abrir tela de criação de conta
            else:
                active_email = active_password = False

        # Eventos de teclado
        if event.type == pygame.KEYDOWN:
            if active_email:
                if event.key == pygame.K_RETURN:
                    active_email = False
                elif event.key == pygame.K_BACKSPACE:
                    login_email_text = login_email_text[:-1]
                else:
                    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._-"
                    if len(login_email_text) < 30 and event.unicode in valid_chars:
                        login_email_text += event.unicode

            elif active_password:
                if event.key == pygame.K_RETURN:
                    active_password = False
                elif event.key == pygame.K_BACKSPACE:
                    login_password_text = login_password_text[:-1]
                else:
                    if len(login_password_text) < 30 and event.unicode.isalnum():
                        login_password_text += event.unicode


      


    # Renderizar fundo
    SCREEN.blit(background, (0, 0))

    # Caixa de texto - E-mail
    email_color = active_color if active_email else inactive_color
    pygame.draw.rect(SCREEN, email_color, email_rect, border_radius=5)
    pygame.draw.rect(SCREEN, border_color, email_rect, 2, border_radius=5)
    if email_text == "" and not active_email:
        email_surface = FONT.render(email_placeholder, True, (150, 150, 150))  # Placeholder em cinza
    else:
        email_surface = FONT.render(email_text, True, (50, 50, 50))
    
    # Caixa de texto - Senha
    password_color = active_color if active_password else inactive_color
    pygame.draw.rect(SCREEN, password_color, password_rect, border_radius=5)
    pygame.draw.rect(SCREEN, border_color, password_rect, 2, border_radius=5)
    if password_text == "" and not active_password:
        password_surface = FONT.render(password_placeholder, True, (150, 150, 150))  # Placeholder em cinza
    else:
        password_display = "*" * len(password_text)  # Exibir senha como "*"
        password_surface = FONT.render(password_display, True, (50, 50, 50))
    
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
    start_text = FONT_LOGIN.render("Login", True, text_color)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    SCREEN.blit(start_text, start_text_rect)
    
        # Renderizar texto "Criar conta"
    mouse_pos = pygame.mouse.get_pos()
    current_color = create_account_hover_color if create_account_rect.collidepoint(mouse_pos) else create_account_color
    create_account_surface = FONT_SMALL.render(create_account_text, True, current_color)
    SCREEN.blit(create_account_surface, create_account_rect.topleft)

        
    # Atualizar a tela
    pygame.display.flip()

pygame.quit()
