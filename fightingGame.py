import pygame
import time
import random
import os
clock = pygame.time.Clock()
filepath="fightingGameFiles"
#Adam "jag tycker ändå det kan funka med ett cirkelargument."
SOUND_PATH = os.path.join(filepath, "sounds")
DEBUG_MODE = 0

skinChance = 0.3

def initSound():
    State.volume = 0.2 #damage can only be heard up to 100*volume
    v=State.volume
    pygame.font.init() # you have to call this at the start, 
                           # if you want to use this module.
    pygame.mixer.init(buffer=32)
    Player.hitSounds = [pygame.mixer.Sound(os.path.join(SOUND_PATH, "soundeffect2.wav")),
        pygame.mixer.Sound(os.path.join(SOUND_PATH, "weaksoundeffect2.wav"))]
    Player.lickSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "lickeffect.wav"))
    Player.lickSound.set_volume(v*0.3)
    Player.growSound = pygame.mixer.Sound(os.path.join(SOUND_PATH,"grasseffect.wav"))
    Player.growSound.set_volume(v*0.4)
    Player.ultSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "ult.wav"))
    Player.ultSound.set_volume(v*0.1)
    Player.bzzzSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bzzzEffect.wav"))
    Player.bzzzSound.set_volume(v*0.05)
    Player.killSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "smashbros.wav"))
    Player.killSound.set_volume(v*0.5)
    Player.gameSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "game.wav"))
    Player.gameSound.set_volume(v*0.5)
    
    pygame.mixer.music.load(os.path.join(filepath, "music.wav")) #must be wav 16bit and stuff?
    pygame.mixer.music.set_volume(v*0.1)
    pygame.mixer.music.play(-1)

def playHitSound(vol):
    i = random.randint(0,1)
    sound = Player.hitSounds[i]
    sound.set_volume(vol*(i+1))
    sound.play()

def endEffect():
    pygame.draw.rect(gameDisplay, (200, 0, 100), (0,0,1000,600), 0)
    Player.freezeTime=1
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
                players+=1
        elif isinstance(player, Pillar):
            pass
        else:
            players+=1
    return players

def pickCharacter(num, b):
    if b:
        if allClasses[num%len(allClasses)] == Bird:
            return Darkbird
        if allClasses[num%len(allClasses)] == Puncher:
            return Darkpuncher
    return allClasses[num%len(allClasses)]

class State():
    idle=0
    stunned=-1

