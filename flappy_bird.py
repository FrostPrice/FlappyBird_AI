import neat # Usado para criar a AI
import pygame
import random
import os
pygame.font.init() # Inicializa as fontes do Pygame

# region - Configs (Contantes)
WIN_WIDTH = 500
WIN_HEIGHT = 800
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("./imgs/bird1.png")), pygame.transform.scale2x(pygame.image.load("./imgs/bird2.png")), pygame.transform.scale2x(pygame.image.load("./imgs/bird3.png"))] # Usado para fazer a animação do passáro

PIPE_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/base.png"))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load("./imgs/bg.png"))

FONT = pygame.font.SysFont("comicsans", 50)
# PS: Usamos o pygame.transform.scale2x() para deixar as imagens maiores
# endregion - Configs

# region - Classes
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

    # Métodos
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
            displacement -= 2 # Tamanho do pulo

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

    def get_mask(self):
        # Uma mascara é um 2D Array de todos os pixels de uma imagem
        # Isso é usado para definir a colisão dos elementos de uma mascara com outro elemento, isso se chama Pixel Perfect Colision
        # Lembre-se que um Pygame Surface sempre será uma caixa em volta da imagem, por isso usamos mascara para delimitar aonde aquela imagem está dentro da caixa
        return pygame.mask.from_surface(self.img)

class Pipe:
    ESPACE_BETWEEN = 200
    VELOCITY = 5

    # Constructor
    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0 # Coordenada Y do cano superior
        self.bottom = 0 # Coordenada Y do cano inferior
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True) # pygame.flip inverte a imagem nos eixos informados
        self.BOTTOM_PIPE = PIPE_IMG

        self.bird_passed = False # Usado pela AI e colisão
        self.set_height() # Vai definir a altura dos Canos (Superior e Inferior junto com o espaço para o passáro passar)

    # Métodos
    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bottom = self.height + self.ESPACE_BETWEEN

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.TOP_PIPE, (self.x, self.top))
        window.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    def get_mask(self):
        # Uma mascara é um 2D Array de todos os pixels de uma imagem
        # Isso é usado para definir a colisão dos elementos de uma mascara com outro elemento, isso se chama Pixel Perfect Colision
        # Lembre-se que um Pygame Surface sempre será uma caixa em volta da imagem, por isso usamos mascara para delimitar aonde aquela imagem está dentro da caixa
        mask_top_pipe = pygame.mask.from_surface(self.TOP_PIPE)
        mask_bottom_pipe = pygame.mask.from_surface(self.BOTTOM_PIPE)

        return mask_top_pipe, mask_bottom_pipe

    def collide(self, bird):
        mask_bird = bird.get_mask()
        mask_top_pipe, mask_bottom_pipe = self.get_mask()

        top_offset = (self.x - bird.x, self.top - round(bird.y)) # O top_offset é a distancia entre o passáro e o cano superior. PS: Não existe pixel em decimal, por isso deve usar o round()
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # O bottom_offset é a distancia entre o passáro e o cano inferior. PS: Não existe pixel em decimal, por isso deve usar o round()

        # Verifica colisão entre as mascáras
        top_point = mask_bird.overlap(mask_top_pipe, top_offset) # Valida se o mask_bird e mask_top_pipe estão um sobre o outro usando o top_offset como referência, senão retorna None
        bottom_point = mask_bird.overlap(mask_bottom_pipe, bottom_offset) # Valida se o mask_bird e mask_bottom_pipe estão um sobre o outro usando o bottom_offset como referência, senão retorna None

        if top_point or bottom_point:
            return True
        
        return False

class Base:
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width()
    VELOCITY = 5

    # Constructor
    def __init__(self, y):
        self.y = y
        self.x_1 = 0
        self.x_2 = self.WIDTH

    # Métodos
    def move(self):
        # Essa função realiza um ciclo entre as imagens, em que uma imagem é movida atrás da outra para criar o efeito de movimento
        self.x_1 -= self.VELOCITY
        self.x_2 -= self.VELOCITY
        
        # Valida se as imagens estão fora da tela
        if self.x_1 + self.WIDTH < 0:
            self.x_1 = self.x_2 + self.WIDTH
        elif self.x_2 + self.WIDTH < 0:
            self.x_2 = self.x_1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x_1, self.y))
        window.blit(self.IMG, (self.x_2, self.y))
