import pygame
import time
import random
import os
clock = pygame.time.Clock()
filepath=""
#"C:/Users/brovar02/Documents/fightingGame/fightingGame-master/"

SOUND_PATH = os.path.join(filepath, "sounds")

def initSound():
    pygame.font.init() # you have to call this at the start, 
                           # if you want to use this module.
    pygame.mixer.init(buffer=32)
    Player.hitSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "soundeffect2.wav"))
    Player.lickSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "lickeffect.wav"))
    Player.lickSound.set_volume(0.2)
    Player.growSound = pygame.mixer.Sound(os.path.join(SOUND_PATH,"grasseffect.wav"))
    Player.growSound.set_volume(0.3)
    Player.ultSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "ult.wav"))
    Player.ultSound.set_volume(0.1)
    Player.bzzzSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bzzzEffect.wav"))
    Player.bzzzSound.set_volume(0.05)
    Player.killSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "smashbros.wav"))
    Player.killSound.set_volume(0.5)
    Player.gameSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "game.wav"))
    Player.gameSound.set_volume(0.5)
    
    pygame.mixer.music.load("music.wav") #must be wav 16bit and stuff?
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

def endEffect():
    pygame.draw.rect(gameDisplay, (200, 0, 100), (96,0,808,504), 0)
    Player.hitLag=1
    if len(Player.players)>2:
        Player.killSound.play()
    else:
        Player.gameSound.play()

def countPlayers():
    players=0
    codes = []
    for player in Player.players:
        if isinstance(player, Tree):
            if not player.code in codes:
                codes.append(player.code)
        else:
            players+=1
    players+=len(codes)
    return players

class State():
    idle=0
    stunned=-1

class Platform():
    
    def generate():
        Platform.platformLayouts = [
        [Platform([350, 340, 650, 360])],
        #[Platform([96, 450, 400, 504]), Platform([96, 400, 200, 450])],
        #[Platform([400,450,600,504])],
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
        (self.hurtboxes[0]+shakeX,self.hurtboxes[1]+shakeY,self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)

class Projectile():
    projectiles = []
    def __init__(self, owner, op=False):
        self.owner = owner
        self.image = self.owner.projbImage
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
            self.x-=self.xv*2
        if isinstance(self.owner, Robot):
            self.xv = (self.facingRight-0.5) * 20
            self.box = [32-8, 16, 32-4, 19, 9+0*self.op, 7]
            self.x-=self.xv*3
        if isinstance(self.owner, Alien):
            self.xv = (self.facingRight-0.5) * -20
            self.box = [3, 14, 7, 17, 7,0,10]
            self.x-=self.xv*4
            self.yv = .5
        if isinstance(self.owner, Monster):
            self.xv = (self.facingRight-0.5) * 8
            self.yv = -1
            self.box = [32-11, 19, 32-7, 22, 11, -44, 0]
        if isinstance(self.owner, Penguin):
            self.y-=10
            if self.op:
                self.xv = (self.facingRight-0.5) * 16
                self.box = [19, 20, 19+3, 20+3, 9]
                self.image = self.owner.projaImage
            else:
                self.xv = (self.facingRight-0.5) * 8
                #self.x+=self.owner.xv
                self.yv = 0.2
                self.box = [18+1,18,18+6,18+5, 23]
        if isinstance(self.owner, Sad):
            self.box = [16-2,15,16+3,20, 50, 10, 50]
            self.x+=(self.owner.facingRight-0.5)*100
        self.xv+=self.owner.xv

    def keys(self, pressed):
        nevercalled
        pass

    def draw(self):
        gameDisplay.blit(self.image[self.facingRight], (self.x+random.randint(-8,8)*self.op+shakeX, self.y+random.randint(-8,8)*self.op+shakeY))
        if random.random()<.1:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)

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
        for player in Player.players+Projectile.projectiles+Platform.platforms:
            if player == self:
                continue
            if isinstance(player, Platform):
                otherBox = player.hurtboxes
            elif player.hitboxes:
                otherBox = player.hitboxes
            else:
                continue
            if self.hurtboxes[2]>otherBox[0] and self.hurtboxes[0]<otherBox[2]:
                if self.hurtboxes[3]>otherBox[1] and self.hurtboxes[1]<otherBox[3]:
                    if self in Projectile.projectiles:
                        Projectile.projectiles.remove(self)
                    if isinstance(player, Player):
                        if (player.state==3 and type(player) in [Golem, Lizard]) or (player.state in [1,2] and type(player) in [Frog, Monster]):
                            player.hp=min(player.hp+30, player.maxhp)
                            Player.lickSound.play()
                            Player.growSound.play()
                    else: #is proj
                        if player in Projectile.projectiles:
                            Projectile.projectiles.remove(player)

