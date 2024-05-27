# Разработай свою игру в этом файле!
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Моя первая игра')
run = True
finish = False
back = (178,34,34)
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,picture,w,h,x,y,x_speed,y_speed):
        super().__init__ (picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('sword.png',30, 35, self.rect.right, self.rect.centery,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    direction = 'left' 
    def __init__(self,picture,w,h,x,y,speed,left,right):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
        self.left = left
        self.right = right
    def update(self):
        if self.rect.x >= self.right:
             self.direction = 'left'
        if self.rect.x <= self.left:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self,picture,w,h,x,y,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()
barriers = sprite.Group()
bullets = sprite.Group()
enemies = sprite.Group() 
wall_1 = GameSprite('wall.jpg',80,180,125,250)
wall_2 = GameSprite('wall.jpg',90,320,410,0)
hero_1 = Player('hero.png',70,70,100,150,0,0)
final = GameSprite("winner.png", 50,50,650,0)
enemy = Enemy('enemy.png',70,70,325,250,10,205,340)
dragon = Enemy('dragon.png',100,100,600,50,7,500,600)
win = transform.scale(image.load('win_1.jpg'), (700,500))
lose = transform.scale(image.load('lose.jpg'), (700,500))
barriers.add(wall_1)
barriers.add(wall_2)
enemies.add(enemy)
enemies.add(dragon)
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                hero_1.y_speed = -15
            elif e.key == K_a:
                hero_1.x_speed = -10
            elif e.key == K_s:
                hero_1.y_speed = 15
            elif e.key == K_d:
                hero_1.x_speed = 10
            elif e.key == K_SPACE:
                hero_1.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                hero_1.y_speed = 0
            elif e.key == K_a:
                hero_1.x_speed = 0 
            elif e.key == K_s:
                hero_1.y_speed = 0
            elif e.key ==K_d:
                hero_1.x_speed = 0
    if finish == False:
        window.fill(back)
        barriers.draw(window)
        hero_1.update()
        hero_1.reset()
        final.reset()
        enemies.update()
        enemies.draw(window) 
        bullets.update()
        bullets.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, enemies, True, True)
        if sprite.collide_rect(hero_1, final):
            finish = True 
            window.blit(win,(0,0))
        if sprite.spritecollide(hero_1,enemies,False):
            finish = True
            window.blit(lose,(0,0)) 
        display.update()
    

    display.update()
