from pygame import *
import random

# Инициализация Pygame
font.init()
# Настройки окна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Космический шутер")

# Шрифты
font_score = font.SysFont('Arial', 30)
font_game_over = font.SysFont('Arial', 50)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=75, height=75):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_x, player_y):
        super().__init__("bullet.png", player_x + 37 - 5, player_y, 10, 10, 20)
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(self.rect.centerx - 5, self.rect.top)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self):
        super().__init__("ufo.png", random.randint(50, win_width - 50), -50, random.randint(1, 3))
        self.passed = False
    
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y > win_height:
            if not self.passed:
                global missed
                missed += 1
                self.passed = True
            self.reset_enemy()
    
    def reset_enemy(self):
        self.rect.x = random.randint(50, win_width - 50)
        self.rect.y = -50
        self.passed = False

player = Player("rocket.png", win_width // 2, win_height - 80, 5)
bullets = sprite.Group()
enemies = sprite.Group()

# Счет
score = 0
missed = 0
win_score = 10
lose_missed = 3

# Враги
for i in range(5):
    enemies.add(Enemy())

# Фон
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# Цикл
game = True
clock = time.Clock()
FPS = 60
finish = False
result = None  

while game:
    # Обработка событий
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                player.fire()
            
    
    if not finish:
        # Обновление экрана
        window.blit(background, (0, 0))
        
        # Обновление и отрисовка объектов
        player.update()
        player.reset()
        
        bullets.update()
        bullets.draw(window)
        
        enemies.update()
        enemies.draw(window)
        
        # Проверка столкновений пуль с врагами
        hits = sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 1
            enemies.add(Enemy())
        
        # Проверка столкновения игрока с врагами
        if sprite.spritecollide(player, enemies, False):
            result = False
            finish = True
        
        # ПОбеда/проигрыш
        if score >= win_score:
            result = True
            finish = True
        elif missed >= lose_missed:
            result = False
            finish = True
        
        # Статы
        score_text = font_score.render(f"Сбито: {score}/{win_score}", True, (255, 255, 255))
        missed_text = font_score.render(f"Пропущено: {missed}/{lose_missed}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        window.blit(missed_text, (10, 50))
    else:
        # Гаме овер
        if result:
            message = font_game_over.render("ПОБЕДА!", True, (0, 255, 0))
        else:
            message = font_game_over.render("ПОРАЖЕНИЕ!", True, (255, 0, 0))
        
    
    display.update()
    clock.tick(FPS)

