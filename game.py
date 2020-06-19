from random import randint, choice
from pygame.locals import *
import pygame
pygame.init()

pygame.display.set_caption("Desenvolvimento de Jogos com Pygame - @noobpythonbr")


# CONSTANTES E VARIÁVEIS GLOBAIS

SCREEN_SIZE = 600, 600
SCREEN = pygame.display.set_mode((SCREEN_SIZE), 0, 32)
FULL = False
FPS = pygame.time.Clock()
FONTE = pygame.font.Font("fontes/Minecrafter.Alt.ttf", 32)
GROUND = pygame.Surface((800, 800))
GROUND.fill((139,105,20))
GAMEOVER = False
GAMEWIN = False
GW_IMAGE = pygame.image.load("imagens/hearth.jpeg")
PX, PY = -200, -200



class Player:
    def __init__(self):
        self.image = pygame.image.load("imagens/girl.png")
        self.sprite_x = 0
        self.sprite_y = 0
        self.sprite_w = 64
        self.sprite_h = 64
        self.sprite_s = 2
        self.sprite_c = 0
        self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),
                                                                                (self.sprite_w, self.sprite_h))
        self.rect = self.sprite.get_rect()
        self.px = SCREEN_SIZE[0] / 2 - self.sprite_w / 2
        self.py = SCREEN_SIZE[1] / 2 - self.sprite_h / 2
                                                                                
        self.directions = [True, False, False, False] # R, L, U, D
        self.is_walking = False
        self.speed = 10
        self.score = 0
		
    def move(self):
        global PX
        global PY
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            if PX > -480:
                self.directions = [True, False, False, False]
                self.is_walking = True
                PX -= self.speed
        
        elif keys[pygame.K_LEFT]:
            if PX < 280:
                self.directions = [False, True, False, False]
                self.is_walking = True
                PX += self.speed
        
        elif keys[pygame.K_UP]:
            if PY < 260:
                self.directions = [False, False, True, False]
                self.is_walking = True
                PY += self.speed
        
        elif keys[pygame.K_DOWN]:
            if PY > -460:
                self.directions = [False, False, False, True]
                self.is_walking = True
                PY -= self.speed
        
        else:
            self.is_walking = False
            self.sprite_x = 0
                
                                                                                    
    def animate(self):
        if self.is_walking:
            if self.sprite_c == self.sprite_s:
                if self.sprite_x < self.image.get_size()[0] - self.sprite_w:
                    self.sprite_x += self.sprite_w
                else:
                    self.sprite_x = 0
                self.sprite_c = 0
            self.sprite_c += 1
                
        if self.directions[0]:
            self.sprite_y = self.sprite_h * 0
                
        if self.directions[1]:
            self.sprite_y = self.sprite_h * 1
                
        if self.directions[2]:
            self.sprite_y = self.sprite_h * 3
                
        if self.directions[3]:
            self.sprite_y = self.sprite_h * 2			
        
    def update(self):
        self.move()
        self.animate()
        
        self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),
                                                                                (self.sprite_w, self.sprite_h))
                                                                                
        self.rect.x = self.px - PX
        self.rect.y = self.py - PY
        SCREEN.blit(self.sprite, (self.px, self.py))
        
        txtScore = FONTE.render(str(self.score), True, (200,200,0), None)
        SCREEN.blit(txtScore, (20, 20))
		
class Enemy:
    def __init__(self):		
        self.image = pygame.image.load("imagens/ghost.png")
        self.image = pygame.transform.flip(self.image, True, False)
        self.sprite_x = 0
        self.sprite_y = 0
        self.sprite_w = 87
        self.sprite_h = 128
        self.sprite_s = 2
        self.sprite_c = 0
        self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),
                                                                                (self.sprite_w, self.sprite_h))
        self.rect = self.sprite.get_rect()
        self.rect.x = 0
        self.rect.y = randint(0, 300)
        
        self.speed = 10		
        self.extra_speed = 0
		
		
    def animate(self):		
        if self.sprite_c == self.sprite_s:
            if self.sprite_x < self.image.get_size()[0] - self.sprite_w:
                self.sprite_x += self.sprite_w
            else:
                self.sprite_x = 0
            self.sprite_c = 0
        self.sprite_c += 1
            
    def move(self):
        self.rect.x += self.speed + self.extra_speed
    
        if self.rect.x > SCREEN_SIZE[0] + 600 or self.rect.x < -600:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.y = randint(0, 300)
            self.speed *= -1
			
    def collision_with_player(self):
        if self.rect.colliderect(player.rect):
            global GAMEOVER
            GAMEOVER = True
			
    def set_speed(self):
        if player.score >= 5:
            self.extra_speed = 2
        elif player.score >= 10:
            self.extra_speed = 4
        elif player.score >= 15:
            self.extra_speed = 6
        elif player.score >= 20:
            self.extra_speed = 8
        elif player.score >= 25:
            self.extra_speed = 10
									
    def update(self):		
        self.move()
        self.animate()
        self.collision_with_player()
        self.set_speed()
        self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),
                                            (self.sprite_w, self.sprite_h))
                                                                                
        SCREEN.blit(self.sprite, (self.rect.x + PX, self.rect.y + PY))

				
class Book:
    def __init__(self):
        self.books = ["book1.png", "book2.png"]
        self.image = pygame.image.load("imagens/" + choice(self.books))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, 800)
        self.rect.y = randint(0, 800)
        
    def collision_with_player(self):
        if self.rect.colliderect(player.rect):
            self.image = pygame.image.load("imagens/" + choice(self.books))
            self.rect.x = randint(0, 800)
            self.rect.y = randint(0, 800)
            player.score += 1
            
            global GAMEWIN
            if player.score >= 10:
                GAMEWIN = True
                                
    def update(self):
        self.collision_with_player()
        SCREEN.blit(self.image, (self.rect.x + PX, self.rect.y + PY))		
	

player = Player()
enemy = Enemy()
book = Book()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if not FULL:
                    SCREEN = pygame.display.set_mode((SCREEN_SIZE), FULLSCREEN, 32)
                    FULL = True
                else:
                    SCREEN = pygame.display.set_mode((SCREEN_SIZE), 0, 32)
                    FULL = False
						
    SCREEN.fill((0,0,0))
    
    if not GAMEOVER and not GAMEWIN:
        SCREEN.blit(GROUND, (PX, PY))	
        
        player.update()
        enemy.update()
        book.update()
        
    elif GAMEOVER:
        txtLoose = FONTE.render("SCORE " + str(player.score), True, (0,0,0), (255,255,0))
        SCREEN.blit(txtLoose, (240, 300))		
            
    elif GAMEWIN:
        SCREEN.blit(GW_IMAGE, (-15, 0))
        txtWin = FONTE.render("OBRIGADO POR JOGAR!", True, (0,0,0), (0,255,0))
        SCREEN.blit(txtWin, (105, 260))
                    
    FPS.tick(30)
    pygame.display.update()
