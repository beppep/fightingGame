import pygame
import time
import random
clock = pygame.time.Clock()
filepath=""
#"C:/Users/brovar02/Documents/fightingGame/fightingGame-master/"

def initSound():
    pygame.mixer.init(buffer=32)
    Player.hitSound = pygame.mixer.Sound("soundeffect2.wav")
    Player.lickSound = pygame.mixer.Sound("lickeffect.wav")
    Player.lickSound.set_volume(0.2)
    Player.growSound = pygame.mixer.Sound("grasseffect.wav")
    Player.growSound.set_volume(0.2)
    Player.ultSound = pygame.mixer.Sound("ult.wav")
    Player.ultSound.set_volume(0.1)
    Player.bzzzSound = pygame.mixer.Sound("bzzzEffect.wav")
    Player.bzzzSound.set_volume(0.2)
    """
    pygame.mixer.music.load("music.wav") #must be wav 16bit and stuff?
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    """

class State():
    idle=0
    stunned=-1

class Platform():
    
    def generate():
        Platform.platformLayouts = [
        [Platform([600, 340, 650, 360]), Platform([96, 450, 200, 504])],
        [Platform([96, 450, 400, 504]), Platform([96, 400, 200, 450])],
        [],
        [],
        [],
        [],
        ]

        mirrors=[]
        for layout in Platform.platformLayouts:
            mirror = []
            for platform in layout:
                box = platform.hurtboxes
                mirror.append(Platform([1000-box[2], box[1], 1000-box[0], box[3]]))
            mirrors.append(mirror)
        Platform.platformLayouts = Platform.platformLayouts+mirrors

        Platform.platforms = random.choice(Platform.platformLayouts)

    def restart():
        Platform.platforms = random.choice(Platform.platformLayouts)

    def __init__(self, hurtboxes):
        self.hurtboxes = hurtboxes
        self.flyingHeight = 0

    def draw(self):
        pygame.draw.rect(gameDisplay, (127, 127, 127), \
        (self.hurtboxes[0],self.hurtboxes[1],self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)

class Projectile():
    projectiles = []
    def __init__(self, owner, op=False):
        self.owner = owner
        self.x = owner.x
        self.y = owner.y
        self.op = op
        self.hitboxes = [1,2,3,4]
        self.facingRight = owner.facingRight
        self.yv=0
        self.xv=0
        if isinstance(self.owner, Green):
            self.xv = (self.facingRight-0.5) * (10+10*self.op)
            self.box = [32-11, 18, 32-6, 32-9, 20+40*op]
        if isinstance(self.owner, Robot):
            self.xv = (self.facingRight-0.5) * 20
            self.box = [32-7, 16, 32-3, 19, 7+0*self.op, 7]
        if isinstance(self.owner, Monster):
            self.xv = (self.facingRight-0.5) * 8
            self.yv = -1
            self.x+=self.xv
            self.box = [32-11, 19, 32-7, 22, 11, -44, 0]
    
    def keys(self, pressed):
        nevercalled
        pass

    def draw(self):
        image = self.owner.projbImage[self.facingRight]
        gameDisplay.blit(image, (self.x+random.randint(-8,8)*self.op, self.y+random.randint(-8,8)*self.op))
        if random.random()<.1:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)

    def physics(self):
        self.x += self.xv
        self.y += self.yv
        data = self.box
        self.hitboxes = [self.x+data[0]*Player.SCALE, self.y+data[1]*Player.SCALE, self.x+data[2]*Player.SCALE, self.y+data[3]*Player.SCALE, data[4]]
        if len(data)>5:
            self.hitboxes.append(data[5])
        if len(data)>6:
            self.hitboxes.append(data[6])
        if self.hitboxes and not self.facingRight:
            right = 32*8 - self.hitboxes[0] +2*self.x
            left = 32*8 - self.hitboxes[2] +2*self.x
            self.hitboxes[0] = left
            self.hitboxes[2] = right
        self.hurtboxes = self.hitboxes
        if self.hurtboxes[0]<100 or self.hurtboxes[2]>900:
            if self in Projectile.projectiles:
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
    SCALE=8
    players=[]
    def __init__(self, x, y, facingRight, controls, joystick=None):
        Player.players.append(self)
        self.CHARGE = 50
        self.flyingHeight=0
        self.onGround = True
        self.x = x
        self.xv = 0
        self.y = y
        self.yv = 0
        self.maxhp = 250
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
        self.random = False
        self.controls = controls
        self.joystick = joystick
        self.pressed = {"a":False,"w":False,"d":False,"1":False,"2":False,"3":False,"4":False,"5":False}

    def init2(self): #after subclass init
        #self.width = self.box[2] - self.box[0]
        #self.height = self.box[3] - self.box[1]
        #self.hurtboxes = self.generateBox(self.box)
        self.hp = self.maxhp
        pass
    def passive(self):
        pass
        """
        if(self.pressed["5"] and self.ultCharge>self.CHARGE):
            self.state = 5
            self.attackFrame = 0
            self.ultCharge = 0
        """
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

        self.flipHitbox()

    def flipHitbox(self):
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
        if self.random:
            target = random.choice(Player.players)
            if random.randint(0,10)==0 and target!=self:
                self.pressed["a"] = target.x < self.x
            #elif random.randint(0,50)==0 and target!=self:
             #   self.pressed["a"] = target.x > self.x
            #self.pressed["a"] = self.pressed["a"] ^ (random.randint(0,20)==0)
            self.pressed["d"] = not self.pressed["a"]
            for i in ["w","1","2","3","4","5"]:
                self.pressed[i] = (random.randint(0,50)==0)# ^ self.pressed[i]
        elif self.joystick:
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
            if self.onGround:
                self.xv+=2
            else:
                self.xv=min(4, self.xv+0.2)
            self.facingRight = True
        elif(self.pressed["a"]):
            if self.onGround:
                self.xv-=2
            else:
                self.xv=max(-4, self.xv-0.2)
            self.facingRight = False

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
        
        if random.random()<0.1:
            self.ultCharge+=1
            #print(Player.players.index(self),":",self.ultCharge,"%")

    def physics(self):
        self.x+=self.xv
        self.hurtboxes = self.generateBox(self.box)
        self.hurtboxes[3]+=self.flyingHeight

        for player in Player.players+Platform.platforms:
            otherbox=player.hurtboxes[:]
            otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.xv<0:
                    self.x += otherbox[2]-self.hurtboxes[0]
                else:
                    self.x += otherbox[0]-self.hurtboxes[2]
                self.xv = 0
        if self.hurtboxes[2]>904:
            self.x += 904-self.hurtboxes[2]
            if self.stun: #bouncy walls
                self.xv=-self.xv*0.5
                self.yv=-abs(self.xv)
            else:
                self.xv=0
        if self.hurtboxes[0]<96:
            self.x += 96-self.hurtboxes[0]
            if self.stun:
                self.xv=-self.xv*0.5
                self.yv=-self.xv
            else:
                self.xv=0

        self.y+=self.yv
        self.hurtboxes = self.generateBox(self.box)
        self.hurtboxes[3]+=self.flyingHeight

        self.onGround=False
        for player in Player.players+Platform.platforms:
            otherbox=player.hurtboxes[:]
            otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.yv<=0:
                    self.y+=otherbox[3]-self.hurtboxes[1]
                    self.yv=0
                #elif self.yv==0:
                 #   pass 
                elif self.yv>=0:
                    self.y+=otherbox[1]-self.hurtboxes[3]
                    self.yv=0
                    self.xv=self.xv*0.5
                    self.onGround=True

        if self.hurtboxes[3]>504:
            self.y+=504-self.hurtboxes[3]
            self.yv=0
            self.xv=self.xv*0.5
            self.onGround=True
        else:
            #unindent makes bird wobble here (no?
            self.yv+=0.9
            #happens all the time?

        self.hurtboxes = self.generateBox(self.box)
        if self.attackBox:
            self.hitboxes = self.generateBox(self.attackBox)
        else:
            self.hitboxes = None

        #self.attackBox= None

        for player in Player.players+Projectile.projectiles:
            if player.hitboxes and not player == self and not self.stun:
                if self.collide(player.hitboxes):
                    if(len(player.hitboxes)==7):
                        self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5],stun=player.hitboxes[6])
                    elif(len(player.hitboxes)==6):
                        self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5]) # player/player.owner for ult charge. bad for pos
                    else:
                        self.hurt(player, player.hitboxes[4])# .owner for ult charge. bad for pos
                    if isinstance(player, Projectile):
                        Projectile.projectiles.remove(player)

    def hurt(self, player, damage, knockback=None, stun=None): #player arg is stupid here. Just send direction or x coord.
        if(self.invincible):
            return
        Player.hitSound.set_volume(damage/50)
        Player.hitSound.play()
        if(knockback==None):
            knockback=damage
        if stun==None:
            stun=knockback
        self.facingRight = player.x>self.x #not player.facingRight
        if stun:
            self.state = State.stunned
            self.attackFrame = 0
        elif self.hp<=0:
            Player.players.remove(self)

        self.hp -= damage
        self.stun = max(self.stun, abs(stun))
        self.yv=-abs(knockback*0.2)
        self.xv=knockback*(self.facingRight-0.5)*-0.2
        

    def generateBox(self, data):
        new = [self.x+data[0]*Player.SCALE, self.y+data[1]*Player.SCALE, self.x+data[2]*Player.SCALE, self.y+data[3]*Player.SCALE]
        if len(data)>4:
            new.append(data[4])
        if len(data)>5:
            new.append(data[5])
        if len(data)>6:
            new.append(data[6])
        return new

    def collide(self, otherBox):
        glitchConstant=1
        if self.hurtboxes[2]>=otherBox[0]+glitchConstant and self.hurtboxes[0]<=otherBox[2]-glitchConstant:
            if self.hurtboxes[3]>=otherBox[1]+glitchConstant and self.hurtboxes[1]<=otherBox[3]-glitchConstant:
                return True
        return False

    def load(name):
        image = pygame.image.load(filepath+name)
        image = pygame.transform.scale(image, (Player.SCALE*32, Player.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        
        if not self.invisible: #character
            image = self.image[self.facingRight]
            gameDisplay.blit(image, (self.x, self.y))
        if random.random()<.1: #yellow
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0],self.hitboxes[1],self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        factor = 0.3
        leftEdge=(self.hurtboxes[0]+self.hurtboxes[2]-self.maxhp*factor)/2
        if self.ultCharge>self.CHARGE and not self.invisible:
            pygame.draw.rect(gameDisplay, (0, 255, 255), (leftEdge-4,self.hurtboxes[1]-32-4,self.maxhp*factor+4,16), 0)
            #pygame.draw.rect(gameDisplay, (0, 0, 255), \
            #(self.hurtboxes[0],self.hurtboxes[1],self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)
        if self.hp>0 and not self.invisible: #health bars
            pygame.draw.rect(gameDisplay, (255, 0, 0), (leftEdge,self.hurtboxes[1]-32+1,self.maxhp*factor,6), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), (leftEdge,self.hurtboxes[1]-32,self.hp*factor,8), 0)

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Puncher, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Puncher.idleImage
        self.init2()

        self.attack1 = [
        [6, self.prePunchImage, None, True],
        [9, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 15]],
        [18, self.punchImage],
        [25, self.prePunchImage],
        ]

        self.attack2 = [
        [12, self.prePunchImage],
        [19, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50]],
        [31, self.punchImage],
        [51, self.prePunchImage],
        ]

        self.long = [
        [19, self.prePunchImage],
        [90, self.prePunchImage, None, True],
        [100, self.punchImage],
        [109, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 40]],
        [130, self.longPunchImage],
        [141, self.punchImage],
        [159, self.prePunchImage],
        ]

        self.extreme = [
        [39, self.prePunchImage],
        [165, self.prePunchImage, None, True],
        [170, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 45, 120]],
        [210, self.punchImage],
        [226, self.prePunchImage],
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
        if self.attackFrame==1:
            Player.ultSound.play()
        self.executeAttack(self.ultimate)

    idleImage = Player.load("idle.png")
    stunnedImage = Player.load("stunned.png")
    longPunchImage = Player.load("longpunch.png")
    prePunchImage = Player.load("prepunch.png")
    punchImage = Player.load("punch.png")
