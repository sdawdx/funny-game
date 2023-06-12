# -*- coding: utf-8 -*-

"""
单人模式：上下左右为右边箭头键，空格攻击
双人模式：P1：上下左右为右边箭头键，L攻击
          P2:上下左右为wsad,F攻击


游戏初始界面-->  {单人模式选择-->单人游戏界面}-->游戏结束
                { 双人模式选择-->双人游戏界面}-->游戏结束
                
游戏初始界面：GAME()
单人模式选择：begin_game()
双人模式选择：Tbegin_game()
单人游戏界面：prun_game()
双人游戏界面：pprun_game()
结束界面：over_game()
"""

import pygame
import sys
from pygame.locals import *
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750
BULLET_NUM=0
HIT=0
KILL=0

 #玩家图片,调整到相应大小
PLAYER_IMGS = [pygame.transform.scale(pygame.image.load("p1.png"), (100,100)),#快速缩放操作
                      pygame.transform.scale(pygame.image.load("p2.png"), (100,100)),
                      pygame.transform.scale(pygame.image.load("p3.png"), (100,100))]
        #敌人图片,调整到相应大小
ENEMY_IMGS = [pygame.transform.scale(pygame.image.load("e1.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e2.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e3.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e4.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e5.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e6.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e7.png"), (70,70)),
                      pygame.transform.scale(pygame.image.load("e8.png"), (70,70))]

BOSS_IMG=[pygame.transform.scale(pygame.image.load("e1.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e2.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e3.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e4.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e5.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e6.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e7.png"), (200,200)),
                      pygame.transform.scale(pygame.image.load("e8.png"), (200,200))]
        
        #子弹图片,调整到相应大小
BULLET_IMGS = [pygame.transform.scale(pygame.image.load("bu1.png"), (50,100)),
                       pygame.transform.scale(pygame.image.load("bu2.png"), (50,100)),
                       pygame.transform.scale(pygame.image.load("bu3.png"), (50,100),),
                       pygame.transform.scale(pygame.image.load("bu1.png"), (100,200)),
                       pygame.transform.scale(pygame.image.load("bu2.png"), (100,200)),
                       pygame.transform.scale(pygame.image.load("bu3.png"), (100,200))]
        
       
        
        #buff图片,调整到相应大小
SPEED_BUFF_IMG =pygame.transform.scale(pygame.image.load("buff2.png"),(70,70))
BIG_BUFF_IMG=pygame.transform.scale(pygame.image.load("bbuff.png"),(100,100))
DESPEED_BUFF_IMG=pygame.transform.scale(pygame.image.load("buff1.png"),(70,70))
BU_SPEED_BUFF_IMG=pygame.transform.scale(pygame.image.load("buff3.png"),(70,70))
HURT_BUFF_IMG=pygame.transform.scale(pygame.image.load("buff4.png"),(60,70))
#音效
pygame.mixer.init()
pygame.mixer.music.load('mla.mp3')#背景音乐
pygame.mixer.music.set_volume(500)
pygame.mixer.music.play(-1)#循环
BULLET_MUS=[pygame.mixer.Sound('bu1.mp3'),pygame.mixer.Sound('bu2.mp3'),pygame.mixer.Sound('bu3.mp3')]#子弹音效
       
bossv=pygame.mixer.Sound("boss1.mp3")
mus=pygame.mixer.Sound('touch.mp3')#碰撞音效
go=pygame.mixer.Sound('gameover.mp3')#游戏失败音效
ev=pygame.mixer.Sound('ev.mp3')#敌人叫声
ev.set_volume(100)

ENEMY_SPEED = 2    #敌人速度
BUFF_SPEED=3   #buff掉落的速度
BUFF_SPAWN_RATE=1000 #buff刷新数量/频率
ENEMY_HP=60
BOSS_SPEED=0.8
BOSS_HP=200
 # 游戏中用到的颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE=(0,191,255)
PINK=(255,182,193)

#创建窗口
window = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))

 # 定义飞行物
class Plane:
            def __init__(self, x, y, img,hp):
                self.x = x
                self.y = y
                self.img = img
                self.hp=hp
                self.width = img.get_width()#获取图片的宽
                self.height = img.get_height()#获取图片的高
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)#返回图片矩形信息
        
            def draw(self):
                window.blit(self.img, (self.x, self.y))#在窗口上添加图片


 # 定义敌人类
class Enemy(Plane):
            def __init__(self, x, y, img,hp):
                super().__init__(x, y, img,hp)
            def move(self):
                self.y += ENEMY_SPEED
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            def draw(self):
                super().draw()
                #血条生成
                pygame.draw.rect(window, (0, 128, 0), (self.rect.x+20, self.rect.y-10, 60, 5))
                pygame.draw.rect(window, (255, 0, 0),(self.rect.x+20 , self.rect.y- 10, 60-self.hp, 5))


class Boss(Plane):
            def __init__(self, x, y, img,hp):
                super().__init__(x, y, img,hp)
            def move(self):
                self.y += BOSS_SPEED
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                #血条生成
            def draw(self):
                super().draw()
                pygame.draw.rect(window, (0, 128, 0), (self.rect.x+50, self.rect.y-10, 100, 10))
                pygame.draw.rect(window, (255, 0, 0),(self.rect.x+50 , self.rect.y- 10, 100 - self.hp*0.5, 10))
        
 #buff类          
