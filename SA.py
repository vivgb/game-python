import sqlite3
import random
import time
import pygame
import pygame, sys, pygame.mixer, random
from button_class import Button

# Dicionário de traduções
Traducoes = {
    "Inglês": {
        "start" : "Game",
        "options": "Options",
        "quit" : "Quit",
        "name_your_cat": "Name your kitten:",
        "start_game": "START",
        "return": "BACK",
        "apply": "APPLY",
        "volume_sound": "Sound Volume",
        "volume_music": "Music Volume",
        "warning": "You chose a cat!",
        "map_selection" : "Map selection"
    },
    "Português": {
        "start" : "Jogar",
        "options": "Opções",
        "quit" : "Sair",
        "name_your_cat": "Nomeie seu gatinho:",
        "start_game": "COMEÇAR",
        "return": "VOLTAR",
        "apply": "APLICAR",
        "volume_sound": "Volume do Som",
        "volume_music": "Volume da Música",
        "warning": "Você escolheu um gato!",
        "map_selection" : "Seleçao de mapa"
    },
    "Espanhol": {
        "start" : "Jugar",
        "options": "Opciones",
        "quit" : "Abandonar",
        "name_your_cat": "Nombra a tu gatito:",
        "start_game": "INICIAR",
        "return": "ATRÁS",
        "apply": "APLICAR",
        "volume_sound": "Volumen del Sonido",
        "volume_music": "Volumen de la Música",
        "warning": "¡Elegiste un gato!",
        "map_selection" : "selección de mapa"
    }
}

# Variável global para o idioma
current_language = "Português"




SLIDER_BACKGROUND_COLOR = (208, 176, 241)  # lilás claro
SLIDER_BORDER_COLOR = (150, 50, 200)  # Roxo claro
CURSOR_COLOR = (100, 0, 150)  # Roxo médio
CURSOR_BORDER_COLOR = (200, 100, 255)  # Roxo claro


current_volume = 0.5  # Volume inicial padrão

pygame.mixer.init()
pygame.init()

SCREEN = pygame.display.set_mode((1131, 637))
pygame.display.set_caption("Cat Adventure")
BG = pygame.image.load("assets/Background.png")
paw_image = pygame.image.load("assets/mao_gatos.png")
paw_image = pygame.transform.scale(paw_image, (50, 50))  # Ajuste o tamanho da imagem


# Definições globais de fontes
FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT = pygame.font.SysFont("Arial", 18)
FONT_LOGIN = pygame.font.SysFont("Arial", 25)


