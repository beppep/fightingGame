import pygame
import time
import random
clock = pygame.time.Clock()
filepath=""
#"C:/Users/brovar02/Documents/fightingGame/fightingGame-master/"

def initSound():
    pygame.mixer.init(buffer=64)
    Player.hitSound = pygame.mixer.Sound("soundeffect2.wav")
    Player.lickSound = pygame.mixer.Sound("lickeffect.wav")
    Player.lickSound.set_volume(0.2)
    Player.growSound = pygame.mixer.Sound("grasseffect.wav")
    Player.growSound.set_volume(0.2)
    """
    pygame.mixer.music.load("music.wav") #must be wav 16bit and stuff?
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    """

class State():
    idle=0
    stunned=-1

class Projectile():
    projectiles = []
    def __init__(self, owner, op=False):
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
            self.box = [32-7, 16, 32-3, 19, 7, 7+20*op]
    
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
        if len(data)==6:
            self.hitboxes.append(data[5])
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
    def __init__(self, x, y, facingRight, controls, joystick=None):
        Player.players.append(self)
        self.SCALE = 8
        self.CHARGE = 20
        self.flyingHeight=0
        self.flying=0
        self.onGround = True
        self.x = x
        self.xv = 0
        self.y = y
        self.yv = 0
        self.maxhp = 200
        self.ultCharge = 0
        self.stun = 0
        self.invincible=False
        self.invisible=False
        self.state = State.idle
        self.attackFrame = 0
        self.attackBox = None
        self.hitboxes = None
        self.hurtboxes = [1,2,3,4] #first frame
        self.facingRight = facingRight
        self.controls = controls
        if joystick:
            self.joystick = joystick
        else:
            self.joystick = False
        self.pressed = {"a":False,"w":False,"d":False,"1":False,"2":False,"3":False,"4":False,"5":False}
        self.loadImages()

    def init2(self): #after subclass init
        #self.width = self.box[2] - self.box[0]
        #self.height = self.box[3] - self.box[1]
        #self.hurtboxes = self.generateBox(self.box)
        self.hp = self.maxhp
        pass
    def passive(self):
        pass
    def action(self):
        self.attackFrame+=1
        self.passive()
        if self.state == State.stunned:
            self.stunned()
        elif self.state == State.idle:
            self.keys()
        elif self.state == 1:
            self.executeAttack(self.attack1, not self.pressed["1"])
        elif self.state == 2:
            self.executeAttack(self.attack2, not self.pressed["2"])
        elif self.state == 3:
            self.attack3(pressed)
        elif self.state == 4:
            self.attack4(pressed)
        elif self.state == 5:
            self.attack5()

        if self.attackBox and not self.facingRight:
            right = 32 - self.attackBox[0]
            left = 32 - self.attackBox[2]
            self.attackBox[0] = left
            self.attackBox[2] = right

    def attack5(self):
        self.state = State.idle
        self.image = self.idleImage
        self.attackBox = None

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

    def getPressed(self, pressed):
        if self.joystick:
            x = self.joystick.get_axis(0)
            triggers = self.joystick.get_axis(2) #lt - rt but 0 = -3.01
            self.pressed["d"] = (x>0.5)
            self.pressed["a"] = (x<-0.5)
            self.pressed["2"] = (triggers<-0.5 and triggers>-2)
            self.pressed["1"] = (triggers>0.5)
            for i in ["w","3","4","5"]:
                self.pressed[i] = (self.joystick.get_button(self.controls[i]))
        else:
            for i in ["a","d","w","1","2","3","4","5"]:
                self.pressed[i] = (pressed[self.controls[i]])

    def keys(self):
        if(self.pressed["d"]):
            if self.onGround or self.flying:
                self.xv=4
            self.facingRight = True
        elif(self.pressed["a"]):
            if self.onGround or self.flying:
                self.xv=-4
            self.facingRight = False
        else:
            if self.onGround or self.flying:
                self.xv=0

        if(self.pressed["w"] and self.onGround):
            self.yv=-18

        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 0
        
        if(self.pressed["2"]):
            self.state = 2
            self.attackFrame = 0

        if(self.pressed["3"]):
            self.state = 3
            self.attackFrame = 0

        if(self.pressed["4"]):
            self.state = 4
            self.attackFrame = 0

        if(self.pressed["5"] and self.ultCharge>self.CHARGE):
            self.state = 5
            self.attackFrame = 0
            self.ultCharge = 0

        if random.random()<0.02:
            self.ultCharge+=1
            print(Player.players.index(self),":",self.ultCharge,"%")

    def physics(self):

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
                self.hurt("right wall", abs(self.xv*2), abs(self.xv*5)) #abs? ok
        if self.hurtboxes[0]<100:
            self.x += 100-self.hurtboxes[0]
            if self.stun:
                self.hurt("left wall", abs(self.xv*2), abs(self.xv*5)) # ok
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
                #elif self.yv==0:
                 #   pass #experimental evidence shows that this happens 
                 #when you are falling onto a player. hence use >= below. #it still happens
                elif self.yv>=0:
                    self.y+=otherbox[1]-self.hurtboxes[3]
                    self.yv=0
                    self.xv=0
                    self.onGround=True

        if self.hurtboxes[3]>500:
            self.y+=500-self.hurtboxes[3]
            self.yv=0
            self.xv=0
            self.onGround=True
        #else:
        #unindent makes bird wobble here (no?
        self.yv+=0.9
            #happens all the time?

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
                    if(len(player.hitboxes)==6):
                        self.hurt(player, player.hitboxes[4],player.hitboxes[5]) # player/player.owner for ult charge. bad for pos
                    else:
                        self.hurt(player, player.hitboxes[4])# .owner for ult charge. bad for pos
                    Projectile.projectiles.remove(player)

    def hurt(self, player, damage, knockback=None): #player arg is stupid here. Just send direction or x coord.
        if(self.invincible):
            return
        Player.hitSound.set_volume(damage/100)
        Player.hitSound.play()
        if(knockback==None):
            knockback=damage
        if player == "left wall":
            self.facingRight = False
        elif player == "right wall":
            self.facingRight = True
        else:
            self.facingRight = player.x>self.x #not player.facingRight
        self.state = State.stunned

        self.hp -= damage
        #if isinstance(player, Player):
         #   player.ultCharge += damage #-= ? for comeback mechanic #doesnt waork anyway. walls and projectiles can hurt you too
        #self.ultCharge += damage
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
        
        if not self.invisible: #character
            image = self.image[self.facingRight]
            gameDisplay.blit(image, (self.x, self.y))
        if random.random()<.1: #yellow
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        if random.random()<.1: #blue
            if self.ultCharge>self.CHARGE:
                pygame.draw.rect(gameDisplay, (0, 0, 255), \
                (self.hurtboxes[0],self.hurtboxes[1],self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)
        if self.hp>0 and not self.invisible: #health bars
            width=self.hurtboxes[2]-self.hurtboxes[0]
            pygame.draw.rect(gameDisplay, (255, 0, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-32+1,width,6), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), \
            (self.hurtboxes[0],self.hurtboxes[1]-32,width*self.hp/self.maxhp,8), 0)

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Puncher, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()

        self.attack1 = [
        [8, self.prePunchImage],
        [12, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 15]],
        [20, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.attack2 = [
        [17, self.prePunchImage],
        [23, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50]],
        [35, self.punchImage],
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
        [50, self.prePunchImage],
        [165, self.prePunchImage, None, True],
        [170, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50, 120]],
        [210, self.punchImage],
        [240, self.prePunchImage],
        ]

        self.ultimate = [
        [5, self.prePunchImage],
        [10, self.punchImage],
        [15, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 80]],
        [20, self.longPunchImage],
        [30, self.punchImage],
        [40, self.prePunchImage],
        ]

    def attack3(self, pressed):
        self.executeAttack(self.long, not self.pressed["3"])

    def attack4(self, pressed):
        self.executeAttack(self.extreme, not self.pressed["4"])
        #self.state = State.idle (??

    def attack5(self):
        self.executeAttack(self.ultimate)

    def loadImages(self):
        self.idleImage = self.load("idle.png")
        self.stunnedImage = self.load("stunned.png")
        self.longPunchImage = self.load("longpunch.png")
        self.prePunchImage = self.load("prepunch.png")
        self.punchImage = self.load("punch.png")
        self.image = self.idleImage   
