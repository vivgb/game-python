import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
screen_width = 1137
screen_height = 637
bottom_panel = 150

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# definir variaveis do jogo
current_fighter = 1 # um de cada vez
total_fighters = 3 # 3 contando com o gato e as ratazana feia
action_cooldown = 0 # tem q ter tempo antes de começar a tretar
action_wait_time = 90 # millisimos segundos po
attack = False
potion = False
# valor de cura da poção
potion_effect = 15
clicked = False
game_over = 0 # se for -1 o jogador perde e 1 ganha

# definir fonte
font = pygame.font.SysFont("Times New Roman", 26)

# definir cor
red = (255,0,0)
green = (0,255,0)

# carregar imagens
# background imagem
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height - bottom_panel))

# panel imagem
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen_width, bottom_panel))

# poção
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()

sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

# fonte para os textos de vitoria e loser
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# Função para desenhar texto centralizado no topo
def draw_centered_text(text, font, color, screen, screen_width, y_position):
    # Renderizar o texto
    rendered_text = font.render(text, True, color)
    # Obter as dimensões do texto
    text_rect = rendered_text.get_rect(center=(screen_width // 2, y_position))
    # Desenhar o texto na tela
    screen.blit(rendered_text, text_rect)

#criar função para desenhar o texto
def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# função para desenhar o fundo
def draw_bg():
    screen.blit(background_img, (0, 0))

# function for drawing panel
def draw_panel():
    # desenha o retangulo do painel
    screen.blit(panel_img, (0, screen_height - bottom_panel))

    hp_font = get_font(18)
    
    # status do gatao
    draw_text(f'{gato.name} HP: {gato.hp}', hp_font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(ratazana_list):
        # nome e hp 
         draw_text(f'{i.name} HP: {i.hp}', hp_font, red, 600, (screen_height - bottom_panel + 10) + count * 60) 


#button class
class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:parado 1:ataque 2:machucado 3:morto
        self.update_time = pygame.time.get_ticks()
        
        #imagens parado
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'img/{self.name}/parado/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #imagens ataque
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'img/{self.name}/ataque/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #imagens machucado
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/hurt/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #imagens morto
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'img/{self.name}/death/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        
        self.image = self.animation_list[self.action][self.frame_index]    
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        
    def update(self):
        #animacao
        animation_cooldown = 100 #million seconds
        self.image = self.animation_list[self.action][self.frame_index] 
        
        #ver se tempo o suficiente passou desde o ultimo update
        if  pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # se a animação começou então volta pro inicio
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3: # caso ele morra nao quero que levante
                self.frame_index = len(self.animation_list[self.action]) - 1 # controla os frame da animação
            else:
                self.parado()
             
             
    # é preciso fazer uma função para que mude para a animação de ficar parado após atacar e vice versa
    def parado(self):
        self.action = 0
        self.frame_index = 0 # garantir que a animacão começe no 0 
        self.update_time = pygame.time.get_ticks() # tempo correto da animação que já foi definido na primeira animação
        
    
    def attack(self,target):
        # causar dano pro ratao
        # valor do dano random
        rand = random.randint(-5,5) # valores entre esses números
        damage = self.strength + rand 
        # tem q diminuir o hp do alvo
        target.hp -= damage
        # animação machucado
        target.hurt()
        # ver se o alvo morreu
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            # animação morto
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # variaveis para fazer a animação de atacar
        self.action = 1 #atacar
        self.frame_index = 0 # garantir que a animacão começe no 0 
        self.update_time = pygame.time.get_ticks() # tempo correto da animação que já foi definido na primeira animação
     
    def hurt(self):
        # animação machucado
        self.action = 2
        self.frame_index = 0 # garantir que a animacão começe no 0 
        self.update_time = pygame.time.get_ticks() # tempo correto da animação que já foi definido na primeira animação
        
    def death(self):
        # animação morto
        self.action = 3
        self.frame_index = 0 # garantir que a animacão começe no 0 
        self.update_time = pygame.time.get_ticks() # tempo correto da animação que já foi definido na primeira animação
        
    def reset(self):
        # se o jogador quiser tentar de novo
        self.alive = True
        # as poções tem que voltar
        self.potions = self.start_potions  
        self.hp = self.max_hp
        self.frame_index = 0
        #voltar para a animação parado
        self.action = 0
        self.update_time = pygame.time.get_ticks()
    
    
    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        
        
    def draw(self, hp):
        # update com novo hp
        self.hp = hp
        # calcular a proporção do hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__ (self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        # mover o texto de dano para desaparecerem logo após 
        self.rect.y -= 1
        # deletar o texto dps de alguns segundos
        self.counter += 1
        if self.counter > 30:
            self.kill() # desaparece com sprite
        
        
        
# Cria instancias de dano e adiciona a esse grupo   
damage_text_group = pygame.sprite.Group()

# instancias fighters
gato = Fighter(400, 350, 'gato', 30, 10, 3)
rato1 = Fighter(700, 360, 'rato', 20, 6, 1)
rato2 = Fighter(900, 360, 'rato', 20, 6, 1)

ratazana_list = [rato1, rato2]

gato_health_bar = HealthBar(100, screen_height - bottom_panel + 40, gato.hp, gato.max_hp)
rato1_health_bar = HealthBar(600, screen_height - bottom_panel + 40, rato1.hp, rato1.max_hp)
rato2_health_bar = HealthBar(600, screen_height - bottom_panel + 100, rato2.hp, rato2.max_hp)

# criar botoes
potion_button = Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = Button(screen, 330, 120, restart_img, 120, 30)


# game loop
run = True
while run:
    clock.tick(fps)

    # desenha fundo
    draw_bg()

    # desenha painel
    draw_panel()
    gato_health_bar.draw(gato.hp)
    rato1_health_bar.draw(rato1.hp)
    rato2_health_bar.draw(rato2.hp)

    # desenhar lutadores
    gato.update()
    gato.draw()
    for rato in ratazana_list:
        rato.update()
        rato.draw()
        
    # desenhar o texto de dano
    damage_text_group.update()
    damage_text_group.draw(screen)
        
    #controlar ação dos jogadores
    # resetar variaveis de ação
    attack = False
    potion = False
    target = None
    #  ter certeza que o mouse é visivel
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, rato in enumerate(ratazana_list):
        if rato.rect.collidepoint(pos):
            # esconder o mouse
            pygame.mouse.set_visible(False)
            # mostrar a espada no logar do cursor
            screen.blit(sword_img,pos)
            if clicked == True and rato.alive == True:
                attack = True
                target = ratazana_list[count]
    
    if potion_button.draw():
        potion = True
    # mostrar o número de poções
    draw_text(str(gato.potions), font, red, 150, screen_height - bottom_panel + 70)
        
    if game_over == 0:
        # ação do jogador
        if gato.alive == True: # primeiro precisa ver se ele não foi de base antes da luta
            if current_fighter == 1: # preparado para a luta
                action_cooldown += 1 # tempo de espera
                if action_cooldown >= action_wait_time: # se esperou o tempo definido
                    # olhar para a ação do jogador
                    # atacar
                    # turno do outro
                    if attack == True and target != None:
                        
                        gato.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #poção
                    if potion == True:
                        if gato.potions > 0:
                            # checar que a poção não ultrapasse o máximo da vida
                            if gato.max_hp - gato.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = gato.max_hp - gato.hp
                            gato.hp += heal_amount
                            gato.potions -= 1
                            damage_text = DamageText(gato.rect.centerx, gato.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
                game_over = -1
                            

                    
        # ação (inimigo) do rato
        for count, rato in enumerate(ratazana_list):  # precisa contar se está no índice 0, 1...
            if current_fighter == 2 + count:  # contar quem está no turno
                action_cooldown += 1
                if rato.alive:  # somente atacar se o rato estiver vivo
                    if action_cooldown >= action_wait_time:
                        # checar se o rato precisa se curar
                        if (rato.hp / rato.max_hp) < 0.5 and rato.potions > 0:
                            # checar que a poção não ultrapasse o máximo da vida
                            if rato.max_hp - rato.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = rato.max_hp - rato.hp
                            rato.hp += heal_amount
                            rato.potions -= 1
                            damage_text = DamageText(rato.rect.centerx, rato.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        # ataque
                        else:
                            rato.attack(gato)
                            current_fighter += 1
                            action_cooldown = 0
                else:  # pular turno de rato morto
                    current_fighter += 1

            
        # se todos os bicho já tiveram seus turnos tem q resetar
        if current_fighter > total_fighters:
            current_fighter = 1


    # verificar se todos os ratos estão mortos
    
    alive_ratos = 0
    for ratos in ratazana_list:
        if ratos.alive == True:
            alive_ratos += 1
    if alive_ratos == 0:
        game_over = 1
    if not gato.alive:
        game_over=-1
    
        
    # verificar se o jogo acabou
    if game_over != 0:
        text_font = get_font(50)
        if game_over == 1:
            # Texto de vitória
            draw_centered_text("Victory", text_font, (255, 255, 255), screen, 1131, 100)
        if game_over == -1:
            # texto de derrota
            draw_centered_text("Defeat", text_font,(255,0,0),screen,1131,100)

        # desenhar botão do restart
        if restart_button.draw():
            gato.reset()
            for rato in ratazana_list:
                rato.reset()
            current_fighter = 1
            action_cooldown =0
            game_over = 0

            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