class Slider:

    def __init__(self, pos, size, initial_val, min_val, max_val):
        self.pos = pos
        self.size = (size[0], 15)  # Altura do slider ajustada
        self.hovered = False
        self.grabbed = False
        self.min_val = min_val
        self.max_val = max_val
        self.initial_val = initial_val

        self.slider_left_pos = self.pos[0] - (self.size[0] // 2)
        self.slider_right_pos = self.pos[0] + (self.size[0] // 2)
        self.slider_top_pos = self.pos[1] - (self.size[1] // 2)
        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        
        # Botão (cursor) ajustado
        self.button_rect = pygame.Rect(
            self.slider_left_pos + (self.initial_val * size[0]) - 5,
            self.slider_top_pos - 10,  # Ajuste para centralizar o botão
            30, 30  
        )

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / val_range) * (self.max_val - self.min_val) + self.min_val


    def render(self, screen):
        # Fundo do slider (linha)
        pygame.draw.rect(screen, SLIDER_BACKGROUND_COLOR, self.container_rect,border_radius=10) # Fundo arredondado
        pygame.draw.rect(screen, SLIDER_BORDER_COLOR, self.container_rect, 2,border_radius=10)  # Borda do slider arredondada

        # Botão do slider (pata de gato)
        paw_center = (self.button_rect.centerx, self.pos[1])  # Centraliza a pata no eixo vertical
        paw_rect = paw_image.get_rect(center=paw_center)
        screen.blit(paw_image, paw_rect)

    def update(self, mouse_pos, mouse_pressed):
        if self.container_rect.collidepoint(mouse_pos):
            self.hovered = True
            if mouse_pressed:
                self.grabbed = True
        else:
            self.hovered = False

        if not mouse_pressed:
            self.grabbed = False

        if self.grabbed:
            self.move_slider(mouse_pos)

class Cat:
    def __init__(self, image_path, pos, sound_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.hover_offset = -10  # Levanta no hover
        self.sound = pygame.mixer.Sound(sound_path)
        self.volume = 0.5  # Volume inicial padrão
        self.sound.set_volume(self.volume)  # Inicializa o som com o volume padrão
        self.sound_played = False

    def set_volume(self, volume):
        """Ajusta o volume do som associado ao gato."""
        self.volume = volume
        self.sound.set_volume(self.volume)  # Atualiza o volume no som

    def play_sound(self):
        """Toca o som com o volume atualizado."""
        self.sound.play()

    def draw(self, screen, mouse_pos):
        """Desenha o botão e verifica hover."""
        if self.rect.collidepoint(mouse_pos):
            if not self.sound_played:
                self.play_sound()
                self.sound_played = True
            screen.blit(self.image, (self.rect.x, self.rect.y + self.hover_offset))
        else:
            self.sound_played = False
            screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

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
                    print("Botão de login clicado!")
                    if not email_text or not password_text:
                        error_message = "Por favor, preencha todos os campos."
                    else:
                        user = autenticar_usuario(db_cursor, email_text, password_text)
                        if user:
                            print("Usuário autenticado:",user)
                            return "main_menu" # Redireciona para a tela do menu principal
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
        
        
def main():
    conexao, db_cursor = conectar_banco()  # Conexão com o banco de dados
    tela_atual = "login"  # A primeira tela é o login

    while True:
        if tela_atual == "login":
            resultado = login_screen(conexao, db_cursor)  # Tela de login
            if resultado == "main_menu":
                tela_atual = "main_menu"
                print("Redirecionando para:", tela_atual)
            elif resultado == "create_account":
                tela_atual = "create_account"
                print("Redirecionando para:",tela_atual)
        elif tela_atual == "main_menu":
            main_menu()  # Tela do menu principal
        elif tela_atual == "create_account":
            create_account_screen(conexao, db_cursor)  # Tela de criar conta (implemente conforme necessário)
            tela_atual = "login"

def game_screen(selected_map):
    running = True
    FONT = get_font(24)
    
    while running:
        SCREEN.fill((50, 50, 50))  # Fundo cinza escuro

        # Exibe o mapa selecionado
        text = FONT.render(f"Mapa selecionado: {selected_map + 1}", True, (255, 255, 255))
        SCREEN.blit(text, (SCREEN.get_width() // 2 - text.get_width() // 2, SCREEN.get_height() // 2 - 20))

        # Exibe mensagem informando que o jogo será implementado
        info_text = FONT.render("Tela do jogo!", True, (255, 255, 255))
        SCREEN.blit(info_text, (SCREEN.get_width() // 2 - info_text.get_width() // 2, SCREEN.get_height() // 2 + 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        
        
def enter_name(selected_cat, cat_image_path):
    
    global current_language  # Indica que vamos usar a variável global
    
    
    user_text = ""
    max_chars = 20  # Limite de caracteres
    FONT = get_font(18)
    SMALL_FONT = get_font(14)

    # Configurações da caixa de texto
    input_rect_width = 400
    input_rect_height = 50
    input_rect = pygame.Rect(
        (SCREEN.get_width() - input_rect_width) // 2,  # Centraliza no eixo X
        SCREEN.get_height() // 2 - 160,  # Centraliza verticalmente
        input_rect_width,
        input_rect_height
    )
    
    
    # carregar a imagem do dado 
    dado_imagem = pygame.image.load("assets/dado.png")
    dado_imagem = pygame.transform.scale(dado_imagem, (70, 70)) # tamanho do dado
    dado_rect = dado_imagem.get_rect(
        center=(input_rect.left - 30, input_rect.centery)
    )  # Posiciona o dado à esquerda da caixa



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
        SCREEN.get_height() // 2 + 150,  # Abaixo da caixa de texto
        200, 50
    )
    
    # nomes aleatorios
    
    nomes_aleatorios = ["Miau", "Biscoito", "Fluffy", "Mingau", "Fofinho"]


    # Fundo
    background_image = pygame.image.load("assets/fundojogar.png")
    background_image = pygame.transform.scale(background_image, SCREEN.get_size())

    BACK_button = pygame.Rect(
        (SCREEN.get_width() - 200),  # Centraliza horizontalmente
        SCREEN.get_height() - 50,  # Abaixo da caixa de texto
        150, 40
    )
    
    # Estados
    active = False
    
    # Configurações de animação
    
    
    frame_largura = 128  # Largura de cada frame (ajuste conforme sua sprite sheet)
    frame_altura = 128   # Altura de cada frame (ajuste conforme sua sprite sheet)
    imagens_lambendo = []

    # Garante o nome correto do arquivo de animação
    sprite_path = f"{cat_image_path.replace('.png', '_lambida.png')}"

    # Carrega a sprite sheet do gato escolhido
    try:
        img_gato = pygame.image.load(sprite_path).convert_alpha()
    except pygame.error:
        print(f"Erro: O arquivo {sprite_path} não foi encontrado. Verifique o nome e o diretório.")
        pygame.quit()
        sys.exit()

    # Calcula o tamanho de cada frame com base no número total de frames
    numero_frames = 4  # Ajuste para o número real de frames na sprite sheet
    frame_largura = img_gato.get_width() // numero_frames
    frame_altura = img_gato.get_height()

    # Define a escala desejada para redimensionar os frames
    nova_largura = 150  # Ajuste conforme necessário
    nova_altura = int((frame_altura / frame_largura) * nova_largura)  # Mantém proporção

    # Dividir e redimensionar os frames
    for i in range(numero_frames):
        frame = img_gato.subsurface(pygame.Rect(
            (i * frame_largura, 0),
            (frame_largura, frame_altura)
        ))
        frame = pygame.transform.scale(frame, (nova_largura, nova_altura))
        imagens_lambendo.append(frame)

    # Calcula o centro da tela
    screen_width, screen_height = 1131, 637  # Dimensões fixas da tela
    center_x = (screen_width - nova_largura) // 2
    center_y = (screen_height - nova_altura) // 2

    # Ajusta o retângulo da animação
    gato_animacao_rect = pygame.Rect(
        center_x,  # Centraliza horizontalmente
        center_y,  # Centraliza verticalmente
        nova_largura,
        nova_altura
    )


    # Variáveis de controle da animação
    animacao_index = 0
    tempo_animacao = 0


    while True:
        ENTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(background_image, (0, 0))

        # Texto superior
        title_text = FONT.render (Traducoes[current_language]["name_your_cat"], True, (106, 13, 173))
        title_rect = title_text.get_rect(center=(SCREEN.get_width() // 2, 120))
        SCREEN.blit(title_text, title_rect)
        

        # Caixa de texto
        color = active_color if active else inactive_color
        pygame.draw.rect(SCREEN, color, input_rect, border_radius=5)
        pygame.draw.rect(SCREEN, border_color, input_rect, 2, border_radius=5)

        # Texto na caixa de texto
        text_surface = FONT.render(user_text, True, (50, 50, 50))
        if text_surface.get_width() > input_rect.width - 20:
            user_text = user_text[:-1]  # Limita caracteres que ultrapassam
        SCREEN.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # Indicador de caracteres
        char_count = SMALL_FONT.render(f"{len(user_text)}/{max_chars}", True, text_color)
        SCREEN.blit(char_count, (input_rect.right + 10, input_rect.y + 15))
        
        # Imagem do dado
        SCREEN.blit(dado_imagem, dado_rect)
        
        # Exibir animação do gato
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_animacao > 100:  # 100ms por frame
            animacao_index = (animacao_index + 1) % len(imagens_lambendo)
            tempo_animacao = tempo_atual

        # Blit do frame atual da animação
        # Renderiza o frame atual da animação centralizado
        SCREEN.blit(imagens_lambendo[animacao_index], gato_animacao_rect)

        # Botão de começar jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT.render(Traducoes[current_language]["start_game"], True, text_color)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)
        
        # Botão de VOLTAR jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if BACK_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, BACK_button, border_radius=8)
        back_text = FONT.render(Traducoes[current_language]["return"], True, text_color)
        start_text_rect = back_text.get_rect(center=BACK_button.center)
        SCREEN.blit(back_text, start_text_rect)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                
                if BACK_button.collidepoint(ENTER_MOUSE_POS):
                    return # volta para a tela de seleção de gatos
                    
                if dado_rect.collidepoint(event.pos):
                    user_text = random.choice(nomes_aleatorios)  # Gera um nome aleatório


                if start_button_rect.collidepoint(event.pos):
                    # Avança para a tela de seleção de mapa
                    selected_map = select_map()
                    if selected_map != -1: # Apenas avança se o usuário não clicar em "Voltar"
                        game_screen(selected_map)# Passa o mapa selecionado para a função play()
                        return

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < max_chars:
                    user_text += event.unicode

        pygame.display.update()



def display_warning_screen_overlay(cat_image_path):
    global current_language 
    
    
    font = get_font(14)  # Fonte tamanho
    clock = pygame.time.Clock()
    cat_image = pygame.image.load(cat_image_path)
    cat_image = pygame.transform.scale(cat_image, (80, 80))  # Gato menor para combinar com o layout

    # Dimensões ajustadas da caixa
    rect_x, rect_y, rect_width, rect_height = 320, 200, 360, 220
    border_thickness = 4  # Borda fina para elegância

    # Paleta de cores
    border_color = (100, 50, 150)  # Roxo suave
    box_color = (240, 230, 250)   # Fundo claro, quase pastel
    text_color = (0, 0, 0)        # Preto
    button_color = (200, 180, 220)  # Roxo claro para o botão
    button_border_color = (100, 50, 150)  # Roxo médio
    button_text_color = (0, 0, 0)  # Preto

    dragging = False  # Flag para controlar se estamos arrastando a caixa
    offset_x, offset_y = 0, 0  # Deslocamento do mouse em relação à posição inicial da caixa

    while True:
        # Não preenche o fundo para preservar o fundo atual
        pygame.draw.rect(SCREEN, border_color,
                         (rect_x - border_thickness, rect_y - border_thickness,
                          rect_width + 2 * border_thickness, rect_height + 2 * border_thickness))
        pygame.draw.rect(SCREEN, box_color,
                         (rect_x, rect_y, rect_width, rect_height))

        # Texto de aviso centralizado
        warning_text = font.render(Traducoes[current_language]["warning"], True, text_color)
        warning_text_rect = warning_text.get_rect(center=(rect_x + rect_width // 2, rect_y + 50))
        SCREEN.blit(warning_text, warning_text_rect)

        # Gato centralizado
        cat_image_rect = cat_image.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2 + 10))
        SCREEN.blit(cat_image, cat_image_rect)

        # Botão "OK"
        ok_button_width, ok_button_height = 80, 30
        ok_button_rect = pygame.Rect(
            rect_x + rect_width // 2 - ok_button_width // 2,
            rect_y + rect_height - ok_button_height - 20,
            ok_button_width,
            ok_button_height
        )
        pygame.draw.rect(SCREEN, button_color, ok_button_rect)
        pygame.draw.rect(SCREEN, button_border_color, ok_button_rect, 2)  # Borda do botão
        ok_text = font.render("OK", True, button_text_color)
        ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
        SCREEN.blit(ok_text, ok_text_rect)

        # Botão "X" minimalista
        x_button_size = 20
        x_button_rect = pygame.Rect(
            rect_x + rect_width - x_button_size - 10,
            rect_y + 10,
            x_button_size,
            x_button_size
        )
        pygame.draw.rect(SCREEN, button_border_color, x_button_rect)
        x_text = font.render("X", True, button_text_color)
        x_text_rect = x_text.get_rect(center=x_button_rect.center)
        SCREEN.blit(x_text, x_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ok_button_rect.collidepoint(mouse_pos) or x_button_rect.collidepoint(mouse_pos):
                    return True  # Retorna após a interação do usuário
        
        # Atualizar a tela
        pygame.display.update()
        clock.tick(30)

def select_map():
    SCREEN_WIDTH, SCREEN_HEIGHT = 1131, 637
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fundo e fonte
    MAP_BG = pygame.image.load("assets/fundojogar.png")
    MAP_BG = pygame.transform.scale(MAP_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    FONT = get_font(24)
    FONT_SMALL = get_font(18)
    
    # Paleta de cores
    bg_color = (240, 230, 250)  # Fundo lilás suave
    border_color = (200, 100, 255)  # Borda roxa clara
    text_color = (50, 50, 50)  # Preto para o texto
    button_color = (200, 150, 255)  # Botão lilás suave
    button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
    active_color = (220, 180, 255)  # Caixa ativa
    inactive_color = bg_color  # Caixa inativa


    # Mapas
    MAP_WIDTH, MAP_HEIGHT = 800, 500  # Tamanhos ajustados para caber na tela
    map_images = [
        pygame.image.load("assets/1.png"),
        pygame.image.load("assets/2.png"),
        pygame.image.load("assets/3.png")
    ]
    map_images = [pygame.transform.scale(img, (MAP_WIDTH, MAP_HEIGHT)) for img in map_images]

    # Centralizar mapas horizontalmente
    SPACING = -370  # Espaçamento entre mapas
    total_width = len(map_images) * MAP_WIDTH + (len(map_images) - 1) * SPACING
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - MAP_HEIGHT) // 2  # Verticalmente no centro

    map_positions = [
        (start_x + i * (MAP_WIDTH + SPACING), start_y) for i in range(len(map_images))
    ]

    # Botão de voltar
    BACK_button = pygame.Rect(
        SCREEN.get_width() - 200,  # Botão no canto inferior direito
        SCREEN.get_height() - 50,
        150, 40
    )

    selected_map = None

    while selected_map is None:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(MAP_BG, (0, 0))

        # Título
        title_text = FONT.render("Seleção de Mapas", True, (106, 13, 173))
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Desenhar mapas
        for idx, (map_image, position) in enumerate(zip(map_images, map_positions)):
            x, y = position
            rect = pygame.Rect(x, y, MAP_WIDTH, MAP_HEIGHT)

            # Levantar mapa se o mouse estiver em cima
            if rect.collidepoint(mouse_pos):
                SCREEN.blit(map_image, (x, y - 10))  # Levanta o mapa
            else:
                SCREEN.blit(map_image, (x, y))

        # Botão de voltar
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if BACK_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, BACK_button, border_radius=8)
        back_text = FONT_SMALL.render(Traducoes[current_language]["return"],True, text_color)
        SCREEN.blit(back_text, back_text.get_rect(center=BACK_button.center))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clique no botão voltar
                if BACK_button.collidepoint(mouse_pos):
                    return -1  # Voltar

                # Clique no mapa
                for idx, position in enumerate(map_positions):
                    rect = pygame.Rect(position[0], position[1], MAP_WIDTH, MAP_HEIGHT)
                    if rect.collidepoint(mouse_pos):
                        selected_map = idx

        pygame.display.update()

    return selected_map

        
def play():
    global current_volume



    # Prosseguir apenas se um mapa foi selecionado
    PLAY_BG = pygame.image.load("assets/fundojogar.png")

    
    # Restante do código de play...

    
    FONT = get_font(18)
    
    # Paleta de cores
    bg_color = (240, 230, 250)  # Fundo lilás suave
    border_color = (200, 100, 255)  # Borda roxa clara
    text_color = (50, 50, 50)  # Preto para o texto
    button_color = (200, 150, 255)  # Botão lilás suave
    button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
    active_color = (220, 180, 255)  # Caixa ativa
    inactive_color = bg_color  # Caixa inativa


    BACK_button = pygame.Rect(
        (SCREEN.get_width() - 200),  # Centraliza horizontalmente
        SCREEN.get_height() - 50,  # Abaixo da caixa de texto
        150, 40
    )
    
    # Cria os gatos e aplica o volume global
    cats = [
        Cat("assets/cat1.png", (300, 200), "assets/audiogato.wav"),
        Cat("assets/cat2.png", (550, 200), "assets/audiogato.wav"),
        Cat("assets/cat3.png", (800, 200), "assets/audiogato.wav"),
        Cat("assets/cat4.png", (300, 400), "assets/audiogato.wav"),
        Cat("assets/cat5.png", (550, 400), "assets/audiogato.wav"),
        Cat("assets/cat6.png", (800, 400), "assets/audiogato.wav")
    ]
    for cat in cats:
        cat.set_volume(current_volume)  # Aplica o volume ajustado

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(PLAY_BG, (0, 0))

        # Desenhar os gatos
        for idx, cat in enumerate(cats):
            cat.draw(SCREEN, PLAY_MOUSE_POS)

        # Botão de VOLTAR jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if BACK_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, BACK_button, border_radius=8)
        back_text = FONT.render(Traducoes[current_language]["return"], True, text_color)
        start_text_rect = back_text.get_rect(center=BACK_button.center)
        SCREEN.blit(back_text, start_text_rect)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clique em gatos
                for idx, cat in enumerate(cats):
                    if cat.is_clicked(PLAY_MOUSE_POS):
                        # Exibe o aviso e aguarda a confirmação do usuário
                        result = display_warning_screen_overlay(f"assets/cat{idx + 1}.png")
                        if result:  # Se o usuário clicar em "OK" ou "X"
                            # Após o aviso, vai para a tela de nomeação
                            enter_name(f"Gato {idx + 1}", f"assets/cat{idx + 1}.png")
                        return  # Sai do loop de evento para evitar problemas
                    
                # Verificar clique no botão de voltar
                if BACK_button.collidepoint(PLAY_MOUSE_POS):
                    return

        pygame.display.update() 


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)



def options(cats):
    global current_volume
    global music_volume
    global current_language  # Permite alterar o idioma global
    
    FONT = get_font(18)
    
    # Paleta de cores
    bg_color = (240, 230, 250)  # Fundo lilás suave
    border_color = (200, 100, 255)  # Borda roxa clara
    text_color = (50, 50, 50)  # Preto para o texto
    button_color = (200, 150, 255)  # Botão lilás suave
    button_hover_color = (170, 120, 230)  # Botão ao passar o mouse
    active_color = (220, 180, 255)  # Caixa ativa
    inactive_color = bg_color  # Caixa inativa
    
    OPTIONS_BACK = pygame.Rect(
        (SCREEN.get_width() - 200),  # Centraliza horizontalmente
        SCREEN.get_height() - 50,  # Abaixo da caixa de texto
        150, 40
    )
    
    # Dimensões do botão
    button_width = 150
    button_height = 40

    # Calculando a posição centralizada
    APPLY_BUTTON = pygame.Rect(
        (1131 - button_width) // 2,  # Centraliza horizontalmente
        637 - 100,                  # Mantém a posição vertical atual
        button_width,
        button_height
    )
    

    # Carregar e redimensionar ícones de som
    sound_icons = {
        "mute": pygame.transform.scale(pygame.image.load("assets/som_mudo.png"), (40, 40)),
        "low": pygame.transform.scale(pygame.image.load("assets/som_baixo.png"), (40, 40)),
        "medium": pygame.transform.scale(pygame.image.load("assets/som_medio.png"), (40, 40)),
        "high": pygame.transform.scale(pygame.image.load("assets/som_alto.png"), (40, 40)),
    }

    icon_music = pygame.transform.scale(pygame.image.load("assets/icon_musica.png"), (40, 40))

    sound_slider = Slider((SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 20), (300, 20), current_volume, 0.0, 1.0)
    music_slider = Slider((SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 100), (300, 20), 0.5, 0.0, 1.0)

    # Opções de idioma para o menu 
    language_options = ["Português", "Inglês", "Espanhol"]
    selected_language_index = 0  # Começa no primeiro idioma da lista

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BG = pygame.image.load("assets/fundojogar.png")
        SCREEN.blit(OPTIONS_BG, (0, 0))

        # Renderizar sliders
        sound_slider.render(SCREEN)
        music_slider.render(SCREEN)

        # Obter valores dos sliders
        sound_volume_value = sound_slider.get_value()
        music_volume_value = music_slider.get_value()

        # Escolher ícone de som com base no valor do slider
        if sound_volume_value == 0:
            sound_icon = sound_icons["mute"]
        elif sound_volume_value <= 0.33:
            sound_icon = sound_icons["low"]
        elif sound_volume_value <= 0.66:
            sound_icon = sound_icons["medium"]
        else:
            sound_icon = sound_icons["high"]

        # Renderizar o ícone ao lado do slider
        icon_rect = sound_icon.get_rect(midright=(sound_slider.container_rect.left - 20, sound_slider.container_rect.centery))
        SCREEN.blit(sound_icon, icon_rect)

        # Renderizar o ícone de música ao lado do slider de música
        music_rect = icon_music.get_rect(midright=(music_slider.container_rect.left - 20, music_slider.container_rect.centery))
        SCREEN.blit(icon_music, music_rect)
        
        
        # Retângulo arredondado para idioma
        language_box_width = 200
        language_box_height = 40
        language_box_x = (SCREEN.get_width() - language_box_width) // 2
        language_box_y = SCREEN.get_height() // 2 + 60
        language_box_rect = pygame.Rect(language_box_x, language_box_y, language_box_width, language_box_height)

        pygame.draw.rect(SCREEN, (208, 176, 241), language_box_rect, border_radius=15)  # Retângulo lilás claro



        # Renderizar o idioma selecionado dentro do retângulo
        language_text = get_font(20).render(language_options[selected_language_index], True, (103,50,138,255))
        language_text_rect = language_text.get_rect(center=language_box_rect.center)
        SCREEN.blit(language_text, language_text_rect)

        # Renderizar as setas fora do retângulo
        left_arrow = get_font(30).render("<", True, (103,50,138,255))
        right_arrow = get_font(30).render(">", True, (103, 50,138,255))
        left_rect = left_arrow.get_rect(midright=(language_box_rect.left - 20, language_box_rect.centery))
        right_rect = right_arrow.get_rect(midleft=(language_box_rect.right + 20, language_box_rect.centery))

        

        SCREEN.blit(left_arrow, left_rect)
        SCREEN.blit(right_arrow, right_rect)
        
        # Botão de VOLTAR jogo
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if OPTIONS_BACK.collidepoint(OPTIONS_MOUSE_POS) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, OPTIONS_BACK, border_radius=8)
        back_text = FONT.render(Traducoes[current_language]["return"], True, text_color)
        start_text_rect = back_text.get_rect(center=OPTIONS_BACK.center)
        SCREEN.blit(back_text, start_text_rect)
        

        # Botões de voltar e aplicar
   
        # Botão de APLICAR
        button_color_actual = button_hover_color if APPLY_BUTTON.collidepoint(OPTIONS_MOUSE_POS) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, APPLY_BUTTON, border_radius=8)
        apply_text = FONT.render(Traducoes[current_language]["apply"], True, text_color)
        apply_text_rect = apply_text.get_rect(center=APPLY_BUTTON.center)
        SCREEN.blit(apply_text, apply_text_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.collidepoint(OPTIONS_MOUSE_POS):
                    return
                if APPLY_BUTTON.collidepoint(OPTIONS_MOUSE_POS):
                    current_volume = sound_volume_value
                    music_volume = music_volume_value
                    current_language = language_options[selected_language_index]  # Define o idioma global aqui
                    for cat in cats:
                        cat.set_volume(current_volume)
                    return
                
                # Verificar cliques nas setas
                if left_rect.collidepoint(OPTIONS_MOUSE_POS):
                    selected_language_index = (selected_language_index - 1) % len(language_options)
                if right_rect.collidepoint(OPTIONS_MOUSE_POS):
                    selected_language_index = (selected_language_index + 1) % len(language_options)

            # Alternar idioma com teclas de seta
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_language_index = (selected_language_index - 1) % len(language_options)
                if event.key == pygame.K_RIGHT:
                    selected_language_index = (selected_language_index + 1) % len(language_options)

        sound_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])
        music_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])

        pygame.display.update()



                    #ideias:
                    #Volume (Música e Efeitos Sonoros):
                    #Idioma
                    #Resolução da Tela

        
def rank():
    while True:
        RANK_MOUSE_POS = pygame.mouse.get_pos()
        RANK_BG = pygame.image.load("assets/fundojogar.png")
        SCREEN.blit(RANK_BG, (0, 0))



        rank_TEXT = get_font(45).render("RAnk.", True, "White")
        rank_RECT = rank_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(rank_TEXT, rank_RECT)

        rank_BACK = Button(image=None, pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                             text_input="VOLTAR", font=get_font(20), base_color="#940d35", hovering_color="Pink")

        rank_BACK.changeColor(RANK_MOUSE_POS)
        rank_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rank_BACK.checkForInput(RANK_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    
    trofeu_image = pygame.image.load("assets/trofeu.png")
    rank_image = pygame.image.load("assets/classificação.png")

    # Opcional: redimensionar as imagens
    rank_image = pygame.transform.scale(rank_image, (80, 80))  # Ajuste o tamanho se necessário

        
    # Cria a lista de gatos
    cats = [
        Cat("assets/cat1.png", (300, 200), "assets/audiogato.wav"),
        Cat("assets/cat2.png", (550, 200), "assets/audiogato.wav"),
        Cat("assets/cat3.png", (800, 200), "assets/audiogato.wav"),
        Cat("assets/cat4.png", (300, 400), "assets/audiogato.wav"),
        Cat("assets/cat5.png", (550, 400), "assets/audiogato.wav"),
        Cat("assets/cat6.png", (800, 400), "assets/audiogato.wav")
    ]

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Botões do menu
        
        
        PLAY_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2.1),
                             text_input=Traducoes[current_language]["start"], font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        OPTIONS_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 1.7),
                                text_input=Traducoes[current_language]["options"], font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 1.4),
                             text_input=Traducoes[current_language]["quit"], font=get_font(25), base_color="#d7fcd4", hovering_color="White")
                
        RANK_BUTTON = Button(image=rank_image, pos=(SCREEN.get_width() // 2 , SCREEN.get_height() - 100),
                            text_input="", font=get_font(25), base_color="White", hovering_color="Green")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, RANK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Já funciona normalmente
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(cats)  # Passa a lista de gatos para opções
                    
      
                if RANK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rank()  
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()




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
    pygame.init()
    conexao, db_cursor = conectar_banco()
    
    try:
        main()  # Deixe o controle para o loop principal
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        conexao.close()
        pygame.quit()

