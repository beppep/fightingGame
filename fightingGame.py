import pygame
import time
import random
clock = pygame.time.Clock()
filepath="C:/Users/brovar02/Documents/fightingGame/fightingGame-master/"
#C:/Users/brovar02/Documents/gameartstuff/

class State():
    idle=0
    stunned=-1

class Projectile():
    projectiles = []
    def __init__(self, owner):
        self.SCALE = 8
        self.owner = owner
        self.x = owner.x
        self.y = owner.y
        self.hitboxes = [1,2,3,4]
        self.facingRight = owner.facingRight
        if isinstance(self.owner, Green):
            self.xv = (self.facingRight-0.5) * 10
            self.box = [32-11, 18, 32-6, 32-9, 20]
        if isinstance(self.owner, Robot):
            self.xv = (self.facingRight-0.5) * 20
            self.box = [32-7, 16, 32-3, 19, 7]
    
    def keys(self, pressed):
        nevercalled
        pass

    def draw(self):
        image = self.owner.projbImage[self.facingRight]
        gameDisplay.blit(image, (self.x, self.y))
        if random.random()<.1:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)

    def physics(self):
        self.x += self.xv
        data = self.box
        self.hitboxes = [self.x+data[0]*self.SCALE, self.y+data[1]*self.SCALE, self.x+data[2]*self.SCALE, self.y+data[3]*self.SCALE, data[4]]
        if self.hitboxes and not self.facingRight:
            right = 32*8 - self.hitboxes[0] +2*self.x
            left = 32*8 - self.hitboxes[2] +2*self.x
            self.hitboxes[0] = left
            self.hitboxes[2] = right
        self.hurtboxes = self.hitboxes
        if self.hurtboxes[0]<100 or self.hurtboxes[2]>900:
            Projectile.projectiles.remove(self)
        #death self
        for player in Player.players+Projectile.projectiles:
            if player.hitboxes and not player == self:
                otherBox = player.hitboxes
                if self.hurtboxes[2]>otherBox[0] and self.hurtboxes[0]<otherBox[2]:
                    if self.hurtboxes[3]>otherBox[1] and self.hurtboxes[1]<otherBox[3]:
                        if self in Projectile.projectiles:
                            Projectile.projectiles.remove(self)
                        if isinstance(player, Projectile) and player in Projectile.projectiles:
                            Projectile.projectiles.remove(player)

