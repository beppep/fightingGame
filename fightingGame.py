import pygame
import time
import random
clock = pygame.time.Clock()

class State():
    idle=0
    stunned=-1
    longpunch=10

class Player():
    players=[]
    def __init__(self, x, y, facingRight, controls):
        Player.players.append(self)
        self.SCALE = 8
        self.x = x
        self.y = y
        self.yv = 0
        self.hp = 200
        self.stun = 0
        self.state = State.idle
        self.attackFrame = 0
        self.holding = False
        self.attackBox = None
        self.hitboxes = None
        self.hurtboxes = [1,2,3,4] #first frame
        self.facingRight = facingRight
        self.controls = controls
        self.loadImages()

    def init2(self): #after subclass init
        #self.width = self.box[2] - self.box[0]
        #self.height = self.box[3] - self.box[1]
        #self.hurtboxes = self.generateBox(self.box)
        pass

    def action(self, pressed):
        if self.state == State.stunned:
            self.stunned()
        elif self.state == State.idle:
            self.keys(pressed)
        elif self.state == 1:
            self.executeAttack(self.attack1)
        elif self.state == 2:
            self.executeAttack(self.attack2)
        elif self.state == State.longpunch:
            self.attack3()

        if self.attackBox and not self.facingRight:
            right = 32 - self.attackBox[0]
            left = 32 - self.attackBox[2]
            self.attackBox[0] = left
            self.attackBox[2] = right

    def executeAttack(self, frameData):
        for part in frameData:
            if self.attackFrame < part[0]:
                self.image = part[1]
                self.attackBox = part[2]
                if self.attackBox:#copy not same obj
                    self.attackBox = self.attackBox[:]#copy
                return
            else:
                pass
        self.state = State.idle
        self.image = self.idleImage
        self.attackBox = None

    def stunned(self):
        if self.attackFrame < self.stun:
            self.image = self.stunnedImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.stun = 0
            if self.hp<=0:
                Player.players.remove(self)

    def keys(self, pressed):
        if(pressed[self.controls["d"]]):
            self.x+=5
            self.facingRight = True
        if(pressed[self.controls["a"]]):
            self.x-=5
            self.facingRight = False

        self.hurtboxes = self.generateBox(self.box)
        
        for player in Player.players:
            if self.collide(player.hurtboxes) and not player==self:
                if not self.facingRight:
                    self.x += player.hurtboxes[2]-self.hurtboxes[0]
                else:
                    self.x += player.hurtboxes[0]-self.hurtboxes[2]
        if self.hurtboxes[2]>900:
            self.x += 900-self.hurtboxes[2]
        if self.hurtboxes[0]<100:
            self.x += 100-self.hurtboxes[0]

        self.hurtboxes = self.generateBox(self.box)

        if(pressed[self.controls["w"]] and self.onGround):
            self.yv=-18

        if(pressed[self.controls["1"]]):
            self.state = 1
            self.attackFrame = 0
        
        if(pressed[self.controls["2"]]):
            self.state = 2
            self.attackFrame = 0

        if(pressed[self.controls["3"]]):
            self.state = State.longpunch
            self.attackFrame = 0
            self.holding = True

    def physics(self):
        self.attackFrame+=1
        self.onGround=False
        self.y+=self.yv
        self.hurtboxes = self.generateBox(self.box)
        for player in Player.players:
            if self.collide(player.hurtboxes) and not player==self:
                if self.yv<0:
                    self.y+=player.hurtboxes[3]-self.hurtboxes[1]
                    self.yv=0
                elif self.yv==0:
                    pass
                elif self.yv>0:
                    self.y+=player.hurtboxes[1]-self.hurtboxes[3]
                    self.yv=0
                    self.onGround=True

        if self.hurtboxes[3]>500:
            self.y+=500-self.hurtboxes[3]
            self.yv=0
            self.onGround=True
        else:
            self.yv+=1 #unindent if u wanna
            #print("h") happens all the time?

        self.hurtboxes = self.generateBox(self.box)
        if self.attackBox:
            self.hitboxes = self.generateBox(self.attackBox)
        else:
            self.hitboxes = None

        for player in Player.players:
            if player.hitboxes and not player == self and not self.stun:
                if self.collide(player.hitboxes):
                    self.state = State.stunned
                    self.hp -= player.hitboxes[4]
                    self.stun = player.hitboxes[4]
                    self.attackFrame = 0
                    #flip facing toward

    def generateBox(self, data):
        new = [self.x+data[0]*self.SCALE, self.y+data[1]*self.SCALE, self.x+data[2]*self.SCALE, self.y+data[3]*self.SCALE]
        if len(data)>4:
            new.append(data[4])
        return new

    def collide(self, otherBox):
        if self.hurtboxes[2]>otherBox[0] and self.hurtboxes[0]<otherBox[2]:
            if self.hurtboxes[3]>otherBox[1] and self.hurtboxes[1]<otherBox[3]:
                return True
        return False

    def load(self, name):
        image = pygame.image.load(name)
        image = pygame.transform.scale(image, (self.SCALE*32, self.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        
        image = self.image[self.facingRight]
        gameDisplay.blit(image, (self.x, self.y))

        if random.random()>.9:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        if self.hp>0:
            width=self.hurtboxes[2]-self.hurtboxes[0]
            pygame.draw.rect(gameDisplay, (255, 0, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-24,width,8), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-24,width*self.hp/200,8), 0)

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Puncher, self).__init__(x, y, facingRight, controls)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()

        self.attack1 = [
        [10, self.prePunchImage, None],
        [15, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 15]],
        [20, self.punchImage, None],
        [30, self.prePunchImage, None],
        ]

        self.attack2 = [
        [20, self.prePunchImage, None],
        [35, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50]],
        [50, self.punchImage, None],
        [70, self.prePunchImage, None],
        ]

    def attack3(self):
        if self.holding and self.attackFrame < 20:
            self.image = self.prePunchImage
        elif self.holding:
            self.image = self.prePunchImage
            if not pressed[self.controls["3"]]:
                self.holding = False
                self.attackFrame = 00
        elif self.attackFrame < 10:
            self.image = self.punchImage
        elif self.attackFrame < 20:
            self.image = self.longPunchImage
            self.attackBox = [32-7, 32-8-6, 32, 32-8, 40]
        elif self.attackFrame < 40:
            self.image = self.longPunchImage
            self.attackBox = None
        elif self.attackFrame < 50:
            self.image = self.punchImage
        elif self.attackFrame < 80:
            self.image = self.idleImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None


    def loadImages(self):
        self.idleImage = self.load("C:/Users/brovar02/Documents/gameartstuff/idle.png")
        self.stunnedImage = self.load("C:/Users/brovar02/Documents/gameartstuff/stunned.png")
        self.longPunchImage = self.load("C:/Users/brovar02/Documents/gameartstuff/longpunch.png")
        self.prePunchImage = self.load("C:/Users/brovar02/Documents/gameartstuff/prepunch.png")
        self.punchImage = self.load("C:/Users/brovar02/Documents/gameartstuff/punch.png")
        self.image = self.idleImage