class SPEED_Buff(Plane):
            def __init__(self,x,y,img,hp):
                super().__init__(x, y, img,hp)
            
            def move(self):
                self.y+=BUFF_SPEED
                self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
                
class DESPEED_Buff(Plane):
            def __init__(self,x,y,img,hp):
                super().__init__(x, y, img,hp)
            
            def move(self):
                self.y+=BUFF_SPEED
                self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
         
class BIG_Buff(Plane):
            def __init__(self,x,y,img,hp):
                super().__init__(x, y, img,hp)
            
            def move(self):
                self.y+=BUFF_SPEED
                self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
                
class HURT_Buff(Plane):
            def __init__(self,x,y,img,hp):
                super().__init__(x, y, img,hp)
            
            def move(self):
                self.y+=BUFF_SPEED
                self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
                
class BU_SPEED_Buff(Plane):
            def __init__(self,x,y,img,hp):
                super().__init__(x, y, img,hp)
            
            def move(self):
                self.y+=BUFF_SPEED
                self.rect=pygame.Rect(self.x,self.y,self.width,self.height)


#########################################################################################################################################
#单人模式游戏界面

def prun_game(ppp):#游戏界面
        pygame.init()
        # 设置游戏窗口的大小和标题
        WIDTH, HEIGHT = 600, 750
        BULLET_SIZE=ppp
        
        # 加载游戏中需要用到的图片素材，并调整大小 
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("单人模式")
        #背景图片
        BG_IMG = pygame.transform.scale(pygame.image.load("bg7.png"), (WIDTH, HEIGHT))
        
        # 设置游戏中常用的一些常量
        PLAYER_SPEED = 5   #玩家速度
        PLAYER_SPEED_MAX=10#玩家速度上限
        BULLET_SPEED = 4 #子弹速度，上限为10
        BULLET_SPEED_MAX=12#子弹速度上线
        BULLET_N=20    #子弹伤害
        BULLET_N_MAX=30#子弹伤害上限
        ENEMY_SPAWN_RATE = 200  #敌人刷新数量/频率，数值越小，生成越多
        
        #消灭怪物数
        global KILL
        KILL=0
  
        # 定义玩家类
        class Player(Plane):
            def __init__(self, x, y, img,hp):
                super().__init__(x, y, img,hp)
                self.bullets = []#增加子弹组
        
            def move(self):
                # 获取用户按键信息
                keys = pygame.key.get_pressed()#按下键盘返回bool列表
                if keys[pygame.K_LEFT] and self.x - PLAYER_SPEED > 0:
                    self.x -= PLAYER_SPEED
                if keys[pygame.K_RIGHT] and self.x + PLAYER_SPEED + self.width < WIDTH:
                    self.x += PLAYER_SPEED
                if keys[pygame.K_UP] and self.y - PLAYER_SPEED > 0:
                    self.y -= PLAYER_SPEED
                if keys[pygame.K_DOWN] and self.y + PLAYER_SPEED + self.height < HEIGHT:
                    self.y += PLAYER_SPEED
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                
            def shoot(self,BULLET_SIZE):
                # 玩家发射子弹的方法
                bullet = Bullet(self.rect.centerx-25 , self.rect.top-50 , BULLET_IMGS[BULLET_SIZE] , 1)
                self.bullets.append(bullet)
        
        
            def draw(self):
                super().draw()
                for bullet in self.bullets:
                    bullet.draw()
            
        # 定义子弹类
        class Bullet(Plane):
            def move(self):
                self.y -= BULLET_SPEED
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 初始化玩家和游戏中用到的列表
        player = Player(WIDTH / 2 - 25, HEIGHT - 100, PLAYER_IMGS[ppp],1)
        enemies = []
        sbuffs=[]
        dsbuffs=[]
        bbuffs=[]
        bsbuffs=[]
        hbuffs=[]
        bosss=[]
        #帧率控制
        clock = pygame.time.Clock()
        
        #字体的大小
        score = 10
        score_font = pygame.font.Font(None, 25)#None代表默认字体
        speed_font=pygame.font.Font(None, 25)
        atk_font=pygame.font.Font(None,25)
        kill_font=pygame.font.Font(None,25)
        
        state=1
        running = True