class Player():
    players=[]
    def __init__(self, x, y, facingRight, controls):
        Player.players.append(self)
        self.SCALE = 8
        self.flyingHeight=0
        self.x = x
        self.xv = 0
        self.y = y
        self.yv = 0
        self.maxhp = 200
        self.stun = 0
        self.invincible=False
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
        self.hp = self.maxhp
        pass
    def passive(self):
        pass
    def action(self, pressed):
        self.passive()
        if self.state == State.stunned:
            self.stunned()
        elif self.state == State.idle:
            self.keys(pressed)
        elif self.state == 1:
            self.executeAttack(self.attack1, not pressed[self.controls["1"]])
        elif self.state == 2:
            self.executeAttack(self.attack2, not pressed[self.controls["2"]])
        elif self.state == 3:
            self.attack3(pressed)
        elif self.state == 4:
            self.attack4(pressed)

        if self.attackBox and not self.facingRight:
            right = 32 - self.attackBox[0]
            left = 32 - self.attackBox[2]
            self.attackBox[0] = left
            self.attackBox[2] = right

    def executeAttack(self, frameData, key=False):
        for part in frameData:
            if self.attackFrame < part[0]:
                self.image = part[1]
                if len(part)>2 and part[2]: #exist and has hitbox
                    self.attackBox = part[2][:]#copy
                else:
                    self.attackBox = None
                if len(part)>3 and part[3]: #if exist and is skipable
                    if key:
                        self.attackFrame = part[0]
                return
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
            self.xv=4
            self.facingRight = True
        elif(pressed[self.controls["a"]]):
            self.xv=-4
            self.facingRight = False
        else:
            self.xv=0

        if(pressed[self.controls["w"]] and self.onGround):
            self.yv=-18

        if(pressed[self.controls["1"]]):
            self.state = 1
            self.attackFrame = 0
        
        if(pressed[self.controls["2"]]):
            self.state = 2
            self.attackFrame = 0

        if(pressed[self.controls["3"]]):
            self.state = 3
            self.attackFrame = 0
            self.holding = True

        if(pressed[self.controls["4"]]):
            self.state = 4
            self.attackFrame = 0

    def physics(self):
        self.attackFrame+=1

        self.x+=self.xv
        self.hurtboxes = self.generateBox(self.box)
        self.hurtboxes[3]+=self.flyingHeight
        for player in Player.players:
            otherbox=player.hurtboxes[:]
            otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.xv<0:
                    self.x += otherbox[2]-self.hurtboxes[0]
                else:
                    self.x += otherbox[0]-self.hurtboxes[2]
        if self.hurtboxes[2]>900:
            self.x += 900-self.hurtboxes[2]
            if self.stun:
                self.hurt("right wall", abs(self.xv*5))
        if self.hurtboxes[0]<100:
            self.x += 100-self.hurtboxes[0]
            if self.stun:
                self.hurt("left wall", abs(self.xv*5 ))
        self.onGround=False
        self.y+=self.yv
        self.hurtboxes = self.generateBox(self.box)
        self.hurtboxes[3]+=self.flyingHeight

        for player in Player.players:
            otherbox=player.hurtboxes[:]
            otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.yv<0:
                    self.y+=otherbox[3]-self.hurtboxes[1]
                    self.yv=0
                elif self.yv==0:
                    pass
                elif self.yv>0:
                    self.y+=otherbox[1]-self.hurtboxes[3]
                    self.yv=0
                    self.xv=0
                    self.onGround=True

        if self.hurtboxes[3]>500:
            self.y+=500-self.hurtboxes[3]
            self.yv=0
            self.xv=0
            self.onGround=True
        else:
            self.yv+=1 #unindent if u wanna
            #print("h") happens all the time?

        self.hurtboxes = self.generateBox(self.box)
        if self.attackBox:
            self.hitboxes = self.generateBox(self.attackBox)
        else:
            self.hitboxes = None

        #self.attackBox= None

        for player in Player.players:
            if player.hitboxes and not player == self and not self.stun:
                if self.collide(player.hitboxes):
                    if(len(player.hitboxes)==6):
                        self.hurt(player, player.hitboxes[4],player.hitboxes[5])
                    else:
                        self.hurt(player, player.hitboxes[4])
        for player in Projectile.projectiles:
            if player.hitboxes and not player == self and not self.stun:
                if self.collide(player.hitboxes):
                    self.hurt(player, player.hitboxes[4])
                    Projectile.projectiles.remove(player)

    def hurt(self, player, damage,knockback=-1):
        if(knockback==-1):
            knockback=damage
        if(self.invincible):
            return
        if player == "left wall":
            self.facingRight = False
        elif player == "right wall":
            self.facingRight = True
        else:
            self.facingRight = player.x>self.x #not player.facingRight
        self.state = State.stunned

        #if isinstance(player, Player):
        self.hp -= damage
        self.stun = max(self.stun, abs(knockback))
        self.attackFrame = 0
        self.yv=-abs(knockback*0.2)
        self.xv=knockback*(self.facingRight-0.5)*-0.2
        

    def generateBox(self, data):
        new = [self.x+data[0]*self.SCALE, self.y+data[1]*self.SCALE, self.x+data[2]*self.SCALE, self.y+data[3]*self.SCALE]
        if len(data)>4:
            new.append(data[4])
        if len(data)>5:
            new.append(data[5])
        return new

    def collide(self, otherBox):
        if self.hurtboxes[2]>otherBox[0] and self.hurtboxes[0]<otherBox[2]:
            if self.hurtboxes[3]>otherBox[1] and self.hurtboxes[1]<otherBox[3]:
                return True
        return False

    def load(self, name):
        image = pygame.image.load(filepath+name)
        image = pygame.transform.scale(image, (self.SCALE*32, self.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        
        image = self.image[self.facingRight]
        gameDisplay.blit(image, (self.x, self.y))

        if random.random()<.8:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        if self.hp>0:
            width=self.hurtboxes[2]-self.hurtboxes[0]
            pygame.draw.rect(gameDisplay, (255, 0, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-32+1,width,6), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-32,width*self.hp/self.maxhp,8), 0)

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Puncher, self).__init__(x, y, facingRight, controls)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()

        self.attack1 = [
        [10, self.prePunchImage],
        [15, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 15]],
        [20, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.attack2 = [
        [20, self.prePunchImage],
        [35, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50]],
        [45, self.punchImage],
        [60, self.prePunchImage],
        ]

        self.long = [
        [20, self.prePunchImage],
        [90, self.prePunchImage, None, True],
        [100, self.punchImage],
        [110, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 40]],
        [130, self.longPunchImage],
        [140, self.punchImage],
        [160, self.prePunchImage],
        ]

        self.extreme = [
        [60, self.prePunchImage],
        [80, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 120]],
        [120, self.punchImage],
        [150, self.prePunchImage],
        ]

    def attack3(self, pressed):
        self.executeAttack(self.long, not pressed[self.controls["3"]])

    def attack4(self, pressed):
        self.executeAttack(self.extreme)
        #self.state = State.idle

    def loadImages(self):
        self.idleImage = self.load("idle.png")
        self.stunnedImage = self.load("stunned.png")
        self.longPunchImage = self.load("longpunch.png")
        self.prePunchImage = self.load("prepunch.png")
        self.punchImage = self.load("punch.png")
        self.image = self.idleImage