class Player():
    hitLag=0
    SCALE=8
    players=[]
    def __init__(self, x, y, facingRight, controls, joystick=None):
        Player.players.append(self)
        self.CHARGE = 50
        self.flyingHeight=0
        self.onGround = True
        self.xspeed=2
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
            self.attack1(pressed)
        elif self.state == 2:
            self.attack2(pressed)
        elif self.state == 3:
            self.attack3(pressed)
        elif self.state == 4:
            self.attack4(pressed)
        elif self.state == 5:
            self.attack5(pressed)

        self.flipHitbox()

    def flipHitbox(self):
        if self.attackBox and not self.facingRight:
            right = 32 - self.attackBox[0]
            left = 32 - self.attackBox[2]
            self.attackBox[0] = left
            self.attackBox[2] = right

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])

    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])

    def attack5(self, pressed):
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
        if random.random()<0.1:
            self.ultCharge+=1

    def getPressed(self, pressed):
        if self.random:
            if AiFocus:
                target = Player.players[0]
            else:
                target = random.choice(Player.players)
            if random.random()<0.1:
                self.pressed["d"] = random.randint(0,1)
            if random.randint(0,20)==0 and target!=self:
                self.pressed["w"] = target.y < self.y

            attacking=False
            for i in ["1","2","3","4","5"]:
                self.pressed[i] = (random.randint(0,40)==0) ^ (self.state!=State.idle)
                if self.pressed[i]:
                    self.pressed["d"] = target.x > self.x
                    if isinstance(self, Alien) and (self.pressed["3"] or self.pressed["4"]):
                        self.pressed["d"] = target.x < self.x
                    if isinstance(self, Lizard) and self.pressed["4"]:
                        self.pressed["d"] = target.x < self.x
                        self.pressed["w"] = True

            self.pressed["a"] = not self.pressed["d"]

        elif self.joystick:
            x = self.joystick.get_axis(0)
            triggers = self.joystick.get_axis(2) #lt - rt but 0 = -3.01
            self.pressed["d"] = (x>0.5)
            self.pressed["a"] = (x<-0.5)
            self.pressed["2"] = self.joystick.get_button(3) #(triggers<-0.5 and triggers>-2)
            self.pressed["1"] = self.joystick.get_button(2) #(triggers>0.5)
            for i in ["w","3","4","5"]:
                self.pressed[i] = (self.joystick.get_button(self.controls[i]))
            self.pressed["3"] += (triggers>0.5)
            self.pressed["4"] += (triggers<-0.5 and triggers>-2)
        else:
            for i in ["a","d","w","1","2","3","4","5"]:
                self.pressed[i] = (pressed[self.controls[i]])

    def keys(self):
        if(self.pressed["d"]):
            if self.onGround:
                self.xv+=self.xspeed
            else:
                self.xv=min(self.xspeed*2, self.xv+0.2)
            self.facingRight = True
        elif(self.pressed["a"]):
            if self.onGround:
                self.xv-=self.xspeed
            else:
                self.xv=max(-self.xspeed*2, self.xv-0.2)
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
            if not isinstance(self,Lizard) and not (isinstance(self,Penguin) and not self.wizard):
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
        self.hurtboxes[0]+=8
        self.hurtboxes[2]-=8

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
        self.hurtboxes[0]+=8
        self.hurtboxes[2]-=8

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
        if not self.stun:
            for player in Player.players+Projectile.projectiles:
                if player.hitboxes and not player == self:
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

        self.hp -= damage
        Player.hitLag = 0.02+damage/800
        if stun:
            self.state = State.stunned
            self.attackFrame = 0
            if self.hp<=0:
                if not (isinstance(self,Tree) and not self.isLastTree()):
                    endEffect()
        elif self.hp<=0:
            endEffect()
            Player.players.remove(self)
        self.stun = max(self.stun, abs(stun))
        self.yv=-abs(knockback*0.2)
        self.xv=knockback*(self.facingRight-0.5)*-0.2
        #effects
        Player.shake=damage//2
        if damage>10+random.random()*10:
            theImage = Player.hurtImage[self.facingRight]
            gameDisplay.blit(theImage, (self.x+self.facingRight*20, self.y))
        

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

    def load(playerName, textureName):
        image = pygame.image.load(os.path.join(filepath, "textures", playerName, textureName))
        image = pygame.transform.scale(image, (Player.SCALE*32, Player.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        
        if not self.invisible: #character
            image = self.image[self.facingRight]
            gameDisplay.blit(image, (self.x+shakeX, self.y+shakeY))
        if random.random()<.1: #yellow
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        factor = 0.3
        leftEdge=(self.hurtboxes[0]+self.hurtboxes[2]-self.maxhp*factor)/2
        if self.ultCharge>self.CHARGE and not self.invisible:
            pygame.draw.rect(gameDisplay, (0, 255, 255), (leftEdge-4,self.hurtboxes[1]-32-4,self.maxhp*factor+8,16), 0)
            #pygame.draw.rect(gameDisplay, (0, 0, 255), \
            #(self.hurtboxes[0],self.hurtboxes[1],self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)
        if self.hp>0 and not self.invisible: #health bars
            pygame.draw.rect(gameDisplay, (255, 0, 0), (leftEdge,self.hurtboxes[1]-32+1,self.maxhp*factor,6), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), (leftEdge,self.hurtboxes[1]-32,self.hp*factor,8), 0)

    
    hurtImage = pygame.image.load(os.path.join(filepath, "textures", "effect.png"))
    hurtImage = pygame.transform.scale(hurtImage, (8*32, 8*32))
    hurtImage = (pygame.transform.flip(hurtImage, True, False), hurtImage)
    text = ""
    shake = 0

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Puncher, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Puncher.idleImage
        self.xspeed = 2.5
        self.init2()

        self.first = [
        [6, self.prePunchImage, None, True],
        [9, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 19]],
        [18, self.punchImage],
        [25, self.prePunchImage],
        ]

        self.second = [
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

    def attack3(self, pressed):
        self.executeAttack(self.long, not self.pressed["3"])
    def attack4(self, pressed):
        self.executeAttack(self.extreme, not self.pressed["4"])
    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            self.image = self.prePunchImage
        if self.attackFrame < 8: 
            self.image = self.punchImage
            self.yv-=4
            self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 10, -125, 43]
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        elif self.attackFrame < 43:
            self.image = self.prePunchImage
            self.attackBox = None
        elif self.attackFrame < 60:
            self.image = self.punchImage
            self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 50, 200, 100]
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("puncher", "idle.png")
    stunnedImage = Player.load("puncher", "stunned.png")
    longPunchImage = Player.load("puncher", "longpunch.png")
    prePunchImage = Player.load("puncher", "prepunch.png")
    punchImage = Player.load("puncher", "punch.png")
    text = "Good at punching! smaller than Big."
