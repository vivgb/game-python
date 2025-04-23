import sqlite3
import random
import time
import pygame

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1131, 637
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Login")



# Paleta de cores
ACTIVE_COLOR = (220, 180, 255)
INACTIVE_COLOR = (240, 230, 250)
BORDER_COLOR = (200, 100, 255)
TEXT_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 150, 255)
BUTTON_HOVER_COLOR = (170, 120, 230)

user_icon = pygame.image.load("assets/login_icon.png")
user_icon = pygame.transform.scale(user_icon, (60, 60))  # Ajuste de tamanho, se necessário


# Carregar a imagem do ícone
user_icon = pygame.image.load("assets/login_icon.png")
password_icon = pygame.image.load("assets/senha_icon.png")

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


def conectar_banco():
    conexao = sqlite3.connect("jogo.db")
    db_cursor = conexao.cursor()
    db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_partidas (
        partida_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        pontuacao INTEGER NOT NULL,
        tempo INTEGER NOT NULL,
        FOREIGN KEY(usuario) REFERENCES usuarios(usuario)
    )
    """)
    conexao.commit()
    return conexao, db_cursor

def cadastrar_usuario(conexao, db_cursor, nome, usuario, senha):
    try:
        db_cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha))
        conexao.commit()
    except sqlite3.IntegrityError:
        raise Exception(f"Erro: O usuário '{usuario}' já existe!")
    
    
    
def create_account_screen(conexao, db_cursor):
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

    name_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 190, input_rect_width, input_rect_height)
    email_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 120, input_rect_width, input_rect_height)
    password_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 - 50, input_rect_width, input_rect_height)
    confirm_password_rect = pygame.Rect((SCREEN_WIDTH - input_rect_width) // 2 + 200, SCREEN_HEIGHT // 2 + 20, input_rect_width, input_rect_height)

    FONT_HEADER = pygame.font.Font(None, 36)
    header_color = (106, 13, 173)

    bg_color = (240, 230, 250)
    border_color = (200, 100, 255)
    text_color = (50, 50, 50)
    button_color = (200, 150, 255)
    button_hover_color = (170, 120, 230)
    active_color = (220, 180, 255)
    inactive_color = bg_color

    start_button_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2 + 250,
        SCREEN_HEIGHT // 2 + 100,
        200, 50
    )
    create_account_background = pygame.image.load("assets/criar_conta.png").convert()

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
                elif start_button_rect.collidepoint(event.pos):
                    # Validar os campos antes de cadastrar
                    if not name_text or not email_text or not password_text:
                        print("Por favor, preencha todos os campos!")
                    elif password_text != confirm_password_text:
                        print("As senhas não coincidem!")
                    else:
                        try:
                            cadastrar_usuario(conexao, db_cursor, name_text, email_text, password_text)
                            print("Conta criada com sucesso!")
                            return  # Voltar à tela anterior ou ao menu principal
                        except Exception as e:
                            print(str(e))

            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        name_text += event.unicode
                elif active_email:
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        email_text += event.unicode
                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode
                elif active_confirm_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                    else:
                        confirm_password_text += event.unicode

        SCREEN.blit(create_account_background, (0, 0))

        header_text = FONT_HEADER.render("Criação de conta", True, header_color)
        header_rect = header_text.get_rect()
        header_rect.topright = (SCREEN_WIDTH - 300, 50)
        SCREEN.blit(header_text, header_rect)

        pygame.draw.rect(SCREEN, active_color if active_name else inactive_color, name_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, name_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, active_color if active_email else inactive_color, email_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, email_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, active_color if active_password else inactive_color, password_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, password_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, active_color if active_confirm_password else inactive_color, confirm_password_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, confirm_password_rect, 2, border_radius=5)

        name_surface = FONT.render(name_text or "Nome", True, text_color)
        email_surface = FONT.render(email_text or "Usuário", True, text_color)
        password_surface = FONT.render("*" * len(password_text) or "Senha", True, text_color)
        confirm_password_surface = FONT.render("*" * len(confirm_password_text) or "Confirmar Senha", True, text_color)

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


def autenticar_usuario(db_cursor, usuario, senha):
    db_cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    return db_cursor.fetchone()


def login_screen(conexao, db_cursor):
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
    
    # Configurações do texto e cores
    create_account_text = "Criar conta"
    create_account_color = (255, 255, 255)
    create_account_hover_color = (128, 128, 128)
    bg_color = (240, 230, 250)
    border_color = (200, 100, 255)
    text_color = (50, 50, 50)
    button_color = (200, 150, 255)
    button_hover_color = (170, 120, 230)
    active_color = (220, 180, 255)
    inactive_color = bg_color

    error_message = ""  # Mensagem de erro para exibir ao usuário

    start_button_rect = pygame.Rect(
        (SCREEN.get_width() - 150) // 2,
        SCREEN.get_height() // 2 + 100,
        150, 40
    )

    email_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2,
        SCREEN_HEIGHT // 2 - 100,
        input_rect_width,
        input_rect_height
    )

    password_rect = pygame.Rect(
        (SCREEN_WIDTH - input_rect_width) // 2,
        SCREEN_HEIGHT // 2 - 30,
        input_rect_width,
        input_rect_height
    )

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
                    return "create_account"  # Indica que o usuário quer criar uma conta
                elif start_button_rect.collidepoint(event.pos):
                    if not email_text or not password_text:
                        error_message = "Por favor, preencha todos os campos."
                    else:
                        user = autenticar_usuario(db_cursor, email_text, password_text)
                        if user:
                            print("Login bem-sucedido!")
                            return user  # Retorna o usuário logado
                        else:
                            error_message = "Usuário ou senha incorretos."

            if event.type == pygame.KEYDOWN:
                if active_email:
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        email_text += event.unicode
                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

        login_background = pygame.image.load("assets/login_fundo.gif").convert()
        SCREEN.blit(login_background, (0, 0))

        # caixa de e-mail
        pygame.draw.rect(SCREEN, active_color if active_email else inactive_color, email_rect, border_radius=10)
        pygame.draw.rect(SCREEN, border_color, email_rect, 2, border_radius=5)
        
        # caixa de senha
        pygame.draw.rect(SCREEN, active_color if active_password else inactive_color, password_rect, border_radius=10)
        pygame.draw.rect(SCREEN, border_color, password_rect, 2, border_radius=5)

        # renderizar textos das caixas
        email_surface = FONT.render(email_text or "Digite seu usuário", True, text_color)
        password_surface = FONT.render("*" * len(password_text) or "Digite sua senha", True, text_color)

               
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
        
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT.render("Login", True, text_color)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)

        current_color = create_account_hover_color if create_account_rect.collidepoint(mouse_pos) else create_account_color
        create_account_surface = FONT_SMALL.render(create_account_text, True, current_color)
        SCREEN.blit(create_account_surface, create_account_rect.topleft)

        # Mensagem de erro
        if error_message:
            error_surface = FONT_SMALL.render(error_message, True, (255, 0, 0))
            error_rect = error_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            SCREEN.blit(error_surface, error_rect)

        pygame.display.flip()


def registrar_partida(conexao, db_cursor, usuario, pontuacao, tempo_jogo):
    db_cursor.execute("INSERT INTO historico_partidas (usuario, pontuacao, tempo) VALUES (?, ?, ?)", (usuario, pontuacao, tempo_jogo))
    conexao.commit()

def jogar_partida():
   
    tempo_inicio = time.time()

    inimigos_derrotados = random.randint(0, 2) 
    pontos_por_inimigo = 1  

    if inimigos_derrotados == 0:
        pontuacao_inimigos = 0
    else:
        pontuacao_inimigos = inimigos_derrotados * pontos_por_inimigo

    tempo_fim = time.time()
    tempo_jogo = int(tempo_fim - tempo_inicio)  

    pontos_por_tempo = tempo_jogo  

    pontuacao_total = pontuacao_inimigos + pontos_por_tempo

    return pontuacao_total, tempo_jogo

def exibir_historico(db_cursor, usuario):
    db_cursor.execute("SELECT pontuacao, tempo FROM historico_partidas WHERE usuario = ?", (usuario,))
    return db_cursor.fetchall()


if __name__ == "__main__":
    pygame.init()  # Inicializa todos os módulos do Pygame antes de qualquer uso

    # Configurações da tela
    SCREEN_WIDTH, SCREEN_HEIGHT = 1131, 637
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tela de Login")

    # Fonte
    FONT_SMALL = pygame.font.SysFont("Arial", 16)
    FONT = pygame.font.SysFont("Arial", 18)
    FONT_LOGIN = pygame.font.SysFont("Arial", 25)

    # Configurar banco de dados
    conexao, db_cursor = conectar_banco()

    try:
        while True:
            # Primeira tela: Login
            resultado_login = login_screen(conexao, db_cursor)

            if resultado_login == "create_account":
                # Se o usuário optar por criar uma conta
                create_account_screen(conexao, db_cursor)
            elif isinstance(resultado_login, tuple):
                # Login bem-sucedido: retorna os dados do usuário
                usuario_logado = resultado_login[1]  # Nome de usuário
                print(f"Bem-vindo, {usuario_logado}!")

                # Exemplo: próxima funcionalidade após login
                pontuacao, tempo_jogo = jogar_partida()
                registrar_partida(conexao, db_cursor, usuario_logado, pontuacao, tempo_jogo)

                # Exibir histórico
                historico = exibir_historico(db_cursor, usuario_logado)
                for partida in historico:
                    print(f"Pontuação: {partida[0]}, Tempo: {partida[1]} segundos.")
                
                # Encerrar após a exibição ou reiniciar o fluxo
                break

    except Exception as e:
        print(f"Erro inesperado: {e}")

    finally:
        # Fechar conexão com o banco e encerrar Pygame
        conexao.close()
        pygame.quit()
