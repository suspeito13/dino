import pygame
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"
TEXT_COLOR_BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.image = pygame.image.load("C:\\Users\\italo\\OneDrive\\Documentos\\GitHub\\dino\\dino_runner\\assets\\moeda.png")  # Defina o caminho da imagem da moeda
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 700
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.collected_coins = []  # Inicialize a lista de moedas coletadas
        self.coin_count = 0  # Inicialize o contador de moedas 

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
       #reset de partida
       self.score = 0
       self.game_speed = 20
       
        # Game loop: events - update - draw
       self.playing = True
       self.obstacle_manager.reset_obstacles()
       while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

   # Atualize a lista de moedas coletadas quando uma moeda for coletada
        for coin in self.obstacle_manager.moedas:
            if self.player.dino_rect.colliderect(coin.rect):
                self.collected_coins.append(coin)
                self.obstacle_manager.moedas.remove(coin)
                self.coin_count += 1  # Adicione esta linha para atualizar o contador de moedas 

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))  # '#FFFFFF'
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        
        pygame.display.update()
        pygame.display.flip()
       
        font = pygame.font.Font(FONT_STYLE, 20)  # Adicione esta linha
        coin_count_text = font.render(f"Moedas: {self.coin_count}", True, TEXT_COLOR_BLACK)
        coin_count_rect = coin_count_text.get_rect()
        coin_count_rect.topleft = (10, 100)  # Posição na tela
        self.screen.blit(coin_count_text, coin_count_rect)
        
        
        coin_x = 10  
        coin_y = 40  
        for coin in self.collected_coins:
            self.screen.blit(coin.image, (coin_x, coin_y))
            coin_x += coin.rect.width + 5  # Espaço entre as moedas


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, TEXT_COLOR_BLACK)
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:  # Tela de inicio
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render("Press any key to start", True, TEXT_COLOR_BLACK)
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
        else:  # Tela de restart
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            font = pygame.font.Font(FONT_STYLE, 22)
        
        # score atingido
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR_BLACK)
        score_rect = score_text.get_rect()
        score_rect.center = (half_screen_width, half_screen_height + 20)
        self.screen.blit(score_text, score_rect)
        
    #número de vezes que o jogador perdeu
        death_count_text = font.render(f"Death Count: {self.death_count}", True, TEXT_COLOR_BLACK)
        death_count_rect = death_count_text.get_rect()
        death_count_rect.center = (half_screen_width, half_screen_height + 50)
        self.screen.blit(death_count_text, death_count_rect)


        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