class Big(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Big, self).__init__(x, y, facingRight, controls,joystick)
        self.box = [16-4, 12, 16+4, 32-4]
        self.image = Big.idleImage
        self.xspeed=1.8
        self.hp=300
        self.init2()

        self.first = [
        [2, self.prePunchImage, [10, 17, 11, 32-9, 20]],
        [12, self.prePunchImage],
        [15, self.midPunchImage],
        [30, self.punchImage, [16, 16, 32-6, 32-8, 33, 50, 30]],
        [45, self.punchImage],
        [52, self.midPunchImage],
        [60, self.prePunchImage],
        ]

        self.second = [
        [2, self.prePunchImage, [10, 17, 11, 32-9, 20]],
        [30, self.prePunchImage],
        [130, self.prePunchImage, None, True],
        [140, self.midPunchImage],
        [150, self.punchImage, [16, 16, 32-6, 32-8, 80, 100, 80]],
        [170, self.punchImage],
        [180, self.midPunchImage],
        [190, self.prePunchImage],
        ]

        self.elbow = [
        [2, self.prePunchImage, [10, 17, 11, 32-9, 20]],
        [15, self.prePunchImage],
        [120, self.prePunchImage, None, True],
        ]

        self.skull = [
        [15, self.stunnedImage, None],
        [25, self.skullImage, [15, 10, 23, 12, 50]],
        [35, self.skullImage, None],
        ]
    
    def attack3(self, pressed):
        #self.executeAttack(self.elbow, not self.pressed["3"])
        
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

    def attack5(self, pressed):
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
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)

        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("big", "idle.png")
    stunnedImage = Player.load("big", "stunned.png")
    prePunchImage = Player.load("big", "prepunch.png")
    midPunchImage = Player.load("big", "midpunch.png")
    punchImage = Player.load("big", "punch.png")
    skullImage = Player.load("big", "skull.png")
    text = "Big!"
class Green(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Green, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-14, 16+3, 32-4]
        self.maxhp = 200
        self.image = Green.idleImage
        self.xspeed = 2.5
        self.init2()

        self.first = [
        [10, self.kickImage, [32-14, 32-6, 32-10, 32-3, 10]],
        [20, self.kickImage, None],
        [25, self.idleImage, None],
        ]

        self.second = [
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
            if self.attackFrame%15==0:
                self.facingRight = not self.facingRight
        else:
            self.hp = min(self.maxhp, self.hp+30)
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):

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
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        elif self.attackFrame < 60:
            self.image = self.skullImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("green", "idle.png")
    stunnedImage = Player.load("green", "stunned.png")
    kickImage = Player.load("green", "kick.png")
    skullImage = Player.load("green", "skull.png")
    projaImage = Player.load("green", "proja.png")
    projbImage = Player.load("green", "projb.png")
    magicImage = Player.load("green", "magic.png")
    text = "Has no arms :("