class Big(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Big, self).__init__(x, y, facingRight, controls,joystick)
        self.box = [16-4, 12, 16+4, 32-4]
        self.image = Big.idleImage
        self.init2()

        self.attack1 = [
        [12, self.prePunchImage],
        [15, self.midPunchImage],
        [30, self.punchImage, [16, 16, 32-6, 32-8, 33]],
        [45, self.punchImage],
        [52, self.midPunchImage],
        [60, self.prePunchImage],
        ]

        self.attack2 = [
        [30, self.prePunchImage, None],
        [40, self.midPunchImage, None],
        [50, self.punchImage, [16, 16, 32-6, 32-8, 80]],
        [70, self.punchImage, None],
        [80, self.midPunchImage, None],
        [90, self.prePunchImage, None],
        ]

        self.skull = [
        [15, self.stunnedImage, None],
        [25, self.skullImage, [15, 10, 23, 12, 50]],
        [35, self.skullImage, None],
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
        if self.attackFrame == 1:
            Player.ultSound.play()

        a=self.attackFrame

        if a%20==8 and a<100:
            self.xv = (self.facingRight-0.5)*6
            self.yv = -3

        if a%20<=8 and a<100:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 10, 18]

        elif a<100: #and a%20>8
            self.image = self.prePunchImage
            self.attackBox = None

        elif self.attackFrame < 110:
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 30, 100]

        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("idle2.png")
    stunnedImage = Player.load("stunned2.png")
    prePunchImage = Player.load("prepunch2.png")
    midPunchImage = Player.load("midpunch2.png")
    punchImage = Player.load("punch2.png")
    skullImage = Player.load("skull2.png")