# endregion - Classes

def draw_window(window, birds, pipes, base, score):
    window.blit(BACKGROUND_IMG, (0, 0)) # window.blit mostra imagens da tela
    for pipe in pipes: # Pode haver mais de 1 cano na tela
        pipe.draw(window)

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)) # O (WIN_WIDTH - 10 - text.get_width() faz com que o texto não saia da tela

    base.draw(window)
    for bird in birds:
        bird.draw(window)

    pygame.display.update() # Mostra os items criados com .draw na tela

# Função Fitness para rodar o jogo
def eval_genome(genomes, config):
    pygame.init()
    window = pygame.display.set_mode(WIN_SIZE) # Define a tela de jogo e o tamanho
    clock = pygame.time.Clock() # Cria o elemento para definir o FPS do jogo
    base = Base(730) # Cria o chão e define a posição y
    pipes = [Pipe(600)] # Cria todos os Canos que aparecem no jogo

    birds = [] # Cria os passáros e define posição (x e y) inicial
    neuron_networks = [] # Guarda as informações dos Nodes
    birds_genomes = [] # Guarda informações dos Genomes dos Passáros

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        neuron_networks.append(network)
        birds.append(Bird(230, 350))
        genome.fitness = 0 # Começa com o Level de Fitness no 0
        birds_genomes.append(genome)

    score = 0
    is_playing = True
    while is_playing:
        clock.tick(30) # Define o FrameRate do jogo pra ser 30 FPS
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
                pygame.quit() # Sai do modo Pygame
                quit() # Saí da aplicação inteira

        pipe_index = 0
        if len(birds) > 0:
            # O Código abaixo faz com que os Passáros olhem para o obstaculo certo
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width(): # Se a posição dos passáros passou o cano do index 0, muda para o segundo cano
                pipe_index = 1
        else: # Se não tiver nenhum passáro, saia do jogo
            is_playing = False
            break

        for index, bird in enumerate(birds): # Condição de vitória para a AI
            bird.move()
            birds_genomes[index].fitness += 0.1

            output = neuron_networks[index].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()
        
        base.move()

        add_pipe = False
        remove_pipe = [] # Lista para remover os canos após sairem da tela
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird): # Valida colisão com o passáro
                    birds_genomes[index].fitness -= 1
                    birds.pop(index)
                    neuron_networks.pop(index)
                    birds_genomes.pop(index)

                if not pipe.bird_passed and pipe.x < bird.x: # Verifica se o passáro passou pelo cano sem colidir
                    pipe.bird_passed = True
                    add_pipe = True # Vai gerar outro cano

            if pipe.x + pipe.TOP_PIPE.get_width() < 0: # Valida se o Cano está fora da tela
                remove_pipe.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for genome in birds_genomes:
                genome.fitness += 5
            pipes.append(Pipe(600))

        for pipe in remove_pipe:
            pipes.remove(pipe)

        # Colisão com o chão e teto
        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(index)
                neuron_networks.pop(index)
                birds_genomes.pop(index)

        draw_window(window, birds, pipes, base, score)

# region - Neat
# As configurações abaixo são de acordo com as informações da Documentação do NEAT: https://neat-python.readthedocs.io/en/latest/xor_example.html
def run(neat_config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, neat_config_file) # Creates the config for Neat
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True)) # Will show statistics in the Console about the Population
    population.add_reporter(neat.StatisticsReporter())

    # A função fitness vai gerar o Fitness para os passáros
    winner = population.run(eval_genome, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    neat_config_path = os.path.join(local_dir, "neat_config")
    run(neat_config_path)
# endregion - Neat