import pygame, sys
from button_class import Button
from botao_gatos import criar_botoes_gatos


pygame.init()

SCREEN = pygame.display.set_mode((1131, 637))
pygame.display.set_caption("Cat Adventure")
BG = pygame.image.load("assets/Background.png")


class Cat:
    def __init__(self, image_path, pos):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (150, 150))  # Redimensiona
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.hover_offset = -10  # Levanta no hover

    def draw(self, screen, mouse_pos):
        # Levanta o botão se o mouse estiver sobre ele
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image, (self.rect.x, self.rect.y + self.hover_offset))
        else:
            screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def enter_name(selected_cat, cat_image_path):
    user_input = ""
    FONT = get_font(20)
    warning_visible = True  # Aviso começa visível

    # Carregar a imagem de fundo
    background_image = pygame.image.load("assets/fundojogar.png")
    background_image = pygame.transform.scale(background_image, SCREEN.get_size())  # Ajusta ao tamanho da tela

    while True:
        SCREEN.blit(background_image, (0, 0))  # Desenha a imagem de fundo
        text = FONT.render(f"Você escolheu o {selected_cat}.", True, "Black")
        SCREEN.blit(text, (50, 200))

        # Exibir o texto digitado pelo usuário
        input_text = FONT.render(user_input, True, "Black")
        SCREEN.blit(input_text, (50, 250))

        # Gerenciar exibição do aviso
        if warning_visible:
            warning_closed = display_warning_screen_overlay(cat_image_path)
            if warning_closed:
                warning_visible = False  # O aviso foi fechado

        # Botão de voltar
        back_button = Button(None, (SCREEN.get_width() - 70, SCREEN.get_height() - 30), "VOLTAR", FONT, "Black", "Red")
        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Processa entrada de nome apenas se o aviso estiver fechado
            if not warning_visible:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(f"Nome inserido: {user_input}")
                        return
                    else:
                        user_input += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(pygame.mouse.get_pos()):
                        return

        pygame.display.update()

def display_warning_screen_overlay(cat_image_path):
    font = get_font(14)
    clock = pygame.time.Clock()
    cat_image = pygame.image.load(cat_image_path)
    cat_image = pygame.transform.scale(cat_image, (80, 80))  # Redimensionar a imagem do gato

    # Dimensões ajustadas da caixa
    rect_x, rect_y, rect_width, rect_height = 320, 200, 360, 220
    border_thickness = 4

    # Paleta de cores
    background_color = (240, 230, 250)  # Cor de fundo da tela
    border_color = (100, 50, 150)
    box_color = (240, 230, 250)
    text_color = (0, 0, 0)
    button_color = (200, 180, 220)
    button_border_color = (100, 50, 150)
    button_text_color = (0, 0, 0)

    dragging = False  # Controle para arrastar a mensagem
    offset_x, offset_y = 0, 0  # Deslocamento do mouse em relação à caixa

    while True:
        # Limpa o fundo antes de redesenhar
        SCREEN.fill(background_color)

        # Desenha a borda e a caixa
        pygame.draw.rect(SCREEN, border_color,
                         (rect_x - border_thickness, rect_y - border_thickness,
                          rect_width + 2 * border_thickness, rect_height + 2 * border_thickness))
        pygame.draw.rect(SCREEN, box_color, (rect_x, rect_y, rect_width, rect_height))

        # Texto centralizado
        warning_text = font.render("Você escolheu um gato!", True, text_color)
        warning_text_rect = warning_text.get_rect(center=(rect_x + rect_width // 2, rect_y + 50))
        SCREEN.blit(warning_text, warning_text_rect)

        # Exibir imagem do gato
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
        pygame.draw.rect(SCREEN, button_border_color, ok_button_rect, 2)
        ok_text = font.render("OK", True, button_text_color)
        ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
        SCREEN.blit(ok_text, ok_text_rect)

        # Botão "X"
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

            # Detecta clique do mouse para começar a arrastar a mensagem
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rect_x <= mouse_pos[0] <= rect_x + rect_width and rect_y <= mouse_pos[1] <= rect_y + rect_height:
                    dragging = True
                    offset_x = mouse_pos[0] - rect_x
                    offset_y = mouse_pos[1] - rect_y
                # Verifica clique no botão "OK"
                if ok_button_rect.collidepoint(mouse_pos):
                    return True
                # Verifica clique no botão "X"
                if x_button_rect.collidepoint(mouse_pos):
                    return True

            # Solta a mensagem ao soltar o botão do mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            # Movimenta a mensagem se estiver arrastando
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    rect_x = mouse_pos[0] - offset_x
                    rect_y = mouse_pos[1] - offset_y

        pygame.display.update()
        clock.tick(30)


        
def play():
    PLAY_BG = pygame.image.load("assets/fundojogar.png")
    cats = [
        Cat("assets/cat1.png", (300, 200)),
        Cat("assets/cat2.png", (550, 200)),
        Cat("assets/cat3.png", (800, 200)),
        Cat("assets/cat4.png", (300, 400)),
        Cat("assets/cat5.png", (550, 400)),
        Cat("assets/cat6.png", (800, 400))
    ]

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
                        enter_name(f"Gato {idx + 1}", f"assets/cat{idx + 1}.png")
                        return  # Sai da tela de jogo após redirecionar

                # Verificar clique no botão de voltar
                if back_button.checkForInput(PLAY_MOUSE_POS):
                    return

        pygame.display.update()



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

    
def options():
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BG = pygame.image.load("assets/fundojogar.png")
        
        
        SCREEN.blit(OPTIONS_BG, (0, 0))

             
        OPTIONS_TEXT = get_font(45).render("Tela opções.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 3))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN.get_width() - 70, SCREEN.get_height() - 30), 
                            text_input="VOLTAR", font=get_font(20), base_color="#940d35", hovering_color="Pink")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
                    
                    #ideias:
                    #Volume (Música e Efeitos Sonoros):
                    #Idioma
                    #Resolução da Tela
                    

        pygame.display.update()
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Reduzi o tamanho da fonte dos botões para 25
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
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()