####################################        
        while running:
            # 处理游戏中的各种事件
            global BULLET_NUM
            global HIT
            window.blit(BG_IMG, (0,0))#窗口添加背景
            
            for event in pygame.event.get():#获得事件
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN :#按下键盘
                    if event.key == pygame.K_SPACE :
                        player.shoot(BULLET_SIZE)
                        BULLET_NUM+=1#射出子弹数量增加
                        bumus=BULLET_MUS[ppp]#子弹音效
                        bumus.set_volume(3)
                        bumus.play()
                        
                    if event.key==pygame.K_p:
                        pygame.time.wait(2000)
            player.move()  
            # 更新玩家和敌机的状态
            
        
            if random.randint(0,ENEMY_SPAWN_RATE) == 0:#随机生成敌人
                enemy = Enemy(random.randint(0, WIDTH - 60), -50, random.choice(ENEMY_IMGS),ENEMY_HP)
                enemies.append(enemy)
                
            if KILL>=30 and KILL%30==0 and state==1:#当击杀怪物累计30个生成boss
                boss=Boss(random.randint(0, WIDTH - 150), -150, random.choice(BOSS_IMG),BOSS_HP)
                bossv.play()        
                state=0
                bosss.append(boss)
                
            for boss in bosss:
                boss.move()
           
            
            if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成移速加成
                buff= SPEED_Buff(random.randint(-20, WIDTH - 50), -50, SPEED_BUFF_IMG,0)
                sbuffs.append(buff)
                
            if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成移速减少
                buff= SPEED_Buff(random.randint(-20, WIDTH - 50), -50, DESPEED_BUFF_IMG,0)
                dsbuffs.append(buff)
                
            if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成子弹速度变快
                 buff= BU_SPEED_Buff(random.randint(-20, WIDTH - 50), -50, BU_SPEED_BUFF_IMG,0)
                 bsbuffs.append(buff)
                 
            if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成攻击力增加
                 buff=HURT_Buff(random.randint(-20, WIDTH - 50), -50, HURT_BUFF_IMG,0)
                 hbuffs.append(buff)
            
                
            for enemy in enemies:
                enemy.move()
                
                
            for sbuff in sbuffs:
                sbuff.move()
                
            for buff in bbuffs:
                buff.move()
                
            for buff in dsbuffs:
                buff.move()
            for buff in hbuffs:
                buff.move()
            for buff in bsbuffs:
                buff.move()
                
            for bullet in player.bullets:
                bullet.move()
        
            # 检测玩家和敌机的碰撞
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    running = False
               
                for bullet in player.bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        HIT+=1
                        enemy.hp-=BULLET_N
                        if enemy.hp<=0:
                            score += 1
                            KILL+=1
                            if ENEMY_SPAWN_RATE>60:#随击杀敌人数增加，敌人刷新速度加快
                                ENEMY_SPAWN_RATE-=2
                            enemies.remove(enemy)
                            ev.play()
                          
                        player.bullets.remove(bullet)
                        mus.play()
                      
                        
                if enemy.rect.bottom>=HEIGHT:#怪物过线，减掉10分
                    score-=10
                    enemies.remove(enemy)
                    
            for boss in bosss:
                    if player.rect.colliderect(boss.rect):
                        running=False 
                    for bullet in player.bullets:
                        if bullet.rect.colliderect(boss.rect):
                            HIT+=1
                            boss.hp-=BULLET_N
                            player.bullets.remove(bullet)
                            if boss.hp<=0:
                               KILL+=1
                               if ENEMY_SPAWN_RATE>=100:
                                      ENEMY_SPAWN_RATE-=20
                               bbuff= BIG_Buff(boss.rect.x,boss.rect.y , BIG_BUFF_IMG,0)
                               bbuffs.append(bbuff)
                               state=1
                               bosss.remove(boss)
                               
            if score<0:#分数小于0则失败
                running=False
                
            #buff效果    
            for buff in sbuffs:#移速增加
                if player.rect.colliderect(buff.rect):
                    if PLAYER_SPEED< PLAYER_SPEED_MAX:
                     PLAYER_SPEED+=0.5
                    sbuffs.remove(buff)
            
            for buff in bbuffs:#子弹变大
                if player.rect.colliderect(buff.rect):
                     BULLET_SIZE=ppp+3
                     if BULLET_N+2.5>BULLET_N_MAX:
                             BULLET_N=BULLET_N_MAX
                     else:
                         BULLET_N+=2
                     bbuffs.remove(buff)
                     
            for buff in dsbuffs:#移速减少
                if player.rect.colliderect(buff.rect):
                    if PLAYER_SPEED>=1:
                     PLAYER_SPEED-=1
                     dsbuffs.remove(buff)
                     
            for buff in hbuffs:#伤害增加
                if player.rect.colliderect(buff.rect):
                      if BULLET_N<BULLET_N_MAX:
                          BULLET_N+=0.5
                      hbuffs.remove(buff)
                      
            for buff in bsbuffs:#子弹速度增加
                if player.rect.colliderect(buff.rect):
                    if BULLET_SPEED<BULLET_SPEED_MAX:
                         BULLET_SPEED+=0.5
                    bsbuffs.remove(buff)        
              
        
            # 绘制游戏界面
            
            player.draw()
            for enemy in enemies:
                enemy.draw()
            for buff in sbuffs:
                buff.draw()
            for buff in bbuffs:
                buff.draw()
            for buff in dsbuffs:
                buff.draw()
            for buff in bsbuffs:
                buff.draw()
            for buff in hbuffs:
                buff.draw()
            for boss in bosss:
                boss.draw()
                
            #游戏数值显示
            score_text = score_font.render("Score: {}".format(score), True ,PINK,WHITE)
            window.blit(score_text, (10, 10))
            
            speed_text = speed_font.render("Speed: ({},{})".format(PLAYER_SPEED,BULLET_SPEED), True, PINK, WHITE)
            window.blit(speed_text, (100, 10))
            
            atk_text = atk_font.render("Atk: {}".format(BULLET_N), True, PINK, WHITE)
            window.blit(atk_text, (250, 10))
            
            kill_text = kill_font.render("Kill: {}".format(KILL), True, PINK, WHITE)
            window.blit(kill_text, (350, 10))
            
            pygame.display.update()
        
            # 控制游戏的刷新速度
            clock.tick(60)
        
        # 游戏结束后显示分数，并在3秒后退出游戏
        GAME_OVER_FONT = pygame.font.Font(None, 72)
        game_over_text = GAME_OVER_FONT.render("Game Over!", True, WHITE, BLACK)
        pygame.mixer.music.stop()
        go.set_volume(200)
        go.play()
        window.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
        pygame.display.update()
        pygame.time.wait(3000)
        ###数据写入文件
        file = open('game_record.txt',mode='a',encoding='utf-8')#只能写，追加
        if ppp==0 and BULLET_NUM!=0:
          file.write("\n单人"+"\t\t杰尼龟"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEED)+"{:3.1f})".format(BULLET_SPEED)
                     +"\t\t{}".format(BULLET_N)+"\t\t{:3d}".format(KILL))
        if ppp==1 and BULLET_NUM!=0:
           file.write("\n单人"+"\t\t小火龙"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEED)+"{:3.1f})".format(BULLET_SPEED)
                      +"\t\t{}".format(BULLET_N)+"\t\t{:3d}".format(KILL))
        if ppp==2 and BULLET_NUM!=0:
            file.write("\n单人"+"\t\t皮卡丘"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEED)+"{:3.1f})".format(BULLET_SPEED)
                       +"\t\t{}".format(BULLET_N)+"\t\t{:3d}".format(KILL))
          
        file.close()
        over_game(ppp)#跳转到游戏结束页面
 #######################################################################################################################################
 #单人模式选择界面
 