class Green(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Green, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-14, 16+3, 32-4]
        self.maxhp = 150
        self.image = Green.idleImage
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

    def attack5(self):

        if self.attackFrame < 20:
            self.image = self.stunnedImage
            self.attackBox = None
        elif self.attackFrame < 25:
            self.image = self.idleImage
        elif self.attackFrame < 33: 
            self.image = self.skullImage
        elif self.attackFrame == 33:
            self.image = self.skullImage
            Projectile.projectiles.append(Projectile(self, op=True))
            Player.ultSound.play()
        elif self.attackFrame < 60:
            self.image = self.skullImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("idle3.png")
    stunnedImage = Player.load("stunned3.png")
    kickImage = Player.load("kick3.png")
    skullImage = Player.load("skull3.png")
    projaImage = Player.load("proja3.png")
    projbImage = Player.load("projb3.png")
    magicImage = Player.load("magic3.png")
class Tree(Player):
            
    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Tree, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-15, 16+3, 32-4]
        self.image = Tree.idleImage
        self.CHARGE = 20
        self.init2()

        self.attack1 = [
        [8, self.preKickImage],
        [16, self.kickImage, [32-16, 32-8-4, 32-9, 32-7, 18]],
        [20, self.kickImage],
        [26, self.preKickImage],
        ]

        self.attack2 = [
        [15, self.preKickImage],
        [28, self.kickImage, [32-16, 32-8-4, 32-9, 32-7, 44]],
        [40, self.kickImage],
        [50, self.preKickImage],
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
            self.y = 200 #far down? 700
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
            Player.ultSound.play()
            new = Tree(self.x, self.y, self.facingRight, self.controls, self.joystick)
            new.hp = self.hp
            new.random = self.random
            self.CHARGE = 200
            self.hp=1
            #move forward
            self.image = self.growImage
            self.invincible=True
            self.x += 400*(self.facingRight-0.5)
            self.y = 700 #far down
        elif self.attackFrame < 20:
            pass
        elif self.attackFrame < 50:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("idle4.png")
    stunnedImage = Player.load("stunned4.png")
    preKickImage = Player.load("prekick4.png")
    kickImage = Player.load("kick4.png")
    growImage = Player.load("grow4.png")
    preGrowImage = Player.load("pregrow4.png")
class Bird(Player):

    def passive(self):
        if(self.pressed["5"] and self.ultCharge>self.CHARGE): #ult
            self.ultCharge = 0
            self.yv-=25
            Player.ultSound.play()

        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

        if self.pressed["w"] and self.yv>=0: #float
            self.yv=2
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Bird, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*Player.SCALE
        self.image = Bird.idleImage
        self.hp = 200
        self.init2()

        self.attack1 = [
        [8, self.prePunchImage],
        [20, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 15]],
        [24, self.punchImage],
        [34, self.prePunchImage],
        ]

        self.attack2 = [
        [15, self.prePunchImage],
        [25, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 40]],
        [50, self.punchImage],
        [70, self.prePunchImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame < 30:
            self.image = self.preelImage #preel/dodgeImage
            self.attackBox = None
        elif self.attackFrame < 150:
            self.image = self.preelImage #preel/dodgeImage
            self.attackBox = None
            if not self.pressed["3"]:
                self.attackFrame = 150

        elif self.attackFrame == 151:
            Player.bzzzSound.play()

        elif self.attackFrame < 180:
            self.image = self.elaImage
            self.attackBox = [0, 15, 32, 32-8, 5]
            if self.attackFrame%6>3:
                self.image = self.elbImage
        
        elif self.attackFrame < 200:
            self.image = self.preelImage
            self.attackBox = None
        elif self.attackFrame < 210:
            self.image = self.idleImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 40:
            self.image = self.dodgeImage
            self.invincible=True
            self.attackBox = None
        elif self.attackFrame < 50:
            self.invincible=False
            self.image = self.idlebImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("idle5.png")
    idlebImage = Player.load("idleb5.png")
    stunnedImage = Player.load("stunned5.png")
    prePunchImage = Player.load("prepunch5.png")
    punchImage = Player.load("punch5.png")
    dodgeImage = Player.load("dodge5.png")
    preelImage = Player.load("preel5.png")
    elaImage = Player.load("ela5.png")
    elbImage = Player.load("elb5.png")
class Robot(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Robot, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.image = Robot.idleImage
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
            self.yv=-17
        elif self.attackFrame < 42:
            self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self):
        if self.attackFrame==1:
            Player.ultSound.play()
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
            if self.attackFrame==15:
                Player.bzzzSound.play()
            if self.attackFrame==81:
                Player.bzzzSound.stop()
        elif self.state == 3:
            self.attack3(pressed)
        elif self.state == 4:
            self.attack4(pressed)
        elif self.state == 5:
            self.attack5()

        self.flipHitbox()

    idleImage = Player.load("idle6.png")
    stunnedImage = Player.load("stunned6.png")
    fireImage = Player.load("fire6.png")
    projbImage = Player.load("proj6.png")
    punchImage = Player.load("punch6.png")
    prePunchImage = Player.load("prepunch6.png")
    jetpackImage = Player.load("jetpack6.png")
class Lizard(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Lizard, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Lizard.idleImage
        self.CHARGE = 30
        self.init2()

        self.attack1 = [
        [6, self.prePunchImage],
        [12, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 10]],
        [18, self.punchImage],
        [24, self.prePunchImage],
        ]

        self.attack2 = [
        [9, self.prePunchImage],
        [18, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 22, 15]],
        [33, self.punchImage],
        [45, self.prePunchImage],
        ]
        self.tail = [
        [7, self.preTailImage],
        [12, self.tailImage, [7, 32-4, 10, 32-2, 17, -17]],
        [20, self.tailImage],
        [30, self.idleImage],
        ]
        self.lick = [
        [8, self.preLickImage],
        [12, self.lickImage, [15, 32-13, 28, 32-12, 0,-30]],
        [15, self.lickImage],
        [22, self.preLickImage],
        ]
    def attack3(self, pressed):
        if self.attackFrame == 5:
            Player.lickSound.play()
        self.executeAttack(self.lick)

    def attack4(self, pressed):
        self.executeAttack(self.tail)

    def passive(self):
        if self.pressed["5"] and self.ultCharge>self.CHARGE:
            Player.ultSound.play()
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None
            self.ultCharge = 0
            self.stun = 0

    preLickImage=Player.load("prelick7.png")
    lickImage=Player.load("lick7.png")
    idleImage = Player.load("idle7.png")
    stunnedImage = Player.load("stunned7.png")
    prePunchImage = Player.load("prepunch7.png")
    punchImage = Player.load("punch7.png")
    preTailImage = Player.load("prekick7.png")
    tailImage = Player.load("kick7.png")