class Big(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Big, self).__init__(x, y, facingRight, controls,joystick)
        self.box = [16-4, 12, 16+4, 32-4]
        self.init2()

        self.attack1 = [
        [12, self.prePunchImage, None],
        [15, self.midPunchImage, None],
        [30, self.punchImage, [16, 16, 32-6, 32-8, 35]],
        [45, self.punchImage, None],
        [60, self.midPunchImage, None],
        ]

        self.attack2 = [
        [30, self.prePunchImage, None],
        [40, self.midPunchImage, None],
        [50, self.punchImage, [16, 16, 32-6, 32-8, 80]],
        [70, self.punchImage, None],
        [90, self.midPunchImage, None],
        ]

        self.skull = [
        [15, self.stunnedImage, None],
        [25, self.skullImage, [15, 10, 23, 12, 50]],
        [40, self.skullImage, None],
        ]

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
            if not self.pressed["3"]:
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

    def attack4(self, pressed):
        self.executeAttack(self.skull, self.pressed["4"])

    def attack5(self):

        a = self.attackFrame

        if a==8 or a==28 or a==48 or a==60:
            self.xv = (self.facingRight-0.5)*8
            self.yv = -3

        if a<=8 or 20<=a and a<=28 or 40<=a and a<=48:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 10]

        elif 8<a and a<20 or 28<a and a<40 or 48<a and a<60:
            self.image = self.prePunchImage
            self.attackBox = None

        elif self.attackFrame < 70:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 20, 100]

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

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Green, self).__init__(x, y, facingRight, controls, joystick)
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
        if self.attackFrame == 1:
            Player.growSound.play()
        if self.attackFrame < 90:
            self.image = self.magicImage
            self.attackBox = None
            if self.attackFrame%10==0:
                self.facingRight = not self.facingRight
        else:
            self.hp = min(self.maxhp, self.hp+30)
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
class Tree(Player):
            
    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Tree, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+2, 32-4]
        self.init2()

        self.attack1 = [
        [8, self.preKickImage],
        [16, self.kickImage, [32-16, 32-8-4, 32-9, 32-7, 18]],
        [20, self.kickImage],
        [26, self.preKickImage],
        ]

        self.attack2 = [
        [20, self.preKickImage],
        [33, self.kickImage, [32-16, 32-8-4, 32-9, 32-7, 44]],
        [45, self.kickImage],
        [55, self.preKickImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        if self.attackFrame < 10:
            self.image = self.preGrowImage
        elif self.attackFrame < 15:
            self.image = self.growImage
            self.invincible=True
        elif self.attackFrame == 15:
            self.invisible=True
            self.x += 300*(self.facingRight-0.5)
            self.y = 100 #far down? 700
        elif self.attackFrame < 40:
            pass
        elif self.attackFrame == 40:
            Player.growSound.play()
        elif self.attackFrame < 50:
            self.invisible = False
        elif self.attackFrame < 65:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        if self.attackFrame < 10:
            self.image = self.preGrowImage
        elif self.attackFrame < 15:
            self.image = self.growImage
            self.invincible=True
        elif self.attackFrame < 100:
            self.invisible=True
            if not self.pressed["4"]:
                self.attackFrame = 100
                Player.growSound.play()
        elif self.attackFrame < 110:
            self.invisible = False
        elif self.attackFrame < 125:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self):
        if self.attackFrame == 1:
            Player.growSound.play()
            new = Tree(self.x, self.y, self.facingRight, self.controls)
            new.hp = self.hp
            #move forward
            self.image = self.growImage
            self.invincible=True
            self.x += 400*(self.facingRight-0.5)
            self.y = 700 #far down
        elif self.attackFrame < 15:
            pass
        elif self.attackFrame < 30:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def loadImages(self):
        self.idleImage = self.load("idle4.png")
        self.stunnedImage = self.load("stunned4.png")
        self.preKickImage = self.load("prekick4.png")
        self.kickImage = self.load("kick4.png")
        self.growImage = self.load("grow4.png")
        self.preGrowImage = self.load("pregrow4.png")
        self.image = self.idleImage
class Bird(Player):

    def passive(self):
        if self.flying:
            if self.yv<-5:
                self.yv=-5
            else:
                self.yv-=0.9
        if self.attackFrame%20<10:
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Bird, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*self.SCALE
        self.flying=0
        self.init2()

        self.attack1 = [
        [15, self.prePunchImage],
        [25, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 17]],
        [34, self.punchImage],
        [44, self.prePunchImage],
        ]

        self.attack2 = [
        [28, self.prePunchImage],
        [43, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 40]],
        [55, self.punchImage],
        [70, self.prePunchImage],
        ]


    def attack3(self, pressed):
        if self.attackFrame < 37:
            self.image = self.preelImage #preel/dodgeImage
            self.attackBox = None
        elif self.attackFrame < 150:
            self.image = self.dodgeImage #preel/dodgeImage
            self.attackBox = None
            if not self.pressed["3"]:
                self.attackFrame = 150

        elif self.attackFrame == 151:
            Player.growSound.play()

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

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Robot, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.projectiles = []
        self.maxhp = 200
        self.init2()

        self.attack1 = [
        [30, self.stunnedImage,None],
        [38, self.fireImage, [20, 32-17, 24, 32-12, 58, 58]],
        [45, self.fireImage, None],
        [60, self.stunnedImage, None],
        ]

        self.attack2 = [
        [15, self.prePunchImage,None],
        [30, self.punchImage, [24, 32-17, 27, 32-12, 6, 12]],
        [80, self.punchImage, [24, 32-17, 27, 32-12, 6, 12],True],
        [110, self.prePunchImage,None],
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
            Player.hitSound.set_volume(0.2)
            Player.hitSound.play()
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

    def attack5(self):
        if self.attackFrame < 60:
            if self.attackFrame%10 ==1:
                self.image = self.fireImage
                Projectile.projectiles.append(Projectile(self, op=True))
                Player.hitSound.set_volume(0.4)
                Player.hitSound.play()
            else:
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

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Lizard, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()

        self.attack1 = [
        [6, self.prePunchImage],
        [12, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 10]],
        [17, self.punchImage],
        [24, self.prePunchImage],
        ]

        self.attack2 = [
        [19, self.prePunchImage],
        [28, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 22, 15]],
        [30, self.punchImage],
        [40, self.prePunchImage],
        ]
        self.tail = [
        [7, self.preTailImage],
        [18, self.tailImage, [7, 32-4, 10, 32-2, 17, -17]],
        [25, self.tailImage],
        [30, self.idleImage],
        ]
        self.lick = [
        [14, self.preLickImage],
        [16, self.lickImage, [15, 32-13, 28, 32-12, 0,-30]],
        [18, self.lickImage],
        [20, self.preLickImage],
        ]
    def attack3(self, pressed):
        if self.attackFrame == 5:
            Player.lickSound.play()
        self.executeAttack(self.lick)

    def attack4(self, pressed):
        self.executeAttack(self.tail)

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

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Can, self).__init__(x, y, facingRight, controls, joystick)
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

#WASD
classes1 = [Robot, Lizard, Can]
#arrows
classes2 = [Puncher, Big, Green, Tree, Bird, Robot, Lizard, Can]

gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Fighting Game")
pygame.display.set_icon(pygame.image.load(filepath+"idle.png"))

initSound()

pygame.joystick.init()
stickNum = pygame.joystick.get_count()
sticks=[]
for i in range(stickNum):
    sticks.append(pygame.joystick.Joystick(i))
    sticks[-1].init()

jump_out = False
while jump_out == False:
    if len(Player.players)<2:
        time.sleep(1)
        Player.players = []
        random.choice(classes1)(200, 500, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_s})
        random.choice(classes2)(600, 500, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
        #random.choice([Lizard])(600, 500, False, {"w":0,"3":4,"4":5,"5":3}, sticks[0])

    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True

    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.getPressed(pressed)
        player.action()
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
