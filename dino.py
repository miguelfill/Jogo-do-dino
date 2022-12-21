import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480

BRANCO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA,))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

somColisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
somColisao.set_volume(1)

somPontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
somPontuacao.set_volume(1)

colidiu = False

escolhaObstaculo = choice([0, 1])

pontos = 0
velocidade = 10

def exibeMensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    textoFormatado = fonte.render(mensagem, True, cor)
    return textoFormatado

def reiniciar():
    global pontos, velocidade, colidiu, escolhaObstaculo
    pontos = 0
    velocidade = 10
    colidiu = False
    dino.rect.y = ALTURA - 64 - 96 // 2
    dino.pulo = False
    dinoVoador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolhaObstaculo = choice([0, 1])

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.somPulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.imagensDinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagensDinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagensDinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = ALTURA - 64 - 96 // 2
        self.rect.center = (100, ALTURA - 64)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.somPulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= self.pos_y_inicial - 150:
                self.pulo = False
            self.rect.y -= 15
        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += 15

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagensDinossauro[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolhaObstaculo
        self.rect.center = (LARGURA, ALTURA - 64)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagensDinoVoador = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagensDinoVoador.append(img)
        self.index_lista = 0
        self.image = self.imagensDinoVoador[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolhaObstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.20
            self.image = self.imagensDinoVoador[int(self.index_lista)]


todasAs_Sprites = pygame.sprite.Group()
dino = Dino()
todasAs_Sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todasAs_Sprites.add(nuvem)

for i in range(LARGURA * 2 // 64):
    chao = Chao(i)
    todasAs_Sprites.add(chao)

cacto = Cacto()
todasAs_Sprites.add(cacto)

dinoVoador = DinoVoador()
todasAs_Sprites.add(dinoVoador)

grupo_Obstaculos = pygame.sprite.Group()
grupo_Obstaculos.add(cacto)
grupo_Obstaculos.add(dinoVoador)

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar()

    colisoes = pygame.sprite.spritecollide(dino, grupo_Obstaculos, False, pygame.sprite.collide_mask)

    todasAs_Sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dinoVoador.rect.topright[0] <= 0:
        escolhaObstaculo = choice([0, 1])
        cacto.rect.x = LARGURA
        dinoVoador.rect.x = LARGURA
        cacto.escolha = escolhaObstaculo
        dinoVoador.escolha = escolhaObstaculo

    if colisoes and colidiu == False:
        somColisao.play()
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        gameOver = exibeMensagem('GAME OVER', 40, (0, 0, 0))
        tela.blit(gameOver, (LARGURA // 2, ALTURA // 2))
        restart = exibeMensagem('Pressione r para reiniciar', 20, (0, 0, 0))
        tela.blit(restart, (LARGURA // 2, (ALTURA // 2) + 60))

    else:
        pontos += 1
        todasAs_Sprites.update()
        texto_pontos = exibeMensagem(pontos, 40, (0, 0, 0))

    if pontos % 100 == 0:
        somPontuacao.play()
        if velocidade >= 25:
            velocidade += 0
        else:
            velocidade += 1


    tela.blit(texto_pontos, (520, 30))

    pygame.display.flip()