class Big(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Big, self).__init__(x, y, facingRight, controls)
        self.box = [16-4, 12, 16+4, 32-4]
        self.init2()

        self.attack1 = [
        [12, self.prePunchImage, None],
        [15, self.midPunchImage, None],
        [30, self.punchImage, [16, 16, 32-6, 32-8, 40]],
        [45, self.punchImage, None],
        [60, self.midPunchImage, None],
        ]

        self.attack2 = [
        [46, self.prePunchImage, None],
        [50, self.midPunchImage, None],
        [60, self.punchImage, [16, 16, 32-6, 32-8, 80]],
        [80, self.punchImage, None],
        [100, self.midPunchImage, None],
        ]

        self.skull = [
        [15, self.stunnedImage, None],
        [25, self.skullImage, [15, 10, 23, 12, 50]],
        [40, self.skullImage, None],
        ]

    def attack4(self, pressed):
        self.executeAttack(self.skull, pressed[self.controls["4"]])

    def attack3(self, pressed):

        if self.attackFrame < 20:
            self.image = self.midPunchImage
            self.attackBox = None
            if self.attackFrame%5==0:
                self.facingRight = not self.facingRight

        elif self.attackFrame < 40:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 20]
            if self.attackFrame%20==0:
                self.facingRight = not self.facingRight

        elif self.attackFrame < 150:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 20]
            if self.attackFrame%20==0:
                self.facingRight = not self.facingRight
            if not pressed[self.controls["3"]]:
                self.holding = False
                self.attackFrame = 150

        elif self.attackFrame < 170:
            self.image = self.prePunchImage
            self.attackBox = None
            if self.attackFrame%5==0:
                self.facingRight = not self.facingRight
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("idle2.png")
        self.stunnedImage = self.load("stunned2.png")
        self.prePunchImage = self.load("prepunch2.png")
        self.midPunchImage = self.load("midpunch2.png")
        self.punchImage = self.load("punch2.png")
        self.skullImage = self.load("skull2.png")
        self.image = self.idleImage