class Tree(Player):

    def passive(self):
        if random.randint(0,50)<1: #dont know if this is needed
            num = countPlayers()
            if num==1:
                Player.players.remove(self)

    def isLastTree(self):
        for player in Player.players:
            if player!=self and isinstance(player, Tree):
                if player.code == self.code:
                    return False
        return True

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Tree, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-15, 16+3, 32-4]
        self.image = Tree.idleImage
        self.CHARGE = 20
        self.code = random.random()
        self.init2()

        self.first = [
        [8, self.preKickImage],
        [16, self.kickImage, [16, 20, 32-9, 32-7, 18]],
        [20, self.kickImage],
        [26, self.preKickImage],
        ]

        self.second = [
        [15, self.preKickImage],
        [28, self.kickImage, [16, 20, 32-9, 32-7, 44]],
        [40, self.kickImage],
        [50, self.preKickImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        elif self.attackFrame < 10:
            self.image = self.preGrowImage
        elif self.attackFrame < 17:
            self.image = self.growImage
            self.invincible=True
        elif self.attackFrame < 40:
            self.invisible=True
        elif self.attackFrame==40:
            self.x += 250*(self.facingRight-0.5)
            Player.growSound.play()
            self.facingRight = not self.facingRight
        elif self.attackFrame < 47:
            self.invisible = False
        elif self.attackFrame < 55:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        elif self.attackFrame < 10:
            self.image = self.preGrowImage
        elif self.attackFrame < 17:
            self.image = self.growImage
            self.invincible=True
        elif self.attackFrame < 40:
            self.invisible=True
        elif self.attackFrame==40:
            Player.growSound.play()
        elif self.attackFrame < 47:
            self.invisible = False
        elif self.attackFrame < 55:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)

            new = Tree(self.x, self.y, self.facingRight, self.controls, self.joystick)
            new.code = self.code

            new.hp = self.hp
            new.random = self.random
            new.state = 5
            new.attackFrame = 2
            new.CHARGE = 200
            new.hp=0
            new.x += 400*(self.facingRight-0.5)
            new.y = 700 #far down

            self.state = State.idle

        elif self.attackFrame < 20:
            self.invincible=True
            self.image = self.growImage
        elif self.attackFrame < 50:
            self.invincible=False
            self.image = self.preGrowImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("tree", "idle.png")
    stunnedImage = Player.load("tree", "stunned.png")
    preKickImage = Player.load("tree", "prekick.png")
    kickImage = Player.load("tree", "kick.png")
    growImage = Player.load("tree", "grow.png")
    preGrowImage = Player.load("tree", "pregrow.png")
    text = "lol waht"
class Sad(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Sad, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-7]
        self.image = Sad.idleImage
        self.flyingHeight=3*Player.SCALE
        self.xspeed = 2
        self.init2()

        self.first = [
        [13, self.preSkullImage],
        [17, self.skullImage, [19, 15, 24, 21, 37]],
        [31, self.skullImage],
        [40, self.preSkullImage],
        ]

        self.second = self.first

        self.jump = [
        [6, self.preJumpImage],
        [12, self.jumpImage, [10, 24, 15, 29, 14, 40]],
        [21, self.jumpImage],
        [29, self.preJumpImage],
        ]


    def attack3(self, pressed):
        self.executeAttack(self.jump, not self.pressed["2"])
        if self.attackFrame==12:
            self.yv=-12
            r=(self.facingRight-0.5)*2
            self.xv=max(self.xv*r,4)*r
    
    def attack4(self, pressed):
        if self.attackFrame > 0:
            if self.attackFrame%20<10:
                self.image = self.magic1Image
            else:
                self.image = self.magic2Image
            for i in Projectile.projectiles:
                i.xv+=(self.facingRight-0.5)*0.5
                i.xv*=0.95
            for i in Player.players:
                i.xv+=(self.facingRight-0.5)*0.5
                i.hp-=0.2
            self.hp+=0.1
            if not self.pressed["4"]:
                self.attackFrame = -2
        else:
            self.state=State.idle
            self.image=self.idleImage
            self.attackBox=None
    
    def attack5(self, pressed):
        if self.attackFrame == 1:
            self.image = self.skullImage
            Projectile.projectiles.append(Projectile(self))
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        elif self.attackFrame <20:
            self.image = self.preSkullImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("sad", "idle.png")
    stunnedImage = Player.load("sad", "stunned.png")
    magic1Image = Player.load("sad", "magic1.png")
    magic2Image = Player.load("sad", "magic2.png")
    preSkullImage = Player.load("sad", "preskull.png")
    skullImage = Player.load("sad", "skull.png")
    preJumpImage = Player.load("sad", "prejump.png")
    jumpImage = Player.load("sad", "jump.png")
    projbImage = Player.load("sad", "somehorn.png")
    text = "Magically moves objects. Is depressed. "

class Bird(Player):

    def passive(self):
        if(self.pressed["5"] and self.ultCharge>self.CHARGE): #ult
            self.ultCharge = 0
            self.yv=-22
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)

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
        self.maxhp = 200
        self.init2()

        self.first = [
        [8, self.prePunchImage],
        [20, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 15]],
        [24, self.punchImage],
        [34, self.prePunchImage],
        ]

        self.second = [
        [15, self.prePunchImage],
        [25, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 38]],
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
                self.attackFrame = 149

        elif self.attackFrame == 150:
            Player.bzzzSound.play()

        elif self.attackFrame < 180:
            self.image = self.elaImage
            self.attackBox = [0, 15, 32, 32-8, 6,5]
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

    idleImage = Player.load("bird", "idle.png")
    idlebImage = Player.load("bird", "idleb.png")
    stunnedImage = Player.load("bird", "stunned.png")
    prePunchImage = Player.load("bird", "prepunch.png")
    punchImage = Player.load("bird", "punch.png")
    dodgeImage = Player.load("bird", "dodge.png")
    preelImage = Player.load("bird", "preel.png")
    elaImage = Player.load("bird", "ela.png")
    elbImage = Player.load("bird", "elb.png")
    text = "can fly and dodge and is op"
