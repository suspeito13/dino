import pygame

class Moeda:
    def __init__(self, x, y):
        self.image = pygame.image.load("C:\\Users\\italo\\OneDrive\\Documentos\\GitHub\\dino\\dino_runner\\assets\\moeda.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
