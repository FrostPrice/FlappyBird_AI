import neat # Usado para criar a AI
import pygame
import random

# region - Configs (Contantes)
WIN_WIDTH = 500
WIN_HEIGHT = 800
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("./imgs/bird1.png")), pygame.transform.scale2x(pygame.image.load("./imgs/bird2.png")), pygame.transform.scale2x(pygame.image.load("./imgs/bird3.png"))] # Usado para fazer a animação do passáro

PIPE_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/base.png"))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/bg.png"))
# PS: Usamos o pygame.transform.scale2x() para deixar as imagens maiores
# endregion - Configs

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    VEL_ROTATION = 10
    ANIMATION_TIME = 5

    # Constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0 # Mantém o controle do "Frame", ou seja, quantas iterações do Loop ele passou
        self.vel = 0
        self.height = self.y # Mantém o controle da posição de onde o pássaro pulou 
        self.img_count = 0 # Para a animacao, e alterar entre as IMGS
        self.img = self.IMGS[0] # A IMGS na posição 0 é a imagem padrão

    def jump(self):
        self.vel = -10.5 # Lembre-se o valor é negativo, pois o valor 0 e 0 (Da coordenada X e Y) começa no canto superior esquerdo, assim temos que dar um valor negativo para fazer o passáro subir
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1 # Controla a qtd. de "segundos" do jogo

        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2 # Controla a qtd. de pixels que o passáro move na coordenada Y

        if displacement >= 16: # Limita para não ter uma velocidade muito alta
            displacement = 16

        if displacement < 0: # Permite o pulo do passáro
            d -= 2 # Tamanho do pulo

        self.y += displacement

        # Animação (Rotação)
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION # Rotaciona o passáro para cima
        else:
            if self.tilt > -90: 
                self.tilt -= self.VEL_ROTATION # Rotaciona o passáro em 90 grau para baixo

    # Desenha o passáro na tela 
    def draw(self, window):
        self.img_count += 1

        # Animação (Imagens) - Controla a imagem que deve aparecer em cada Frame de acorco com o tempo de animação
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Usado para usar a imagem da asa parada enquanto o passáro está caindo
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2 # Evita um bug que a animação pula um Frame

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center) # Define o ponto de rotação no centro da imagem, sem isso ficará no canto superior esquerdo
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self): # Para colisão
        return pygame.from_surface(self.img)

def draw_window(window, bird):
    window.blit(BACKGROUND_IMG, (0, 0)) # window.blit mostra imagens da tela
    bird.draw(window)
    pygame.display.update()

# Função principal para rodar o jogo
def main():
    pygame.init()
    window = pygame.display.set_mode(WIN_SIZE) # Define a tela de jogo e o tamanho
    bird = Bird(200, 200) # Cria o passáro e a posição inicial
    clock = pygame.time.Clock()
    is_playing = True

    while is_playing:
        clock.tick(30) # Define o FrameRate do jogo pra ser 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
        bird.move()
        draw_window(window, bird)

    pygame.quit()

main()