class Platform():
    
    def generate():
        Platform.platformLayouts = [
        #[Platform([360, 330, 640, 355])],
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
        if isinstance(self.owner, Green) and random.random()<0.5:
            self.image = self.owner.projaImage
        self.x = owner.x
        self.y = owner.y
        self.op = op
        self.hitboxes = [1,2,3,4]
        self.facingRight = owner.facingRight
        self.yv=0
        self.xv=0
        if isinstance(self.owner, Green):
            self.xv = (self.facingRight-0.5) * (12+8*self.op)
            self.box = [32-11, 18, 32-6, 32-9, 20+20*op,20+20*op,20+self.owner.attackFrame*op]
        if isinstance(self.owner, Robot):
            self.xv = (self.facingRight-0.5) * 20
            self.box = [32-8, 16, 32-4, 19, 12+3*self.op, 12]
        if isinstance(self.owner, Alien):
            self.xv = (self.facingRight-0.5) * -20
            self.box = [3, 14, 7, 17, 7,0,0]
            self.yv = .5
        if isinstance(self.owner, Glitch):
            self.xv = (self.facingRight-0.5) * 40
            self.box = [23, 19, 30, 23, 35]
            self.x -= self.xv * 2
        if isinstance(self.owner, Monster):
            self.xv = (self.facingRight-0.5) * 8
            self.yv = -0.7
            self.box = [21, 19, 26, 22, 15,-60,5]
        if isinstance(self.owner, Penguin):
            self.y-=10
            if self.op:
                self.xv = (self.facingRight-0.5) * 16
                self.box = [19, 20, 19+3, 20+3, 9]
                self.image = self.owner.projaImage
            else:
                self.xv = (self.facingRight-0.5) * 8
                self.yv = 0.4
                self.box = [18+1,18,18+6,18+5, 23]
        if isinstance(self.owner, Sad):
            self.box = [16-2,15,16+3,20, 50,10,50]
            self.x+=(self.owner.facingRight-0.5)*120
            self.xv=(self.owner.facingRight-0.5)*0
            self.lifetime = 0
        if isinstance(self.owner, Animals):
            self.box = [24,22,25,23, 5,15,10]
            self.y+=(self.owner.attackFrame%7)*6-16
            self.xv=(self.owner.facingRight-0.5) * 16
        if isinstance(self.owner, Frog):
            self.box = [18,20,21,22, 23]
            self.xv=(self.owner.facingRight-0.5) * 8
            self.x+=(self.owner.facingRight-0.5) * 64
        if isinstance(self.owner, Cat):
            self.box = [15,14,17,19, 3]
            self.xv=(self.owner.facingRight-0.5) * 32
            self.y+=16
            self.x+=(self.owner.facingRight-0.5) * 64
        self.xv+=self.owner.xv
        self.x+=self.owner.xv

    def keys(self):
        nevercalled
        pass
    def confirmedHit(self,damage):
        pass
        if not isinstance(self.owner, Alien) and not isinstance(self.owner, Animals):
            self.owner.confirmedHit(damage)
        elif isinstance(self.owner, Alien):
            self.owner.ultCharge+=2
    def draw(self):
        if hasattr(self, "image"):
            image = self.image
        else:
            image = self.owner.projbImage
        if self.op:
            gameDisplay.blit(image[self.facingRight], (int(self.x+random.randint(-1,1)*8+shakeX), int(self.y+random.randint(-1,1)*8+shakeY)))
        else:
            gameDisplay.blit(image[self.facingRight], (int(self.x+shakeX), int(self.y+shakeY)))
        
        if random.random()<0.9 and DEBUG_MODE:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
            if random.random()<0.5:
                pygame.draw.rect(gameDisplay, (0, 0, 255), \
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
        if len(data)>7:
            self.hitboxes.append(data[7])
        if self.hitboxes and not self.facingRight: # flip hitbox
            right = 32*8 - self.hitboxes[0] +2*self.x
            left = 32*8 - self.hitboxes[2] +2*self.x
            self.hitboxes[0] = left
            self.hitboxes[2] = right
        self.hurtboxes = self.hitboxes
        if self.hurtboxes[2]<100 or self.hurtboxes[0]>900:
            if self in Projectile.projectiles:
                Projectile.projectiles.remove(self)
        #death self by collision with hitboxes and such
        if isinstance(self.owner, Sad):
            if self.lifetime<20:
                self.lifetime+=1
                return
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
                    if self in Projectile.projectiles and not (isinstance(player, Player) and player.invincible):
                        Projectile.projectiles.remove(self)
                    if isinstance(player, Player):
                        player.confirmedHit(otherBox[4])
                        if (player.attack in ["lick","lick2"]):
                            player.hp=min(player.hp+30, player.maxhp)
                            Player.lickSound.play()
                            Player.growSound.play()
                    else: #is proj
                        if player in Projectile.projectiles:
                            Projectile.projectiles.remove(player)

class Player():
    freezeTime=0
    SCALE=8
    players=[]
    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        Player.players.append(self)
        self.loadImages(skin)
        self.image = self.idleImage
        self.CHARGE = 50
        self.flyingHeight=0
        self.onGround = True
        self.xspeed=2.5
        self.x = x
        self.xv = 0
        self.y = y
        self.yv = 0
        self.maxhp = 250
        self.ultCharge = 0
        self.ultError = 0
        self.stun = 0
        self.hitLag = 0
        self.invincible=False
        self.invisible=False
        self.state = State.idle
        self.attack = ""
        self.attackFrame = 0
        self.attackBox = None
        self.hitboxes = None
        self.hurtboxes = [1,2,3,4] #first frame
        self.facingRight = facingRight
        self.random = False
        self.controls = controls
        self.joystick = joystick
        self.pressed = {"a":False,"w":False,"d":False,"1":False,"2":False,"3":False,"4":False}
        self.doubleJump = True #-1 means w is released
        self.canDoubleJump = False

    def init2(self): #after subclass init
        #self.width = self.box[2] - self.box[0]
        #self.height = self.box[3] - self.box[1]
        #self.hurtboxes = self.generateBox(self.box)
        self.hp = self.maxhp
        pass
    def passive(self):
        pass
    def grounded(self):
        self.xv=self.xv*0.5
        self.onGround=True
        self.doubleJump=True
        pass #before yv=0
    def action(self):
        if self.hitLag>0:
            return
        self.attackFrame+=1
        if self.ultError:
            self.ultError-=1
        self.passive()
        if self.state == State.stunned:
            self.stunned()
        elif self.state == State.idle:
            self.keys()
        if self.state == 1:
            self.doAttack(pressed)

        self.flipHitbox()

    def flipHitbox(self):
        if self.attackBox and not self.facingRight:
            right = 32 - self.attackBox[0]
            left = 32 - self.attackBox[2]
            self.attackBox[0] = left
            self.attackBox[2] = right

    def useUltCharge(self):
        if (self.ultCharge>=self.CHARGE):
            self.ultCharge = 0
            return True
        else:
            self.ultError = 16
            return False

    def executeAttack(self, frameData, key=False):
        for part in frameData: # [lastframe, image, hitbox?, skippable] 
            if self.attackFrame <= part[0]:
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
        self.ultCharge+=0.1 #?

    def getPressed(self, pressed):
        if self.random:
            if AiFocus:
                target = Player.players[0]
            else:
                enemies = Player.players[:]
                #enemies.remove(self)
                target = random.choice(enemies)
            if random.random()<0.1:
                self.pressed["d"] = random.randint(0,1)
            if random.randint(0,20)==0:
                self.pressed["w"] = (target.y < self.y) ^ (random.random()<0.5)
            if not self.onGround:
                self.pressed["w"] = random.randint(0,1)

            attacking=False
            for i in ["1","2","3","4"]:
                #self.pressed[i] = (random.randint(0,15+10*int(i))==0) ^ (self.state!=State.idle)
                if random.random()<0.02:
                    self.pressed[i] = (random.randint(0,3)==0)
                if self.pressed[i]:
                    self.pressed["d"] = target.x > self.x
                    if isinstance(self, Alien) and (self.pressed["3"] or self.pressed["4"]):
                        self.pressed["d"] = target.x < self.x
                    if (isinstance(self, Lizard) or isinstance(self, Penguin)) and self.pressed["4"]:
                        self.pressed["d"] = target.x < self.x
                        #self.pressed["w"] = True

            self.pressed["a"] = not self.pressed["d"]

        elif self.joystick:
            x = self.joystick.get_axis(0)
            triggers = self.joystick.get_axis(2) #lt - rt but 0 = -3.01
            self.pressed["d"] = (x>0.5)
            self.pressed["a"] = (x<-0.5)
            self.pressed["2"] = self.joystick.get_button(3) #(triggers<-0.5 and triggers>-2)
            self.pressed["1"] = self.joystick.get_button(2) #(triggers>0.5)
            for i in ["w","3","4"]:
                self.pressed[i] = (self.joystick.get_button(self.controls[i]))
            self.pressed["3"] += (triggers>0.5)
            self.pressed["4"] += (triggers<-0.5 and triggers>-2)
        else:
            for i in ["a","d","w","1","2","3","4"]:
                self.pressed[i] = (pressed[self.controls[i]])

    def keys(self):
        if(self.pressed["d"]):
            if self.onGround:
                self.xv+=self.xspeed*1.2
                #self.xv=self.xspeed*2
            else:
                self.xv=max(min(self.xspeed*2, self.xv+0.2), self.xv)
            self.facingRight = True
        elif(self.pressed["a"]):
            if self.onGround:
                #self.xv=-self.xspeed*2
                self.xv-=self.xspeed*1.2
            else:
                self.xv=min(max(-self.xspeed*2, self.xv-0.2), self.xv)
            self.facingRight = False

        if(self.pressed["w"]):
            if (self.onGround and not (isinstance(self, Ninja) and self.stance!=0)):
                self.yv=-17.1
            if self.doubleJump==-1 and self.canDoubleJump:
                self.yv=-13.6
                self.doubleJump=0
                theImage = Player.hurtImage2[not self.facingRight]
                gameDisplay.blit(theImage, (int(self.x), int(self.y)+40))
        
        self.ultCharge+=0.1
        #print(Player.players.index(self),":",self.ultCharge,"%")

    def physics(self):
        if self.hitLag>0:
            self.hitLag-=1
            return

        self.onGround = False

        #gravity
        self.yv+=0.75
        self.yv*=0.97

        #move
        self.x+=self.xv
        self.y+=self.yv

        #boxes
        self.hurtboxes = self.generateBox(self.box)
        #self.hurtboxes[3]+=self.flyingHeight
        self.hurtboxes[0]+=8
        self.hurtboxes[2]-=8

        #collide
        Xfixes = []
        Yfixes = []
        for player in Player.players+Platform.platforms:
            otherbox=player.hurtboxes[:]
            #otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                Xfixes.append(otherbox[2]-self.hurtboxes[0])
                Xfixes.append(otherbox[0]-self.hurtboxes[2])
                Yfixes.append(otherbox[3]-self.hurtboxes[1])
                Yfixes.append(otherbox[1]-self.hurtboxes[3])
        if Xfixes:
            Xfix = min(Xfixes, key=abs)
            Yfix = min(Yfixes, key=abs)
            if abs(Xfix)<abs(Yfix):
                self.x+=Xfix
                if self.xv*Xfix < 0:
                    self.xv = 0
            else:
                #print(self.yv, self.y ,Yfix)
                self.y+=Yfix
                if self.yv*Yfix < 0:
                    self.yv=0
                if Yfix<0:
                    self.grounded()

        #bounds
        if self.hurtboxes[2]>904:
            self.x += 904-self.hurtboxes[2]
            if self.stun and not isinstance(self,Golem): #bouncy walls
                self.xv=-self.xv*0.5
                self.yv=-abs(self.yv)
            else:
                self.xv=0
        if self.hurtboxes[0]<96:
            self.x += 96-self.hurtboxes[0]
            if self.stun and not isinstance(self,Golem):
                self.xv=-self.xv*0.5
                self.yv=-abs(self.yv)
            else:
                self.xv=0
        if self.hurtboxes[3]+self.flyingHeight>504:
            self.y += 504-self.flyingHeight-self.hurtboxes[3]
            self.yv=0
            self.grounded()

        #jump shit
        if not self.onGround and self.doubleJump==1 and not self.pressed["w"]:
            self.doubleJump = -1 #ready

        #attack
        self.hurtboxes = self.generateBox(self.box)
        if self.attackBox:
            self.hitboxes = self.generateBox(self.attackBox)
        else:
            self.hitboxes = None

        #hit
        if (not self.stun or self.stun>16 and self.attackFrame>10) and not self.invincible:
            for player in Player.players+Projectile.projectiles:
                if player.hitboxes and not player == self and not (isinstance(player, Projectile) and isinstance(player.owner, Sad) and player.lifetime<20):
                    enemybox = player.hitboxes # for ninja extended hurtbox
                    if isinstance(self, Ninja) and self.stance==1:
                        enemybox[3]+=2*Player.SCALE
                    if self.collide(enemybox):
                        if(len(player.hitboxes)==8):
                            self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5],stun=player.hitboxes[6],angle=player.hitboxes[7])
                        elif(len(player.hitboxes)==7):
                            self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5],stun=player.hitboxes[6])
                        elif(len(player.hitboxes)==6):
                            self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5]) # player/player.owner for ult charge. bad for pos
                        else:
                            self.hurt(player, player.hitboxes[4])# .owner for ult charge. bad for pos
                        if isinstance(player, Projectile):
                            Projectile.projectiles.remove(player)

    def hurt(self, player, damage, knockback=None, stun=None, angle = 0): #  angle: [-1 to 1]
        if(self.invincible):
            #print("shouldnt be called by physics() then?")
            return
        player.confirmedHit(damage)
        playHitSound(State.volume*damage*0.01)
        if(knockback==None):
            knockback=damage
        if stun==None:
            stun=knockback
        self.facingRight = player.x>self.x #not player.facingRight

        self.hp -= damage
        self.hitLag = max(self.hitLag, int(damage*0.2))
        if hasattr(player, "hitLag"):
            player.hitLag = max(player.hitLag, int(damage*0.2))
        #Player.freezeTime = damage*0.003
        if stun:
            self.state = State.stunned
            self.image = self.stunnedImage
            if self.hp<=0:
                if not (isinstance(self,Tree) and not self.isLastTree()):
                    endEffect()
        elif self.hp<=0:
            endEffect()
            Player.players.remove(self)
        self.stun = max(self.stun-self.attackFrame, abs(stun))
        if self.stun:
            self.attackFrame = 0
        if knockback:
            if isinstance(self, Glitch):
                self.yv=-abs(knockback)*(0.2+angle*0.2)
                self.x+=16*knockback*(self.facingRight-0.5)*(-0.2+angle*0.2)
                self.xv=0
                self.image = self.preGlitchImage
            else:
                self.yv=-abs(knockback)*(0.2+angle*0.2)
                self.xv=knockback*(self.facingRight-0.5)*(-0.2+angle*0.2)
        #effects
        Player.shake=max(Player.shake, int(damage))
        if damage>10+random.random()*40:
            theImage = Player.hurtImage[self.facingRight]
            gameDisplay.blit(theImage, (int(self.x)+self.facingRight*20, int(self.y)))
        if damage>10+random.random()*30:
            theImage = Player.hurtImage2[self.facingRight]
            gameDisplay.blit(theImage, (int(self.x)+self.facingRight*20, int(self.y)))
        
    def confirmedHit(self,damage):
        pass
    def generateBox(self, data):
        new = [self.x+data[0]*Player.SCALE, self.y+data[1]*Player.SCALE, self.x+data[2]*Player.SCALE, self.y+data[3]*Player.SCALE]
        if len(data)>4:
            new.append(data[4])
        if len(data)>5:
            new.append(data[5])
        if len(data)>6:
            new.append(data[6])
        if len(data)>7:
            new.append(data[7])
        return new

    def collide(self, otherBox):
        glitchConstant=0 #replicatable glitch with constant 1 and >= and can
        if self.hurtboxes[2]>otherBox[0]+glitchConstant and self.hurtboxes[0]<otherBox[2]-glitchConstant:
            if self.hurtboxes[3]>otherBox[1]+glitchConstant and self.hurtboxes[1]<otherBox[3]-glitchConstant:
                return True
        return False

    def load(playerName, textureName, skin=0):
        image = pygame.image.load(os.path.join(filepath, "textures", playerName, textureName))
        
        if skin:
            for i in range(32):
                for j in range(32):
                    color = image.get_at((i,j))
                    if not color == (0,0,0,0):
                        if skin<3:
                            color=pygame.Color(color[(0+skin)%3],color[(1+skin)%3],color[(2+skin)%3],color[3])
                            image.set_at((i,j),color)
                        else:
                            color=pygame.Color(color[(2+skin)%3],color[(1+skin)%3],color[(0+skin)%3],color[3])
                            image.set_at((i,j),color)
        
        image = pygame.transform.scale(image, (Player.SCALE*32, Player.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        factor = 0.3
        leftEdge=int((self.hurtboxes[0]+self.hurtboxes[2]-self.maxhp*factor)*0.5+shakeX)
        if not self.invisible and self.ultCharge>1:
            if self.ultCharge>=self.CHARGE:
                color = (255,255-255/16*self.ultError,255-255/16*self.ultError)
            elif self.ultError:
                color = (127+128/16*self.ultError,255-255/16*self.ultError,255-255/16*self.ultError)
            else:
                color = (127,255,255)
            wdt = int(min((self.maxhp*factor+8),((self.maxhp*factor+8)*self.ultCharge)//self.CHARGE))
            pygame.draw.rect(gameDisplay, color, (leftEdge-4,int(self.hurtboxes[1]-32-4+shakeY),wdt, 16), 0)
        if self.hp>0 and not self.invisible: #health bars
            pygame.draw.rect(gameDisplay, (255, 0, 0), (leftEdge,int(self.hurtboxes[1]-32+1+shakeY),int(self.maxhp*factor),6), 0)
            pygame.draw.rect(gameDisplay, (0, 255, 0), (leftEdge,int(self.hurtboxes[1]-32+shakeY),int(self.hp*factor),8), 0)

        if not self.invisible: #character
            image = self.image[self.facingRight]
            gameDisplay.blit(image, (int(self.x+shakeX), int(self.y+shakeY)))
        
        if random.random()<0.9 and DEBUG_MODE: #yellow
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
            if random.random()<0.5: # blue
                pygame.draw.rect(gameDisplay, (255*self.invincible, 0, 255), \
                (self.hurtboxes[0]+shakeX,self.hurtboxes[1]+shakeY,self.hurtboxes[2]-self.hurtboxes[0],self.hurtboxes[3]-self.hurtboxes[1]), 0)
        
    hurtImage = pygame.image.load(os.path.join(filepath, "textures", "effect.png"))
    hurtImage = pygame.transform.scale(hurtImage, (8*32, 8*32))
    hurtImage = (pygame.transform.flip(hurtImage, True, False), hurtImage)
    hurtImage2 = pygame.image.load(os.path.join(filepath, "textures", "effect2.png"))
    hurtImage2 = pygame.transform.scale(hurtImage2, (8*32, 8*32))
    hurtImage2 = (pygame.transform.flip(hurtImage2, True, False), hurtImage2)
    text = ""
    shake = 0

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Puncher, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()
        self.canDoubleJump = True
        self.xspeed = 3

        self.first = [
        [3, self.prePunchImage, None, True],
        [6, self.midPunchImage, None, True],
        [9, self.postPunchImage, [32-10-6, 19, 32-10, 23, 19]],
        [18, self.postPunchImage],
        [25, self.midPunchImage],
        ]

        self.second = [
        [10, self.prePunchImage],
        [16, self.midPunchImage],
        [20, self.punchImage, [32-9-7, 18, 32-9, 24, 49]],
        [24, self.punchImage],
        [34, self.postPunchImage],
        [40, self.midPunchImage],
        [50, self.prePunchImage],
        ]

        self.long = [
        [19, self.prePunchImage],
        [90, self.prePunchImage, None, True],
        [95, self.midPunchImage],
        #[100, self.midPunchImage],
        [100, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 45,50,55]],
        [103, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 45,50,55]],
        [130, self.longPunchImage],
        [138, self.postPunchImage],
        [146, self.midPunchImage],
        [155, self.prePunchImage],
        ]

        self.extreme = [
        [36, self.prePunchImage],
        [162, self.prePunchImage, None, True],
        [167, self.midPunchImage],
        [170, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 80, 100]],
        [180, self.punchImage],
        [205, self.postPunchImage],
        [215, self.midPunchImage],
        [225, self.prePunchImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "extreme"
        
        elif(self.pressed["4"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"
            else:
                self.state = State.idle

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
        elif self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
            if self.attackFrame==10:
                if self.pressed["2"]:
                    self.attack = "longpunch"
                else:
                    self.xv+=(self.facingRight-0.5)*8
                    self.yv-=2
        elif self.attack == "longpunch":
            self.executeAttack(self.long, not self.pressed["2"])
        elif self.attack == "extreme":
            self.executeAttack(self.extreme, not self.pressed["3"])
            if not self.pressed["3"] and self.attackFrame<4:
                self.xv*=-1
                self.yv*=-1
                self.state = State.idle
                self.image = self.cursedImage
                self.attackBox = None
        elif self.attack == "ult":
            if self.attackFrame == 1:
                Player.ultSound.play()

            a=self.attackFrame

            if a<200:
                if a%7==0:
                    self.xv += (self.facingRight-0.5)*0.5
                    self.yv = -2
                if a%7<=3:
                    self.image = self.postPunchImage
                    self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 3,9,7]
                else:
                    self.image = self.prePunchImage
                    self.attackBox = None

                if not self.pressed["4"] and self.attackFrame>25:
                    self.attackFrame = 200

            elif self.attackFrame < 208:
                self.image = self.punchImage
                self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 3,9,70]
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            elif self.attackFrame < 215:
                self.image = self.postPunchImage
                self.attackBox = None
            elif self.attackFrame < 225:
                self.image = self.midPunchImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("puncher", "idle.png", skin=skinChoice)
        self.cursedImage = Player.load("puncher", "cursed.png", skin=skinChoice)
        self.stunnedImage = Player.load("puncher", "stunned.png", skin=skinChoice)
        self.longPunchImage = Player.load("puncher", "longpunch.png", skin=skinChoice)
        self.prePunchImage = Player.load("puncher", "prepunch.png", skin=skinChoice)
        self.midPunchImage = Player.load("puncher", "midpunch.png", skin=skinChoice)
        self.punchImage = Player.load("puncher", "punch.png", skin=skinChoice)
        self.postPunchImage = Player.load("puncher", "postpunch.png", skin=skinChoice)

    cssImages = [Player.load("puncher", "idle.png", skin=i) for i in range(6)]
    text = "They said no human could ever compete in the arena. They? proved them wrong"
    text = "The only humans strong enough to compete in the arena"
    helpTexts =[
    "Pro tips:",
    "Can double jump.",
    "Press Down for SUPER",
    "Hold Attack2 for a very long punch.",
    "Press Attack3 very short to reverse in the air!",
    "(Forbidden technique! Will curse you!)",
    "Use the insanely strong punch after SUPER.",
    ] #B
class Darkpuncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.init2()
        self.canDoubleJump = False
        self.xspeed = 2

        self.first = [
        [5, self.prePunchImage, None, True],
        [10, self.midPunchImage],
        [15, self.punchImage, [32-10-6, 19, 32-10, 23, 25]],
        [23, self.punchImage],
        [31, self.midPunchImage],
        ]

        self.second = [
        [8, self.prePunchImage],
        [14, self.midPunchImage],
        [18, self.punchImage, [32-9-7, 18, 32-9, 24, 35,35,35,-0.5]],
        [22, self.punchImage],
        [30, self.punchImage],
        [35, self.midPunchImage],
        [40, self.prePunchImage],
        ]

        self.long = [
        [15, self.prePunchImage],
        [60, self.prePunchImage, None, True],
        [65, self.midPunchImage],
        #[100, self.midPunchImage],
        [70, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 5,40,5,-0.8]],
        [75, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 30,40,40,0.5]],
        [85, self.longPunchImage],
        [90, self.punchImage],
        [95, self.midPunchImage],
        [100, self.prePunchImage],
        ]

        self.extreme = [
        [25, self.prePunchImage],
        [60, self.prePunchImage, None, True],
        [65, self.midPunchImage],
        [70, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 60,60,60,-0.5]],
        [77, self.punchImage],
        [83, self.midPunchImage],
        [90, self.prePunchImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "longpunch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "extreme"
        
        elif(self.pressed["4"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"
            else:
                self.state = State.idle

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==10:
                if self.pressed["1"]:
                    self.attack = "punch"
        elif self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        elif self.attack == "longpunch":
            self.executeAttack(self.long, not self.pressed["2"])
        elif self.attack == "extreme":
            self.executeAttack(self.extreme, not self.pressed["3"])
            if self.attackFrame<100:
                self.xv=0
                self.yv=0
        elif self.attack == "ult":
            if self.attackFrame == 1:
                Player.ultSound.play()

            a=self.attackFrame

            if a<100:
                if a%10==0:
                    self.xv = (self.facingRight-0.5)*2
                    self.yv = -2
                if a%10<=3:
                    self.image = self.punchImage
                    self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 5,10,10]
                else:
                    self.image = self.prePunchImage
                    self.attackBox = None

                if not self.pressed["4"] and self.attackFrame>20:
                    self.attackFrame = 100

            elif self.attackFrame < 110:
                self.image = self.punchImage
                self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 30,60,60,-0.5]
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            elif self.attackFrame < 115:
                self.image = self.punchImage
                self.attackBox = None
            elif self.attackFrame < 130:
                self.image = self.midPunchImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("darkpuncher", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("darkpuncher", "stunned.png", skin=skinChoice)
        self.longPunchImage = Player.load("darkpuncher", "longpunch.png", skin=skinChoice)
        self.prePunchImage = Player.load("darkpuncher", "prepunch.png", skin=skinChoice)
        self.midPunchImage = Player.load("darkpuncher", "midpunch.png", skin=skinChoice)
        self.punchImage = Player.load("darkpuncher", "punch.png", skin=skinChoice)

    cssImages = [Player.load("darkpuncher", "idle.png", skin=i) for i in range(6)]
    text = "Wretched beings of uncertain origin."
class Big(Player):
    
    def grounded(self):
        Player.shake+=int(self.yv)
        super().grounded()
    
    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Big, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-4, 12, 16+4, 32-4]
        self.xspeed=2
        self.hp=300
        self.init2()


        self.first = [
        [3, self.prePunchImage, [10, 17, 11, 32-9, 20]],
        [12, self.prePunchImage],
        [15, self.midPunchImage],
        [25, self.punchImage, [16, 16, 32-6, 32-8, 40,50,40,-0.2]],
        [35, self.punchImage],
        [42, self.midPunchImage],
        [50, self.prePunchImage],
        ]

        self.second = [
        [4, self.prePunchImage, [10, 17, 11, 32-9, 30]],
        [30, self.prePunchImage],
        [130, self.prePunchImage, None, True],
        [140, self.midPunchImage],
        [150, self.punchImage, [16, 16, 32-6, 32-8, 80,100,80,-0.5]],
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
        [14, self.stunnedImage],
        [16, self.idleImage],
        [25, self.skullImage, [15, 10, 23, 12, 50]],
        [35, self.skullImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "horns"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "spin"
        
        elif(self.pressed["4"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"
            else:
                self.state = State.idle

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame == 10 and self.pressed["1"]:
                self.attack = "punch"
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["1"])
        if self.attack == "horns":
            self.executeAttack(self.skull, not self.pressed["2"])
        elif self.attack == "spin":
            if self.attackFrame < 20:
                self.image = self.prePunchImage
                self.attackBox = None
                if self.attackFrame%5==0:
                    self.facingRight = not self.facingRight

            elif self.attackFrame < 150:
                self.yv-=0.7
                self.image = self.punchImage
                self.attackBox = [16, 16, 32-6, 32-8, 18]
                if self.attackFrame%10==0:
                    self.facingRight = not self.facingRight
                if not self.pressed["3"] and self.attackFrame>35:
                    self.attackFrame = 150

            elif self.attackFrame < 170:
                self.image = self.midPunchImage
                self.attackBox = None
                if self.attackFrame%7==0:
                    self.facingRight = not self.facingRight
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        elif self.attack == "ult":
            if self.attackFrame == 1:
                if self.useUltCharge():
                    Player.ultSound.play()
                else:
                    return

            a=self.attackFrame

            if a%15==5 and a<60:
                self.xv = (self.facingRight-0.5)*6
                self.yv = -3

            if a%15<=5 and a<60:
                self.image = self.punchImage
                self.attackBox = [16, 16, 32-6, 32-8, 10, 14]

            elif a<60: #and a%20>8 btw
                self.image = self.prePunchImage
                self.attackBox = None

            elif self.attackFrame < 70:
                self.image = self.punchImage
                self.attackBox = [16, 16, 32-6, 32-8, 50, 90]
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("big", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("big", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("big", "prepunch.png", skin=skinChoice)
        self.midPunchImage = Player.load("big", "midpunch.png", skin=skinChoice)
        self.punchImage = Player.load("big", "punch.png", skin=skinChoice)
        self.skullImage = Player.load("big", "skull.png", skin=skinChoice)

    cssImages = [Player.load("big", "idle.png", skin=i) for i in range(6)]
    text = "Big!"
    helpTexts =[
    "Pro tips:",
    "Press Down for SUPER.",
    "You can elbow people.",
    "Hold the spinning attack to spin longer",
    "You can use the spinning attack to fly briefly.",
    ]
class Green(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Green, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-14, 16+3, 32-4]
        self.maxhp = 200
        self.xspeed = 2.5
        self.init2()
        self.canDoubleJump = True

        self.first = [
        [3, self.idleImage, None, True],
        [8, self.kickImage, [32-14, 32-6, 32-10, 32-3, 12]],
        [20, self.kickImage, None],
        [25, self.idleImage, None],
        ]

        self.second = [
        [15, self.stunnedImage, None],
        [20, self.skullImage, [32-9-5, 32-8-6, 32-9, 32-9, 40]],
        [40, self.skullImage, None],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "kick"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            if self.useUltCharge():
                self.attack = "ult"
            else:
                self.attack = "shoot"
        
        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "heal"

    def doAttack(self, pressed):
        if self.attack == "kick":
            self.executeAttack(self.first, not self.pressed["1"])
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "shoot":
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
        if self.attack == "heal":
            if self.attackFrame == 1:
                Player.growSound.play()
            if self.attackFrame < 90:
                self.image = self.magicImage
                self.attackBox = None
                if self.attackFrame%15==0:
                    self.facingRight = not self.facingRight
            else:
                self.hp = min(self.maxhp, self.hp+30)
                self.ultCharge += 10
                self.state = State.idle
                self.image = self.idleImage
        if self.attack == "ult":
            if self.attackFrame < 10:
                self.image = self.stunnedImage
                self.attackBox = None
            elif self.attackFrame < 15:
                self.image = self.skullImage
            elif self.attackFrame == 33 or self.attackFrame==15:
                self.image = self.skullImage
                Projectile.projectiles.append(Projectile(self, op=True))
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            elif self.attackFrame < 33:
                self.image = self.stunnedImage
            elif self.attackFrame < 50:
                self.image = self.skullImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("green", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("green", "stunned.png", skin=skinChoice)
        self.kickImage = Player.load("green", "kick.png", skin=skinChoice)
        self.skullImage = Player.load("green", "skull.png", skin=skinChoice)
        self.projaImage = Player.load("green", "proja.png", skin=skinChoice)
        self.projbImage = Player.load("green", "projb.png", skin=skinChoice)
        self.magicImage = Player.load("green", "magic.png", skin=skinChoice)

    cssImages = [Player.load("green", "idle.png", skin=i) for i in range(6)]
    text = "Wormlike magical creatures without arms"
    helpTexts =[
    "Pro tips:",
    "Press Down to heal and charge SUPER",
    "Can double jump.",
    "Jump forward/backwards while shooting",
    "to change the speed of projectiles.",
    ]
class Tree(Player):

    def passive(self):
        if random.randint(0,50)<1: #dont know if this is needed
            if countPlayers()<2:
                if self in Player.players:
                    Player.players.remove(self)

    def isLastTree(self):
        for player in Player.players:
            if player!=self and isinstance(player, Tree):
                if player.code == self.code:
                    return False
        return True

    def hurt(self, player, damage, knockback=None, stun=None, angle=0):
        self.box = [16-3, 32-15, 16+3, 32-4]
        super().hurt(player, damage, knockback, stun, angle)

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Tree, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-15, 16+3, 32-4]
        self.CHARGE = 25
        self.xspeed = 2
        self.code = random.random()
        self.init2()

        self.skin = skin

        self.first = [
        [8, self.preKickImage],
        [16, self.kickImage, [16, 20, 32-9, 32-7, 22]],
        [20, self.kickImage],
        [26, self.preKickImage],
        ]

        self.second = [
        [15, self.preKickImage],
        [18, self.kickImage, [16,20,32-9,32-7, 45,45,45,-0.2]],
        [25, self.kickImage, [16,20,32-9,32-7, 35]],
        [40, self.kickImage],
        [50, self.preKickImage],
        ]

        self.down = [
        [17, self.preKickImage],
        [26, self.downImage, [14,24,18,30, 35,20,30,-2]],
        [34, self.downImage],
        [44, self.preKickImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "kick"

        elif(self.pressed["3"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"
            else:
                self.state = State.idle

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            if self.y == 280:
                self.attack = "grow"
            else:
                self.attack = "down"
        
    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["4"])
        if self.attack == "kick":
            self.executeAttack(self.second, not self.pressed["4"])
        if self.attack == "down":
            if self.attackFrame<15 and self.y == 280:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
            else:
                self.executeAttack(self.down, not self.pressed["4"])
        if self.attack == "grow":
            if self.attackFrame == 1:
                Player.growSound.play()

            if self.attackFrame < 10:
                self.image = self.preGrowImage
                self.box = [16-3, 32-12, 16+3, 32-4]
            elif self.attackFrame < 17:
                self.image = self.growImage
                self.box = [16-3, 32-8, 16+3, 32-4]
                self.invincible=True
            elif self.attackFrame==17:
                self.box = [16-3, 32-4, 16+3, 32-4]
                self.invisible=True
                if (self.pressed["d"]-self.pressed["a"])*(self.facingRight-0.5) > 0:
                    self.x += 250*(self.facingRight-0.5)
                    #Player.growSound.play()
                    self.facingRight = not self.facingRight
            elif self.attackFrame<27:
                pass
            elif self.attackFrame < 37:
                self.image = self.growImage
                self.invisible=False
                self.attackBox = [16-2, 32-8, 16+2, 32-4, 20,20,20,1]
            elif self.attackFrame < 47:
                self.attackBox = [16-2, 32-12, 16+2, 32-4, 20,20,20,1]
                self.box = [16-3, 32-8, 16+3, 32-4]
                self.invincible=False
                self.image = self.preGrowImage
            elif self.attackFrame < 57:
                self.box = [16-3, 32-12, 16+3, 32-4]
                self.attackBox = [16-2, 32-15, 16+2, 32-4, 20,40,20,0.2]
                self.image = self.idleImage
            elif self.attackFrame < 65:
                self.box = [16-3, 32-15, 16+3, 32-4]
            else:
                self.state = State.idle
                self.attackBox = None
        if self.attack == "ult":

            Player.growSound.play()
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

            new = Tree(self.x, self.y, self.facingRight, self.controls, self.joystick, self.skin)
            new.code = self.code

            new.hp = self.hp
            new.random = self.random
            new.state = 1
            new.attack = "grow"
            new.attackFrame = 20
            new.box = [16-3, 32-4, 16+3, 32-4]
            new.invisible=True
            new.CHARGE = 100
            new.hp=0
            new.x += 400*(self.facingRight-0.5)
            new.y = 700 #far down

            self.state = State.idle

    def loadImages(self, skinChoice):    
        self.idleImage = Player.load("tree", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("tree", "stunned.png", skin=skinChoice)
        self.preKickImage = Player.load("tree", "prekick.png", skin=skinChoice)
        self.kickImage = Player.load("tree", "kick.png", skin=skinChoice)
        self.growImage = Player.load("tree", "grow.png", skin=skinChoice)
        self.preGrowImage = Player.load("tree", "pregrow.png", skin=skinChoice)
        self.downImage = Player.load("tree", "down.png", skin=skinChoice)

    cssImages = [Player.load("tree", "idle.png", skin=i) for i in range(6)]
    text = "A subspecies of acer platanoides evolved as an r-strategist"
    helpTexts =[
    "Pro tips:",
    "You can move forward while using Down.",
    "In the air Down is a down attack.",
    "Summon clones yo! It's the SUPER.",
    ]
class Sad(Player):

    def grounded(self):
        self.onGround=True
        self.doubleJump=True

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Sad, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-17, 16+3, 32-6]
        self.flyingHeight=2*Player.SCALE
        self.init2()
        self.xspeed = 0

        self.punch = [
        [10, self.stunnedImage],
        [13, self.idleImage],
        [16, self.preSkullImage],
        [20, self.skullImage, [19, 15, 24, 22, 35]],
        [31, self.skullImage],
        [37, self.preSkullImage],
        ]

        self.jump = [
        [6, self.preJumpImage],
        [12, self.jumpImage, [10, 24, 15, 29, 16, 40]],
        [21, self.jumpImage],
        [29, self.preJumpImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "magic"

        elif(self.pressed["3"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jump"
        
    def doAttack(self, pressed):
        if self.attack == "punch":
            self.executeAttack(self.punch, not self.pressed["1"])
        if self.attack == "magic":
            #self.yv -= 0.5
            #self.yv *= 0.5

            self.ultCharge+=0.1
            if self.attackFrame%20<10:
                self.image = self.magic1Image
            else:
                self.image = self.magic2Image
            for i in Projectile.projectiles:
                i.xv+=(self.facingRight-0.5)*0.5
                i.xv*=0.99
            for i in Player.players:
                i.xv+=(self.facingRight-0.5)*0.5
                i.xv*=0.99
                i.hp-=0.2
            self.hp+=0.1
            if not self.pressed["2"]:
                self.state=State.idle
                self.image=self.idleImage
                self.attackBox=None
    
        if self.attack == "jump":
            self.executeAttack(self.jump, not self.pressed["4"])
            if self.attackFrame==12:
                self.yv=-11
                r=(self.facingRight-0.5)*2
                self.xv=max(self.xv*r,4)*r
    
        if self.attack == "ult":
            if self.attackFrame<10:
                self.image=self.stunnedImage
            elif self.attackFrame == 10:
                self.image = self.magic2Image
                Projectile.projectiles.append(Projectile(self, op=True))
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            elif self.attackFrame <20:
                self.image = self.magic1Image
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):    
        self.idleImage = Player.load("sad", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("sad", "stunned.png", skin=skinChoice)
        self.magic1Image = Player.load("sad", "magic1.png", skin=skinChoice)
        self.magic2Image = Player.load("sad", "magic2.png", skin=skinChoice)
        self.preSkullImage = Player.load("sad", "preskull.png", skin=skinChoice)
        self.skullImage = Player.load("sad", "skull.png", skin=skinChoice)
        self.preJumpImage = Player.load("sad", "prejump.png", skin=skinChoice)
        self.jumpImage = Player.load("sad", "jump.png", skin=skinChoice)
        self.projbImage = Player.load("sad", "somehorn.png", skin=skinChoice)
    
    cssImages = [Player.load("sad", "idle.png", skin=i) for i in range(6)]
    text = "Solemnity is the key to telekinesis"
    helpTexts =[
    "Pro tips:",
    "You cannot move and have no friction.",
    "Attack2 pushes everything and hurts everyone.",
    "Use Attack2 and Attack3 to move.",
    "SUPER summons a projectile that you can push.",
    ]
class Animals(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Animals, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-5, 19, 16+5, 32-4]
        self.init2()

        self.first = [
        [4, self.prePunchImage],
        [7, self.punchImage, [24,21,26,23, 12,12,12,0.5]],
        [11, self.punchImage],
        [16, self.prePunchImage],
        ]

        self.second = [
        #[8, self.prePunchImage],
        #[13, self.punchImage, [24,21,26,23, 9,0,9]],
        [16, self.punchImage],
        [23, self.punchImage, [24,21,26,23, 7,-40,10,0.8]],
        [32, self.postPunchImage, [22,14,24,16, 7,-30,20]],
        [37, self.prePunchImage],
        ]

        self.fourth = [
        [10, self.preKickImage],
        [15, self.kickImage, [15,28,19,32, 30]],
        [25, self.kickImage],
        [35, self.preKickImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "lick"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "fly"

        elif(self.pressed["3"]):
            if self.ultCharge>8:
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"
            else:
                self.ultError = 16
                self.state = State.idle

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "down"
    def doAttack(self, pressed):
        if self.attack == "lick":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==1:
                Player.lickSound.play()
            if self.attackFrame == 10 and self.pressed["1"]:
                self.attack = "lick2"
        elif self.attack == "lick2":
            self.executeAttack(self.second, not self.pressed["2"])
            if self.attackFrame==5:
                Player.lickSound.play()
        elif self.attack == "fly":
            if self.attackFrame<10:
                self.image=self.preFlyImage
            elif self.attackFrame<100:
                if self.attackFrame%10<5:
                    self.image = self.flyImage
                    self.attackBox=None
                else:
                    self.image = self.fly2Image
                    if self.attackFrame >90:
                        self.attackBox=[10,12,23,15, 7,37,7,0.5]
                    else:
                        self.attackBox=[10,12,23,15, 7,-17,7,0.5]

                if(self.pressed["d"]):
                    self.xv=min(self.xspeed*2, self.xv+0.1)
                    self.facingRight = True
                if(self.pressed["a"]):
                    self.xv=max(-self.xspeed*2, self.xv-0.1)
                    self.facingRight = False

                self.yv-=1
                self.yv=self.yv*0.95
                if not (self.pressed["2"]):
                    self.attackFrame=99
            elif self.attackFrame<110:
                self.image = self.preFlyImage
                self.yv=self.yv*0.95
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "down":
            if self.onGround and self.attackFrame>14 and self.attackFrame<20:
                self.yv=-13
            self.executeAttack(self.fourth, not self.pressed["4"])
        if self.attack == "ult":
            if self.attackFrame==1:
                self.ultCharge = min(self.ultCharge, self.CHARGE)
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            if self.attackFrame<12:
                self.ultCharge-=0.5
                self.image = self.preUltImage
            elif self.ultCharge>0 and self.attackFrame<999:
                self.image = self.ultImage
                if self.attackFrame%3==1:
                    Player.lickSound.stop()
                    Player.lickSound.play()
                    Projectile.projectiles.append(Projectile(self, op=True))
                self.ultCharge-=0.5
            elif self.attackFrame<999:
                self.ultCharge = 0
                self.attackFrame = 1000
            elif 1000<=self.attackFrame<1015:
                self.image = self.preUltImage
            else:
                self.ultCharge = 0
                self.state = State.idle
                self.image = self.idleImage

    def confirmedHit(self, damage):
        if self.attack=="down":
            self.yv=-13

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("animals", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("animals", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("animals", "prelick.png", skin=skinChoice)
        self.punchImage = Player.load("animals", "lick.png", skin=skinChoice)
        self.postPunchImage = Player.load("animals", "postlick.png", skin=skinChoice)
        self.preKickImage = Player.load("animals", "prekick.png", skin=skinChoice)
        self.kickImage = Player.load("animals", "kick.png", skin=skinChoice)
        self.preFlyImage = Player.load("animals", "prefly.png", skin=skinChoice)
        self.flyImage = Player.load("animals", "fly.png", skin=skinChoice)
        self.fly2Image = Player.load("animals", "fly2.png", skin=skinChoice)
        self.ultImage = Player.load("animals", "ult.png", skin=skinChoice)
        self.preUltImage = Player.load("animals", "preult.png", skin=skinChoice)
        self.projbImage = Player.load("animals", "projb.png", skin=skinChoice)
        self.projbImage = [self.projbImage[0].convert_alpha(),self.projbImage[1].convert_alpha()]
    
    cssImages = [Player.load("animals", "idle.png", skin=i) for i in range(6)]
    text = "The animal is bloody. The snake is fighting. The relationship is questionable."# (symbiosis or ?)
    helpTexts =[
    "Pro tips:",
    "Hold Attack1 to scoop people onto your back.",
    "Hold Attack2 to fly.",
    "You can use SUPER even if it is not fully charged.",
    "You can eat projectiles. Even your own.",
    ]
class Pufferfish(Player):

    def confirmedHit(self, damage):
        if self.attack=="slap":
            self.ultCharge+=30
        if self.attack in ["puff","puff2"]:
            self.hp=min(self.hp+damage//2, self.maxhp)

    def passive(self):
        if self.pressed["4"]:
            if self.ultCharge>self.CHARGE:
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                Player.ultSound.play()
                Pillar(self.x,-300,True,{"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_s})
                self.ultCharge = 0
            else:
                self.ultError = 16
        if self.image == self.longImage or self.image == self.longPunchImage:
            self.yv-=0.8
            self.yv*=0.95
        elif self.image in [self.preImage,self.prePunchImage,self.punchImage]:
            self.yv-=0.5
            self.yv*=0.97

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Pufferfish, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-4, 18, 16+4, 32-6] #16+-3 is actual box but it grows so...
        self.maxhp=200
        self.init2()

        self.first = [
        [14, self.prePunchImage],
        [19, self.punchImage, [16-6, 17, 16+6, 32-4, 22]],
        [23, self.prePunchImage], 
        [34, self.preImage],
        ]

        self.second = [
        [21, self.prePunchImage],
        [27, self.punchImage, [16-6, 17, 16+6, 32-4, 10,8]],
        [37, self.longPunchImage, [16-7, 16, 16+7, 32-3, 25]],
        [45, self.longPunchImage],
        [52, self.prePunchImage],
        [61, self.preImage],
        ]

        self.tail = [
        [30, self.magicImage],
        [300, self.magicImage, None, True],
        ]

        self.ball = [
        [5, self.preImage],
        [200, self.longImage, None, True],
        [205, self.preImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "puff"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "slap"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "fly"

    def doAttack(self, pressed):
        if self.attack == "puff":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==10 and self.pressed["1"]:
                self.attack = "puff2"
        if self.attack == "puff2":
            self.executeAttack(self.second, not self.pressed["1"])
        if self.attack == "slap":
            self.executeAttack(self.tail, not self.pressed["2"])
            self.xv+=(self.facingRight-0.5)*0.2
            if self.pressed["a"] and not self.pressed["d"] and self.facingRight:
                self.facingRight = False
                self.attackBox = [10, 19, 13, 25, 30]
                self.yv-=3
                self.yv*=0.9
            if self.pressed["d"] and not self.pressed["a"] and not self.facingRight:
                self.facingRight = True
                self.attackBox = [10, 19, 13, 25, 30]
                self.yv-=3
                self.yv*=0.9

        if self.attack == "fly":
            self.executeAttack(self.ball, not self.pressed["3"])
            self.ultCharge+=0.1
            if(self.pressed["d"]):
                self.xv=min(self.xspeed*2, self.xv+0.1)
                self.facingRight = True
            if(self.pressed["a"]):
                self.xv=max(-self.xspeed*2, self.xv-0.1)
                self.facingRight = False

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("pufferfish", "idle.png", skin=skinChoice)
        self.prePunchImage = Player.load("pufferfish", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("pufferfish", "punch.png", skin=skinChoice)
        self.longPunchImage = Player.load("pufferfish", "longpunch.png", skin=skinChoice)
        self.preImage = Player.load("pufferfish", "pre.png", skin=skinChoice)
        self.longImage = Player.load("pufferfish", "long.png", skin=skinChoice)
        self.magicImage = Player.load("pufferfish", "magic.png", skin=skinChoice)
        self.stunnedImage = Player.load("pufferfish", "stunned.png", skin=skinChoice)

    cssImages = [Player.load("pufferfish", "idle.png", skin=i) for i in range(6)]
    text = "Has a sharp and swift fin and can heal by sucking blood using its spikes. Can summon the spear of Helios."
    helpTexts =[
    "Pro tips:",
    "Hold Attack1 to spike more.",
    "Hold Attack2 while turning around to slap people!",
    "Hold Attack3 to fly.",
    "SUPER summons the spear yo!",
    ]
class Crawler(Player):
    
    def passive(self):
        if self.evil:
            self.idleImage = self.evilImage
            self.stunnedImage = self.evilStunnedImage
            self.xspeed = 3
            self.canDoubleJump = 0
        else:
            self.idleImage = self.normalImage
            self.stunnedImage = self.normalStunnedImage
            self.xspeed = 1.5
            self.canDoubleJump = 1
        if self.evil:
            if self.image == self.preImage:
                self.yv-=0.51
                self.yv*=0.97
                self.box = [11,14,20,26]
            elif self.image == self.longImage:
                self.yv-=0.79
                self.yv*=0.95
                self.box = [10,14,21,25]
            else:
                self.box = [12,15,20,27]
    def confirmedHit(self, damage):
        if self.attack=="sting" and not self.evil:
            self.xv=max(abs(self.xv), 3)*(self.facingRight*2-1)
            self.yv=-11.5
        if self.evil:
            self.hp=min(self.hp+damage//2, self.maxhp)
            #self.ultCharge+=10

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [12, 13, 20, 27]
        self.xspeed = 1.5
        self.maxhp = 200
        self.evil = 0
        self.init2()
        self.canDoubleJump = True

        self.sting = [
        [6, self.prePunchImage],
        [10, self.punchImage, [24, 12, 28, 16, 14, 50, 14]], #y goes down to 16 to hit bird
        [15, self.punchImage],
        [20, self.prePunchImage],
        ]

        self.glide = [
        [9, self.preKickImage],
        [16, self.kickImage, [17, 23, 17+9, 27, 15,60,15, 0.3]],
        [29, self.kickImage],
        [43, self.preKickImage],
        ]

        self.stab = [
        [3, self.preLickImage],
        [6, self.lickImage, [20, 17, 25, 21, 21]],
        [13, self.lickImage],
        [22, self.preLickImage],
        ]

        self.ball = [
        [11, self.preImage],
        [200, self.longImage, None, True],
        [211, self.preImage],
        ]

        self.spinner = [
        [2, self.preImage],
        [5, self.longImage],
        [45, self.longPunchImage, [7, 12, 24, 27, 10,7]],
        [55, self.longImage],
        [60, self.preImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            if not self.evil:
                self.attack = "sting"
            else:
                self.attack = "stab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            if not self.evil:
                self.attack = "kick"
            else:
                self.attack = "fly"

        elif(self.pressed["3"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                if self.evil:
                    self.attack = "ult"
                else:
                    self.attack = "fastevil"
            else:
                self.state = State.idle

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            if not self.evil:
                self.attack = "evil"
            else:
                self.attack = "normal"

    def doAttack(self, pressed):
        if self.attack == "sting":
            self.executeAttack(self.sting, not self.pressed["1"])
        if self.attack == "stab":
            self.executeAttack(self.stab, not self.pressed["1"])
        if self.attack == "kick":
            self.executeAttack(self.glide, not self.pressed["2"])
            if 9<self.attackFrame<19 and self.onGround: #jumpcancel slide
                self.xv=(self.facingRight-0.5)*10
            if 16<self.attackFrame<24:# and self.onGround:
                if self.pressed["w"] and (self.onGround or self.doubleJump==-1):
                    if not self.onGround:
                        self.doubleJump=0
                        theImage = Player.hurtImage2[not self.facingRight]
                        gameDisplay.blit(theImage, (int(self.x), int(self.y)+40))
                    self.yv=-13.1
                    self.state = State.idle
                    self.image = self.idleImage
                    self.attackBox = None
        if self.attack == "fly":
            self.executeAttack(self.ball, not self.pressed["2"])
            self.ultCharge+=0.1
            if(self.pressed["d"]):
                self.xv=min(self.xspeed*2, self.xv+0.1)
                self.facingRight = True
            if(self.pressed["a"]):
                self.xv=max(-self.xspeed*2, self.xv-0.1)
                self.facingRight = False

        if self.attack == "evil":
            if self.attackFrame==5:
                Player.lickSound.play()
            if self.attackFrame < 4:
                self.image = self.idleImage
            elif self.attackFrame < 24:
                self.image = self.preEvilImage
            elif self.attackFrame == 24:
                self.evil = 1
                self.box = [12, 15, 20, 27]
            elif self.attackFrame < 44:
                self.image = self.midEvilImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "normal":
            if self.attackFrame==5:
                Player.lickSound.play()
            if self.attackFrame < 9:
                self.image = self.midEvilImage
            elif self.attackFrame == 14:
                self.evil = 0
                self.box = [12, 13, 20, 27]
            elif self.attackFrame < 20:
                self.image = self.preEvilImage
            elif self.attackFrame < 24:
                self.image = self.idleImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "fastevil":
            if self.attackFrame == 1:
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                Player.ultSound.play()
                Player.lickSound.play()
                self.ultCharge = 30
                self.evil = 1
                self.box = [12, 15, 20, 27]
            if self.attackFrame < 8:
                self.image = self.preEvilImage
            elif self.attackFrame < 12:
                self.image = self.midEvilImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "ult":
            if self.attackFrame == 1:
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                Player.ultSound.play()
                Player.bzzzSound.play()
            self.executeAttack(self.spinner, not self.pressed["3"])
            if 5<self.attackFrame<45:
                if (self.attackFrame%8)<4:
                    self.image = self.longPunch2Image
                self.yv-=0.79
                self.yv*=0.95

    def loadImages(self, skinChoice):
        self.normalImage = Player.load("crawler", "idle.png", skin=skinChoice)
        self.idleImage = self.normalImage
        self.normalStunnedImage = Player.load("crawler", "hurt.png", skin=skinChoice)
        self.evilStunnedImage=Player.load("crawler", "evilhurt.png", skin=skinChoice)
        self.prePunchImage = Player.load("crawler", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("crawler", "punch.png", skin=skinChoice)
        self.preKickImage = Player.load("crawler", "prekick.png", skin=skinChoice)
        self.kickImage = Player.load("crawler", "kick.png", skin=skinChoice)
        self.preLickImage=Player.load("crawler", "prelick.png", skin=skinChoice)
        self.lickImage=Player.load("crawler", "lick.png", skin=skinChoice)
        self.preEvilImage=Player.load("crawler", "preevil.png", skin=skinChoice)
        self.midEvilImage=Player.load("crawler", "midevil.png", skin=skinChoice)
        self.evilImage=Player.load("crawler", "evil.png", skin=skinChoice)
        self.preImage=Player.load("crawler", "prelong.png", skin=skinChoice)
        self.longImage=Player.load("crawler", "long.png", skin=skinChoice)
        self.longPunchImage=Player.load("crawler", "longpunch.png", skin=skinChoice)
        self.longPunch2Image=Player.load("crawler", "longpunch2.png", skin=skinChoice)

    cssImages = [Player.load("crawler", "idle.png", skin=i) for i in range(6)]
    text = "Don't let it turn inside out. It is much scarier that way..."
    helpTexts =[
    "Pro tips:",
    "Jump while slidekicking to jump-cancel it.",
    "SUPER just turns you inside out very fast.",
    "SUPER while inside out is very good.",
    "Inside out form has lifesteal.",
    ]
class Ninja(Player):

    def passive(self):
        if self.state == State.stunned and self.stance == 1:
            self.stance = 2
        if self.stance == 1:
            self.box = [16-11,24,16+11,28] #lying
            self.idleImage = self.lyingImage
            self.stunnedImage = self.stunned2Image
            self.xspeed = 0
            self.canDoubleJump = 0
        elif self.stance == 0:
            self.box = [16-5,14,16+5,28] #standing
            self.idleImage = self.standingImage
            self.stunnedImage = self.stunned1Image
            self.xspeed = 2
            #self.canDoubleJump = 1
        else:
            self.box = [16-10,21,16+10,28] #crawling
            self.idleImage = self.crawlingImage
            self.stunnedImage = self.stunned2Image
            self.xspeed = 1
            self.canDoubleJump = 0


    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Ninja, self).__init__(x, y, facingRight, controls, joystick, skin)
        #self.box = [16-11,23,16+11,28] #lying
        #self.box = [16-11,21,16+11,28] #crawling
        self.box = [16-5,14,16+5,28] #standing
        self.init2()
        self.canDoubleJump = False
        self.stance = 0 # 0:standing, 1:lying, 2:crawling

        self.stabData = [
        [4, self.stab1Image],
        [7, self.stab2Image, [26,17,32,21, 18]],
        [15, self.stab2Image],
        [20, self.stab1Image],
        [250, self.whirl1Image],
        ]

        self.jabData = [
        [6, self.jab1Image],
        [9, self.jab2Image, [21,14,27,20, 20]],
        [13, self.jab2Image],
        [20, self.jab1Image],
        [25, self.idleImage],
        ]

        self.lanceData = [
        [4, self.idleImage],
        [6, self.lanceImages[0]],
        [8, self.lanceImages[0], [2,19,11,24, 19]],
        [14, self.lanceImages[1]],
        [17, self.lanceImages[2], [22,19,30,24, 45]],
        [28, self.lanceImages[3]],
        [33, self.lanceImages[2], [2,19,11,24, 19]],
        [43, self.lanceImages[1]],
        [50, self.lanceImages[0]],#, [12,9,16,13, 10,40]],
        [58, self.idleImage],
        ]


        self.stingData = [
        [4, self.pierceImages[3]],
        [8, self.pierceImages[4], [25,22,32,27, 15]],
        [11, self.pierceImages[4]],
        [15, self.pierceImages[3]],
        [180, self.crawlingImage],
        ]

        self.kick = [
        [4, self.kickImages[0]],
        [8, self.kickImages[1]],
        [12, self.kickImages[2], [6,15,11,21, 25,-30,25]],
        [15, self.kickImages[2]],
        [20, self.kickImages[1]],
        [25, self.kickImages[0]],
        [28, self.crawlingImage],
        ]

        self.pierce = [
        [5, self.pierceImages[0]],
        [10, self.pierceImages[1]],
        [15, self.pierceImages[2]],
        [23, self.pierceImages[3], [25,22,30,28, 45, 50]],
        [29, self.pierceImages[3]],
        [350, self.crawlingImage],
        ]

        self.roll = [
        [5, self.rollImages[0]],
        [10, self.rollImages[1]],
        [15, self.rollImages[2]],
        [20, self.rollImages[3]],
        [25, self.rollImages[4]],
        [30, self.rollImages[5]],
        [350, self.standingImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            if self.stance == 0:
                self.attack = "jab"
            else:
                if self.pressed["2"]:
                    if self.useUltCharge():
                        self.attack = "screw"
                    else:
                        self.state = 0
                else:
                    self.attack = "sting"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            if self.stance == 0:
                self.attack = "lance"
            else:
                self.attack = "stab"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            if self.stance == 0:
                if self.useUltCharge():
                    self.attack = "ult"
                else:
                    self.state = 0
            elif self.stance == 1:
                self.attack = "spin"
            else:
                self.attack = "kick"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            if self.stance == 0:
                self.attack = "pierce"
            else:
                self.attack = "roll"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.jabData, not self.pressed["1"])
        if self.attack == "lance":
            self.executeAttack(self.lanceData, not self.pressed["2"])
        if self.attack == "stab":
            if self.stance == 2:
                if self.attackFrame < 5:
                    self.image = self.turnImage
                elif self.attackFrame < 9:
                    self.image = self.idleImage
                    self.stance = 1
                    self.attackFrame = 1
            else:
                self.executeAttack(self.stabData, not self.pressed["2"])
                if self.attackFrame == 25:
                    self.state = 0
                    self.image = self.lyingImage
                    self.attackBox = None
        if self.attack == "sting":
            self.executeAttack(self.stingData, not self.pressed["1"])
            if self.attackFrame < 4 and self.stance == 1:
                self.image = self.turnImage
            if self.attackFrame == 18:
                self.state = 0
                self.image = self.crawlingImage
                self.stance = 2
                self.attackBox = None
        if self.attack == "spin":
            self.xv+=(self.pressed["d"]-self.pressed["a"])*0.05
            if self.attackFrame < 13:
                self.image = self.whirl1Image
            elif self.attackFrame < 100:
                self.yv-=0.9
                self.image = [self.whirl1Image,self.whirl2Image][self.attackFrame%6<4]
                self.attackBox = [9,17,23,21, 6,12]
                if not self.pressed["3"] and self.attackFrame>35:
                    self.attackFrame = 100
            elif self.attackFrame < 115:
                self.yv-=1
                self.image = [self.whirl1Image,self.whirl2Image][self.attackFrame%6<4]
                self.attackBox = [9,17,23,21, 10,40,20,0.5]
            elif self.attackFrame < 125:
                self.image = self.whirl1Image
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "pierce":
            self.executeAttack(self.pierce, not self.pressed["3"])
            if 10<self.attackFrame<20:
                self.xv=(self.facingRight-0.5)*12
            if self.attackFrame==10:
                self.stance = 2
                self.yv-=3
            if self.attackFrame==35:
                self.state = 0
                self.image = self.crawlingImage
                self.attackBox = None
        if self.attack == "kick":
            self.executeAttack(self.kick, not self.pressed["3"])

        if self.attack == "roll":
            self.executeAttack(self.roll, not self.pressed["4"])
            if self.attackFrame == 1 and self.stance == 2:
                self.facingRight = not self.facingRight
                self.yv = 0
            if 2 < self.attackFrame < 24:
                self.invincible = True
                self.xv = (self.facingRight-0.5) * -8
            if self.attackFrame == 24:
                self.invincible = False
                self.facingRight = not self.facingRight
                self.stance = 0
            if self.attackFrame == 35:
                self.state = 0
                self.image = self.standingImage
                self.attackBox = None

        if self.attack == "screw":
            if self.attackFrame == 1:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

            if self.attackFrame < 50:
                self.image = [self.pierceImages[4], self.turnImage, self.crawlingImage, self.pierceImages[3]][(self.attackFrame//2)%4]
                self.xv = (self.facingRight-0.5)*10
                self.yv = 0
                self.attackBox = [25,22,32,27, 8]
            elif self.attackFrame < 60:
                self.image = self.pierceImages[4]
                self.attackBox = [25,22,32,27, 40,59]
            elif self.attackFrame < 80:
                self.image = self.crawlingImage
                self.stance = 2
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "ult":
            if self.attackFrame == 1:
                Player.growSound.play()
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            length = 90
            self.xv = 0
            self.yv = 0
            if self.attackFrame < 5:
                self.image = self.magicImages[0]
            if self.attackFrame < 10:
                self.image = self.magicImages[1]
            elif self.attackFrame < length:
                self.xv = (self.pressed["d"]-self.pressed["a"])*4
                self.yv = (self.pressed["4"]-self.pressed["w"])*4
                if self.pressed["a"]:
                    self.facingRight = False
                if self.pressed["d"]:
                    self.facingRight = True
                self.hp-=0.2
                self.image = [self.magicImages[2],self.magicImages[3]][(self.attackFrame//4)%2]
                self.attackBox = [6,13,26,29, 2,4]
            elif self.attackFrame < length+7:
                self.attackBox = [6,13,26,30, 30]
                self.image = self.magicImages[2]
            elif self.attackFrame < length+14:
                self.image = self.magicImages[1]
                self.attackBox = None
            elif self.attackFrame < length+23:
                self.image = self.magicImages[0]
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.standingImage = Player.load("ninja", "standing.png", skin=skinChoice)
        self.idleImage = self.standingImage
        self.lyingImage = Player.load("ninja", "lying.png", skin=skinChoice)
        self.crawlingImage = Player.load("ninja", "crawling.png", skin=skinChoice)
        self.whirl1Image = Player.load("ninja", "whirl1.png", skin=skinChoice)
        self.whirl2Image = Player.load("ninja", "whirl2.png", skin=skinChoice)
        self.stab1Image = Player.load("ninja", "stab1.png", skin=skinChoice)
        self.stab2Image = Player.load("ninja", "stab2.png", skin=skinChoice)
        self.jab1Image = Player.load("ninja", "jab1.png", skin=skinChoice)
        self.jab2Image = Player.load("ninja", "jab2.png", skin=skinChoice)
        self.pierceImages = [Player.load("ninja", "pierce"+str(i)+".png", skin=skinChoice) for i in range(1,6)]
        self.kickImages = [Player.load("ninja", "kick"+str(i)+".png", skin=skinChoice) for i in range(1,4)]
        self.rollImages = [Player.load("ninja", "roll"+str(i)+".png", skin=skinChoice) for i in range(1,7)]
        self.lanceImages = [Player.load("ninja", "lance"+str(i)+".png", skin=skinChoice) for i in range(1,5)]
        self.magicImages = [Player.load("ninja", "magic"+str(i)+".png", skin=skinChoice) for i in range(1,5)]
        self.turnImage = Player.load("ninja", "turn.png", skin=skinChoice)
        self.stunned1Image = Player.load("ninja", "stunned1.png", skin=skinChoice)
        self.stunned2Image = Player.load("ninja", "stunned2.png", skin=skinChoice)
        self.cssImages = [Player.load("ninja", "standing.png", skin=i) for i in range(6)]

    cssImages = [Player.load("ninja", "standing.png", skin=i) for i in range(6)]
    text = "They use a variety of different techniques and tactics to effectively use their weapons in combat."
    helpTexts =[
    "Pro tips:",
    "Press Down to lie down/stand up.",
    "Press Attack1/2 to flip around.",
    "Pressing both uses SUPER.",
    "While lying on your back: Hold Attack3 to fly!",
    "While standing Attack3 is a whirlwind SUPER.",
    ]

class Bird(Player):

    def confirmedHit(self, damage):
        if self.attack=="el":
            self.ultCharge+=1
        
    def passive(self):
        if self.pressed["3"]:
            if self.ultCharge>self.CHARGE: #ult
                self.ultCharge = 0
                self.yv=-22
                self.xv=(self.facingRight-0.5)*10
                self.state = State.idle
                self.stun = 0
                self.attackBox =None
                self.onGround = False
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            else:
                self.ultError = 16
        self.yv-=0.1

        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

        if self.pressed["w"] and (self.yv>=0 or (-18<self.yv<-17 and not self.stun)): #float
            self.yv=1
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Bird, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*Player.SCALE
        self.CHARGE = 25
        self.maxhp = 200
        self.init2()

        self.first = [
        [8, self.prePunchImage],
        [12, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 20]],
        [24, self.punchImage],
        [30, self.prePunchImage],
        ]

        self.second = [
        [20, self.prePunchImage],
        [25, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 43]],
        [50, self.punchImage],
        [60, self.prePunchImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "el"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "dodge"

    def doAttack(self, pressed):
        if self.attack == "punch":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==8 and self.pressed["1"]:
                self.attack = "punch2"
        elif self.attack == "punch2":
            self.executeAttack(self.second, not self.pressed["1"])
        elif self.attack == "el":
            if self.pressed["a"] and not self.pressed["d"] and self.facingRight:
                self.facingRight = False
            if self.pressed["d"] and not self.pressed["a"] and not self.facingRight:
                self.facingRight = True

            if self.attackFrame < 30:
                self.image = self.preelImage #preel/dodgeImage
                self.attackBox = None
            elif self.attackFrame < 150:
                self.image = self.preelImage #preel/dodgeImage
                self.attackBox = None
                if not self.pressed["2"]:
                    self.attackFrame = 149

            elif self.attackFrame == 150:
                Player.bzzzSound.play()

            elif self.attackFrame < 176:
                self.image = self.elaImage
                self.attackBox = [0, 15, 9, 24, 7,6]
                if self.attackFrame%6>2:
                    self.attackBox = [23, 15, 23+9, 24, 7,6]
                    self.image = self.elbImage
            elif self.attackFrame < 182:
                self.image = self.elaImage
                self.attackBox = [0, 15, 9, 24, 17,26]
                if self.attackFrame%6>2:
                    self.attackBox = [23, 15, 23+9, 24, 17, 26]
                    self.image = self.elbImage
            
            elif self.attackFrame < 205:
                self.image = self.preelImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        elif self.attack == "dodge":
            if self.attackFrame < 2:
                self.invincible=False
                self.image = self.idlebImage
            elif self.attackFrame < 30:
                self.image = self.dodgeImage
                self.invincible=True
            elif self.attackFrame < 40:
                self.invincible=False
                self.image = self.idlebImage
            else:
                self.state = State.idle
                self.image = self.idleImage

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("bird", "idle.png", skin=skinChoice)
        self.idlebImage = Player.load("bird", "idleb.png", skin=skinChoice)
        self.stunnedImage = Player.load("bird", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("bird", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("bird", "punch.png", skin=skinChoice)
        self.dodgeImage = Player.load("bird", "dodge.png", skin=skinChoice)
        self.preelImage = Player.load("bird", "preel.png", skin=skinChoice)
        self.elaImage = Player.load("bird", "ela.png", skin=skinChoice)
        self.elbImage = Player.load("bird", "elb.png", skin=skinChoice)

    cssImages = [Player.load("bird", "idle.png", skin=i) for i in range(6)]
    text = "The electric avian predator"
    helpTexts =[
    "Pro tips:",
    "Hold Up to float.",
    "Press Down to dodge",
    "SUPER is a high jump that cancels anything.",
    "Float while using SUPER to not really",
    "jump very high. (useful?)",
    ] #N
class Darkbird(Player):

    def confirmedHit(self, damage):
        if self.attack=="el":
            self.ultCharge+=2
            self.hp = min(self.hp+2,self.maxhp)
        
    def passive(self):
        if self.pressed["3"]:
            if self.ultCharge>self.CHARGE: #ult
                self.ultCharge = 0
                self.yv=-10
                self.xv=(self.facingRight-0.5)*10
                self.state = State.idle
                self.stun = 0
                self.attackBox =None
                self.onGround = False
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            else:
                self.ultError = 16
        self.yv-=0.2

        if self.attackFrame%16<8: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

        if self.pressed["w"] and (self.yv>=0 or (-18<self.yv<-17 and not self.stun)): #float
            self.yv=0.2
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*Player.SCALE
        self.xspeed = 2
        self.canDoubleJump = True
        self.CHARGE = 50
        self.maxhp = 150
        self.elCharge = 0
        self.init2()

        self.first = [
        [10, self.prePunchImage],
        [15, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 24]],
        [28, self.punchImage],
        [36, self.prePunchImage],
        ]

        self.second = [
        [28, self.prePunchImage],
        [33, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 23,23,23,0.5]],
        [40, self.punchImage],
        [48, self.prePunchImage],
        [55, self.punchImage, [32-9, 32-8-7, 32-1, 32-10, 23]],
        [60, self.punchImage],
        [70, self.prePunchImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "el"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "dodge"

    def doAttack(self, pressed):
        if self.attack == "punch":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==9 and self.pressed["1"]:
                self.attack = "punch2"
        elif self.attack == "punch2":
            self.executeAttack(self.second, not self.pressed["1"])
        elif self.attack == "el":
            if self.pressed["a"] and not self.pressed["d"] and self.facingRight:
                self.facingRight = False
            if self.pressed["d"] and not self.pressed["a"] and not self.facingRight:
                self.facingRight = True

            if self.attackFrame < 20:
                self.image = self.preelImage #preel/dodgeImage
                self.attackBox = None
                self.elCharge = 0
            elif self.attackFrame < 100:
                self.image = self.preelImage #preel/dodgeImage
                self.attackBox = None
                self.elCharge += 1
                self.hp-=0.5
                if not self.pressed["2"]:
                    self.attackFrame = 99

            elif self.attackFrame == 100:
                Player.bzzzSound.play()

            elif self.attackFrame < 116+self.elCharge//2:
                self.image = self.elaImage
                self.attackBox = [0, 15, 9, 24, 7,6]
                if self.attackFrame%6>2:
                    self.attackBox = [23, 15, 23+9, 24, 7,6]
                    self.image = self.elbImage
            elif self.attackFrame < 122+self.elCharge//2:
                self.image = self.elaImage
                self.attackBox = [0, 15, 9, 24, 17,26]
                if self.attackFrame%6>2:
                    self.attackBox = [23, 15, 23+9, 24, 17, 26]
                    self.image = self.elbImage
            
            elif self.attackFrame < 145+self.elCharge//2:
                self.image = self.preelImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        elif self.attack == "dodge":
            if self.attackFrame < 3:
                self.invincible=False
                self.image = self.preelImage
            elif self.attackFrame < 22:
                self.image = self.dodgeImage
                self.invincible=True
            elif self.attackFrame < 30:
                self.invincible=False
                self.image = self.preelImage
            else:
                self.state = State.idle
                self.image = self.idleImage

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("darkbird", "idle.png", skin=skinChoice)
        self.idlebImage = Player.load("darkbird", "idleb.png", skin=skinChoice)
        self.stunnedImage = Player.load("darkbird", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("darkbird", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("darkbird", "punch.png", skin=skinChoice)
        self.dodgeImage = Player.load("darkbird", "dodge.png", skin=skinChoice)
        self.preelImage = Player.load("darkbird", "preel.png", skin=skinChoice)
        self.elaImage = Player.load("darkbird", "ela.png", skin=skinChoice)
        self.elbImage = Player.load("darkbird", "elb.png", skin=skinChoice)

    cssImages = [Player.load("darkbird", "idle.png", skin=i) for i in range(6)]
    text = "The dark dual predator"
class Robot(Player):

    def grounded(self):
        Player.shake+=int(self.yv*0.6)
        super().grounded()
    
    def passive(self):
        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage
        self.yv+=0.15
        if self.state == State.stunned:
            self.stun-=0.3
            self.yv-=0.1

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Robot, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.init2()

        self.first = [
        [15, self.prePunchImage],#,[19, 10, 23, 13, 6, 40, 12]],
        [30, self.punchImage, [24, 32-17, 27, 32-12, 6, 12]],
        [100, self.punchImage, [24, 32-17, 27, 32-12, 5, 12],True],
        [120, self.prePunchImage],
        ]

        self.second = [
        [5, self.idleImage],
        [30, self.stunnedImage],
        [38, self.fireImage, [20, 32-17, 24, 32-12, 48, 58]],
        [45, self.fireImage],
        [60, self.stunnedImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "drill"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            if self.useUltCharge():
                self.attack = "ult"
            else:
                self.attack = "shoot"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "down"
        

    def doAttack(self, pressed):
        if self.attack == "drill":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame==15:
                Player.bzzzSound.play()
            if self.attackFrame==101:
                Player.bzzzSound.stop()
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
            if self.attackFrame == 31:
                if not self.pressed["1"]:
                    self.xv += (self.facingRight-0.5)*-10
                    self.yv = -4

        if self.attack == "shoot":
            if self.attackFrame < 8:
                self.image = self.idleImage
                self.attackBox = None        
            elif self.attackFrame < 14: 
                self.image = self.fireImage
            elif self.attackFrame == 14:
                if not self.pressed["1"]:
                    self.xv += (self.facingRight-0.5)*-8
                    self.yv = -3
                self.image = self.fireImage
                Projectile.projectiles.append(Projectile(self))
                playHitSound(State.volume*0.2)
            elif self.attackFrame < 42:
                self.image = self.stunnedImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "down":
            if self.attackFrame < 10:
                self.image = self.idleImage
                self.attackBox = None        
            elif self.attackFrame < 15: 
                self.image = self.jetpackImage
                self.attackBox = [13, 32-7, 18, 32-3, 20]
            elif self.attackFrame == 15:
                self.image = self.jetpackImage
                self.attackBox = None
                if not self.pressed["1"]:
                    self.yv=-14
            elif self.attackFrame < 32:
                self.image = self.stunnedImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "ult":
            if self.attackFrame == 1:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            if self.attackFrame < 60:
                if self.attackFrame%10 ==1:
                    self.image = self.fireImage
                    Projectile.projectiles.append(Projectile(self, op=True))
                    playHitSound(State.volume*0.2)
                    pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                else:
                    self.image = self.stunnedImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    nam1=["A","B","C","X","Y","Z"]
    nam2=[str(i) for i in range(10)]
    name = random.choice(nam1)
    for i in range(random.randint(1,2)):
        name = name + random.choice(nam1+nam2)
    text = "name: "+name

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("robot", "idle.png", skin=skinChoice)
        self.idlebImage = Player.load("robot", "idleb.png", skin=skinChoice)
        self.stunnedImage = Player.load("robot", "stunned.png", skin=skinChoice)
        self.fireImage = Player.load("robot", "fire.png", skin=skinChoice)
        self.projbImage = Player.load("robot", "proj.png", skin=skinChoice)
        self.punchImage = Player.load("robot", "punch.png", skin=skinChoice)
        self.prePunchImage = Player.load("robot", "prepunch.png", skin=skinChoice)
        self.jetpackImage = Player.load("robot", "jetpack.png", skin=skinChoice)

    cssImages = [Player.load("robot", "idle.png", skin=i) for i in range(6)]
    helpTexts =[
    "Pro tips:",
    "Hold Attack1 to drill longer.",
    "Jump forward/backwards while shooting",
    "to change the speed of projectiles.",
    "Hold Attack1 while using other attacks to prevent recoil.",
    ]
class Lizard(Player):

    def confirmedHit(self, damage):
        if self.attack == "tail":
            self.ultCharge = max(self.ultCharge+20, self.CHARGE)
            self.yv=-2
        if self.attack == "sweep":
            self.ultCharge = max(self.ultCharge+25, self.CHARGE)

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Lizard, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-17, 16+3, 32-4] # not here
        self.maxhp = 200
        #self.xspeed = 3  not here
        self.CHARGE = 25
        self.init2()
        self.canDoubleJump = True
        self.can_crouch = True
        self.magicSprites = False

        self.first = [
        [3, self.prePunchImage],
        [5, self.midPunchImage],
        [9, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 23,23,23,0.5]],
        [17, self.punchImage],
        [24, self.midPunchImage],
        [26, self.idleImage],
        ]

        self.second = [
        [10, self.prePunchImage],
        [14, self.midPunchImage],
        [20, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 30,30,40,0.5]],
        [29, self.punchImage],
        [34, self.midPunchImage],
        [43, self.prePunchImage],
        ]
        self.sweep = [
        [8, self.preSweepImage],
        [12, self.sweepImage, [18, 24, 27, 28, 15,50,20,0.5]],
        [15, self.sweepImage],
        [20, self.preSweepImage],
        [23, self.crouchImage],
        ]
        self.tail = [
        [11, self.preTailImage],
        [16, self.tailImage, [7, 32-4, 10, 32-2, 27,-23,23,0.5]],
        [25, self.tailImage],
        ]
        self.lick = [
        [9, self.preLickImage],
        [13, self.lickImage],
        [16, self.lickImage, [15, 32-13, 28, 20, 0,-25]],
        [33, self.preLickImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            if self.pressed["4"]:
                self.attack = "sweep"
            else:
                self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            if self.pressed["4"]:
                if self.y==280:
                    self.attack = "sweep"
                else:
                    self.attack = "tail"
            else:
                self.attack = "lick"

        elif(self.pressed["3"]):
            if not self.pressed["4"]:
                self.state = 1
                self.attackFrame = 1
                self.attack = "punch"

        if self.state == 1:
            self.magicSprites = False

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "sweep":
            self.executeAttack(self.sweep, not self.pressed["1"])
        if self.attack == "tail":
            self.executeAttack(self.tail, not self.pressed["2"])
        if self.attack == "lick":
            self.executeAttack(self.lick, not self.pressed["2"])
            if self.attackFrame == 7:
                Player.lickSound.play()

    def passive(self):
        if self.pressed["3"] and self.pressed["4"]:
            if self.ultCharge>self.CHARGE and not self.state==State.idle:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                self.ultCharge = 0
                self.stun = 0
                self.xv = 0
                self.yv = -2
                self.state = State.idle
                self.magicSprites = True
                self.attackBox = None
            else:
                self.ultError = 16

        if self.state==State.idle and self.can_crouch:
            if self.pressed["4"]:
                if self.magicSprites:
                    self.image = self.crouchMagicImage
                else:
                    self.idleImage = self.crouchImage
                    self.image = self.idleImage
                self.box = [16-3, 32-14, 16+3, 32-4]
                if self.onGround:
                    self.xspeed = 0
            else:
                if self.magicSprites:
                    self.image = self.magicImage
                else:
                    self.idleImage = self.standingImage
                    self.image = self.idleImage
                self.box = [16-3, 32-17, 16+3, 32-4]
                self.xspeed = 3

    def loadImages(self, skinChoice):
        self.preLickImage = Player.load("lizard", "prelick.png", skin=skinChoice)
        self.lickImage = Player.load("lizard", "lick.png", skin=skinChoice)
        self.standingImage = Player.load("lizard", "idle.png", skin=skinChoice)
        self.idleImage = self.standingImage
        self.magicImage = Player.load("lizard", "magic.png", skin=skinChoice)
        self.crouchMagicImage = Player.load("lizard", "magiccrouch.png", skin=skinChoice)
        self.stunnedImage = Player.load("lizard", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("lizard", "prepunch.png", skin=skinChoice)
        self.midPunchImage = Player.load("lizard", "midpunch.png", skin=skinChoice)
        self.punchImage = Player.load("lizard", "punch.png", skin=skinChoice)
        self.preTailImage = Player.load("lizard", "crouchprekick.png", skin=skinChoice)
        self.tailImage = Player.load("lizard", "crouchkick.png", skin=skinChoice)
        self.crouchImage = Player.load("lizard", "crouch.png", skin=skinChoice)
        self.preSweepImage = Player.load("lizard", "presweep.png", skin=skinChoice)
        self.sweepImage = Player.load("lizard", "sweep.png", skin=skinChoice)

    cssImages = [Player.load("lizard", "idle.png", skin=i) for i in range(6)]
    text = "To master the reptile you must first understand endlag"
    helpTexts =[
    "Pro tips:",
    "Can double jump.",
    "Press down to use different attacks.",
    "Down and Attack3 is the SUPER.",
    "SUPER cancels anything. (high skill!)",
    "Hitting with the tail charges your SUPER.",
    ]
class Golem(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Golem, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [11, 15, 21, 28]
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [10, self.punchImage, [21, 18, 25, 22, 20]],
        [17, self.punchImage],
        [23, self.prePunchImage],
        ]

        self.second = [
        [11, self.prePunchImage],
        [15, self.kickImage, [17, 23, 23, 27, 10,-32,17,0.5]],
        [22, self.kickImage],
        [28, self.prePunchImage],
        [35, self.punchImage, [21, 18, 25, 22, 10,45,22,0.5]],
        [39, self.punchImage],
        [42, self.prePunchImage],
        ]

        self.grass = [
        [21, self.preGrassImage],
        [41, self.grassImage, [21, 19, 32, 24, 5, 5]],
        [46, self.grassImage, [21, 19, 32, 24, 12, 22]],
        [69, self.preGrassImage],
        ]

        self.lick = [
        [6, self.preLickImage],
        [9, self.lickImage, [20, 9, 24, 13, 24]],
        [17, self.lickImage],
        [26, self.preLickImage],
        ]

        self.ultimate = [
        [50, self.fireImage, [9,6,24,30, 25, 50], True],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "lick"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "grass"

        elif(self.pressed["4"]):
            if self.useUltCharge():
                self.attack = "fire"
                self.state = 1
                self.attackFrame = 1

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame == 7 and self.pressed["1"]:
                self.attack = "kick"
        if self.attack == "kick":
            self.executeAttack(self.second, not self.pressed["1"])
        if self.attack == "lick":
            self.executeAttack(self.lick, not self.pressed["2"])
            if self.attackFrame==1:
                Player.lickSound.play()
        if self.attack == "grass":
            self.executeAttack(self.grass, not self.pressed["3"])
            if self.attackFrame==20:
                Player.bzzzSound.play()
                Player.growSound.play()
        if self.attack == "fire":
            self.executeAttack(self.ultimate, not self.pressed["4"])
            if self.attackFrame==1:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

    def confirmedHit(self, damage):
        if self.attack == "grass":
            self.xv*=0.5
            self.yv*=0.2

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("golem", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("golem", "stunned.png", skin=skinChoice)
        self.fireImage = Player.load("golem", "fire.png", skin=skinChoice)
        self.prePunchImage = Player.load("golem", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("golem", "punch.png", skin=skinChoice)
        self.kickImage = Player.load("golem", "kick.png", skin=skinChoice)
        self.preGrassImage = Player.load("golem", "pregrass.png", skin=skinChoice)
        self.grassImage = Player.load("golem", "grass.png", skin=skinChoice)
        self.preLickImage = Player.load("golem", "prelick.png", skin=skinChoice)
        self.lickImage = Player.load("golem", "lick.png", skin=skinChoice)

    cssImages = [Player.load("golem", "idle.png", skin=i) for i in range(6)]
    text = "Animated igneous rock infused with elemental powers"
    helpTexts =[
    "Pro tips:",
    "Hold Attack1 to kick and punch upward.",
    "You can eat projectiles.",
    "Hold Down to SUPER for ver y long.",
    ]
class Alien(Player):

    def passive(self):
        self.yv-=0.1

    def confirmedHit(self, damage):
        self.yv= -5 +4*(self.attack=="ult") -2*(self.attack=="punch")
        self.ultCharge+=2

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Alien, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [13, 14, 19, 28]
        self.init2()
        self.xspeed=3#.5
        self.canDoubleJump = True

        self.first = [
        [8, self.prePunchImage],
        [15, self.punchImage, [17, 19, 23, 23, 8,-20,20,0.5]],
        [16, self.punchImage],
        [20, self.prePunchImage],
        [30, self.punchImage, [17, 19, 23, 23, 15,20,15,0.8]],
        [34, self.prePunchImage],
        ]

        self.second = [
        [20, self.prePunchImage],
        [23, self.punchImage, [17, 19, 23, 23, 33,33,36,0.8]],
        [27, self.punchImage],
        [41, self.prePunchImage],
        ]

        self.ultimate = [
        [5, self.footImage,[19, 23, 23, 28, 5,-20,10,0.5]],
        [15, self.armImage, [19, 17, 24, 20, 4,-15,4,0.5]],
        [19, self.rise1Image, [19, 17, 24, 20, 4,22,4]],
        [23, self.rise2Image, [19, 15, 24, 18, 4,-10,4,0.5]],
        [27, self.rise3Image, [19, 13, 24, 16, 4,-10,4,0.5]],
        [31, self.rise4Image, [19, 11, 24, 14, 4,15,4]],
        [35, self.rise3Image, [19, 13, 24, 16, 4,-5,4,-2.0]],
        [39, self.rise2Image, [19, 15, 24, 18, 4,0,4]],
        [44, self.rise1Image, [19, 17, 24, 20, 15,60]],
        [56, self.idleImage]
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "shoot"

        elif(self.pressed["4"]):
            self.attack = "back"
            self.state = 1
            self.attackFrame = 1

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame == 33 and self.pressed["1"]:
                if self.useUltCharge():
                    self.attack = "ult"
                    self.attackFrame = 1
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "shoot":
            if self.attackFrame < 7:
                self.image = self.stunnedImage
            elif self.attackFrame == 10:
                self.image = self.fireImage
                Projectile.projectiles.append(Projectile(self))
                self.yv -= 2
                self.xv += (self.facingRight*2-1)*2
            elif self.attackFrame < 16:
                self.image = self.fireImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "back":
            if self.attackFrame < 5:
                self.image = self.preHairImage
                self.attackBox = None
            elif self.attackFrame < 8:
                self.yv=-5
                self.xv-=(self.facingRight-0.5)*3
                self.image = self.hairImage
                self.attackBox = [5, 20, 9, 24, 20,66,15,0.3]
            elif self.attackFrame < 17:
                self.image = self.hairImage
                self.attackBox = None
            elif self.attackFrame < 22:
                self.image = self.preHairImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "ult":
            if self.attackFrame==1:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            self.executeAttack(self.ultimate)

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("alien", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("alien", "stunned.png", skin=skinChoice)
        self.fireImage = Player.load("alien", "fire.png", skin=skinChoice)
        self.prePunchImage = Player.load("alien", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("alien", "punch.png", skin=skinChoice)
        self.preHairImage = Player.load("alien", "prehair.png", skin=skinChoice)
        self.hairImage = Player.load("alien", "hair.png", skin=skinChoice)
        self.projbImage = Player.load("alien", "proj.png", skin=skinChoice)
        
        self.footImage = Player.load("alien", "foot.png", skin=skinChoice)
        self.armImage = Player.load("alien", "arm.png", skin=skinChoice)
        self.rise1Image = Player.load("alien", "rise1.png", skin=skinChoice)
        self.rise2Image = Player.load("alien", "rise2.png", skin=skinChoice)
        self.rise3Image = Player.load("alien", "rise3.png", skin=skinChoice)
        self.rise4Image = Player.load("alien", "rise4.png", skin=skinChoice)

    cssImages = [Player.load("alien", "idle.png", skin=i) for i in range(6)]
    text = "Trained in higher gravity"
    helpTexts =[
    "Pro tips:",
    "Can double jump.",
    "Hold Attack1 to transition into SUPER.",
    "Dealing damage charges your SUPER.",
    ]
class Glitch(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Glitch, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [13, 15, 19, 28]
        self.canDoubleJump = True
        self.glitchCharge = 0
        self.init2()

        self.first = [
        [10, self.prePunchImage],
        [16, self.punchImage, [15, 19, 22, 22, 30,30,27]],
        [22, self.punchImage],
        [32, self.prePunchImage]
        ]
        self.second = [
        [5, self.idleImage],
        [13, self.chimneyImage, [15, 8, 20, 13, 30,50,30, 0.5]],
        [17, self.chimneyImage],
        [23, self.idleImage],
        ]
        self.glitch = [
        #[10, self.idleImage],
        [27, self.preGlitchImage],
        [40, self.glitchImage, [9, 15, 23, 27, 5,-4,2]],
        [45, self.glitchImage, [9, 15, 23, 27, 10,50]],
        [60, self.idleImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            if not (self.image==self.shimmerImage):
                self.attack = "punch"
            else:
                self.attack="shoot"
                self.attackFrame=46
        
        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "up"
            if(self.image==self.shimmerImage):
                self.attackFrame = 5

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "glitch"
            if(self.image==self.shimmerImage):
                self.attackFrame = 25

        elif(self.pressed["4"]):
            if self.useUltCharge():
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                self.image = self.shimmerImage
                self.state = State.idle
                self.attackBox = None

    def doAttack(self, pressed):
        if self.attack == "punch":
            if self.attackFrame==11:
                self.xv+=(self.facingRight-0.5)*10
            if self.attackFrame==9 and self.pressed["1"]:
                self.attack = "shoot"
            self.executeAttack(self.first, not self.pressed["1"])

        if self.attack == "up":
            if self.attackFrame==6:
                self.yv+=10
            self.executeAttack(self.second, not self.pressed["2"])

        if self.attack == "glitch":
            self.executeAttack(self.glitch, not self.pressed["3"])

        if self.attack == "shoot":
            if self.attackFrame < 12:
                self.image = self.prePunchImage
            elif self.attackFrame < 16: 
                self.image = self.punchImage
                if self.attackFrame==13:
                    self.xv+=(self.facingRight-0.5)*10
                self.attackBox = [15, 19, 22, 22, 18,36,27]
            elif self.attackFrame < 20: 
                self.image = self.preFire1Image
                self.attackBox = None
            elif self.attackFrame < 28: 
                self.image = self.preFire2Image
            elif self.attackFrame < 36: 
                self.image = self.preFire3Image
            elif self.attackFrame < 44: 
                self.image = self.preFire4Image
            elif self.attackFrame < 48: 
                self.image = self.fireImage
            elif self.attackFrame == 48:
                self.image = self.fireImage
                Projectile.projectiles.append(Projectile(self))
                playHitSound(State.volume*0.4)
                Player.shake+=10
                self.xv-=(self.facingRight-0.5)*10
            elif self.attackFrame < 55:
                self.image = self.prePunchImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def confirmedHit(self, damage):
        if self.attack=="glitch":
            self.xv*=0.5
            self.yv*=0.2
            self.xv = (self.pressed["d"]-self.pressed["a"])*4
            self.yv = (self.pressed["w"]-self.pressed["4"])*-4
        #self.image=self.shimmerImage # this is really funny actually
    def passive(self):
        if(self.image==self.shimmerImage):
            self.xspeed = 4
            self.box = [13,11,19,16]
            self.flyingHeight=12*Player.SCALE

        else:
            self.box = [13, 15, 19, 28]
            self.xspeed = 2.5
            self.flyingHeight=0

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("glitch", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("glitch", "stunned.png", skin=skinChoice)
        self.fireImage = Player.load("glitch", "fire.png", skin=skinChoice)
        self.prePunchImage = Player.load("glitch", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("glitch", "punch.png", skin=skinChoice)
        self.shimmerImage = Player.load("glitch", "shimmer.png", skin=skinChoice)
        self.chimneyImage = Player.load("glitch", "chimney.png", skin=skinChoice)
        self.projbImage = Player.load("glitch", "proj.png", skin=skinChoice)

        self.preGlitchImage = Player.load("glitch", "preGlitch.png", skin=skinChoice)
        self.glitchImage = Player.load("glitch", "glitch.png", skin=skinChoice)
        self.preFire1Image = Player.load("glitch", "preFire1.png", skin=skinChoice)
        self.preFire2Image = Player.load("glitch", "preFire2.png", skin=skinChoice)
        self.preFire3Image = Player.load("glitch", "preFire3.png", skin=skinChoice)
        self.preFire4Image = Player.load("glitch", "preFire4.png", skin=skinChoice)

    cssImages = [Player.load("glitch", "idle.png", skin=i) for i in range(6)]
    text = "A glitch in the simulation"
    helpTexts =[
    "Pro tips:",
    "Can double jump."
    "Hold Attack1 to shoot a missile.",
    "SUPER makes your body invulnerable",
    "and makes your next attack instant.",
    "You are glitchy. Take it as you will.",
    ]
class Rat(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Rat, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [13, 17, 19, 28]
        self.hp = 200
        self.xspeed=2
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [12, self.punchImage, [18, 17, 24, 25, 9,9,8]],
        [22, self.prePunchImage],
        ]
        self.second = [
        [5, self.idleImage],
        [10, self.preJump1Image],
        [15, self.preJump2Image],
        [20, self.preTail1Image],
        [27, self.nibbleImage, [21, 25, 25, 29, 10,-5,15]],
        [34, self.preTail1Image],
        [41, self.nibbleImage, [21, 25, 25, 29, 15,-5,15]],
        [48, self.preTail1Image],
        [55, self.nibbleImage, [21, 25, 25, 29, 20,30,19]],
        [62, self.preTail1Image],
        [68, self.preJump1Image],
        ]
        self.tail = [
        [2, self.idleImage],
        [5, self.preJump1Image],
        [10, self.preJump2Image],
        [15, self.preTail1Image],
        [20, self.preTail2Image],
        [24, self.tailImage, [22, 8, 32, 19, 20,30,25]],
        [30, self.tailImage],
        [35, self.preTail2Image],
        [40, self.preTail1Image],
        [45, self.preJump1Image],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "dash"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "tail"

    def passive(self):
        self.xspeed=max(1.8,self.xspeed*0.997)
        if self.useUltCharge():
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            self.xspeed+=6
        else:
            self.ultError = 0

    def confirmedHit(self,damage):
        self.xspeed+=damage/8

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
        elif self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        elif self.attack == "dash":
            if self.attackFrame < 6:
                self.image = self.idleImage
            elif self.attackFrame < 12: 
                self.image = self.preJump1Image
            elif self.attackFrame < 18: 
                self.image = self.preJump2Image
            elif self.attackFrame < 24: 
                self.image = self.preTail1Image
            elif self.attackFrame < 30:
                self.image = self.jumpImage
                self.xv=(self.facingRight*2-1)*(self.xspeed*2)
                self.yv=-4
            elif self.attackFrame < 34:
                self.image = self.preJump1Image
            elif self.attackFrame < 42:
                self.attackBox = [18, 17, 25, 25, 5+4*self.xspeed,5+4*self.xspeed,20]
                self.image = self.punchImage
            elif self.attackFrame < 45:
                self.attackBox = None
                self.image = self.punchImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        elif self.attack == "tail":
            self.executeAttack(self.tail, not self.pressed["4"])

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("rat", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("rat", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("rat", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("rat", "punch.png", skin=skinChoice)

        self.jumpImage = Player.load("rat", "jump.png", skin=skinChoice)
        self.nibbleImage = Player.load("rat", "nibble.png", skin=skinChoice)
        self.preJump1Image = Player.load("rat", "preJump1.png", skin=skinChoice)
        self.preJump2Image = Player.load("rat", "preJump2.png", skin=skinChoice)

        self.preTail1Image = Player.load("rat", "preTail1.png", skin=skinChoice)
        self.preTail2Image = Player.load("rat", "preTail2.png", skin=skinChoice)
        self.tailImage = Player.load("rat", "tail.png", skin=skinChoice)

    cssImages = [Player.load("rat", "idle.png", skin=i) for i in range(6)]
    text = "Technically a mouse.        (BANNED)"
    helpTexts =[
    "Pro tips:",
    "Dealing damage makes you faster.",
    "When the SUPER charges you also become faster.",
    "Attack3 becomes stronger when you are faster.",
    ]
class Skugg(Player):

    def passive(self):
        if self.state == State.idle:
            if not self.onGround:
                self.image = self.idleImage
            elif self.pressed["d"] or self.pressed["a"]:
                self.image = self.walkImages[(self.attackFrame//4)%8]
            else:
                self.image = self.idleImage

            if self.useUltCharge():
                self.state = 1
                self.attack = "ult"
                self.attackFrame = 1
            else:
                self.ultError = 0
    def grounded(self):
        Player.shake+=int(self.yv)
        super().grounded()

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Skugg, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [4, 12, 28, 32]
        self.maxhp = 300
        self.xspeed=2

        self.image = self.idleImage
        self.init2()

        self.first = [
        [5, self.kickImages[0]],
        [10, self.kickImages[1]],
        [15, self.kickImages[2]],
        [20, self.kickImages[3]],
        [30, self.kickImages[4], [22, 22, 32, 28, 8, -20, 11]],
        [40, self.kickImages[5], [22, 21, 30, 28, 8, 20, 10]],
        [50, self.kickImages[6], [22, 20, 32, 28, 30, -120, 30]],
        [54, self.kickImages[7]],
        [58, self.kickImages[8]],
        [62, self.kickImages[9]],
        [66, self.kickImages[10]],
        ]

        self.second = [
        [5, self.skullImages[0]],
        [10, self.skullImages[1]],
        [15, self.skullImages[2]],
        [20, self.skullImages[3]],
        [30, self.skullImages[4], [24, 8, 32, 20, 57, 57, 48]],
        [35, self.skullImages[3]],
        [40, self.skullImages[2]],
        [45, self.skullImages[1]],
        [50, self.skullImages[0]],
        ]

        self.jump = [
        [4, self.jumpImages[0]],
        [8, self.jumpImages[1]],
        [12, self.jumpImages[2]],
        [16, self.jumpImages[3]],
        [20, self.jumpImages[4], [21, 4, 31, 8, 48]],
        [23, self.jumpImages[5], [21, 1, 31, 8, 52]],
        [26, self.jumpImages[5], [2, 3, 4, 6, 50,-50, 35]],
        [30, self.jumpImages[4]],
        [34, self.jumpImages[1]],
        [38, self.jumpImages[0]],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "skull"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "el"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jump"

    def doAttack(self, pressed):
        if self.attack == "punch":
            self.executeAttack(self.first, not self.pressed["1"])
        if self.attack == "skull":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "el":
            if self.attackFrame==1:
                Player.bzzzSound.play()
            if self.attackFrame<5:
                self.image = self.idleImage
            elif self.pressed["3"] or self.attackFrame<30:
                self.image = self.elImages[(self.attackFrame//3)%4]
                if self.attackFrame%12>5:
                    self.attackBox = [1, 1, 9, 8, 10,-50,17]
                    #nästan ingenting är teoretiskt omöjligt
                else:
                    self.attackBox = [19, 8, 30, 13, 13]
            else:
                self.bzzzSound.stop()
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "jump":
            self.executeAttack(self.jump, not self.pressed["4"])
            if self.attackFrame==19:
                self.yv=-11.1

        if self.attack == "ult":
            if self.attackFrame == 1:
                Player.ultSound.play()
                Player.growSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                self.invincible = True
            if self.attackFrame == 5*8:
                self.box = [16-8, 16, 16+8, 32]
            if self.attackFrame < 5*17:
                self.image = self.ultImages[self.attackFrame//5]
            else:
                if self in Player.players:
                    Player.players.remove(self)
                new = random.choice(legalClasses)(self.x, self.y, self.facingRight, self.controls, self.joystick)
                new.hp = min(new.maxhp, self.hp)
                new.random = self.random
                new.ultCharge = new.CHARGE

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("skugg", "idle.png", skin=skinChoice)
        self.walkImages = [Player.load("skugg", "SkuggVarg_0"+str(i)+".png", skin=skinChoice) for i in range(2,10)]
        self.elImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png", skin=skinChoice) for i in range(11,15)]
        self.jumpImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png", skin=skinChoice) for i in range(19,25)]
        self.kickImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png", skin=skinChoice) for i in range(26,37)]
        self.skullImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png", skin=skinChoice) for i in range(38,43)]
        self.ultImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png", skin=skinChoice) for i in range(44,61)]
        self.stunnedImage = Player.load("skugg", "SkuggVarg_16.png", skin=skinChoice)

    cssImages = [Player.load("skugg", "idle.png", skin=i) for i in range(6)]
    text = "Simultaneous wolf or elk silhouette?        (BANNED)"
    helpTexts =[
    "Pro tips:",
    "Use Attack1 to hit the opponent upwards.",
    "You should probably know every other",
    "character because your SUPER transforms",
    "you even if you dont want! xD",
    ]

class Knight(Player):

    def passive(self):
        if self.state == State.stunned:
            self.box = [16-3, 16, 16+3, 32-4]

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 16, 16+3, 32-4]
        self.init2()
        self.canDoubleJump = False
        self.xspeed = 2

        self.first = [
        [4, self.prePunchImage],
        [8, self.idleImage],
        [12, self.midPunchImage],
        [16, self.punchImage, [23,17,29,22, 19]],
        [24, self.punchImage],
        [30, self.midPunchImage],
        ]

        self.second = [
        [9, self.prePunchImage],
        [109, self.prePunchImage, None, True],
        [112, self.idleImage],
        [115, self.midPunchImage],
        [118, self.punchImage, [23,17,29,22, 29]],
        [120, self.longPunchImage, [23,20,29,23, 29]],
        [125, self.longPunchImage, [23,20,29,23, 29]],
        [132, self.punchImage],
        [138, self.midPunchImage],
        ]

        self.block = [
        [10, self.preBlockImage],
        [20, self.blockImage, [17,19,21,25, 9,33,9]],
        [100, self.blockImage, [17,19,21,25, 0,33,0], True],
        [110, self.preBlockImage],
        ]

        self.parkour = [
        [300, self.lyingImage, None, True],
        [301, self.idleImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "shield"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jump"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["2"])
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "block":
            self.executeAttack(self.block, not self.pressed["3"])
            if 10<self.attackFrame<=100:
                pass
                #self.invincible = True
            else:
                self.invincible = False
        if self.attack == "jump":
            self.executeAttack(self.parkour, not self.pressed["4"])
            if self.attackFrame==1:
                self.box = [16-6, 22, 16+6, 32-4]
            if self.attackFrame==301:
                if self.onGround:
                    if self.pressed["w"]:
                        self.yv=-30
                self.box = [16-3, 16, 16+3, 32-4]
            
    def loadImages(self, skinChoice):
        self.idleImage = Player.load("suspended", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("suspended", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("suspended", "prepunch.png", skin=skinChoice)
        self.midPunchImage = Player.load("suspended", "midpunch.png", skin=skinChoice)
        self.punchImage = Player.load("suspended", "punch.png", skin=skinChoice)
        self.longPunchImage = Player.load("suspended", "longpunch.png", skin=skinChoice)
        self.preBlockImage = Player.load("suspended", "preblock.png", skin=skinChoice)
        self.blockImage = Player.load("suspended", "block.png", skin=skinChoice)
        self.lyingImage = Player.load("suspended", "lying.png", skin=skinChoice)

    cssImages = [Player.load("suspended", "idle.png", skin=i) for i in range(6)]
    text = "Suspended Knight" # noel skriv nåt bra
class Can(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Can, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-5, 28-19, 16+5, 32-8]
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

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            if self.useUltCharge():
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                self.image = self.prePunchImage
                self.state = State.idle

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "down"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["2"])
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "down":
            if self.attackFrame == 1:
                Player.growSound.play()
            elif self.attackFrame<100:
                self.image = self.waterImage
                self.attackBox = [13,31,16,32, 1, 0, 0]
                self.yv-=0.9
                self.yv=self.yv*0.95
                self.facingRight = not self.facingRight
                if not (self.pressed["3"] or self.pressed["4"]):
                    self.attackFrame=99
            elif self.attackFrame<109:
                self.image = self.idleImage
                self.facingRight = not self.facingRight
                #self.yv=self.yv*0.95
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
            #self.state = State.idle (wut

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("can", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("can", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("can", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("can", "punch.png", skin=skinChoice)
        self.waterImage = Player.load("can", "water.png", skin=skinChoice)

    cssImages = [Player.load("can", "idle.png", skin=i) for i in range(6)]
    text = "DANSKA BURKEN        (BANNED)"
    helpTexts =[
    "Pro tips:",
    "Press Down to SUPER. It doesn't do much.",
    "Can't double jump."
    ] #An
class Frog(Player):

    def passive(self):
        if self.pressed["4"] and self.attack == "leap" and self.state == 1 and not self.y==288:
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Frog, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-5, 32-16, 16+5, 32-5]
        self.CHARGE=10
        self.init2()

        self.first = [
        [10, self.prePunchImage],
        [15, self.punchImage, [20, 21, 27, 25, 21]],
        [18, self.punchImage],
        [25, self.prePunchImage],
        ]

        self.second = [
        [5, self.preLickImage],
        [13, self.lickImage, [22, 14, 27, 21, 7,50,3,0.5]],
        [18, self.lickImage],
        [25, self.preLickImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "lick"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "leap"

        elif(self.pressed["4"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "shoot"
            else:
                self.state = 0

    def doAttack(self, pressed):
        if self.attack == "punch":
            self.executeAttack(self.first, not self.pressed["1"])
        if self.attack == "lick":
            self.executeAttack(self.second, not self.pressed["2"])
            if self.attackFrame==1:
                Player.lickSound.play()
        if self.attack == "leap":
            if self.attackFrame < 15:
                self.image = self.stunnedImage
                self.attackBox = None        
            elif self.attackFrame == 15: 
                self.image = self.idleImage
                self.xv += (self.facingRight-0.5)*12
                self.yv = -20
            elif self.attackFrame < 500:
                self.image = self.jumpImage
                if self.onGround:
                    self.attackFrame = 500
                    Player.shake=16
            elif self.attackFrame < 510:
                self.image = self.landImage
                self.attackBox = [16-6, 32-8, 16+5, 32-3, 40,40,40,0.8]
            elif self.attackFrame < 520:
                self.image = self.idleImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "ult":
            if self.attackFrame==1:
                Player.ultSound.play()
            if self.attackFrame < 15: 
                self.image = self.stunnedImage
                self.facingRight = not self.facingRight
                self.yv = -4
                self.xv *= 0.8
            elif self.attackFrame == 15:
                self.image = self.idleImage
                self.xv = 0
                self.yv = 16
            elif self.attackFrame < 500:
                self.yv = min(16, self.yv) #max speed but can be knocked for fun
                self.image = self.jumpImage
                if self.onGround:
                    self.attackFrame = 500
                    Player.shake=int(self.yv)
            elif self.attackFrame < 508:
                self.image = self.landImage
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
                self.attackBox = [16-6, 32-8, 16+5, 32-3, 30, 60, 30, 0.8]
            elif self.attackFrame < 518:
                self.image = self.idleImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "shoot":
            if self.attackFrame==1:
                Player.ultSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            if self.attackFrame < 5: 
                self.image = self.stunnedImage
            elif self.attackFrame < 15:
                self.image = self.preUltImage
            elif self.attackFrame == 20:
                Projectile.projectiles.append(Projectile(self, op=True))
                self.image = self.ultImage
            elif self.attackFrame < 30:
                self.image = self.ultImage
                self.attackBox = None
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("frog", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("frog", "stunned.png", skin=skinChoice)
        self.preLickImage = Player.load("frog", "prelick.png", skin=skinChoice)
        self.lickImage = Player.load("frog", "lick.png", skin=skinChoice)
        self.prePunchImage = Player.load("frog", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("frog", "punch.png", skin=skinChoice)
        self.jumpImage = Player.load("frog", "jump.png", skin=skinChoice)
        self.landImage = Player.load("frog", "land.png", skin=skinChoice)
        self.preUltImage = Player.load("frog", "preult.png", skin=skinChoice)
        self.ultImage = Player.load("frog", "ult.png", skin=skinChoice)
        self.projbImage = Player.load("frog", "fly.png", skin=skinChoice)

    cssImages = [Player.load("frog", "idle.png", skin=i) for i in range(6)]
    text = "Toad is toad :)"
    helpTexts =[
    "Pro tips:",
    "Press Down for SUPER.",
    "SUPER while using the leap to",
    " do a stomp dive thing...",
    "Jump forward/backwards before leaping",
    " to change the speed of the leap.",
    "You can eat the flies if you're quick, frog.",
    ] #E
class Monster(Player):

    def confirmedHit(self, damage):
        if self.attack=="tail":
            self.yv=-15

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super(Monster, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-5, 16, 16+5, 32-4]
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [11, self.punch2Image, [21, 22, 26, 25, 27,50,15]],
        [14, self.punch2Image],
        [17, self.prePunchImage],
        [22, self.idleImage],
        ]

        self.second = [
        [15, self.prePunchImage],
        [18, self.punch2Image],
        [21, self.punchImage, [22, 20, 26, 23, 48,90,36]],
        [27, self.punchImage],
        [33, self.punch2Image],
        [38, self.prePunchImage],
        [43, self.idleImage],
        ]

        self.tail = [
        [7, self.preKickImage],
        [13, self.kickImage, [7, 26, 12, 31, 20]],
        [18, self.kickImage],
        [22, self.idleImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "lick"

        if(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "shoot"

        if(self.pressed["3"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"

        if(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "tail"

    def doAttack(self, pressed):
        if self.attack == "lick":
            self.executeAttack(self.first, not self.pressed["1"])
            if self.attackFrame == 6 and self.pressed["1"]:
                self.attack = "lick2"
        if self.attack == "lick2":
            self.executeAttack(self.second, not self.pressed["1"])
        if self.attack == "shoot":
            if self.attackFrame < 18:
                self.image = self.prePunchImage
                self.attackBox = None
            elif self.attackFrame < 23:
                self.image = self.punch2Image
            elif self.attackFrame == 23:
                self.image = self.punchImage
                Projectile.projectiles.append(Projectile(self))
            elif self.attackFrame < 30:
                self.image = self.punchImage
            elif self.attackFrame < 36:
                self.image = self.punch2Image
            elif self.attackFrame < 43:
                self.image = self.prePunchImage
            elif self.attackFrame < 46:
                self.image = self.idleImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "tail":
            self.executeAttack(self.tail, not self.pressed["4"])

        if self.attack == "ult":
            if self.attackFrame==1:
                self.ultCharge = self.CHARGE
                Player.ultSound.play()
                Player.growSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            elif self.ultCharge>0:
                self.ultCharge-=0.2
                self.yv-=0.4
                self.image = self.prePunchImage
                self.hp=min(self.hp+0.5, self.maxhp)
                self.facingRight = not self.facingRight
            else:
                self.ultCharge = 0
                self.state = State.idle
                self.image = self.idleImage

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("monster", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("monster", "stunned.png", skin=skinChoice)
        self.prePunchImage = Player.load("monster", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("monster", "punch.png", skin=skinChoice)
        self.punch2Image = Player.load("monster", "punch2.png", skin=skinChoice)
        self.preKickImage = Player.load("monster", "prekick.png", skin=skinChoice)
        self.kickImage = Player.load("monster", "kick.png", skin=skinChoice)
        self.projbImage = Player.load("monster", "proj.png", skin=skinChoice)

    cssImages = [Player.load("monster", "idle.png", skin=i) for i in range(6)]
    text = "Uses kinetic acid produced in the tongue to perform various strategies."
    helpTexts =[
    "Pro tips:",
    "You can eat your own projectiles.",
    "Jump forward/backwards while shooting",
    "to change the speed of projectiles.",
    "SUPER makes you heal. (and low gravity!)",
    ] #Al
class Penguin(Player):

    def passive(self):
        if self.wizard:
            self.idleImage = self.wizardImage
            self.stunnedImage = self.stunnedWizardImage
            self.xspeed = 2
            self.canDoubleJump = True
        else:
            self.idleImage = self.ninjaImage
            self.stunnedImage = self.stunnedNinjaImage
            self.xspeed = 3.5
            self.canDoubleJump = False

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Penguin, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.xspeed = 3.5
        self.wizard = False
        self.init2()

        self.first = [
        [6, self.prePunchImage],
        [11, self.punchImage, [18, 19, 24, 23, 16]],
        [20, self.punchImage],
        [25, self.prePunchImage],
        ]

        self.second = [
        [12, self.prePunchImage],
        [21, self.punchImage, [18, 19, 24, 23, 38]],
        [30, self.punchImage],
        [36, self.ninjaImage],
        [44, self.prePunchImage],
        ]

        self.magic = [
        [10, self.preMagicImage],
        [14, self.midMagicImage],
        [70, self.magicImage, [23,17,24+6,17+6, 10,10,10,0], True],
        [78, self.magicImage],
        [85, self.midMagicImage],
        [95,self.preMagicImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            if self.wizard:
                self.attack = "magic"
            else:
                self.attack = "jab"

        if(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            if self.wizard:
                self.attack = "throw"
            else:
                self.attack = "punch"

        if(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            if self.wizard:
                if self.useUltCharge():
                    self.attack = "ult"
                else:
                    self.state = State.idle
            else:
                self.attack = "shoot"

        if(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "switch"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
        if self.attack == "magic":
            self.executeAttack(self.magic, not self.pressed["1"])
            if self.attackFrame==17 and self.wizard:
                Player.bzzzSound.play()
                Player.growSound.play()
            if 17<self.attackFrame<70 and self.wizard:
                self.yv*=0.5
        if self.attack == "shoot":
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
            elif self.attackFrame < 41:
                self.image = self.punchImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "throw":
            if self.attackFrame < 10:
                self.image = self.preHatImage
                self.attackBox = None
            elif self.attackFrame < 22: 
                self.image = self.midHatImage
            elif self.attackFrame == 22:
                self.wizard = False
                self.image = self.midHatImage
                Projectile.projectiles.append(Projectile(self))
            elif self.attackFrame < 42:
                self.image = self.punchImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

        if self.attack == "switch":
            self.ultCharge+=0.1
            if self.attackFrame < 12:
                self.image = self.preHatImage
            elif self.attackFrame == 12:
                self.attackBox = [9,15,14,19, 10]
                self.wizard = not self.wizard
            elif self.attackFrame < 15+6*self.wizard:
                self.attackBox = None
                self.image = self.idleImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None
        if self.attack == "ult":
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
                #self.yv-=0.5
                self.image = self.wizardImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def loadImages(self, skinChoice):
        self.ninjaImage = Player.load("penguin", "ninja.png", skin=skinChoice)
        self.idleImage = self.ninjaImage
        self.stunnedNinjaImage = Player.load("penguin", "stunnedninja.png", skin=skinChoice)
        self.prePunchImage = Player.load("penguin", "prepunch.png", skin=skinChoice)
        self.punchImage = Player.load("penguin", "punch.png", skin=skinChoice)
        self.projaImage = Player.load("penguin", "star.png", skin=skinChoice)
        self.projbImage = Player.load("penguin", "hat.png", skin=skinChoice)
        self.preHatImage = Player.load("penguin", "prehat.png", skin=skinChoice)
        self.midHatImage = Player.load("penguin", "midhat.png", skin=skinChoice)
        self.wizardImage = Player.load("penguin", "wizard.png", skin=skinChoice)
        self.stunnedWizardImage = Player.load("penguin", "stunnedwizard.png", skin=skinChoice)
        self.preMagicImage = Player.load("penguin", "premagic.png", skin=skinChoice)
        self.midMagicImage = Player.load("penguin", "midmagic.png", skin=skinChoice)
        self.magicImage = Player.load("penguin", "magic.png", skin=skinChoice)
        self.haloImage = Player.load("penguin", "halo.png", skin=skinChoice)
        self.halo2Image = Player.load("penguin", "halo2.png", skin=skinChoice)

    cssImages = [Player.load("penguin", "ninja.png", skin=i) for i in range(6)]
    text = "Is a wizard sometimes."
    helpTexts =[
    "Pro tips:",
    "Hold Attack1 to attack longer.",
    "You must be a wizard to use SUPER",
    "Can double jump only while wizard.",
    "Jump forward/backwards while throwing",
    "to change the speed of projectiles.",
    ] #Al
class Turtle(Player):

    def passive(self):
        self.yv += 0.2
        if self.state == State.stunned:
            self.yv -= 0.1
            self.stun-=0.2
        if self.state == State.idle and self.attackFrame>1:
            self.armor = False

    def confirmedHit(self, damage):
        if self.attack=="ult":
            self.yv*=0.1

    def hurt(self, player, damage, knockback=None, stun=None, angle=0):
        if self.armor:
            if knockback==None:
                knockback = damage
            if stun==None:
                stun = damage
            super().hurt(player, damage//2, knockback//2, stun//2, angle)
        else:
            super().hurt(player, damage, knockback, stun, angle)

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super(Turtle, self).__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-6, 21, 16+6, 21+7]
        self.xspeed = 1
        self.init2()
        self.canDoubleJump = False
        self.armor = False

        self.first = [
        [3, self.idleImage],
        [5, self.punchImage, [21, 22, 25, 26, 11]],
        [10, self.punchImage],
        [15, self.idleImage],
        ]

        self.second = [
        [5, self.preshellImage],
        [10, self.shellImage],
        [20, self.dashImage, [7, 24, 7+17, 27, 28]],
        [25, self.dashImage],
        [30, self.shellImage],
        [35, self.preshellImage],
        ]

        self.spike = [
        [5, self.preshellImage],
        [10, self.prespikeImage],
        [90, self.spikeImage, [10, 20, 10+12, 24, 20,40,20,0.3], True],
        [96, self.prespikeImage],
        [102, self.shellImage],
        [108, self.preshellImage],
        ]

        self.dash = [
        [5, self.preshellImage],
        [55, self.dashImage, [21, 22, 25, 26, 9]],
        [60, self.preultImage, [21, 22, 25, 26, 9]],
        [71, self.ultImage, [8, 20, 26, 26, 30, 45]],
        [75, self.preultImage],
        [79, self.shellImage],
        [83, self.preshellImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "punch"

        elif(self.pressed["3"]):
            if self.useUltCharge():
                self.state = 1
                self.attackFrame = 1
                self.attack = "ult"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "spikes"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])

        if self.attack == "punch":
            self.executeAttack(self.second, not self.pressed["2"])
            if 10<self.attackFrame<20:
                self.xv=(self.facingRight-0.5)*12
            if self.attackFrame==10:
                self.yv-=5
            if self.attackFrame==5:
                self.armor = True
            if self.attackFrame==30:
                self.armor = False

        if self.attack == "spikes":
            self.executeAttack(self.spike, not self.pressed["4"])
            if 10<self.attackFrame<90:
                self.armor = True
                if self.pressed["d"]:
                    self.xv=1
                    self.facingRight = True
                if self.pressed["a"]:
                    self.xv=-1
                    self.facingRight = False
            else:
                self.armor = False
            self.yv*=0.9

        if self.attack == "ult":
            if self.attackFrame == 1:
                self.invincible=True
                Player.ultSound.play()
            self.executeAttack(self.dash, not self.pressed["3"])
            if self.attackFrame == 61:
                self.invincible=False
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

            if self.attackFrame < 61:
                self.xv = (self.facingRight-0.5)*20
                self.yv-=0.5

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("turtle", "idle.png", skin=skinChoice)
        self.preshellImage = Player.load("turtle", "preshell.png", skin=skinChoice)
        self.shellImage = Player.load("turtle", "shell.png", skin=skinChoice)
        self.spikeImage = Player.load("turtle", "spike.png", skin=skinChoice)
        self.prespikeImage = Player.load("turtle", "prespike.png", skin=skinChoice)
        self.dashImage = Player.load("turtle", "dash.png", skin=skinChoice)
        self.ultImage = Player.load("turtle", "ult.png", skin=skinChoice)
        self.preultImage = Player.load("turtle", "preult.png", skin=skinChoice)
        self.stunnedImage = Player.load("turtle", "stunned.png", skin=skinChoice)
        self.punchImage = Player.load("turtle", "punch.png", skin=skinChoice)

    cssImages = [Player.load("turtle", "idle.png", skin=i) for i in range(6)]
    text = "Were chosen to fight in the arena because of their indestructable shells."
    helpTexts =[
    "Pro tips:",
    "Hold Down to take less damage.",
    "Attack3 is the SUPER.",
    ] #Ar
class Cat(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-3, 32-16, 16+3, 32-4]
        self.init2()
        self.canDoubleJump = False
        #self.CHARGE= 10

        self.first = [
        [5, self.prePunchImage, None, True],
        [8, self.punchImage, [16, 20, 23, 25, 14]],
        [13, self.punchImage],
        [19, self.prePunchImage],
        ]

        self.second = [
        [18, self.preBiteImage],
        [23, self.biteImage, [32-9-7, 32-8-6, 32-9, 32-8, 29]],
        [33, self.biteImage],
        ]

        self.long = [
        [9, self.preTailImage],
        [14, self.tailImage],
        [19, self.tailImage, [32-8, 32-10, 32-2, 32-5, 22, -33, 22]],
        [29, self.preTailImage],
        ]

        self.teleport = [
        [9, self.preMagicImage],
        [23, self.magicImage],
        [29, self.preMagicImage],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

        elif(self.pressed["2"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "lick"

        elif(self.pressed["3"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "long"

        elif(self.pressed["4"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "down"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])

        if self.attack == "lick":
            self.executeAttack(self.second, not self.pressed["2"])
            if self.attackFrame==1:
                self.yv-=4
            if self.attackFrame<9:
                if self.pressed["2"]:
                    self.image = self.stunnedImage
            if self.attackFrame==9:
                if self.pressed["2"] and self.useUltCharge():
                    self.attack = "ult"
                    self.attackFrame = 1
                else:
                    self.xv+=(self.facingRight-0.5)*8
        if self.attack == "long":
            self.executeAttack(self.long, not self.pressed["3"])
            if self.attackFrame==17: #15
                if (self.x<200-128 and not self.facingRight) or (self.x>800-128 and self.facingRight):
                    self.xv = (self.facingRight-0.5)*7
                    self.yv = -12
        if self.attack == "down":
            self.executeAttack(self.teleport, not self.pressed["4"])
            if self.attackFrame==12:
                self.invincible = True
            if self.attackFrame==16:
                self.x+=(self.facingRight-0.5)*400
                self.facingRight = not self.facingRight
            if self.attackFrame==20:
                self.invincible = False
            if self.attackFrame>12 and self.yv>1:
                self.yv-=0.9

        if self.attack == "ult":
            LASERTIME = 60
            if self.attackFrame == 1:
                self.image = self.stunnedImage
                self.attackBox = None
                Player.ultSound.play()
                Player.bzzzSound.play()
                pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            if self.attackFrame < 10:
                self.image = self.stunnedImage
            elif self.attackFrame < LASERTIME:
                self.image = self.ultImage
                self.xv *= 0.9
                self.yv = 0
                if self.attackFrame % 3 == 0:
                    Projectile.projectiles.append(Projectile(self))
            elif self.attackFrame < LASERTIME + 8:
                self.image = self.idleImage
            elif self.attackFrame < LASERTIME + 15:
                self.image = self.idleImage
            else:
                self.state = State.idle
                self.image = self.idleImage
                self.attackBox = None

    def confirmedHit(self,damage):
        if self.attack == "lick":
            self.hp=min(self.hp+10, self.maxhp)
            #self.ultCharge+=10
        if self.attack == "long":
            self.xv = (self.facingRight-0.5)*10
            self.yv = -8

    def loadImages(self, skinChoice):
        self.idleImage = Player.load("cat", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("cat", "stunned.png", skin=skinChoice)
        self.punchImage = Player.load("cat", "punch.png", skin=skinChoice)
        self.prePunchImage = Player.load("cat", "prepunch.png", skin=skinChoice)
        self.tailImage = Player.load("cat", "tail.png", skin=skinChoice)
        self.preTailImage = Player.load("cat", "pretail.png", skin=skinChoice)
        self.biteImage = Player.load("cat", "bite.png", skin=skinChoice)
        self.preBiteImage = Player.load("cat", "prebite.png", skin=skinChoice)
        self.magicImage = Player.load("cat", "magic.png", skin=skinChoice)
        self.preMagicImage = Player.load("cat", "premagic.png", skin=skinChoice)
        self.ultImage = Player.load("cat", "ult.png", skin=skinChoice)
        self.projbImage = Player.load("cat", "laser.png", skin=skinChoice)

    cssImages = [Player.load("cat", "idle.png", skin=i) for i in range(6)]
    text = "The curse of the spirit of the cat."
    helpTexts =[
    "Pro tips:",
    "Biting heals you.",
    "You can grab onto walls with your tail btw.",
    "Hold Bite for SUPER."
    ] #J
class Weight(Player):

    def passive(self):
        if self.pressed["4"]:
            self.yv += 3
            self.yv = min(self.yv, 12)
            self.image = self.downImage
        else:
            self.yv -= 0.1
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls,joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [11, 17, 21, 28]
        self.init2()
        self.canDoubleJump = False
        #self.CHARGE= 10

        self.first = [
        [5, self.idleImage, None, True],
        ]

    def keys(self):
        super().keys()
        if(self.pressed["1"]):
            self.state = 1
            self.attackFrame = 1
            self.attack = "jab"

    def doAttack(self, pressed):
        if self.attack == "jab":
            self.executeAttack(self.first, not self.pressed["1"])
    
    def loadImages(self, skinChoice):
        self.idleImage = Player.load("weight", "idle.png", skin=skinChoice)
        self.stunnedImage = Player.load("weight", "idle.png", skin=skinChoice)
        self.downImage = Player.load("weight", "down.png", skin=skinChoice)

    cssImages = [Player.load("weight", "idle.png", skin=i) for i in range(6)]
    text = "The curse of the spirit of the cat." #S

class Pillar(Player):

    def confirmedHit(self, damage):
        pass
        self.yv=-10 #-10 if we dont want the infinite
        print(self.yv)

    def passive(self):
        if random.randint(1,30)==1:
            if countPlayers()<2:
                if self in Player.players:
                    Player.players.remove(self)

    def __init__(self, x, y, facingRight, controls, joystick=None,skin=0):
        super().__init__(x, y, facingRight, controls, joystick, skin)
        self.box = [16-2, 1, 16+2, 30]
        self.attackBox = [16-3,31,16+3,32,20,10]
        self.maxhp=0
        self.durability = 200
        self.CHARGE=10000
        self.init2()

    def action(self):
        self.passive()

    def hurt(self, player, damage, knockback=0, stun=0, angle=0):
        self.durability-=damage
        if self.durability<=0:
            if self in Player.players:
                Player.players.remove(self)
            #player.confirmedHit(damage)
            playHitSound(State.volume*damage*0.01)
            Player.shake+=int(damage)
    
    def loadImages(self, skinChoice):
        idle1Image = Player.load("pufferfish", "pillar.png", skin=skinChoice)
        idle2Image = Player.load("pufferfish", "pillar2.png", skin=skinChoice)
        self.idleImage = random.choice([idle1Image, idle2Image])

legalClasses = [
Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Crawler, Ninja, Bird, Robot, Lizard, Golem, Alien, Glitch, Frog, Monster, Penguin, Turtle, Cat,
]

allClasses = legalClasses + [
Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Crawler, Ninja, Bird, Robot, Lizard, Golem, Alien, Glitch, Rat, Skugg, Can, Frog, Monster, Penguin, Turtle, Cat,
] + legalClasses

def restart():
    Player.players = []
    choices = []
    skinChoice = 0
    skinChoices = []
    num = 0
    myfont = pygame.font.SysFont('Calibri', 100)
    myfont2 = pygame.font.SysFont('Calibri', 20)
    pressed = pygame.key.get_pressed()
    while State.jump_out == False and not pressed[pygame.K_q]:
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
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            skinChoice = (skinChoice+1)%6
            lag+=0.1
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            skinChoice = (skinChoice-1)%6
            lag+=0.1
        if pressed[pygame.K_1]:
            Player.AIoption+=1
            if Player.AIoption==4:
                Player.AIoption=0
                State.playerCount+=1
            if Player.AIoption==3:
                State.playerCount-=1
            lag+=0.2
        if pressed[pygame.K_2]:
            Player.AI2option+=1
            if Player.AI2option==4:
                Player.AI2option=0
                State.playerCount+=1
            if Player.AI2option==3:
                State.playerCount-=1
            lag+=0.2
        if pressed[pygame.K_r]:
            choices.append(random.choice(legalClasses))
            skinChoices.append(random.randint(1,5)*(random.random()<skinChance))
            #num=0
            if len(choices)>=State.playerCount:
                return (choices, skinChoices)
            lag+=0.5
        if pressed[pygame.K_BACKSPACE] and len(choices)>0:
            choices.pop()
            skinChoices.pop()
            #num=0
            lag+=0.5
        if pressed[pygame.K_SPACE] or pressed[pygame.K_RETURN]:
            choices.append(pickCharacter(num,pressed[pygame.K_b]))
            skinChoices.append(skinChoice)
            skinChoice = (skinChoice+1)%6
            #num=0
            if len(choices)>=State.playerCount:
                return (choices, skinChoices)
            lag+=0.5

        #draw
        gameDisplay.fill((100,100,100))
        pygame.draw.rect(gameDisplay,(200,200,200),(400+64,0,16*8,200+28*8),0)
        for i in range(len(choices)):
            gameDisplay.blit(choices[i].cssImages[skinChoices[i]][1], (100*i, 0))
        for i in [-4,-3,-2,-1,0,1,2,3,4]:
            gameDisplay.blit(allClasses[(num-i)%len(allClasses)].cssImages[skinChoice*(i==0)][1], (400-104*i, 200))
        currentFocusedClass = allClasses[num%len(allClasses)]
        name = currentFocusedClass.__name__
        if name == "Green":
            name = ["Green","Red","Blue","Green","Blue","Red"][skinChoice%6]
        text = currentFocusedClass.text
        if hasattr(currentFocusedClass,"helpTexts"):
            if pressed[pygame.K_h]:
                helpTexts = currentFocusedClass.helpTexts
            else:
                helpTexts = ["(press H for pro tips)"]
        if len(choices)==0:
            helpLetterDown = ["S","Down"][(Player.AIoption>=2)]
            if Player.AIoption<2:
                helpLetters = [["I","O","P"],["X","C","V"]][Player.AIoption]
            else:
                helpLetters = [["X","C","V"],["I","O","P"]][Player.AI2option%2]
        else:
            helpLetterDown = ["S","Down"][(Player.AI2option<2)]
            if Player.AI2option<2:
                helpLetters = [["X","C","V"],["I","O","P"]][Player.AI2option]
            else:
                helpLetters = [["I","O","P"],["X","C","V"]][Player.AIoption%2]
        helpTexts = [helpText.replace("Attack1", helpLetters[0]).replace("Attack2", helpLetters[1]).replace("Attack3", helpLetters[2]).replace("Down", helpLetterDown) for helpText in helpTexts]
        textsurface = myfont.render(name, True, (0, 0, 0))
        textsurface2 = myfont2.render(text, True, (0, 0, 0))
        textsurfacesHelp = [myfont2.render(helpText, True, (0, 0, 0)) for helpText in helpTexts]
        textsurfaceAI = myfont2.render("player 1: "+["WASD, IOP","WASD, XCV","AI","Off"][Player.AIoption]+"                        (press 1)", True, (0,0,0))
        textsurfaceAI2 = myfont2.render("player 2: "+["Arrowkeys, XCV","Arrowkeys, IOP","AI","Off"][Player.AI2option]+"                (press 2)", True, (0,0,0))
        gameDisplay.blit(textsurface,(545-len(name)*24,450))
        gameDisplay.blit(textsurface2,(10,570))
        for i in range(len(textsurfacesHelp)):
            gameDisplay.blit(textsurfacesHelp[i],(600,10+ 20*i))
        gameDisplay.blit(textsurfaceAI,(10,10))
        gameDisplay.blit(textsurfaceAI2,(10,50))

        pygame.display.update()
        clock.tick(60)
        time.sleep(lag)
    
    pygame.quit()
    quit()

gameDisplay = pygame.display.set_mode((1000, 600),)# pygame.FULLSCREEN)
backgrounds = []
for name in ["LDbackground.png","LDbackground2.png","background4.png","LDbackground.png","LDbackground2.png","background4.png","background.png","background2.png","background3.png"]:
    background = pygame.image.load(os.path.join(filepath, "textures", name))
    background = pygame.transform.scale(background, (1000, 600))
    backgrounds.append(background)
    backgrounds.append(pygame.transform.flip(background, True, False))
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
State.playerCount = 2+len(sticks)
State.frameRate = 60
State.jump_out = False
Player.AIoption = 1 #0:XCV 1:IOP 2:ai 3:off
Player.AI2option = 1 #0:IOP 1:XCV 2:ai 3:off
while State.jump_out == False:

    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            State.jump_out = True
    if Player.freezeTime:
        time.sleep(Player.freezeTime)
        Player.freezeTime=0
    if len(Player.players)<2 or pressed[pygame.K_ESCAPE]:
        choices, skinChoices = restart()
        
        if Player.AIoption != 3:
            if Player.AIoption == 0:
                choices[0](200, 300, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_i, "2":pygame.K_o,"3":pygame.K_p,"4":pygame.K_s},skin=skinChoices[0])
            else:
                choices[0](200, 300, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_s},skin=skinChoices[0])
            if Player.AIoption == 2:
                Player.players[-1].random=1

        humansBefore=len(Player.players)
        if Player.AI2option != 3:
            if Player.AI2option == 0:
                choices[humansBefore](600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_x,"2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_DOWN},skin=skinChoices[humansBefore])
            else:
                choices[humansBefore](600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_i,"2":pygame.K_o,"3":pygame.K_p,"4":pygame.K_DOWN},skin=skinChoices[humansBefore])
            if Player.AI2option == 2:
                Player.players[-1].random=1
        humansBefore=len(Player.players)
        for i in range(len(sticks)):
            choices[humansBefore+i](400, 300, False, {"w":0,"3":4,"4":5}, sticks[i],skinChoices[humansBefore+i])
        AiFocus = 0 #cannot be 1!!!! or it crashes when ai is alone.
        #Player.players[0].hp = 50

        currentBackground = random.choice(backgrounds)
        Platform.restart()
        Player.shake=0
        Projectile.projectiles=[]
        pygame.display.update()
    
    #shake
    if Player.shake>0 and not Player.freezeTime:
        Player.shake-=2
        shakeX = (random.random()-0.5)*Player.shake
        shakeY = (random.random()-0.5)*Player.shake
    else:
        shakeX = 0
        shakeY = 0
    #background
    gameDisplay.blit(currentBackground, (int(shakeX),int(shakeY)))
    
    #draw platforms
    for player in Platform.platforms:
        player.draw()

    #draw flashes
    pressed = pygame.key.get_pressed()
    for player in Player.players:
        player.getPressed(pressed)
        player.action()
    for player in Player.players+Projectile.projectiles:
        player.physics()

    #draw players
    for player in Projectile.projectiles+Player.players:
        player.draw()

    pygame.display.update()
    clock.tick(State.frameRate)
    
    
pygame.quit()
#quit() #bad for pyinstaller
