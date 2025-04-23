import pygame, sys, pygame.mixer 
from button_class import Button
import random

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
    

   
class Dropdown:
    def __init__(self, pos, width, height, options, font, bg_color, text_color, hover_color, default = "Selecione"):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.options = options
        self.selected = default
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.expanded = False
        self.selected = options[0]

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        
        # Fundo do dropdown (quando fechado)
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.text_color, self.rect, 2, border_radius=5)  # Borda
        
        text_surface = self.font.render(self.selected, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
        
        # Se expandido, mostrar as opções
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x, 
                    self.rect.y + (i + 1) * self.rect.height, 
                    self.rect.width, 
                    self.rect.height
                )
                # Alterar cor se o mouse estiver sobre a opção
                option_color = self.hover_color if option_rect.collidepoint(mouse_pos) else self.bg_color
                pygame.draw.rect(screen, option_color, option_rect)
                pygame.draw.rect(screen, self.text_color, option_rect, 1)
                text_surface = self.font.render(option, True, self.text_color)
                screen.blit(text_surface, (option_rect.x + 10, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):  # Clique no menu principal
                self.expanded = not self.expanded
            elif self.expanded:  # Clique em uma opção
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height
                    )
                    if option_rect.collidepoint(mouse_pos):
                        self.selected = option
                        self.expanded = False
                        return option  # Retorna a opção selecionada
                self.expanded = False  # Fecha se clicado fora das opções
        return None

    
def enter_name(selected_cat, cat_image_path):
    
    
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

    # Botão "COMEÇAR JOGO"
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

    # Estados
    active = False

    while True:
        SCREEN.blit(background_image, (0, 0))

        # Texto superior
        title_text = FONT.render("Nomeie seu gatinho:", True, (106, 13, 173))
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

        # Botão de começar jogo
        mouse_pos = pygame.mouse.get_pos()
        button_color_actual = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(SCREEN, button_color_actual, start_button_rect, border_radius=8)
        start_text = FONT.render("COMEÇAR", True, (text_color))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_text, start_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                    
                if dado_rect.collidepoint(event.pos):
                    user_text = random.choice(nomes_aleatorios)  # Gera um nome aleatório


                if start_button_rect.collidepoint(event.pos):
                    # Avança para outra página (implemente a lógica aqui)
                    print(f"Nome escolhido: {user_text}")
                    return

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < max_chars:
                    user_text += event.unicode

        pygame.display.update()



def display_warning_screen_overlay(cat_image_path):
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
        warning_text = font.render("Você escolheu um gato!", True, text_color)
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


        
def play():
    global current_volume  # Referência ao volume global
    PLAY_BG = pygame.image.load("assets/fundojogar.png")
    
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

        # Botão de voltar
        back_button = Button(image=None, 
                             pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                             text_input="VOLTAR", 
                             font=get_font(20), 
                             base_color="#940d35", 
                             hovering_color="Pink")
        back_button.changeColor(PLAY_MOUSE_POS)
        back_button.update(SCREEN)
        
        
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
                if back_button.checkForInput(PLAY_MOUSE_POS):
                    return

        pygame.display.update()





def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)



def options(cats):
    global current_volume
    global music_volume
    
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

    dropdown = Dropdown(
        pos=(SCREEN.get_width() // 2 - 150, SCREEN.get_height() // 2 + 50),  # Abaixo do slider
        width=300, height=40,
        options=["Inglês", "Português", "Espanhol"],
        font=get_font(20),
        bg_color=(50, 0, 75),
        text_color=(255, 255, 255),
        hover_color=(100, 50, 150)
    )

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


        # Renderizar dropdown
        dropdown.draw(SCREEN)
        

        # Botões de voltar e aplicar
        OPTIONS_BACK = Button(image=None, pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                             text_input="VOLTAR", font=get_font(20), base_color="#940d35", hovering_color="Pink")
        APPLY_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() - 65),
                              text_input="APLICAR", font=get_font(20), base_color="#301934", hovering_color="#6A0DAD")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        APPLY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        APPLY_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return
                if APPLY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    current_volume = sound_volume_value  # Atualiza o volume global de som
                    music_volume = music_volume_value    # Atualiza o volume global de música
                    for cat in cats:
                        cat.set_volume(current_volume) # Atualiza o volume dos gatos
                    print(f"Volume som: {current_volume}, Volume música: {music_volume}")  # Para depuração
                    print(f"Dropdown selecionado: {dropdown.selected}")
                    return

            dropdown_selection = dropdown.handle_event(event)
            if dropdown_selection:
                print(f"Selecionado: {dropdown_selection}")

        sound_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])
        music_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])

        pygame.display.update()


                    #ideias:
                    #Volume (Música e Efeitos Sonoros):
                    #Idioma
                    #Resolução da Tela
def trofeu():
    while True:
        TROFEU_MOUSE_POS = pygame.mouse.get_pos()
        TROFEU_BG = pygame.image.load("assets/fundojogar.png")
        SCREEN.blit(TROFEU_BG, (0, 0))


        trofeu_TEXT = get_font(25).render("TROFEUS.", True, "White")
        trofeu_RECT = trofeu_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(trofeu_TEXT, trofeu_RECT)

        trofeu_BACK = Button(image=None, pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                             text_input="VOLTAR", font=get_font(20), base_color="#940d35", hovering_color="Pink")

        trofeu_BACK.changeColor(TROFEU_MOUSE_POS)
        trofeu_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if trofeu_BACK.checkForInput(TROFEU_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
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
    trofeu_image = pygame.transform.scale(trofeu_image, (64, 64))  # Ajuste o tamanho se necessário
    rank_image = pygame.transform.scale(rank_image, (64, 64))  # Ajuste o tamanho se necessário

        
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
                             text_input="Jogar", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        OPTIONS_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 1.7),
                                text_input="Opções", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 1.4),
                             text_input="Sair", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
                
        TROFEU_BUTTON = Button(image=trofeu_image, pos=(SCREEN.get_width() // 2 - 30, SCREEN.get_height() - 100),
                            text_input="", font=get_font(25), base_color="White", hovering_color="Green")

        RANK_BUTTON = Button(image=rank_image, pos=(SCREEN.get_width() // 2 + 30, SCREEN.get_height() - 100),
                            text_input="", font=get_font(25), base_color="White", hovering_color="Green")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, TROFEU_BUTTON, RANK_BUTTON]:
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
                    
                if TROFEU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    trofeu()  
                    
                if RANK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rank()  
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