class Big(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Big, self).__init__(x, y, facingRight, controls)
        self.box = [16-4, 12, 16+4, 32-4]
        self.init2()

        self.attack1 = [
        [15, self.prePunchImage, None],
        [30, self.punchImage, [16, 16, 32-6, 32-8, 40]],
        [45, self.punchImage, None],
        [60, self.prePunchImage, None],
        ]

        self.attack2 = [
        [40, self.prePunchImage, None],
        [60, self.punchImage, [16, 16, 32-6, 32-8, 80]],
        [80, self.punchImage, None],
        [100, self.prePunchImage, None],
        ]

    def attack3(self):

        if self.holding and self.attackFrame < 20:
            self.image = self.prePunchImage
            self.attackBox = None
            if self.attackFrame%5==0:
                self.facingRight = not self.facingRight

        elif self.holding and self.attackFrame < 40:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 10]
            if self.attackFrame%20==0:
                self.facingRight = not self.facingRight

        elif self.holding and self.attackFrame < 150: # max duration
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 10]
            if self.attackFrame%20==0:
                self.facingRight = not self.facingRight
            if not pressed[self.controls["3"]]:
                self.holding = False
                self.attackFrame = 0
            
        elif self.holding:
            self.holding = False
            self.attackFrame = 0 # max duration bug fix
            
        elif self.attackFrame < 20:
            self.image = self.idleImage
            self.attackBox = None
            if self.attackFrame%5==0:
                self.facingRight = not self.facingRight
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("C:/Users/brovar02/Documents/gameartstuff/idle2.png")
        self.stunnedImage = self.load("C:/Users/brovar02/Documents/gameartstuff/stunned2.png")
        self.prePunchImage = self.load("C:/Users/brovar02/Documents/gameartstuff/prepunch2.png")
        self.punchImage = self.load("C:/Users/brovar02/Documents/gameartstuff/punch2.png")
        self.image = self.idleImage



gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Fighting Game")
jump_out = False
while jump_out == False:
    if len(Player.players)<2:
        time.sleep(1)
        Player.players = []
        playerOne = Big(200, 500, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_SPACE, "2":pygame.K_v,"3":pygame.K_b})
        playerTwo = Big(600, 500, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_DOWN,"2":pygame.K_p,"3":pygame.K_o})

    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True

    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.action(pressed)
    for player in Player.players:
        player.physics()
          
    pygame.draw.rect(gameDisplay, (50, 50, 50), (0, 0, 1000, 600), 0)
    pygame.draw.rect(gameDisplay, (100, 200, 255), (100, 0, 800, 500), 0)
    for player in Player.players:
        player.draw()
        
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()


"""





"""