from pickle import TRUE
import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("SPACEFIGHTER BY SURYA")

background=pygame.image.load('background.png')
icon=pygame.image.load('ufo.png')
kill=pygame.image.load('kill.png')

pygame.display.set_icon(icon)

mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.5)

PlayerImg=pygame.image.load('player.png')
PlayerX=370
PlayerY=480
PlayerX_change=0



EnemyImg=[]
EnemyX = []
EnemyY = []
EnemyX_change=[]
EnemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0,735)) 
    EnemyY.append(random.randint(50,200))
    EnemyX_change.append(8)
    EnemyY_change.append(50)



BulletImg=pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change=0
BulletY_change=5
Bullet_state= "ready"

score_value=0
font=pygame.font.Font('Sunny Fever.ttf',52)

textX=10
testY=10

over_font=pygame.font.Font('freesansbold.ttf', 64)

def scoreboard(x,y):
    score=font.render("SCORE: " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text=over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(PlayerImg,(x,y))

def enemy(x, y,i):
    screen.blit(EnemyImg[i],(x,y))

def bullet(x,y):
    global Bullet_state
    Bullet_state="fire"
    screen.blit(BulletImg,(x+16,y+10))

def iscollision(EnemyX,EnemyY,BulletX,BulletY):
    distance=math.sqrt(math.pow((EnemyX-BulletX),2)+math.pow((EnemyY-BulletY),2))
    if distance<27:
        return True
    else:
        return False


running = True


while running:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                PlayerX_change= -5
            if event.key==pygame.K_RIGHT:
                PlayerX_change= 5
            if event.key==pygame.K_SPACE:
                if Bullet_state =="ready":
                    bulletsound=mixer.Sound('laser.wav')
                    bulletsound.play()

                    BulletX= PlayerX
                    bullet(BulletX,BulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                PlayerX_change=0



    PlayerX+=PlayerX_change
    if PlayerX<=0:
        PlayerX=0
    elif PlayerX>=736:
        PlayerX=736


    for i in range(num_of_enemies):
        if EnemyY[i]>430:
            for j in range(num_of_enemies):
                EnemyY[j]=2000
            game_over()
            break

        EnemyX[i] += EnemyX_change[i]

        if EnemyX[i]<=0:
            EnemyX_change[i]=3
            EnemyY[i]+=EnemyY_change[i]
        elif EnemyX[i]>=736:
            EnemyX_change[i]= -3
            EnemyY[i]+=EnemyY_change[i]

        collision= iscollision(EnemyX[i],EnemyY[i],BulletX,BulletY)
        if collision:
            screen.blit(kill,(EnemyX[i],EnemyY[i]))
            collisionsound=mixer.Sound('explosion.wav')
            collisionsound.play()

            BulletY=480
            Bullet_state="ready"
            score_value+=1
            EnemyX[i] = random.randint(0,735)
            EnemyY[i] = random.randint(50,200)

        enemy(EnemyX[i],EnemyY[i],i)
        


    if Bullet_state=="fire":
        bullet(BulletX,BulletY)
        BulletY-=BulletY_change

    if BulletY<=0:
        BulletY=480
        Bullet_state="ready"


    player(PlayerX,PlayerY)
    scoreboard(textX,testY)
    
    pygame.display.update()