class Robot(Player):
    
    def passive(self):
        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Robot, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.image = Robot.idleImage
        self.init2()

        self.first = [
        [30, self.stunnedImage,None],
        [38, self.fireImage, [20, 32-17, 24, 32-12, 48, 58]],
        [45, self.fireImage, None],
        [60, self.stunnedImage, None],
        ]

        self.second = [
        [15, self.prePunchImage,None],
        [30, self.punchImage, [24, 32-17, 27, 32-12, 8, 12]],
        [80, self.punchImage, [24, 32-17, 27, 32-12, 8, 12],True],
        [110, self.prePunchImage,None],
        ]

    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==15:
            Player.bzzzSound.play()
        if self.attackFrame==81:
            Player.bzzzSound.stop()

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

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        if self.attackFrame < 60:
            if self.attackFrame%10 ==1:
                self.image = self.fireImage
                Projectile.projectiles.append(Projectile(self, op=True))
                Player.hitSound.set_volume(0.4)
                Player.hitSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
            else:
                self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("robot", "idle.png")
    idlebImage = Player.load("robot", "idleb.png")
    stunnedImage = Player.load("robot", "stunned.png")
    fireImage = Player.load("robot", "fire.png")
    projbImage = Player.load("robot", "proj.png")
    punchImage = Player.load("robot", "punch.png")
    prePunchImage = Player.load("robot", "prepunch.png")
    jetpackImage = Player.load("robot", "jetpack.png")
class Lizard(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Lizard, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Lizard.idleImage
        self.xspeed = 2.5
        self.CHARGE = 30
        self.init2()

        self.first = [
        [6, self.prePunchImage],
        [12, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 10]],
        [18, self.punchImage],
        [24, self.prePunchImage],
        ]

        self.second = [
        [9, self.prePunchImage],
        [18, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 20]],
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
        if self.pressed["5"] and self.ultCharge>self.CHARGE and not self.state==State.idle:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
            self.ultCharge = 0
            self.stun = 0
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    preLickImage=Player.load("lizard", "prelick.png")
    lickImage=Player.load("lizard", "lick.png")
    idleImage = Player.load("lizard", "idle.png")
    stunnedImage = Player.load("lizard", "stunned.png")
    prePunchImage = Player.load("lizard", "prepunch.png")
    punchImage = Player.load("lizard", "punch.png")
    preTailImage = Player.load("lizard", "prekick.png")
    tailImage = Player.load("lizard", "kick.png")
    text = "Cool pro animation cancel character!"