def begin_game():
        game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("人物选择界面-单人")#窗口名称
        
        background_image = pygame.transform.scale(pygame.image.load("bg6.png"), (600,750))
        game_window.blit(background_image, (0, 0))
        #游戏开始选择
        start_button0 = pygame.transform.scale(pygame.image.load("p11.png"), (150,150))#单人模式
        start_button_x0 = 200
        start_button_y0 = 50
        game_window.blit(start_button0, (start_button_x0, start_button_y0))

        start_button1 = pygame.transform.scale(pygame.image.load("p22.png"), (150,150))
        start_button_x1 = 200
        start_button_y1 = 250
        game_window.blit(start_button1, (start_button_x1, start_button_y1))
        
        start_button2 = pygame.transform.scale(pygame.image.load("p33.png"), (150,150))
        start_button_x2 = 200
        start_button_y2 = 450
        game_window.blit(start_button2, (start_button_x2, start_button_y2))
        
        start_button3 = pygame.transform.scale(pygame.image.load("tc1.png"), (200,100))
        start_button_x3 = 200
        start_button_y3 = 600
        game_window.blit(start_button3, (start_button_x3, start_button_y3))
        
        
        pygame.display.update()
        
        PLAYER_VOI=[pygame.mixer.Sound('p1v.mp3'),pygame.mixer.Sound('p2v.mp3'),pygame.mixer.Sound('p3v.mp3')]
        A=True
        while A:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:#监测鼠标鼠标
                    if start_button_x0+150> event.pos[0] > start_button_x0 and start_button_y0+150> event.pos[1] > start_button_y0:
                           voi=PLAYER_VOI[0]
                           voi.set_volume(5)
                           voi.play() 
                           A=False
                           prun_game(0)
                    if start_button_x1+150> event.pos[0] > start_button_x1 and start_button_y1+150> event.pos[1] > start_button_y1:
                            voi=PLAYER_VOI[1]
                            voi.set_volume(5)
                            voi.play()
                            A=False
                            prun_game(1)
                    if start_button_x2+150> event.pos[0] > start_button_x2 and start_button_y2+150> event.pos[1] > start_button_y2:
                            voi=PLAYER_VOI[2]
                            voi.set_volume(1000)
                            voi.play()
                            A=False
                            prun_game(2)
                    if start_button_x3+200> event.pos[0] > start_button_x3 and start_button_y3+100> event.pos[1] > start_button_y3:
                        A=False     
                        pygame.quit()
##########################################################################################################################################
#游戏结束界面

def over_game(ppp):
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))#设置窗口
    pygame.display.set_caption("游戏结束界面")
    
    background_image = pygame.transform.scale(pygame.image.load("bg2.png"), (600,750))
    window.blit(background_image, (0, 0))
    #游戏开始按钮
    
    start_button1 = pygame.transform.scale(pygame.image.load("over2.png"), (200,60))
    start_button_x1 = 200
    start_button_y1 = 350
    window.blit(start_button1, (start_button_x1, start_button_y1))
    
    start_button2 = pygame.transform.scale(pygame.image.load("over5.png"), (200,60))
    start_button_x2 = 200
    start_button_y2 = 450
    window.blit(start_button2, (start_button_x2, start_button_y2))
    
    pygame.display.update()
    
    A=True
    while A:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:

                if start_button_x1+200> event.pos[0] > start_button_x1 and start_button_y1+60> event.pos[1] > start_button_y1:
                        A=False
                        pygame.quit()
                if start_button_x2+200> event.pos[0] > start_button_x2 and start_button_y2+60> event.pos[1] > start_button_y2:
                        A=False
                        GAME()#返回游戏开始界面
############################################################################################################################################### 
#双人模式游戏界面

