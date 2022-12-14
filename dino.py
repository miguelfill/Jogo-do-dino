import pygame
from pygame.locals import *
from sys import exit
import os

diretorioPrincipal = os.path.dirname(__file__)
diretorioImagens = os.path.join(diretorioPrincipal, 'imagens')
diretorioSons = os.path.join(diretorioPrincipal, 'sons')

LARGURA = 640
ALTURA = 480

BRANCO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA,))

pygame.display.set_caption('Dino Game')

spriteSheet = pygame.image.load(os.path.join(diretorioImagens, 'dinoSpritesheet.png')).convert_alpha()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagensDinossauro = []
        for i in range(3):
            img = spriteSheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagensDinossauro.append(img)

        self.indexLista = 0
        self.image = self.imagensDinossauro[self.indexLista]
        self.rect = self.image.get_rect()
        self.rect_center = (100,100)

    def update(self):
        if self.indexLista > 2:
            self.indexLista = 0
        self.indexLista += 0.25
        self.image = self.imagensDinossauro[int(self.indexLista)]


todasAs_Sprites = pygame.sprite.Group()
dino = Dino()
todasAs_Sprites.add(dino)

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    todasAs_Sprites.draw(tela)
    todasAs_Sprites.update()

    pygame.display.flip()