class Can(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Can, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 28-19, 16+5, 32-8]
        self.image = self.idleImage
        self.init2()

        self.attack1 = [
        [10, self.prePunchImage],
        [15, self.punchImage, [26, 13, 29, 18, 15]],
        [20, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.attack2 = [
        [20, self.prePunchImage],
        [35, self.punchImage, [26, 13, 29, 18, 45]],
        [45, self.punchImage],
        [60, self.prePunchImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        elif self.attackFrame<20:
            self.image = self.waterImage
            self.attackBox = [13,31,16,32, 3, 0, 0]
            self.yv-=1.2
            self.hp-=0.1
            if self.hp<=0:
                Player.players.remove(self)
            self.facingRight = not self.facingRight
        elif self.attackFrame<29:
            self.image = self.idleImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        self.attack3(pressed)
        #self.state = State.idle (wut

    def attack5(self):
        Player.ultSound.play()
        self.image = self.prePunchImage
        self.state = State.idle

    idleImage = Player.load("idle8.png")
    stunnedImage = Player.load("stunned8.png")
    prePunchImage = Player.load("prepunch8.png")
    punchImage = Player.load("punch8.png")
    waterImage = Player.load("water8.png")
class Frog(Player):

    def passive(self):
        if(self.pressed["5"] and self.ultCharge>self.CHARGE):
            self.state = 5
            self.attackFrame = 0
            self.ultCharge = 0

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Frog, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-16, 16+3, 32-6]
        self.image = Frog.idleImage
        self.CHARGE=30
        self.init2()

        self.attack1 = [
        [9, self.preLickImage],
        [12, self.lickImage, [26, 18, 28, 21, 15, 25]],
        [16, self.lickImage],
        [34, self.preLickImage],
        ]

        self.attack2 = [
        [9, self.preLickImage],
        [12, self.lickImage, [26, 18, 28, 21, 10, -30]],
        [18, self.lickImage],
        [38, self.preLickImage],
        ]


    def attack3(self, pressed):
        if self.attackFrame < 15:
            self.image = self.stunnedImage
            self.attackBox = None        
        elif self.attackFrame == 15: 
            self.image = self.preLickImage
            self.xv = (self.facingRight-0.5)*8
            self.yv = -16
        elif self.attackFrame < 500:
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 505:
            self.image = self.jumpImage
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 32]
        elif self.attackFrame < 530:
            self.image = self.jumpImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 30:
            self.image = self.stunnedImage
            self.attackBox = None        
        elif self.attackFrame == 30: 
            self.image = self.preLickImage
            self.xv = (self.facingRight-0.5)*12
            self.yv = -24
        elif self.attackFrame < 500:
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 510:
            self.image = self.jumpImage
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 40]
        elif self.attackFrame < 550:
            self.image = self.jumpImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self):
        if self.attackFrame==1:
            Player.ultSound.play()
        if self.attackFrame < 15: 
            self.image = self.stunnedImage
            self.facingRight = not self.facingRight
            self.xv = 0
            self.yv = -4
        if self.attackFrame == 15:
            self.image = self.preLickImage
            self.xv = 0
            self.yv = 8
        elif self.attackFrame < 500:
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 510:
            self.image = self.jumpImage
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 60, 100]
        elif self.attackFrame < 530:
            self.image = self.jumpImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def action(self):
        self.attackFrame+=1
        self.passive()
        if self.state == State.stunned:
            self.stunned()
        elif self.state == State.idle:
            self.keys()
        elif self.state == 1:
            self.executeAttack(self.attack1, not self.pressed["1"])
            if self.attackFrame==1:
                Player.lickSound.play()
        elif self.state == 2:
            self.executeAttack(self.attack2, not self.pressed["2"])
            if self.attackFrame==1:
                Player.lickSound.play()
        elif self.state == 3:
            self.attack3(pressed)
        elif self.state == 4:
            self.attack4(pressed)
        elif self.state == 5:
            self.attack5()

        self.flipHitbox()

    idleImage = Player.load("idle9.png")
    stunnedImage = Player.load("stunned9.png")
    preLickImage = Player.load("prelick9.png")
    lickImage = Player.load("lick9.png")
    jumpImage = Player.load("jump.png")