def pprun_game(a,b):
         #游戏界面
            pygame.init()
            pygame.mixer.init()
            # 设置游戏窗口的大小和标题
            WIDTH, HEIGHT = 600, 750
            BULLET_A=a
            BULLET_B=b
            
            # 加载游戏中需要用到的图片素材，并调整大小 
            window = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("双人模式")
            BG_IMG = pygame.transform.scale(pygame.image.load("bg7.png"), (WIDTH, HEIGHT))
            # 设置游戏中常用的一些常量
            PLAYER_SPEEDA = 5   #玩家速度
            PLAYER_SPEEDB=5
            PLAYER_SPEED_MAX=10
         
            
            BULLET_SPEEDA = 4 #子弹速度，上限为10
            BULLET_SPEEDB = 4
            
            BULLET_SPEED_MAX=12
            BULLET_NA=20   
            BULLET_NB=20  #子弹伤害
            BULLET_N_MAX=30
            
            
            ENEMY_SPAWN_RATE = 200   #敌人刷新数量/频率，数值越小，生成越多

            BUFF_SPAWN_RATE=1000 #buff刷新数量/频率
            
            
            KILL=0
            KILLA=0
            KILLB=0
          
           
            
            # 定义类
            class Plane:
                def __init__(self, x, y, img,hp):
                    self.x = x
                    self.y = y
                    self.img = img
                    self.hp=hp
                    self.width = img.get_width()
                    self.height = img.get_height()
                    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
                def draw(self):
                    window.blit(self.img, (self.x, self.y))
            
            # 定义玩家类
            class Player(Plane):
                def __init__(self, x, y, img,hp):
                    super().__init__(x, y, img,hp)
                    self.bullets = []
            
                def amove(self):
                    # 获取用户按键信息
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT] and self.x - PLAYER_SPEEDA> 0:
                        self.x -= PLAYER_SPEEDA
                    if keys[pygame.K_RIGHT] and self.x + PLAYER_SPEEDA + self.width < WIDTH:
                        self.x += PLAYER_SPEEDA
                    if keys[pygame.K_UP] and self.y - PLAYER_SPEEDA > 0:
                        self.y -= PLAYER_SPEEDA
                    if keys[pygame.K_DOWN] and self.y + PLAYER_SPEEDA+ self.height < HEIGHT:
                        self.y += PLAYER_SPEEDA
                    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                def bmove(self):
                    # 获取用户按键信息
                    ks = pygame.key.get_pressed()
                    if ks[pygame.K_a] and self.x - PLAYER_SPEEDB > 0:
                        self.x -= PLAYER_SPEEDB
                    if ks[pygame.K_d] and self.x + PLAYER_SPEEDB + self.width < WIDTH:
                        self.x += PLAYER_SPEEDB
                    if ks[pygame.K_w] and self.y - PLAYER_SPEEDB > 0:
                        self.y -= PLAYER_SPEEDB
                    if ks[pygame.K_s] and self.y + PLAYER_SPEEDB + self.height < HEIGHT:
                        self.y += PLAYER_SPEEDB
                    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                def shoot(self,BULLET_SIZE):
                    # 玩家发射子弹的方法
                    bullet = Bullet(self.rect.centerx-25 , self.rect.top-50 , BULLET_IMGS[BULLET_SIZE],1)
                    self.bullets.append(bullet)
            
            
                def draw(self):
                    super().draw()
                    for bullet in self.bullets:
                        bullet.draw()
            
           
                    
            # 定义子弹类
            class Bullet(Plane):
                def move(self):
                    if self in playera.bullets:
                     self.y -= BULLET_SPEEDA
                     self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    if self in playerb.bullets:
                      self.y -= BULLET_SPEEDB 
                      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  
            # 初始化玩家和敌机，并设置游戏循环
            
            enemies = []
            sbuffs=[]
            dsbuffs=[]
            bbuffs=[]
            bsbuffs=[]
            hbuffs=[]
            
            bosss=[]
            clock = pygame.time.Clock()
            
            #字体的大小
            score = 10
            score_font = pygame.font.Font(None, 40)
            speed_font=pygame.font.Font(None, 25)
            atk_font=pygame.font.Font(None,25)
            kill_font=pygame.font.Font(None,40)
            play_font=pygame.font.Font(None,30)
            
            playera = Player(WIDTH / 2 - 25, HEIGHT - 100, PLAYER_IMGS[a],1)
            playerb=Player(WIDTH / 2 - 25, HEIGHT - 100, PLAYER_IMGS[b],1)
            state=1
            running = True
    ####################################        
            while running:
                # 处理游戏中的各种事件
                global BULLET_NUM
                global HIT
               
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False 
                    elif event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_l :
                            playera.shoot(BULLET_A)
                            BULLET_NUM+=1
                            bumus=BULLET_MUS[a]
                            bumus.set_volume(3)
                            bumus.play()
                            
                        if event.key == pygame.K_f  :
                            playerb.shoot(BULLET_B)
                            BULLET_NUM+=1
                            bumus=BULLET_MUS[b]
                            bumus.set_volume(3)
                            bumus.play()
                            
                        if event.key==pygame.K_p:
                            pygame.time.wait(2000)
                            
                      
                   
                playera.amove()   
                playerb.bmove()
                # 更新玩家和敌机的状态
                
               
             #生成各种敌人  
                if random.randint(0,ENEMY_SPAWN_RATE-50) == 0:#随机生成敌人
                    enemy = Enemy(random.randint(0, WIDTH - 60), -50, random.choice(ENEMY_IMGS),ENEMY_HP)
                    enemies.append(enemy)
                    
                if KILL>=30 and KILL%30==0 and state==1:#生成boss
                    boss=Boss(random.randint(0, WIDTH - 150), -150, random.choice(BOSS_IMG),BOSS_HP)
                    bossv.play()        
                    state=0
                    bosss.append(boss)
                    
                for boss in bosss:
                    boss.move()
               
                
                if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成移速加成
                    buff= SPEED_Buff(random.randint(-20, WIDTH - 50), -50, SPEED_BUFF_IMG,0)
                    sbuffs.append(buff)
                    
                if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成移速减少
                    buff= SPEED_Buff(random.randint(-20, WIDTH - 50), -50, DESPEED_BUFF_IMG,0)
                    dsbuffs.append(buff)
                    
                if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成子弹速度变快
                     buff= BU_SPEED_Buff(random.randint(-20, WIDTH - 50), -50, BU_SPEED_BUFF_IMG,0)
                     bsbuffs.append(buff)
                     
                if random.randint(0,BUFF_SPAWN_RATE) == 0:#随机生成攻击力增加
                     buff=HURT_Buff(random.randint(-20, WIDTH - 50), -50, HURT_BUFF_IMG,0)
                     hbuffs.append(buff)
                
                    
                for enemy in enemies:
                    enemy.move()
                    
                    
                for sbuff in sbuffs:
                    sbuff.move()
                    
                for buff in bbuffs:
                    buff.move()
                    
                for buff in dsbuffs:
                    buff.move()
                for buff in hbuffs:
                    buff.move()
                for buff in bsbuffs:
                    buff.move()
                    
                for bullet in playera.bullets:
                    bullet.move()
                    
                for bullet in playerb.bullets:
                     bullet.move()
            
                # 检测玩家和敌机的碰撞
                for enemy in enemies:
                    if playera.rect.colliderect(enemy.rect):
                        running = False
                    if playerb.rect.colliderect(enemy.rect):
                        running=False
                        
                    for bullet in playera.bullets:
                        if bullet.rect.colliderect(enemy.rect):
                            HIT+=1
                            enemy.hp-=BULLET_NA
                            if enemy.hp<=0:
                                score += 1
                                KILLA+=1
                                KILL+=1
                                if ENEMY_SPAWN_RATE>60:#随击杀敌人数增加，敌人刷新速度加快
                                    ENEMY_SPAWN_RATE-=2
                                enemies.remove(enemy)
                                ev.play()
                              
                            playera.bullets.remove(bullet)
                            mus.play()
                          
                    for bullet in playerb.bullets:#玩家b的子弹命中
                        if bullet.rect.colliderect(enemy.rect):
                            HIT+=1
                            enemy.hp-=BULLET_NB
                            if enemy.hp<=0:
                                score += 1
                                KILLB+=1
                                KILL+=1
                                if ENEMY_SPAWN_RATE>60:
                                    ENEMY_SPAWN_RATE-=2
                                enemies.remove(enemy)
                                ev.play()
                              
                            playerb.bullets.remove(bullet)
                            mus.play()   
                            
                    if enemy.rect.bottom>=HEIGHT:#怪物过线，减掉10分
                        score-=10
                        enemies.remove(enemy)
                        
                for boss in bosss:#玩家a的子弹命中
                        if playera.rect.colliderect(boss.rect):
                            running=False 
                        for bullet in playera.bullets:
                            if bullet.rect.colliderect(boss.rect):
                                HIT+=1
                                boss.hp-=BULLET_NA
                                playera.bullets.remove(bullet)
                                if boss.hp<=0:
                                   KILLA+=1
                                   KILL+=1
                                   if ENEMY_SPAWN_RATE>=100:
                                          ENEMY_SPAWN_RATE-=20
                                   bbuff= BIG_Buff(boss.rect.x,boss.rect.y , BIG_BUFF_IMG,0)
                                   bbuffs.append(bbuff)
                                   state=1
                                   bosss.remove(boss)
                                   
                for boss in bosss:
                        if playerb.rect.colliderect(boss.rect):
                            running=False 
                        for bullet in playerb.bullets:
                            if bullet.rect.colliderect(boss.rect):
                                HIT+=1
                                boss.hp-=BULLET_NB
                                playerb.bullets.remove(bullet)
                                if boss.hp<=0:
                                   KILLB+=1
                                   KILL+=1
                                   if ENEMY_SPAWN_RATE>=100:
                                          ENEMY_SPAWN_RATE-=20
                                   bbuff= BIG_Buff(boss.rect.x,boss.rect.y , BIG_BUFF_IMG,0)
                                   bbuffs.append(bbuff)
                                   state=1
                                   bosss.remove(boss)                   
                if score<0:
                    running=False
                    
                for buff in sbuffs:#移速增加
                    if playera.rect.colliderect(buff.rect):
                        if PLAYER_SPEEDA< PLAYER_SPEED_MAX:
                         PLAYER_SPEEDA+=0.5
                        sbuffs.remove(buff)
                for buff in sbuffs:#移速增加
                    if playerb.rect.colliderect(buff.rect):
                        if PLAYER_SPEEDB<10:
                         PLAYER_SPEEDB+=0.5
                        sbuffs.remove(buff)
                        
                for buff in bbuffs:#子弹变大
                    if playera.rect.colliderect(buff.rect):
                         BULLET_A=a+3
                         if BULLET_NA+2.5>BULLET_N_MAX:
                                 BULLET_NA=BULLET_N_MAX
                         else:
                             BULLET_NA+=2
                         bbuffs.remove(buff)
                         
                for buff in bbuffs:#子弹变大
                     if playerb.rect.colliderect(buff.rect):
                          BULLET_B=b+3
                          if BULLET_NB+2.5>BULLET_N_MAX:
                                  BULLET_NB=BULLET_N_MAX
                          else:
                              BULLET_NB+=2
                          bbuffs.remove(buff)     
                          
                for buff in dsbuffs:#移速减少
                    if playera.rect.colliderect(buff.rect):
                        if PLAYER_SPEEDA>=1:
                         PLAYER_SPEEDA-=1
                         dsbuffs.remove(buff)
                for buff in dsbuffs:#移速减少
                    if playerb.rect.colliderect(buff.rect):
                        if PLAYER_SPEEDB>=1:
                         PLAYER_SPEEDB-=1
                         dsbuffs.remove(buff)
                         
                for buff in hbuffs:#伤害增加
                    if playera.rect.colliderect(buff.rect):
                          if BULLET_NA<BULLET_N_MAX:
                              BULLET_NA+=0.5
                          hbuffs.remove(buff)
                for buff in hbuffs:#伤害增加
                    if playerb.rect.colliderect(buff.rect):
                          if BULLET_NB<BULLET_N_MAX:
                              BULLET_NB+=0.5
                          hbuffs.remove(buff)
                          
                for buff in bsbuffs:#子弹速度增加
                    if playera.rect.colliderect(buff.rect):
                        if BULLET_SPEEDA<BULLET_SPEED_MAX:
                             BULLET_SPEEDA+=0.5
                        bsbuffs.remove(buff)        
                for buff in bsbuffs:#子弹速度增加
                     if playerb.rect.colliderect(buff.rect):
                         if BULLET_SPEEDB<BULLET_SPEED_MAX:
                              BULLET_SPEEDB+=0.5
                         bsbuffs.remove(buff)                  

                # 绘制游戏界面
                window.blit(BG_IMG, (0,0))
                playera.draw()#绘制角色a
                playerb.draw()#绘制角色b
            
                for enemy in enemies:
                    enemy.draw()
                for buff in sbuffs:
                    buff.draw()
                for buff in bbuffs:
                    buff.draw()
                for buff in dsbuffs:
                    buff.draw()
                for buff in bsbuffs:
                    buff.draw()
                for buff in hbuffs:
                    buff.draw()
                for boss in bosss:
                    boss.draw()
                    
                #游戏数值显示
                score_text = score_font.render("Score: {}".format(score), True ,BLACK,WHITE)
                window.blit(score_text, (450, 10))
                kill_text = kill_font.render("Kill: {}".format(KILL), True, BLACK, WHITE)
                window.blit(kill_text, (300, 10))
                
                
                play_text=play_font.render("P1: ",True,BLUE,WHITE)
                window.blit(play_text,(10,10))
                
                
                speed_text = speed_font.render("Speed: ({},{})".format(PLAYER_SPEEDA,BULLET_SPEEDA), True, BLUE, WHITE)
                window.blit(speed_text, (50, 10))
                
                atk_text = atk_font.render("Atk: {}".format(BULLET_NA), True, BLUE, WHITE)
                window.blit(atk_text, (200, 10))
                
               
                
                
                play_text=play_font.render("P2: ",True,PINK,WHITE)
                window.blit(play_text,(10,30))
                            
                speed_text = speed_font.render("Speed: ({},{})".format(PLAYER_SPEEDB,BULLET_SPEEDB), True, PINK, WHITE)
                window.blit(speed_text, (50, 30))
                
                atk_text = atk_font.render("Atk: {}".format(BULLET_NB), True, PINK, WHITE)
                window.blit(atk_text, (200, 30))
                

                pygame.display.update()
            
                # 控制游戏的刷新速度
                clock.tick(60)
            
            # 游戏结束后显示分数，并在3秒后退出游戏
            GAME_OVER_FONT = pygame.font.Font(None, 72)
            game_over_text = GAME_OVER_FONT.render("Game Over!", True, WHITE, BLACK)
            pygame.mixer.music.stop()
            go.set_volume(200)
            go.play()
            window.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
            pygame.display.update()
            pygame.time.wait(3000)
            over_game(a)
            ###数据写入文件
            file = open('game_record.txt',mode='a',encoding='utf-8')
            if a==0 and BULLET_NUM!=0:
              file.write("\n双人"+"\t\t杰尼龟"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDA)+"{:3.1f})".format(BULLET_SPEEDA)
                         +"\t\t{}".format(BULLET_NA)+"\t\t{:3d}".format(KILLA))
            if a==1 and BULLET_NUM!=0:
               file.write("\n双人"+"\t\t小火龙"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDA)+"{:3.1f})".format(BULLET_SPEEDA)
                          +"\t\t{}".format(BULLET_NA)+"\t\t{:3d}".format(KILLA))
            if a==2 and BULLET_NUM!=0:
                file.write("\n单人"+"\t\t皮卡丘"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDA)+"{:3.1f})".format(BULLET_SPEEDA)
                           +"\t\t{}".format(BULLET_NA)+"\t\t{:3d}".format(KILLA))
            if b==0 and BULLET_NUM!=0:
               file.write("\n  "+"\t\t杰尼龟"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDB)+"{:3.1f})".format(BULLET_SPEEDB)
                          +"\t\t{}".format(BULLET_NB)+"\t\t{:3d}".format(KILLB))
            if b==1 and BULLET_NUM!=0:
                file.write("\n  "+"\t\t小火龙"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDB)+"{:3.1f})".format(BULLET_SPEEDB)
                           +"\t\t{}".format(BULLET_NB)+"\t\t{:3d}".format(KILLB))
            if b==2 and BULLET_NUM!=0:
                 file.write("\n  "+"\t\t皮卡丘"+"\t\t{:3d}".format(score)+"\t{:4.2f}%".format(HIT/BULLET_NUM*100)+"\t\t({:3.1f},".format(PLAYER_SPEEDB)+"{:3.1f})".format(BULLET_SPEEDB)
                            +"\t\t{}".format(BULLET_NB)+"\t\t{:3d}".format(KILLB)) 
            file.close()
