import pygame
import random

import pygame
from dino_runner.components.coin import Moeda
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SCREEN_WIDTH

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.moedas = []  
        self.when_appears = 0  

    def generate_coins(self, score):
      if len(self.moedas) == 0 and self.when_appears == score:
        self.when_appears += random.randint(100, 200)
        num_coins = 0  # Valor padrão
        if random.random() <= 0.5:  # 50% chance
            num_coins = random.randint(1, 3)  # Atribuição dentro do if
        for _ in range(num_coins):
         coin_x = random.randint(70, SCREEN_WIDTH)  # Defina uma posição aleatória dentro da largura da tela
         coin_y = random.randint(220, 280)
         self.moedas.append(Moeda(SCREEN_WIDTH + random.randint(800, 1200), coin_y))
         


    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]

        self.generate_coins(game.score)
 
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0, 1)])
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    self.obstacles.remove(obstacle)
        for coin in self.moedas:
            coin.update(game.game_speed)



    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        for coin in self.moedas: 
            coin.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
        self.when_appears = random.randint(100, 200)
