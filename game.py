from typing import Any
import pygame

pygame.init()

window = pygame.display.set_mode((800,500))
pygame.display.set_caption("лабіринт")

background = pygame.transform.scale(pygame.image.load("background.jpg"),(800,500))
# player = pygame.transform.scale(pygame.image.load("heeo.png"),(50,50))
# enemy = pygame.transform.scale(pygame.image.load("cyborg.png"),(50,50))
# treasure = pygame.transform.scale(pygame.image.load("treasure.png"),(50,50))

game_over = False

clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()

kick = pygame.mixer.Sound("kick.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image,player_x=0,player_y=0,player_speed=5):
        self.image = pygame.transform.scale(pygame.image.load(player_image),(65,65))
        self.rect = self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
        self.speed = player_speed

    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= 800 - 65:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(pygame.sprite.Sprite):
    def __init__(self, r,g,b,x,y,width,height):
        self.r = r
        self.g=g
        self.b=b
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((r,g,b))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y        

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player = Player("hero.png",0,0,5)
enemy = Enemy("cyborg.png",100,100,2)
treasure = GameSprite("treasure.png",200,200,5)

#212, 54, 15
w1 = Wall(212, 54, 15, 350, 200, 40, 20)
w2 = Wall(212, 54, 15, 500, 300, 400, 20)

while not game_over:
    window.blit(background,(0,0))

    w1.draw()
    w2.draw()
    player.draw()
    enemy.draw()
    treasure.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        

    player.update()
    enemy.update()
    treasure.update()

    if player.rect.colliderect(enemy) or player.rect.colliderect(w1) or player.rect.colliderect(w2):
        kick.play()
        # game_over = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()