class Monster(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Monster, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 16, 16+5, 32-4]
        self.image = Monster.idleImage
        self.init2()

        self.attack1 = [
        [7, self.prePunchImage],
        [11, self.punchImage, [22, 20, 26, 23, 20, 50, 5]],
        [14, self.punchImage],
        [17, self.prePunchImage],
        [22, self.idleImage],
        ]

        self.attack2 = [
        [15, self.prePunchImage],
        [21, self.punchImage, [22, 20, 26, 23, 30, 90, 10]],
        [27, self.punchImage],
        [37, self.prePunchImage],
        [43, self.idleImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame < 18:
            self.image = self.prePunchImage
            self.attackBox = None
        elif self.attackFrame == 23:
            self.image = self.punchImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 30:
            self.image = self.punchImage
        elif self.attackFrame < 44:
            self.image = self.prePunchImage
        elif self.attackFrame < 48:
            self.image = self.idleImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        self.attack3(pressed)
        #self.state = State.idle

    def attack5(self):
        if self.attackFrame==1:
            Player.ultSound.play()
            Player.growSound.play()
        if self.attackFrame < 57:
            self.yv+=0.5
            self.image = self.prePunchImage
            self.hp=min(self.hp+1, self.maxhp)
            self.facingRight = not self.facingRight
        else:
            self.state = State.idle
            self.image = self.idleImage

    idleImage = Player.load("idle10.png")
    stunnedImage = Player.load("stunned10.png")
    prePunchImage = Player.load("prepunch10.png")
    punchImage = Player.load("punch10.png")
    projbImage = Player.load("proj10.png")

allClasses = [Puncher, Big, Green, Tree, Bird, Robot, Lizard, Can, Frog, Monster]

def restart():
    Player.players = []
    choices = []
    num = 0
    while State.jump_out == False:
        #pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                State.jump_out = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            num-=1
            time.sleep(0.1)
        if pressed[pygame.K_RIGHT]:
            num+=1
            time.sleep(0.1)
        if pressed[pygame.K_r]:
            choices.append(random.choice(allClasses))
            num=0
            if len(choices)==State.playerCount:
                return choices
            time.sleep(0.5)
        if pressed[pygame.K_SPACE]:
            choices.append(allClasses[num%len(allClasses)])
            num=0
            if len(choices)==State.playerCount:
                return choices
            time.sleep(0.5)

        #draw
        gameDisplay.fill((100,100,100))
        pygame.draw.rect(gameDisplay,(200,200,200),(400+64,0,16*8,300+28*8),0)
        for i in range(len(choices)):
            gameDisplay.blit(choices[i].idleImage[1], (100*i, 0))
        for i in [-2,-1,0,1,2]:
            gameDisplay.blit(allClasses[(num-i)%len(allClasses)].idleImage[1], (400-100*i, 300))
        
        pygame.display.update()
        clock.tick(100)
    
    pygame.quit()
    quit()

gameDisplay = pygame.display.set_mode((1000, 600))
backgrounds = []
for name in ["background.png","background2.png"]:
    background = pygame.image.load(filepath+name)
    background = pygame.transform.scale(background, (1000, 600))
    backgrounds.append(background)
pygame.display.set_caption("Fighting Game")
pygame.display.set_icon(pygame.image.load(filepath+"idle.png"))
Platform.generate()

initSound()

pygame.joystick.init()
stickNum = pygame.joystick.get_count()
sticks=[]
for i in range(stickNum):
    sticks.append(pygame.joystick.Joystick(i))
    sticks[-1].init()

State.playerCount = 2 # HERE * * * * * * * * *

State.jump_out = False
while State.jump_out == False:
    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            State.jump_out = True
    if len(Player.players)<2:
        time.sleep(1)
        choices = restart()

        # HERE * * * * * * * * *
        choices[0](200, 100, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_s})
        choices[1](600, 100, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
        #random.choice(class3)(400, 100, False, {"w":0,"3":4,"4":5,"5":3}, sticks[0])
        
        for i in range(0):
            #random.choice(allClasses)(600, 100, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
            choices[1](600, 100, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
            Player.players[-1].random=1
        # HERE * * * * * * * * *

        currentBackground = random.choice(backgrounds)
        Platform.restart()
        pygame.display.update()
        time.sleep(1)
    

    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.getPressed(pressed)
        player.action()
    for player in Player.players+Projectile.projectiles:
        player.physics()
    #draw
    gameDisplay.blit(currentBackground, (0,0))
    for player in Player.players+Projectile.projectiles+Platform.platforms:
        player.draw()
        
    pygame.display.update()
    clock.tick(75)
    
pygame.quit()
quit()


"""
#ella gjorde kutty så ru vet!!!!/ella





"""