#################################################################################################################################  
#双人模式选择界面        
def Tbegin_game():
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("人物选择界面-双人")
    
    background_image = pygame.transform.scale(pygame.image.load("bg6.png"), (600,750))
    game_window.blit(background_image, (0, 0))
    #游戏开始按钮
    start_button0 = pygame.transform.scale(pygame.image.load("p11.png"), (150,150))
    start_button_x0 = 200
    start_button_y0 = 50
    game_window.blit(start_button0, (start_button_x0, start_button_y0))
    
    start_button1 = pygame.transform.scale(pygame.image.load("p22.png"), (150,150))
    start_button_x1 = 200
    start_button_y1 = 250
    game_window.blit(start_button1, (start_button_x1, start_button_y1))
    
    start_button2 = pygame.transform.scale(pygame.image.load("p33.png"), (150,150))
    start_button_x2 = 200
    start_button_y2 = 450
    game_window.blit(start_button2, (start_button_x2, start_button_y2))
    
    start_button3 = pygame.transform.scale(pygame.image.load("tc1.png"), (200,100))
    start_button_x3 = 200
    start_button_y3 = 600
    game_window.blit(start_button3, (start_button_x3, start_button_y3))
    
    
    pygame.display.update()
    
    PLAYER_VOI=[pygame.mixer.Sound('p1v.mp3'),pygame.mixer.Sound('p2v.mp3'),pygame.mixer.Sound('p3v.mp3')]
    A=True
    s=[]
    n=0
    while A:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_button_x0+150> event.pos[0] > start_button_x0 and start_button_y0+150> event.pos[1] > start_button_y0:
                       voi=PLAYER_VOI[0]
                       voi.set_volume(5)
                       voi.play() 
                       s.append(0)
                       n+=1
                       if n==2:
                          pprun_game(s[1],s[0])
                          A=False 
                if start_button_x1+150> event.pos[0] > start_button_x1 and start_button_y1+150> event.pos[1] > start_button_y1:
                        voi=PLAYER_VOI[1]
                        voi.set_volume(5)
                        voi.play()
                        s.append(1)
                        n+=1
                        if n==2:
                            pprun_game(s[1],s[0])
                            A=False
                if start_button_x2+150> event.pos[0] > start_button_x2 and start_button_y2+150> event.pos[1] > start_button_y2:
                        voi=PLAYER_VOI[2]
                        voi.set_volume(1000)
                        voi.play()
                        s.append(2)
                        n+=1
                        if n==2:
                            pprun_game(s[0],s[1])
                            A=False
                if start_button_x3+200> event.pos[0] > start_button_x3 and start_button_y3+100> event.pos[1] > start_button_y3:
                    A=False     
                    pygame.quit()


