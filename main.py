import pygame
from pygame import freetype
import json
import os
import random
from math import sin, cos, pi, atan2, degrees
import os.path
from os import path
import xlsxwriter
import xlrd






pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.freetype.was_init():
    pygame.freetype.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()


#---------Globals
clock = pygame.time.Clock() #sets up a clock used for throttleing the fps
global origin
origin = ''




YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (12, 255, 0)
DK_GREEN = (51, 102, 0)
BLUE = (18, 0, 255)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 224 * 2
SCREEN_HEIGHT = 288 * 2

explosion_anim = []

def set_explo():
    for i in range(82):
        filename = 'images/round_vortex/frame00{}.png'.format(i)
        img = get_image(filename)
        explosion_anim.append(img)

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)



def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))




#-----Classes

#TODO create enemy grid for enemies to take up positions in
#enemy_grid = {pos1: [], }



class Enemy(pygame.sprite.Sprite):

    def __init__(self, start_pos, tar_pos):
        super().__init__()
        self.en_images = []
        img = get_image('./images/player_ship/1.png')
        img = pygame.transform.scale(img, (SCREEN_WIDTH // 10, SCREEN_WIDTH // 10))
        self.en_images.append(img)
        self.image = self.en_images[0]
        self.rect = self.image.get_rect()
        #TODO xy position will be taken out and referenced through the entry paths
        self.speed = 2
        self.hp = 1
        self.pos = start_pos
        self.target_pos = tar_pos
        self.angle = get_angle(self.pos, self.target_pos)
        self.rect.center = self.pos

        self.moving = True
        self.cooldown = 2000
        self.now = pygame.time.get_ticks()

        self.last = 0

    def set_target_pos(self, tar_pos):
        self.target_pos = tar_pos


    def update(self):
        # updates the location
        self.angle = get_angle(self.pos, self.target_pos)
        self.pos = project(self.pos, self.angle, self.speed)
        self.rect.center = self.pos
        self.now = pygame.time.get_ticks()

        #TODO fix the damn movement - seriously

        if self.rect.y < (SCREEN_HEIGHT - (SCREEN_HEIGHT//3)):
            if self.now - self.last >= self.cooldown:
                self.last = self.now
                self.fire_at_ply(x = self.rect.x, y = self.rect.y)


    def fire_at_ply(self, x, y):
        fire = Enemy_bullet([x,y], [game.player.rect.x, game.player.rect.y])
        game.all_sprites_list.add(fire)
        game.enemy_bullet_list.add(fire)
        pass










        #TODO flush out the enemy class


#TODO handles the moving of the group as a whole
class Enemy_group(object):
    def __init__(self):


        pass

#see functions below

#TODO add fire bullet to the player class

class Player(pygame.sprite.Sprite):
    #class for the player
    def __init__(self):
        super().__init__()
        self.creation_time = pygame.time.get_ticks()
        self.images = []
        img = get_image('./images/player_ship/8.png')
        img = pygame.transform.scale(img, (SCREEN_WIDTH // 10, SCREEN_WIDTH//10))
        self.images.append(img)
        self.image = self.images[0]
        img = get_image('./images/player_ship/7.png')
        img = pygame.transform.scale(img, (SCREEN_WIDTH // 10, SCREEN_WIDTH // 10))
        self.images.append(img)
        alpha = 255
        img = get_image('./images/player_ship/9.png').convert_alpha()
        img = pygame.transform.scale(img, (SCREEN_WIDTH // 10, SCREEN_WIDTH // 10))
        self.images.append(img)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2)
        self.rect.y = (SCREEN_HEIGHT - (img.get_height() + 20))
        self.width = self.image.get_rect().width
        self.speed = 2
        self.lives = 2
        self.previous_x = 0
        self.last = pygame.time.get_ticks()

    def update(self):
        #updates the location
        if self.rect.x > SCREEN_WIDTH - (SCREEN_WIDTH//10):
            self.rect.x = SCREEN_WIDTH - (SCREEN_WIDTH//10)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x == self.previous_x:
            self.no_move()
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        self.previous_x = self.rect.x

    def no_move(self):
        self.image = self.images[0]

    def move_x(self, val):
        self.previous_x = self.rect.x
        self.rect.x = self.rect.x + (val * self.speed)
        if val > 0:
            self.image = self.images[1]
        elif val < 0:
            self.image = self.images[2]

    def get_y(self):
        return self.rect.centery

    def get_x(self):
        return self.rect.centerx


class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos):
        super().__init__()
        self.images = []
        img = get_image('./images/fx/pl_lazer.png')
        img = pygame.transform.scale(img, (img.get_rect().width//2, img.get_rect().height//2))
        self.rot = degrees(get_angle(pos, target_pos))
        img = pygame.transform.rotate(img, self.rot)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 2
        pygame.mixer.Sound('./sounds/effect/en_lsz.ogg').play()
        self.pos = pos
        self.target_pos = target_pos
        self.angle = get_angle(self.pos, [game.player.rect.x, SCREEN_HEIGHT + 100])


    def update(self):
        self.pos = project(self.pos, self.angle, self.speed)
        self.rect.center = self.pos

        self.rect.y += (2 * self.speed)


        if self.rect.y > (SCREEN_HEIGHT + 10):
            self.kill()






class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.images = []
        img = get_image('./images/fx/pl_lazer.png')
        img = pygame.transform.scale(img, (img.get_rect().width//2, img.get_rect().height//2))
        self.rot = 90
        img = pygame.transform.rotate(img, self.rot)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 2
        pygame.mixer.Sound('./sounds/effect/pl_lsz.ogg').play()
        self.pos = pos



    def update(self):
        self.rect.y -= (2 * self.speed)
        if self.rect.y < -10:

            self.kill()




#TODO flush out level object
class Level(object):
    def __init__(self):
        self.num_of_enemies = 40
        self.level_num = 1
        self.max_level = 255

    def level_start(self):
        pass

    def level_finish(self):
        pass

#TODO finish highscore object (CWI)
class high_score(object):

    def __init__(self):
        self.default_hs = [['aaa', 20000]]
        self.high_scores =[]
        self.load_hs_info()




    def check_score(self, score):
        self.high_scores.append(['bbb', score])
        l = len(self.high_scores)
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if (self.high_scores[j][1] > self.high_scores[j+1][1]):
                    tempo = self.high_scores[j]
                    self.high_scores[j] = self.high_scores[j+1]
                    self.high_scores[j+1] = tempo

        return self.high_scores[0][1]

    def display_hs():

        pass

    def hs_enter_name():
        pass


    def save_hs_info(self):
        #writing to xlsx files - https://xlsxwriter.readthedocs.io/
        l = len(self.high_scores)
        for i in range(0, l):
            for j in range(0, 1-i-1):
                if (self.high_scores[j][1] == 'bbb'):
                    self.high_scores[j][0] = hs_enter_name()


        hs_workbook = xlsxwriter.Workbook('./data/hsdata.xlsx')
        hs_worksheet = hs_workbook.add_worksheet()

        row = 0
        col = 0

        for hs_p, hs in (self.high_scores):
            hs_worksheet.write(row, col, hs_p)
            hs_worksheet.write(row, col + 1, hs)
        hs_workbook.close()



    def load_hs_info(self):
        #reading xlsx files - https://www.geeksforgeeks.org/reading-excel-file-using-python/
        try:
            xlrd_loc = ('./data/hsdata.xlsx')
            xlrd_wb = xlrd.open_workbook(xlrd_loc)
            xlrd_sheet = xlrd_wb.sheet_by_index(0)
            xlrd_sheet.cell_value(0, 0)
        except FileNotFoundError:
            self.high_scores = self.default_hs
            self.save_hs_info()
            self.load_hs_info()
        else:
            pass

        xlrd_loc = ('./data/hsdata.xlsx')
        xlrd_wb = xlrd.open_workbook(xlrd_loc)
        xlrd_sheet = xlrd_wb.sheet_by_index(0)
        xlrd_sheet.cell_value(0,0)

        tot_num_rows = xlrd_sheet.nrows
        tot_num_col = xlrd_sheet.ncols

        for row in range(tot_num_rows):
            self.high_scores.append(xlrd_sheet.row_values(row))

        if self.high_scores == []:
            self.high_scores = self.default_hs



        pass


#TODO add high score to game object as a sprite and display it :D

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos1, pos2):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = pos1
        self.rect.centery = pos2
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 15

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()

            else:
                pos1 = self.rect.centerx
                pos2 = self.rect.centery
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = pos1
                self.rect.centery = pos2


class Score_exp(pygame.sprite.Sprite):
    def __init__(self, pos1, pos2):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = get_image('./images/100score.png')
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos2 = pos2
        self.rect.x = pos1
        self.rect.y = pos2

    def update(self):
        if self.rect.y < self.pos2 - 30:
            self.kill()
        else:
            self.rect.y -= 0.25


class Game(object):                                     #class reps an instance of the game
    def __init__(self):                                 #creates all attributes of the game
        set_explo()
        self.score = 0
        self.high_score = high_score()
        self.score_list = pygame.sprite.Group()
        self.game_over = False


        #create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy1 = Enemy(start_pos = [(SCREEN_WIDTH + 20), (SCREEN_HEIGHT - 10)], tar_pos = [(SCREEN_WIDTH//2), 100])


                                                        #todo remove and replace enemy creation in the level object
        self.player = Player()  #create the player
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.enemy1 = Enemy(start_pos=[(SCREEN_WIDTH + 20), (SCREEN_HEIGHT - 10)], tar_pos=[(SCREEN_WIDTH // 2), 100])
        self.enemy_list = pygame.sprite.Group()
        self.enemy_list.add(self.enemy1)                #todo remove and add elsewhere...
        #self.all_sprites_list.add(self.hscore)         #todo impliment
        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.enemy1)

    def process_events(self):                           #process all the events and return true if we close the window
        pygame.event.pump()
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_ESCAPE]:
            print(self.high_score.check_score(self.score))
            self.high_score.save_hs_info()
            raise SystemExit
        if keyinput[pygame.K_LEFT]:
            self.player.move_x(-1)

        if keyinput[pygame.K_RIGHT]:
            self.player.move_x(1)

        if keyinput[pygame.K_SPACE]:
            self.cooldown = 400                         #cool down for bullet firing
            now = pygame.time.get_ticks()
            if now - self.player.last >= self.cooldown:
                self.player.last = now

                bullet = Bullet(pos = [self.player.get_x(), self.player.get_y()])

                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)

        return False


    def run_logic(self):                                #method runs each frame and updates positions
        if not self.game_over:                          #and checks for collisions

            self.all_sprites_list.update()              #move all sprites


            #see if the player block has collided with stuff
            #Checks to see if fire - aka enemy bullets hit player
            for fire in self.enemy_bullet_list:
                player_hit_list = pygame.sprite.spritecollide(fire, self.player_list, True)
                for self.player in player_hit_list:
                    self.player.lives -= 1
                    self.enemy_bullet_list.remove(fire)
                    self.explo = Explosion(self.player.rect.centerx, self.player.rect.centery)
                    self.all_sprites_list.add(self.explo)
                    self.player.kill()

            #checks to see if player has hit something.
            for self.player in self.player_list:
                enemy_hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, True)
                for self.enemy in enemy_hit_list:
                    if self.player.creation_time > 20:
                        self.explo = Explosion(self.player.rect.centerx, self.player.rect.centery)
                        self.player.lives -= 1
                        self.player.kill()
                        #todo fix player respawn after death




            for bullet in self.bullet_list:
                enemy_hit_list = pygame.sprite.spritecollide(bullet, self.enemy_list, True)
                for self.enemy in enemy_hit_list:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    self.score_up = 100
                    self.score += self.score_up
                    self.high_score.check_score(self.score)
                    self.enemy.hp -= 1
                    if self.enemy.hp <= 0:
                        self.explo = Explosion(self.enemy.rect.centerx, self.enemy.rect.centery)
                        self.all_sprites_list.add(self.explo)
                        score_fly = Score_exp(self.enemy.rect.centerx, self.enemy.rect.centery)
                        self.all_sprites_list.add(score_fly)
                        self.enemy.kill()
                        print(self.score)
                        self.enemy1 = Enemy(start_pos=[(SCREEN_WIDTH + 20), (SCREEN_HEIGHT - 10)],
                                            tar_pos=[(SCREEN_WIDTH // 2), 100])
                        self.enemy_list.add(self.enemy1)  # todo remove and add elsewhere...
                        #print(self.hscore)




                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)







            #
            # TODO if len(self.enemy_list) == 0:
            #     self.level_over = True

    def display_frame(self, screen):
            screen.fill(WHITE)
            screen.blit(BG1, [0,0])

            #self.hscore.display_hs()
            #self.player.display_lives()
            #todo display player lives and level information


            if self.game_over:                      #game over text on screen
                text_var = pygame.freetype.Font('./images/font/future_thin.ttf', 16, False, False)
                text_var2 = text_var.render("Game Over, click to restart", fgcolor = BLACK)
                center_x = (SCREEN_WIDTH // 2) - (text_var2[0].get_width() // 2)
                center_y = (SCREEN_HEIGHT // 2) - (text_var2[0].get_height() // 2)
                screen.blit(text_var2[0], [center_x, center_y])

            if not self.game_over:
                self.all_sprites_list.draw(screen)


            pygame.display.flip()



_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
    return image

#TODO define functions for enemies to call for movment


def main():
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game - fuck that")
    pygame.mouse.set_visible(False)

    #create our objects and set data
    done = False
    clock = pygame.time.Clock()

    #creates gme instance
    global game
    game = Game()

    #TODO title screen insert here

    #main game loop
    while not done:
        #process events
        done = game.process_events()
        #update stuff
        game.run_logic()
        #draw
        game.display_frame(screen)
        #pause for the next frame
        clock.tick(60)


    pygame.quit() # closes window and exits

BG1 = get_image('./images/bg/bg1.png')
#call the main function and start up the game

if __name__ == '__main__':
    main()


#TODO add sounds
#TODO add challenge level logic
#TODO add boss level, sprites, logic
#TODO add powerups
#TODO add logic for ship capture and two ship fighting