class Golem(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Golem, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [11, 15, 20, 28]
        self.image = self.idleImage
        self.init2()

        self.first = [
        [5, self.prePunchImage],
        [8, self.punchImage, [18, 23, 22, 27, 8, 8, 11]],
        [14, self.punchImage],
        [18, self.punchImage, [21, 17, 24, 22, 10, 20, 10]],
        [26, self.prePunchImage],
        ]

        self.second = [
        [21, self.prePunchImage],
        [25, self.punchImage, [18, 23, 22, 27, 11, -50, 17]],
        [38, self.prePunchImage],
        [45, self.punchImage, [21, 17, 24, 22, 15, -60, 20]],
        [54, self.prePunchImage],
        ]

        self.lick = [
        [5, self.preLickImage],
        [8, self.lickImage, [20, 9, 24, 13, 25]],
        [14, self.lickImage],
        [20, self.preLickImage],
        ]

        self.grass = [
        [23, self.preGrassImage],
        [43, self.grassImage, [21, 19, 32, 24, 5, 5]],
        [48, self.grassImage, [21, 19, 32, 24, 12, 22]],
        [64, self.preGrassImage],
        ]

        self.ultimate = [
        [50, self.fireImage, [9,6,24,30, 25, 50], True],
        ]

    def attack3(self, pressed):
        if self.attackFrame==1:
            Player.lickSound.play()
        self.executeAttack(self.lick, not self.pressed["3"])

    def attack4(self, pressed):
        if self.attackFrame==20:
            Player.bzzzSound.play()
            Player.growSound.play()
        self.executeAttack(self.grass, not self.pressed["4"])
        #self.state = State.idle (??

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        self.executeAttack(self.ultimate, not self.pressed["5"])

    idleImage = Player.load("golem", "idle.png")
    stunnedImage = Player.load("golem", "stunned.png")
    fireImage = Player.load("golem", "fire.png")
    prePunchImage = Player.load("golem", "prepunch.png")
    punchImage = Player.load("golem", "punch.png")
    preGrassImage = Player.load("golem", "pregrass.png")
    grassImage = Player.load("golem", "grass.png")
    preLickImage = Player.load("golem", "prelick.png")
    lickImage = Player.load("golem", "lick.png")
    text = "Isn't from space."
class Alien(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Alien, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [13, 14, 19, 28]
        self.image = self.idleImage
        self.init2()
        self.xspeed=3

        self.first = [
        [10, self.prePunchImage],
        [15, self.punchImage, [17, 19, 23, 23, 5,-10]],
        [18, self.punchImage],
        [22, self.prePunchImage],
        [32, self.punchImage, [17, 19, 23, 23, 12]],
        [40, self.prePunchImage],
        ]

        self.second = [
        [20, self.prePunchImage],
        [25, self.punchImage, [17, 19, 23, 23, 20,-10, 35]],
        [27, self.punchImage],
        [44, self.prePunchImage],
        ]

        self.ultimate = [
        [5, self.idleImage],
        [10, self.footImage,[19, 23, 23, 28, 5,-35,5]],
        [20, self.armImage, [19, 17, 24, 20, 1, -30,10]],
        [24, self.rise1Image, [19, 17, 24, 20, 1, -28,4]],
        [28, self.rise2Image, [19, 15, 24, 18, 2, -22,4]],
        [32, self.rise3Image, [19, 13, 24, 16, 5, -15,4]],
        [36, self.rise4Image, [19, 11, 24, 14, 10, 0,4]],
        [40, self.rise3Image, [19, 13, 24, 16, 5, 0,4]],
        [44, self.rise2Image, [19, 15, 24, 18, 2, 0,4]],
        [48, self.rise1Image, [19, 17, 24, 20, 10, 70]],
        [60, self.idleImage]
        ]

    def attack3(self, pressed):
        #self.executeAttack(self.hair, not self.pressed["3"])

        if self.attackFrame < 5:
            self.image = self.preHairImage
            self.attackBox = None
            self.xv=self.xv-(self.facingRight*2-1)*2        
        elif self.attackFrame < 8: 
            self.image = self.hairImage
            self.attackBox = [5, 16, 9, 24, 10,15]
        elif self.attackFrame < 17:
            self.image = self.hairImage
            self.attackBox = None
        elif self.attackFrame < 22:
            self.image = self.preHairImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):


        if self.attackFrame < 13:
            self.image = self.stunnedImage
        elif self.attackFrame < 22: 
            self.image = self.fireImage
        elif self.attackFrame == 22:
            self.image = self.fireImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 27:
            self.image = self.idleImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        self.executeAttack(self.ultimate)

    idleImage = Player.load("alien", "idle.png")
    stunnedImage = Player.load("alien", "stunned.png")
    fireImage = Player.load("alien", "fire.png")
    prePunchImage = Player.load("alien", "prepunch.png")
    punchImage = Player.load("alien", "punch.png")
    preHairImage = Player.load("alien", "prehair.png")
    hairImage = Player.load("alien", "hair.png")
    projbImage = Player.load("alien", "proj.png")
    
    footImage = Player.load("alien", "foot.png")
    armImage = Player.load("alien", "arm.png")
    rise1Image = Player.load("alien", "rise1.png")
    rise2Image = Player.load("alien", "rise2.png")
    rise3Image = Player.load("alien", "rise3.png")
    rise4Image = Player.load("alien", "rise4.png")
    text = "Is from space."

class Can(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Can, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 28-19, 16+5, 32-8]
        self.image = self.idleImage
        self.init2()

        self.first = [
        [10, self.prePunchImage],
        [15, self.punchImage, [26, 13, 29, 18, 15]],
        [20, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.second = [
        [20, self.prePunchImage],
        [35, self.punchImage, [26, 13, 29, 18, 45]],
        [45, self.punchImage],
        [60, self.prePunchImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
        elif self.attackFrame<100:
            self.image = self.waterImage
            self.attackBox = [13,31,16,32, 1, 0, 0]
            self.yv-=1
            self.yv=self.yv*0.95
            self.facingRight = not self.facingRight
            if not (self.pressed["3"] or self.pressed["4"]):
                self.attackFrame=99
        elif self.attackFrame<109:
            self.image = self.idleImage
            self.facingRight = not self.facingRight
            self.yv=self.yv*0.95
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        self.attack3(pressed)
        #self.state = State.idle (wut

    def attack5(self, pressed):
        Player.ultSound.play()
        pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        self.image = self.prePunchImage
        self.state = State.idle

    idleImage = Player.load("can", "idle.png")
    stunnedImage = Player.load("can", "stunned.png")
    prePunchImage = Player.load("can", "prepunch.png")
    punchImage = Player.load("can", "punch.png")
    waterImage = Player.load("can", "water.png")
    text = "DANSKA BURKEN"
class Frog(Player):

    def passive(self):
        if(self.pressed["5"] and self.ultCharge>self.CHARGE and not self.stun):
            self.state = 5
            self.attackFrame = 0
            self.ultCharge = 0

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Frog, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-16, 16+3, 32-6]
        self.image = Frog.idleImage
        self.xspeed = 2.5
        self.CHARGE=30
        self.init2()

        self.first = [
        [9, self.preLickImage],
        [12, self.lickImage, [26, 18, 28, 21, 15, 25]],
        [16, self.lickImage],
        [34, self.preLickImage],
        ]

        self.second = [
        [9, self.preLickImage],
        [12, self.lickImage, [26, 18, 28, 21, 10, -30]],
        [18, self.lickImage],
        [38, self.preLickImage],
        ]

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])
        if self.attackFrame==1:
            Player.lickSound.play()
    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==1:
            Player.lickSound.play()

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

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        if self.attackFrame < 15: 
            self.image = self.stunnedImage
            self.facingRight = not self.facingRight
            self.yv = -4
        elif self.attackFrame == 15:
            self.image = self.preLickImage
            self.xv = 0
            self.yv = 16
        elif self.attackFrame < 500:
            self.yv = min(16, self.yv) #max speed but can be knocked for fun
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 510:
            self.image = self.jumpImage
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
            self.attackBox = [16-6, 32-8, 16+5, 32-3, self.attackFrame//15+10, self.attackFrame//15+40]
        elif self.attackFrame < 530:
            self.image = self.jumpImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("frog", "idle.png")
    stunnedImage = Player.load("frog", "stunned.png")
    preLickImage = Player.load("frog", "prelick.png")
    lickImage = Player.load("frog", "lick.png")
    jumpImage = Player.load("frog", "jump.png")
    text = "bad i didnt make this"
class Monster(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Monster, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 16, 16+5, 32-4]
        self.image = Monster.idleImage
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [11, self.punchImage, [22, 20, 26, 23, 20, 50, 5]],
        [14, self.punchImage],
        [17, self.prePunchImage],
        [22, self.idleImage],
        ]

        self.second = [
        [15, self.prePunchImage],
        [21, self.punchImage, [22, 20, 26, 23, 35, 90, 10]],
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

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            Player.growSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (96,0,808,504), 0)
        if self.attackFrame < 217:

            self.yv-=0.5
            self.image = self.prePunchImage
            self.hp=min(self.hp+0.7, self.maxhp)
            self.facingRight = not self.facingRight
        else:
            self.state = State.idle
            self.image = self.idleImage

    idleImage = Player.load("monster", "idle.png")
    stunnedImage = Player.load("monster", "stunned.png")
    prePunchImage = Player.load("monster", "prepunch.png")
    punchImage = Player.load("monster", "punch.png")
    projbImage = Player.load("monster", "proj.png")
    text = "This character is very interesting."
class Penguin(Player):

    def passive(self):
        if self.wizard:
            self.idleImage = self.wizardImage
            self.stunnedImage = self.stunnedWizardImage
            self.first = self.wizardFirst
            self.second = self.wizardSecond
            self.attack3 = self.throw
            self.xspeed = 1.8
        else:
            self.idleImage = self.ninjaImage
            self.stunnedImage = self.stunnedNinjaImage
            self.first = self.ninjaFirst
            self.second = self.ninjaSecond
            self.attack3 = self.shuriken
            self.xspeed = 2.5

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Penguin, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = self.ninjaImage
        self.xspeed = 2.5
        self.wizard = False
        self.init2()

        self.ninjaFirst = [
        [6, self.prePunchImage],
        [12, self.punchImage, [18, 19, 24, 23, 16]],
        [20, self.punchImage],
        [28, self.prePunchImage],
        ]

        self.ninjaSecond = [
        [12, self.prePunchImage],
        [21, self.punchImage, [18, 19, 24, 23, 37]],
        [30, self.punchImage],
        [36, self.ninjaImage],
        [46, self.prePunchImage],
        ]

        self.wizardFirst = [
        [10, self.preMagicImage],
        [17, self.midMagicImage],
        [72, self.magicImage, [23,17,24+6,17+6, 5,10], True],
        [78, self.magicImage],
        [85, self.midMagicImage],
        [90,self.preMagicImage],
        ]
        self.wizardSecond = self.wizardFirst

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])
        if self.attackFrame==1 and self.wizard:
            Player.bzzzSound.play()
            Player.growSound.play()
    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==1 and self.wizard:
            Player.bzzzSound.play()
            Player.growSound.play()

    def shuriken(self,pressed):
        if self.attackFrame < 10:
            self.image = self.prePunchImage
            self.attackBox = None
        elif self.attackFrame < 16:
            self.image = self.idleImage
        elif self.attackFrame < 23: 
            self.image = self.punchImage
        elif self.attackFrame == 23:
            self.image = self.punchImage
            Projectile.projectiles.append(Projectile(self, op=True))
        elif self.attackFrame < 46:
            self.image = self.idleImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def throw(self,pressed):
        if self.attackFrame < 18:
            self.image = self.preHatImage
            self.attackBox = None
        elif self.attackFrame < 28: 
            self.image = self.midHatImage
        elif self.attackFrame == 28:
            self.wizard = not self.wizard
            self.image = self.midHatImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 109:
            self.image = self.punchImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 9:
            self.image = self.preHatImage
        elif self.attackFrame == 9:
            self.wizard = not self.wizard
        elif self.attackFrame < 16:
            self.image = self.idleImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            Player.bzzzSound.play()
            Player.growSound.play()
            self.invincible=True
        elif self.attackFrame==10:
            self.invincible=False
        if self.attackFrame < 96:
            self.image = random.choice([self.haloImage,self.halo2Image,self.wizardImage])
            self.xv=(self.facingRight-0.5)*8
            self.yv-=1
            self.yv*=0.95
            self.attackBox = [9,8,9+13,8+21, 5,20,6]
        elif self.attackFrame < 106:
            self.invincible=False
            self.attackBox = None
            self.yv-=1
            self.image = self.wizardImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    ninjaImage = Player.load("penguin", "ninja.png")
    stunnedNinjaImage = Player.load("penguin", "stunnedninja.png")
    prePunchImage = Player.load("penguin", "prepunch.png")
    punchImage = Player.load("penguin", "punch.png")
    projaImage = Player.load("penguin", "star.png")
    projbImage = Player.load("penguin", "hat.png")
    preHatImage = Player.load("penguin", "prehat.png")
    midHatImage = Player.load("penguin", "midhat.png")
    wizardImage = Player.load("penguin", "wizard.png")
    stunnedWizardImage = Player.load("penguin", "stunnedwizard.png")
    preMagicImage = Player.load("penguin", "premagic.png")
    midMagicImage = Player.load("penguin", "midmagic.png")
    magicImage = Player.load("penguin", "magic.png")
    haloImage = Player.load("penguin", "halo.png")
    halo2Image = Player.load("penguin", "halo2.png")
    text = "Is a wizard sometimes."

    idleImage = ninjaImage #selesctscreen