class Green(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Green, self).__init__(x, y, facingRight, controls)
        self.box = [16-3, 32-14, 16+3, 32-4]
        self.projectiles = []
        self.maxhp = 120
        self.init2()

        self.attack1 = [
        [10, self.kickImage, [32-14, 32-6, 32-10, 32-3, 10]],
        [20, self.kickImage, None],
        [25, self.idleImage, None],
        ]

        self.attack2 = [
        [15, self.stunnedImage, None],
        [25, self.skullImage, [32-9-5, 32-8-6, 32-9, 32-9, 40]],
        [40, self.skullImage, None],
        ]

    def attack3(self, pressed):

        if self.attackFrame < 20:
            self.image = self.stunnedImage
            self.attackBox = None
        elif self.attackFrame < 25:
            self.image = self.idleImage
        elif self.attackFrame < 33: 
            self.image = self.skullImage
        elif self.attackFrame == 33:
            self.image = self.skullImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 60:
            self.image = self.skullImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 70:
            self.image = self.magicImage
            self.attackBox = None
            if self.attackFrame%10==0:
                self.facingRight = not self.facingRight
        else:
            self.hp = min(self.maxhp, self.hp+20)
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("idle3.png")
        self.stunnedImage = self.load("stunned3.png")
        self.kickImage = self.load("kick3.png")
        self.skullImage = self.load("skull3.png")
        self.projaImage = self.load("proja3.png")
        self.projbImage = self.load("projb3.png")
        self.magicImage = self.load("magic3.png")
        self.image = self.idleImage

class Bird(Player):
    def passive(self):
        if self.attackFrame%20<10:
            self.image = self.idlebImage
        else:

            self.image = self.idleImage
    def __init__(self, x, y, facingRight, controls):
        super(Bird, self).__init__(x, y, facingRight, controls)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*self.SCALE
        self.init2()

        self.attack1 = [
        [22, self.prePunchImage],
        [28, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 17]],
        [35, self.punchImage],
        [44, self.prePunchImage],
        ]

        self.attack2 = [
        [30, self.prePunchImage],
        [45, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 40]],
        [55, self.punchImage],
        [70, self.prePunchImage],
        ]


    def attack3(self, pressed):
        if self.attackFrame < 38:
            self.image = self.dodgeImage
            self.attackBox = None
        elif self.attackFrame < 150:
            self.image = self.dodgeImage
            self.attackBox = None
            if not pressed[self.controls["3"]]:
                self.holding = False
                self.attackFrame = 150

        elif self.attackFrame < 180:
            self.image = self.elaImage
            self.attackBox = [0, 15, 32, 32-8, 5]
            if self.attackFrame%6>3:
                self.image = self.elbImage

        elif self.attackFrame < 200:
            self.image = self.preelImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 60:
            self.image = self.dodgeImage
            self.invincible=True
            self.attackBox = None
        elif self.attackFrame < 70:
            self.invincible=False
            self.image = self.idlebImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("idle5.png")
        self.idlebImage = self.load("idleb5.png")
        self.stunnedImage = self.load("stunned5.png")
        self.prePunchImage = self.load("prepunch5.png")
        self.punchImage = self.load("punch5.png")
        self.dodgeImage = self.load("dodge5.png")
        self.preelImage = self.load("preel5.png")
        self.elaImage = self.load("ela5.png")
        self.elbImage = self.load("elb5.png")
        self.image = self.idleImage

class Robot(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Robot, self).__init__(x, y, facingRight, controls)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.projectiles = []
        self.maxhp = 200
        self.init2()

        self.attack1 = [
        [33, self.stunnedImage,None],
        [38, self.fireImage, [20, 32-17, 24, 32-12, 58]],
        [45, self.fireImage, None],
        [60, self.stunnedImage, None],
        ]

        self.attack2 = [
        [15, self.prePunchImage,None],
        [30, self.punchImage, [24, 32-17, 27, 32-12, 7, 10]],
        [300, self.punchImage, [24, 32-17, 27, 32-12, 7, 10],True],
        [320, self.prePunchImage,None],
        ]

    def attack3(self, pressed):
        if self.attackFrame < 8:
            self.image = self.idleImage
            self.attackBox = None        
        elif self.attackFrame < 14: 
            self.image = self.fireImage
        elif self.attackFrame == 14:
            self.image = self.fireImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 42:
            self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 15:
            self.image = self.idleImage
            self.attackBox = None        
        elif self.attackFrame < 20: 
            self.image = self.jetpackImage
            self.attackBox = [13, 32-7, 18, 32-3, 15]
        elif self.attackFrame == 20:
            self.image = self.jetpackImage
            self.attackBox = None
            self.yv=-20
        elif self.attackFrame < 82:
            self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("idle6.png")
        self.stunnedImage = self.load("stunned6.png")
        self.fireImage = self.load("fire6.png")
        self.projbImage = self.load("proj6.png")
        self.punchImage = self.load("punch6.png")
        self.prePunchImage = self.load("prepunch6.png")
        self.jetpackImage = self.load("jetpack6.png")
        self.image = self.idleImage