#################################################################################################################################
#游戏初始界面

def GAME():
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("游戏开始界面")
    
    background_image = pygame.transform.scale(pygame.image.load("bg5.png"), (600,750))
    game_window.blit(background_image, (0, 0))
    #游戏开始按钮
    start_button0 = pygame.transform.scale(pygame.image.load("GAME1.png"), (200,60))
    start_button_x0 = 200
    start_button_y0 = 150
    game_window.blit(start_button0, (start_button_x0, start_button_y0))
    
    start_button1 = pygame.transform.scale(pygame.image.load("GAME2.png"), (200,60))
    start_button_x1 = 200
    start_button_y1 = 250
    game_window.blit(start_button1, (start_button_x1, start_button_y1))
    
    start_button2 = pygame.transform.scale(pygame.image.load("tc1.png"), (200,100))
    start_button_x2 = 200
    start_button_y2 = 350
    game_window.blit(start_button2, (start_button_x2, start_button_y2))
    
    
    pygame.display.update()
    A=True
    while A:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_button_x0+200> event.pos[0] > start_button_x0 and start_button_y0+60> event.pos[1] > start_button_y0:
                       begin_game()
                       A=False
                if start_button_x1+200> event.pos[0] > start_button_x1 and start_button_y1+60> event.pos[1] > start_button_y1:
                        Tbegin_game()
                        A=False
                if start_button_x2+200> event.pos[0] > start_button_x2 and start_button_y2+100> event.pos[1] > start_button_y2:
                    A=False     
                    pygame.quit()
                    

GAME()  