allClasses = [
Puncher, Big, Green, Tree, Sad, Bird, Robot, Lizard, Golem, Alien, Can, Frog, Monster, Penguin,
Puncher, Big, Green, Tree, Sad, Bird, Robot, Lizard, Golem, Alien, Monster, Penguin,
]

def restart():
    Player.players = []
    choices = []
    num = 0
    myfont = pygame.font.SysFont('Times New', 100)
    myfont2 = pygame.font.SysFont('Times New Roman', 20)
    while State.jump_out == False:
        #pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                State.jump_out = True

        lag=0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            num-=1
            lag+=0.1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            num+=1
            lag+=0.1
        if pressed[pygame.K_r]:
            choices.append(random.choice(allClasses))
            num=0
            if len(choices)==State.playerCount:
                return choices
            lag+=0.5
        if pressed[pygame.K_SPACE] or pressed[pygame.K_RETURN]:
            choices.append(allClasses[num%len(allClasses)])
            num=0
            if len(choices)==State.playerCount:
                return choices
            lag+=0.5

        #draw
        gameDisplay.fill((100,100,100))
        pygame.draw.rect(gameDisplay,(200,200,200),(400+64,0,16*8,200+28*8),0)
        for i in range(len(choices)):
            gameDisplay.blit(choices[i].idleImage[1], (100*i, 0))
        for i in [-2,-1,0,1,2]:
            gameDisplay.blit(allClasses[(num-i)%len(allClasses)].idleImage[1], (400-100*i, 200))
        
        name = allClasses[num%len(allClasses)].__name__
        text = allClasses[num%len(allClasses)].text
        textsurface = myfont.render(name, True, (0, 0, 0))
        textsurface2 = myfont2.render(text, True, (0, 0, 0))
        gameDisplay.blit(textsurface,(545-len(name)*24,450))
        gameDisplay.blit(textsurface2,(10,570))

        pygame.display.update()
        clock.tick(100)
        time.sleep(lag)
    
    pygame.quit()
    quit()