class Lizard(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Lizard, self).__init__(x, y, facingRight, controls)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()

        self.attack1 = [
        [7, self.prePunchImage],
        [12, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 10]],
        [17, self.punchImage],
        [24, self.prePunchImage],
        ]

        self.attack2 = [
        [20, self.prePunchImage],
        [28, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 22, 15]],
        [30, self.punchImage],
        [40, self.prePunchImage],
        ]
        self.tail = [
        [8, self.preTailImage],
        [20, self.tailImage, [7, 32-4, 10, 32-2, 17, -17]],
        [25, self.tailImage],
        [35, self.idleImage],
        ]
        self.lick = [
        [14, self.preLickImage],
        [16, self.lickImage, [25, 32-14, 27, 32-10, 1,-30]],
        [18, self.lickImage],
        [20, self.preLickImage],
        ]
    def attack3(self, pressed):
        self.executeAttack(self.tail)

    def attack4(self, pressed):
        self.executeAttack(self.lick)
        """
        if self.attackFrame < 14:
            self.image = self.preLickImage
            self.attackBox = None        
        elif self.attackFrame == 14: 
            self.image = self.lickImage
            self.attackBox = [25, 32-14, 27, 32-10, 5,-50]
        elif self.attackFrame < 20:
            self.attackBox = None
            self.image = self.lickImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None
        """
        #self.state = State.idle

    def loadImages(self):
        self.preLickImage=self.load("prelick7.png")
        self.lickImage=self.load("lick7.png")
        self.idleImage = self.load("idle7.png")
        self.stunnedImage = self.load("stunned7.png")
        self.prePunchImage = self.load("prepunch7.png")
        self.punchImage = self.load("punch7.png")
        self.preTailImage = self.load("prekick7.png")
        self.tailImage = self.load("kick7.png")
        self.image = self.idleImage

class Can(Player):

    def __init__(self, x, y, facingRight, controls):
        super(Can, self).__init__(x, y, facingRight, controls)
        self.box = [16-5, 32-19, 16+5, 32-4]
        self.init2()

        self.attack1 = [
        [10, self.prePunchImage],
        [15, self.punchImage, [26, 17, 29, 22, 15]],
        [20, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.attack2 = [
        [20, self.prePunchImage],
        [35, self.punchImage, [26, 17, 29, 22, 50]],
        [45, self.punchImage],
        [60, self.prePunchImage],
        ]

    def attack3(self, pressed):
        self.executeAttack(self.attack2)

    def attack4(self, pressed):
        self.executeAttack(self.attack2)
        #self.state = State.idle

    def loadImages(self):
        self.idleImage = self.load("idle8.png")
        self.stunnedImage = self.load("stunned8.png")
        self.prePunchImage = self.load("prepunch8.png")
        self.punchImage = self.load("punch8.png")
        self.image = self.idleImage


classes = [Puncher, Big, Green, Bird, Robot, Lizard, Can]


gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Fighting Game")
pygame.display.set_icon(pygame.image.load(filepath+"idle.png"))
jump_out = False
while jump_out == False:
    if len(Player.players)<2:
        time.sleep(1)
        Player.players = []
        #random.choice(classes)(200, 500, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b})
        #random.choice(classes)(600, 500, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_DOWN,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p})
        random.choice(classes)(200, 500, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b})
        random.choice(classes)(600, 500, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_DOWN,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p})

        #Puncher(200, 500, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b})
        #Lizard(600, 500, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_DOWN,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p})
    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True

    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.action(pressed)
    for player in Player.players+Projectile.projectiles:
        player.physics()
          
    pygame.draw.rect(gameDisplay, (50, 50, 50), (0, 0, 1000, 600), 0)
    pygame.draw.rect(gameDisplay, (100, 200, 255), (100, 0, 800, 500), 0)
    for player in Player.players+Projectile.projectiles:
        player.draw()
        
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()


"""





"""
