import pygame
import numpy
import random
from sys import exit
# set the dimensions of the window here.
WIDTH = 700
HEIGHT = 840
BACKGROUND = (0, 0, 0)
backgroundImage = pygame.image.load("bg2.png")
pygame.font.init()
programIcon = pygame.image.load('p1_front.png')
pygame.display.set_icon(programIcon)
#define font
font_score = pygame.font.SysFont('Lucida Grande', 30)
fine_print = pygame.font.SysFont('Lucida Grande', 18)
#define colors
white = (255, 255, 255)
yellow = (250,250,210)
pygame.mixer.init()
jumpSound = pygame.mixer.Sound('jump.wav')
levelSound = pygame.mixer.Sound('level.wav')
collectSound = pygame.mixer.Sound('giggle.mp3')
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
# main menu screen

def get_high_score():
    high_score_file = open("high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]
        self.mask = pygame.mask.from_surface(self.image )
    def update(self):
        pass
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")
        self.walk_cycle = [
            pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1, 12)
        ]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 0.7
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_a]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        elif key[pygame.K_d]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed
            jumpSound.play()
        if key[pygame.K_w] and onground:
            self.vsp = -self.jumpspeed
            jumpSound.play()
        if key[pygame.K_SPACE] and onground:
            self.vsp = -self.jumpspeed
            jumpSound.play()
        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)
    
    
        
    def move(self, x, y, boxes):
        dx = x
        dy = y
        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])


    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("box.png", startx, starty)

    
    
class Alien(Sprite):
  def __init__(self, startx, starty):
    super().__init__("alien.png", startx, starty)
    
aliens = pygame.sprite.Group() 
boxes = pygame.sprite.Group()


def add_aliens():
    aliens.add(Alien(random.randint(500, 630), 50))
    aliens.add(Alien(random.randint(70, 150), 50))
    aliens.add(Alien(random.randint(600, 630), 260))
    aliens.add(Alien(random.randint(50, 400), 260))
    aliens.add(Alien(random.randint(50, 630), 470))
    aliens.add(Alien(random.randint(50, 630), 470))
def make_border():
  #bottom of screen loop to add boxes
    for bx in range(0, 700, 70):
      boxes.add(Box(bx, 630))
    for bx in range(0, 770, 70):
      boxes.add(Box(bx, 700))
    for bx in range(0, 770, 70):
      boxes.add(Box(bx, 770))
    for bx in range(0, 770, 70):
      boxes.add(Box(bx, 840))
  # top
    for bx in range(0, 700, 70):
      boxes.add(Box(bx, 0))
  # left
    for bx in range(0, 630, 70):
      boxes.add(Box(0, bx))
  # right
    for bx in range(0, 700, 70):
      boxes.add(Box(700, bx))
def make_level():
  # second row
  for i in range(3):
      boxes.add(Box(random.randint(1,9)*70, 420))
  # top row
  for i in range(2):
      boxes.add(Box(random.randint(1,9)*70, 210))
pygame.display.set_caption("Trouble with Tribbles")     
def main():
    pygame.init()
    music = pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    def draw_text(text, font, color, x, y):
      img = font.render(text, True, color)
      screen.blit(img, (x, y))
    def draw_screen():
        screen.blit(backgroundImage, (0, 0))
        #screen.fill(BACKGROUND)
        player.draw(screen)
        boxes.draw(screen)
        aliens.draw(screen)
        draw_text("Score: " + str(score), font_score, white, 5, 0)
        draw_text("A little solitaire type game.", fine_print, yellow, 230, 0)
        draw_text("This is a 'little break from work' game.", fine_print, yellow, 180, 595)
        draw_text("Level: " + str(level), font_score, white, 568, 0)
        draw_text("Object: Collect as many aliens as possible", font_score, white, 5, 620)
        draw_text("You can't get them all, but be a good crew member", fine_print, yellow, 5, 690)
        draw_text("and clean up as many as you can.", fine_print, yellow, 5, 715)
        draw_text("before the boxes block them off!", font_score, white, 5, 650)
        draw_text("High Score: " + str(high_score), font_score, white, 5, 750)
        draw_text("Escape to Restart", font_score, white, 370, 750)
        draw_text("Close window to Quit", font_score, white, 370, 775)
        draw_text("If you get stuck hit escape to 'redeal'", fine_print, white, 5, 780)
        draw_text("Use arrows or 'a' and 'd' to move. Use up arrow, 'w', or space to jump.", fine_print, yellow, 44, 815)
    clock = pygame.time.Clock()
    score = 0
    level = 1
    numAliens = 6
    running = True
    high_score = get_high_score()
    player = Player(100, 300)
    make_border()
    make_level()
    add_aliens()
    while running:
        pygame.event.pump()
        player.update(boxes)
        if pygame.sprite.spritecollide(player, aliens, True):
          score +=1
          collectSound.play()
          if score > high_score:
                    high_score = score
                    try:
                        # Write the file to disk
                        high_score_file = open("high_score.txt", "w")
                        high_score_file.write(str(high_score))
                        high_score_file.close()
                    except IOError:
                        # Hm, can't write it.
                        print("Unable to save the high score.")
          numAliens -=1
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_ESCAPE]:
            levelSound.play()
            running = False
            pygame.QUIT
            boxes.empty()
            aliens.empty()
            main()
        

        if numAliens <=level:
          add_aliens()
          player = Player(100, 320)
          make_level()
          numAliens = numAliens + 6
          level +=1
          levelSound.play()
        
        # Draw loop
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
        

if __name__ == "__main__":
    main()
pygame.quit()
exit()