gameDisplay = pygame.display.set_mode((1000, 600))
backgrounds = []
for name in ["background.png","background2.png"]:
    background = pygame.image.load(os.path.join(filepath, "textures", name))
    background = pygame.transform.scale(background, (1000, 600))
    backgrounds.append(background)
pygame.display.set_caption("Fighting Game")
pygame.display.set_icon(pygame.image.load(os.path.join(filepath, "textures", "puncher", "idle.png")))
Platform.generate()

initSound()

pygame.joystick.init()
stickNum = pygame.joystick.get_count()
sticks=[]
for i in range(stickNum):
    sticks.append(pygame.joystick.Joystick(i))
    sticks[-1].init()

State.playerCount = 2 # HERE * * * * * * * * *
State.frameRate = 75
State.jump_out = False
while State.jump_out == False:
    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            State.jump_out = True
    if len(Player.players)<2:
        choices = restart()

        # HERE * * * * * * * * *
        choices[0](200, 300, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_s})
        #choices[1](600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
        #choices[1](400, 300, False, {"w":0,"3":4,"4":5,"5":1}, sticks[0])
        
        AiFocus = True
        for i in range(1):
            #random.choice(allClasses)(600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
            choices[-i+1](600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_u,"2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_DOWN})
            Player.players[-1].random=1
        # HERE * * * * * * * * *

        currentBackground = random.choice(backgrounds)
        Platform.restart()
        pygame.display.update()
    
    #shake
    if Player.shake:
        Player.shake-=1
        shakeX = (random.random()-0.5)*Player.shake
        shakeY = (random.random()-0.5)*Player.shake
    else:
        shakeX = 0
        shakeY = 0
    #background
    gameDisplay.blit(currentBackground, (0+shakeX,0+shakeY))

    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.getPressed(pressed)
        player.action()
    for player in Player.players+Projectile.projectiles:
        player.physics()

    #draw
    for player in Player.players+Projectile.projectiles+Platform.platforms:
        player.draw()
        
    pygame.display.update()
    clock.tick(State.frameRate)
    if Player.hitLag:
        time.sleep(Player.hitLag)
        Player.hitLag=0
    
pygame.quit()
quit()


"""
#ella gjorde frog så ru vet!!!!/ella





"""
