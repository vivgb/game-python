import pygame, sys, pygame.mixer 
from button_class import Button
from botao_gatos import criar_botoes_gatos
import pygame_gui

SLIDER_BACKGROUND_COLOR = (50, 0, 75)  # Roxo escuro
SLIDER_BORDER_COLOR = (150, 50, 200)  # Roxo claro
CURSOR_COLOR = (100, 0, 150)  # Roxo médio
CURSOR_BORDER_COLOR = (200, 100, 255)  # Roxo claro


current_volume = 0.5  # Volume inicial padrão

pygame.mixer.init()
pygame.init()

SCREEN = pygame.display.set_mode((1131, 637))
pygame.display.set_caption("Cat Adventure")
BG = pygame.image.load("assets/Background.png")

class Slider:
    def __init__(self, pos, size, initial_val, min_val, max_val):
        self.pos = pos
        self.size = (size[0], 8)  # Altura do slider ajustada
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
            self.slider_top_pos - 6,  # Ajuste para centralizar o botão
            12, 20  # Cursor levemente retangular
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
        pygame.draw.rect(screen, SLIDER_BACKGROUND_COLOR, self.container_rect)
        pygame.draw.rect(screen, SLIDER_BORDER_COLOR, self.container_rect, 2)  # Borda roxa clara

        # Botão do slider (cursor)
        pygame.draw.rect(screen, CURSOR_COLOR, self.button_rect)  # Roxo médio
        pygame.draw.rect(screen, CURSOR_BORDER_COLOR, self.button_rect, 1)  # Borda roxa clara

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





def enter_name(selected_cat, cat_image_path):
    pygame.display.set_caption("Digite o Nome do Gato")
    
    FONT = get_font(20)
    warning_visible = True  # Aviso começa visível
    # Carregar a imagem de fundo
    background_image = pygame.image.load("assets/fundojogar.png")
    background_image = pygame.transform.scale(background_image, SCREEN.get_size())  # Ajusta ao tamanho da tela

    
    manager = pygame_gui.UIManager(SCREEN.get_size())
    

    
    text_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN.get_width() // 2 - 150, SCREEN.get_height() // 2 - 25), (300, 50)),
        manager=manager,
        object_id='#name_input'
    )
    
    font = get_font(20)
    clock = pygame.time.Clock()
    user_name = ""
    
    
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        SCREEN.blit(background_image, (0, 0))  # Desenha a imagem de fundo
        
        # Exibir instrução
        text = font.render(f"Você escolheu o {selected_cat}. Digite o nome:", True, "Black")
        SCREEN.blit(text, (SCREEN.get_width() // 2 - text.get_width() // 2, SCREEN.get_height() // 2 - 100))
        
        # Gerenciar exibição do aviso
        if warning_visible:
            warning_closed = display_warning_screen_overlay(cat_image_path)
            if warning_closed:
                warning_visible = False  # O aviso foi fechado
                
        # Botão de voltar
        back_button = Button(None, (SCREEN.get_width() - 70, SCREEN.get_height() - 30), "VOLTAR", FONT, "Black", "Red")
        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        # Atualizar eventos e interface do gerenciador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_object_id == '#name_input':
                    user_name = event.text
                    print(f"Nome escolhido: {user_name}")
                    return user_name  # Retorna o nome do usuário para uso posterior
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)

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

            # Detectar clique no botão "OK"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ok_button_rect.collidepoint(mouse_pos):
                    return True
                if x_button_rect.collidepoint(mouse_pos):
                    return True

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
                        # Redireciona para a tela de entrada de nome
                        user_name= enter_name(f"Gato {idx + 1}", f"assets/cat{idx + 1}.png")
                        print(f"Nome final do gato {idx + 1 }: `")
                        return  # Sai da tela de jogo após redirecionar

                # Verificar clique no botão de voltar
                if back_button.checkForInput(PLAY_MOUSE_POS):
                    return

        pygame.display.update()





def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

    
def options(cats):
    global current_volume  # Referência ao volume global
    global music_volume    # Volume para música de fundo

    # Criar sliders para som e música
    sound_slider = Slider((SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 20), (300, 20), current_volume, 0.0, 1.0)
    music_slider = Slider((SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 100), (300, 20), 0.5, 0.0, 1.0)

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BG = pygame.image.load("assets/fundojogar.png")
        SCREEN.blit(OPTIONS_BG, (0, 0))

        # Títulos menores e posicionados acima dos sliders
        MUSIC_TEXT = get_font(20).render("MUSICA", True, (200, 200, 255))  # Texto lilás-claro, menor
        MUSIC_RECT = MUSIC_TEXT.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 140))
        SCREEN.blit(MUSIC_TEXT, MUSIC_RECT)

        SOUND_TEXT = get_font(20).render("SOM", True, (200, 200, 255))  # Texto lilás-claro, menor
        SOUND_RECT = SOUND_TEXT.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 60))
        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        # Renderizar sliders
        sound_slider.render(SCREEN)
        music_slider.render(SCREEN)

        # Atualizar sliders com entrada do mouse
        sound_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])
        music_slider.update(OPTIONS_MOUSE_POS, pygame.mouse.get_pressed()[0])

        # Obter valores dos sliders
        sound_volume_value = sound_slider.get_value()
        music_volume_value = music_slider.get_value()

        # Botões estilizados
        OPTIONS_BACK = Button(image=None, 
                             pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                             text_input="VOLTAR", 
                             font=get_font(20), 
                             base_color="#940d35", 
                             hovering_color="Pink")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        APPLY_BUTTON = Button(image=None, pos=(SCREEN.get_width() // 2, SCREEN.get_height() - 150),
                              text_input="APLICAR", font=get_font(25), base_color="#301934", hovering_color="#6A0DAD")

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
                        cat.set_volume(current_volume)  # Atualiza o volume dos gatos
                    print(f"Volume som: {current_volume}, Volume música: {music_volume}")  # Para depuração
                    return

        pygame.display.update()


                    #ideias:
                    #Volume (Música e Efeitos Sonoros):
                    #Idioma
                    #Resolução da Tela


def main_menu():
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

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
