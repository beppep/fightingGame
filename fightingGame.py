import pygame
import time
import random
import os
clock = pygame.time.Clock()
filepath=""
#Adam "jag tycker ändå det kan funka med ett cirkelargument."
SOUND_PATH = os.path.join(filepath, "sounds")

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
    
    pygame.mixer.music.load("music.wav") #must be wav 16bit and stuff?
    pygame.mixer.music.set_volume(v*0.1)
    pygame.mixer.music.play(-1)

def playHitSound(vol):
    i = random.randint(0,1)
    sound = Player.hitSounds[i]
    sound.set_volume(vol*(i+1))
    sound.play()

def endEffect():
    pygame.draw.rect(gameDisplay, (200, 0, 100), (0,0,1000,600), 0)
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
            self.box = [32-11, 18, 32-6, 32-9, 20+40*op, 20+40*op, 20+self.owner.attackFrame*op]
            self.x-=self.xv*2
        if isinstance(self.owner, Robot):
            self.xv = (self.facingRight-0.5) * 20
            self.box = [32-8, 16, 32-4, 19, 12+3*self.op, 12]
            self.x-=self.xv*3
        if isinstance(self.owner, Alien):
            self.xv = (self.facingRight-0.5) * -20
            self.box = [3, 14, 7, 17, 7,0,20]
            self.x-=self.xv*4
            self.yv = .5
        if isinstance(self.owner, Glitch):
            self.xv = (self.facingRight-0.5) * 40
            self.box = [23, 19, 32, 23, 35]
            self.x-=self.xv*2
        if isinstance(self.owner, Monster):
            self.xv = (self.facingRight-0.5) * 8
            self.yv = -0.7
            self.box = [32-11, 19, 32-7, 22, 15, -60, 0]
        if isinstance(self.owner, Penguin):
            self.y-=10
            if self.op:
                self.xv = (self.facingRight-0.5) * 16
                self.box = [19, 20, 19+3, 20+3, 9]
                self.image = self.owner.projaImage
            else:
                self.xv = (self.facingRight-0.5) * 8
                self.x+=self.owner.xv
                self.yv = 0.4
                self.box = [18+1,18,18+6,18+5, 23]
        if isinstance(self.owner, Sad):
            self.box = [16-2,15,16+3,20, 50, 10, 50]
            self.x+=(self.owner.facingRight-0.5)*120
            self.xv=(self.owner.facingRight-0.5)*0
            self.lifetime = 0
        if isinstance(self.owner, Animals):
            self.box = [24,22,25,23, 3,15,10]
            self.y+=(self.owner.attackFrame%7)*6-16
            self.xv=(self.owner.facingRight-0.5) * 16
            self.x-=self.xv
        self.xv+=self.owner.xv

    def keys(self, pressed):
        nevercalled
        pass
    def confirmedHit(self,damage):
        pass   
    def draw(self):
        if self.op:
            gameDisplay.blit(self.image[self.facingRight], (int(self.x+random.randint(-1,1)*8+shakeX), int(self.y+random.randint(-1,1)*8+shakeY)))
        else:
            gameDisplay.blit(self.image[self.facingRight], (int(self.x+shakeX), int(self.y+shakeY)))
        """
        if random.random()<.1:
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        """

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
        if self.hurtboxes[2]<100 or self.hurtboxes[0]>900:
            if self in Projectile.projectiles:
                Projectile.projectiles.remove(self)
        #death self by collision with hitboxes and such
        if isinstance(self.owner, Sad):
            if self.lifetime<40:
                self.lifetime+=1
                print(self.lifetime)
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
                        if (player.state==3 and type(player) == Lizard) or player.state==4 and type(player)==Golem or (player.state in [1,2] and type(player) in [Frog, Monster, Animals]):
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
        self.xspeed=2.5
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
        """
        if(self.pressed["5"] and self.ultCharge>self.CHARGE):
            self.state = 5
            self.attackFrame = 0
            self.ultCharge = 0
        """
    def grounded(self):
        pass #before yv=0
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
        self.ultCharge+=0.1 #?

    def getPressed(self, pressed):
        if self.random:
            if AiFocus:
                target = Player.players[0]
            else:
                enemies = Player.players[:]
                enemies.remove(self)
                target = random.choice(enemies)
            if random.random()<0.1:
                self.pressed["d"] = random.randint(0,1)
            if random.randint(0,20)==0:
                self.pressed["w"] = (target.y < self.y) ^ (random.random()<0.5)
            if not self.onGround:
                self.pressed["w"] = random.randint(0,1)

            attacking=False
            for i in ["1","2","3","4","5"]:
                #self.pressed[i] = (random.randint(0,15+10*int(i))==0) ^ (self.state!=State.idle)
                if random.random()<0.02:
                    self.pressed[i] = (random.randint(0,3)==0)
                if self.pressed[i]:
                    self.pressed["d"] = target.x > self.x
                    if isinstance(self, Alien) and (self.pressed["3"] or self.pressed["4"]):
                        self.pressed["d"] = target.x < self.x
                    if isinstance(self, Lizard) and self.pressed["4"]:
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
                self.xv+=self.xspeed*1.2
                #self.xv=self.xspeed*2
            else:
                self.xv=min(self.xspeed*2, self.xv+0.2)
            self.facingRight = True
        elif(self.pressed["a"]):
            if self.onGround:
                #self.xv=-self.xspeed*2
                self.xv-=self.xspeed*1.2
            else:
                self.xv=max(-self.xspeed*2, self.xv-0.2)
            self.facingRight = False

        if(self.pressed["w"]):
            if (self.onGround):
                self.yv=-17.1
            if self.doubleJump==-1 and self.canDoubleJump:
                self.yv=-13.6
                self.doubleJump=0
                theImage = Player.hurtImage2[not self.facingRight]
                gameDisplay.blit(theImage, (int(self.x), int(self.y)+40))

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
            if not isinstance(self,Lizard) and not isinstance(self, Monster) and not (isinstance(self,Penguin) and not self.wizard):
                self.state = 5
                self.attackFrame = 0
                self.ultCharge = 0
        
        self.ultCharge+=0.1
        #print(Player.players.index(self),":",self.ultCharge,"%")

    def physics(self):

        self.x+=self.xv
        self.hurtboxes = self.generateBox(self.box)
        #self.hurtboxes[3]+=self.flyingHeight
        self.hurtboxes[0]+=8
        self.hurtboxes[2]-=8

        for player in Player.players+Platform.platforms:
            otherbox=player.hurtboxes[:]
            #otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.xv==0:
                    pass
                elif self.xv<0:
                    self.x += otherbox[2]-self.hurtboxes[0]
                    #print(self.yv)
                    #print(player.yv)
                else:
                    self.x += otherbox[0]-self.hurtboxes[2]
                self.xv = 0
        if self.hurtboxes[2]>904:
            self.x += 904-self.hurtboxes[2]
            if self.stun and not isinstance(self,Golem): #bouncy walls
                self.xv=-self.xv*0.5
                self.yv=-abs(self.xv)
            else:
                self.xv=0
        if self.hurtboxes[0]<96:
            self.x += 96-self.hurtboxes[0]
            if self.stun and not isinstance(self,Golem):
                self.xv=-self.xv*0.5
                self.yv=-abs(self.xv)
            else:
                self.xv=0

        self.y+=self.yv
        self.hurtboxes = self.generateBox(self.box)
        #self.hurtboxes[3]+=self.flyingHeight
        self.hurtboxes[0]+=8
        self.hurtboxes[2]-=8

        self.onGround=False
        for player in Player.players+Platform.platforms:
            otherbox=player.hurtboxes[:]
            #otherbox[3]+=player.flyingHeight
            if self.collide(otherbox) and not player==self:
                if self.yv<=0:
                    self.y+=otherbox[3]-self.hurtboxes[1]
                    self.yv=0
                #elif self.yv==0:
                 #   pass 
                elif self.yv>=0:
                    self.y+=otherbox[1]-self.hurtboxes[3]
                    self.grounded()
                    self.yv=0.32
                    self.xv=self.xv*0.5
                    self.onGround=True
                    self.doubleJump=True

        if self.hurtboxes[3]+self.flyingHeight>504:
            self.y+=504-self.hurtboxes[3]-self.flyingHeight
            self.grounded()
            self.yv=0.33
            self.xv=self.xv*0.5
            self.onGround=True
            self.doubleJump = True
        else:
            #unindent makes bird wobble here (no?
            self.yv+=0.797
            self.yv*=0.97
            #happens all the time?
        
        if not self.onGround and self.doubleJump==1 and not self.pressed["w"]:
            self.doubleJump = -1 #ready

        self.hurtboxes = self.generateBox(self.box)
        if self.attackBox:
            self.hitboxes = self.generateBox(self.attackBox)
        else:
            self.hitboxes = None

        #self.attackBox= None
        if not (self.stun or self.invincible):
            for player in Player.players+Projectile.projectiles:
                if player.hitboxes and not player == self and not (isinstance(player, Projectile) and isinstance(player.owner, Sad) and player.lifetime<40):
                    if self.collide(player.hitboxes):
                        if(len(player.hitboxes)==7):
                            self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5],stun=player.hitboxes[6])
                        elif(len(player.hitboxes)==6):
                            self.hurt(player, player.hitboxes[4],knockback=player.hitboxes[5]) # player/player.owner for ult charge. bad for pos
                        else:
                            self.hurt(player, player.hitboxes[4])# .owner for ult charge. bad for pos
                        if isinstance(player, Projectile):
                            Projectile.projectiles.remove(player)

    def hurt(self, player, damage, knockback=None, stun=None):
        if(self.invincible):
            print("shouldnt be called by physics() then?")
            return
        player.confirmedHit(damage)
        playHitSound(State.volume*damage*0.01)
        if(knockback==None):
            knockback=damage
        if stun==None:
            stun=knockback
        self.facingRight = player.x>self.x #not player.facingRight

        self.hp -= damage
        Player.hitLag = damage*0.003
        if stun:
            self.state = State.stunned
            self.image = self.stunnedImage
            self.attackFrame = 0
            if self.hp<=0:
                if not (isinstance(self,Tree) and not self.isLastTree()):
                    endEffect()
        elif self.hp<=0:
            endEffect()
            Player.players.remove(self)
        self.stun = max(self.stun, abs(stun))
        if knockback:
            self.yv=-abs(knockback*0.2)
            self.xv=knockback*(self.facingRight-0.5)*-0.2
        #effects
        Player.shake+=int(damage)
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
        return new

    def collide(self, otherBox):
        glitchConstant=1 #replicatable glitch with constant 1 and >= and can
        if self.hurtboxes[2]>otherBox[0]+glitchConstant and self.hurtboxes[0]<otherBox[2]-glitchConstant:
            if self.hurtboxes[3]>otherBox[1]+glitchConstant and self.hurtboxes[1]<otherBox[3]-glitchConstant:
                return True
        return False

    def load(playerName, textureName):
        image = pygame.image.load(os.path.join(filepath, "textures", playerName, textureName))
        """
        #print(image.get_palette())
        for i in range(32):
            for j in range(32):
                #color = image.get_at((i,j))
                #if not color == (0,0,0,255):
                color=pygame.Color(255,255,255,255)
                image.set_at((i,j),color)
        """
        image = pygame.transform.scale(image, (Player.SCALE*32, Player.SCALE*32))
        return (pygame.transform.flip(image, True, False), image)

    def draw(self):
        factor = 0.3
        leftEdge=int((self.hurtboxes[0]+self.hurtboxes[2]-self.maxhp*factor)*0.5+shakeX)
        if not self.invisible and self.ultCharge>1:
            if self.ultCharge>self.CHARGE:
                color = (255,255,255)
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
        """
        if random.random()<0.9: #yellow
            if self.hitboxes:
                pygame.draw.rect(gameDisplay, (255, 255, 0), \
                (self.hitboxes[0]+shakeX,self.hitboxes[1]+shakeY,self.hitboxes[2]-self.hitboxes[0],self.hitboxes[3]-self.hitboxes[1]), 0)
        """
    hurtImage = pygame.image.load(os.path.join(filepath, "textures", "effect.png"))
    hurtImage = pygame.transform.scale(hurtImage, (8*32, 8*32))
    hurtImage = (pygame.transform.flip(hurtImage, True, False), hurtImage)
    hurtImage2 = pygame.image.load(os.path.join(filepath, "textures", "effect2.png"))
    hurtImage2 = pygame.transform.scale(hurtImage2, (8*32, 8*32))
    hurtImage2 = (pygame.transform.flip(hurtImage2, True, False), hurtImage2)
    text = ""
    shake = 0

class Puncher(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Puncher, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Puncher.idleImage
        self.xspeed = 2.5
        self.init2()
        self.canDoubleJump = True

        self.first = [
        [6, self.midPunchImage, None, True],
        [9, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 19]],
        [18, self.punchImage],
        [25, self.midPunchImage],
        ]

        self.second = [
        [10, self.prePunchImage],
        [16, self.midPunchImage],
        [19, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 50]],
        [34, self.punchImage],
        [51, self.midPunchImage],
        ]

        self.long = [
        [19, self.prePunchImage],
        [90, self.prePunchImage, None, True],
        [95, self.midPunchImage],
        #[100, self.midPunchImage],
        [100, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 45,50,55]],
        [103, self.longPunchImage, [32-7, 32-8-6, 32, 32-8, 45,50,55]],
        [125, self.longPunchImage],
        [140, self.punchImage],
        [155, self.midPunchImage],
        ]

        self.extreme = [
        [36, self.prePunchImage],
        [162, self.prePunchImage, None, True],
        [167, self.midPunchImage],
        [170, self.punchImage, [32-9-7, 32-8-6, 32-9, 32-8, 80, 100]],
        [205, self.punchImage],
        [215, self.midPunchImage],
        [225, self.prePunchImage],
        ]

    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==10:
            self.xv+=(self.facingRight-0.5)*8
            self.yv-=4
    def attack3(self, pressed):
        self.executeAttack(self.long, not self.pressed["3"])
    def attack4(self, pressed):
        self.executeAttack(self.extreme, not self.pressed["4"])
    def attack5(self, pressed):
        if self.attackFrame == 1:
            Player.ultSound.play()

        a=self.attackFrame

        if a<200:
            if a%7==0:
                self.xv += (self.facingRight-0.5)*0.5
                self.yv = -2
            if a%7<=3:
                self.image = self.punchImage
                self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 3,9,7]
            else:
                self.image = self.prePunchImage
                self.attackBox = None

            if not self.pressed["5"] and self.attackFrame>25:
                self.attackFrame = 200

        elif self.attackFrame < 208:
            self.image = self.punchImage
            self.attackBox = [32-9-7, 32-8-6, 32-9, 32-8, 3,9,70]
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        elif self.attackFrame < 225:
            self.image = self.punchImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.cursedImage
            self.attackBox = None

    idleImage = Player.load("puncher", "idle.png")
    cursedImage = Player.load("puncher", "cursed.png")
    stunnedImage = Player.load("puncher", "stunned.png")
    longPunchImage = Player.load("puncher", "longpunch.png")
    prePunchImage = Player.load("puncher", "prepunch.png")
    midPunchImage = Player.load("puncher", "midpunch.png")
    punchImage = Player.load("puncher", "punch.png")
    text = "They said no human could ever compete in the arena. They? proved them wrong"
    text = "The only humans strong enough to compete in the arena"
class Big(Player):
    
    def grounded(self):
        Player.shake+=int(self.yv)
    
    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Big, self).__init__(x, y, facingRight, controls,joystick)
        self.box = [16-4, 12, 16+4, 32-4]
        self.image = Big.idleImage
        self.xspeed=2
        self.hp=300
        self.init2()

        self.first = [
        [3, self.prePunchImage, [10, 17, 11, 32-9, 20]],
        [12, self.prePunchImage],
        [15, self.midPunchImage],
        [25, self.punchImage, [16, 16, 32-6, 32-8, 33, 50, 33]],
        [45, self.punchImage],
        [52, self.midPunchImage],
        [60, self.prePunchImage],
        ]

        self.second = [
        [4, self.prePunchImage, [10, 17, 11, 32-9, 30]],
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
            self.image = self.prePunchImage
            self.attackBox = None
            if self.attackFrame%5==0:
                self.facingRight = not self.facingRight

        elif self.attackFrame < 150:
            self.yv-=0.76
            self.image = self.punchImage
            self.attackBox = [16, 16, 32-6, 32-8, 18]
            if self.attackFrame%10==0:
                self.facingRight = not self.facingRight
            if not self.pressed["3"] and self.attackFrame>35:
                self.attackFrame = 150

        elif self.attackFrame < 170:
            self.image = self.midPunchImage
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
        self.xspeed = 3
        self.init2()
        self.canDoubleJump = True

        self.first = [
        [3, self.idleImage, None],
        [8, self.kickImage, [32-14, 32-6, 32-10, 32-3, 10]],
        [20, self.kickImage, None],
        [25, self.idleImage, None],
        ]

        self.second = [
        [15, self.stunnedImage, None],
        [20, self.skullImage, [32-9-5, 32-8-6, 32-9, 32-9, 40]],
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
    text = "Wormlike magical creatures without arms"
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

    def hurt(self, player, damage, knockback=None, stun=None):
        self.box = [16-3, 32-15, 16+3, 32-4]
        super().hurt(player, damage, knockback, stun)

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Tree, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-15, 16+3, 32-4]
        self.image = Tree.idleImage
        self.CHARGE = 25
        self.xspeed = 2
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
        [28, self.kickImage, [16, 20, 32-9, 32-7, 41]],
        [40, self.kickImage],
        [50, self.preKickImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame == 1:
            if not self.y==280:
                self.state = State.idle
            else:
                Player.growSound.play()
        elif self.attackFrame < 10:
            self.image = self.preGrowImage
            self.box = [16-3, 32-12, 16+3, 32-4]
        elif self.attackFrame < 17:
            self.image = self.growImage
            self.box = [16-3, 32-8, 16+3, 32-4]
            self.invincible=True
        elif self.attackFrame==17:
            self.box = [16-3, 32-4, 16+3, 32-4]
            self.invisible=True
            self.x += 250*(self.facingRight-0.5)
            #Player.growSound.play()
            self.facingRight = not self.facingRight
        elif self.attackFrame<27:
            pass
        elif self.attackFrame < 37:
            self.invisible=False
            self.attackBox = [16-2, 32-8, 16+2, 32-4,20,60,20]
        elif self.attackFrame < 47:
            self.attackBox = [16-2, 32-12, 16+2, 32-4,15,50,15]
            self.box = [16-3, 32-8, 16+3, 32-4]
            self.invincible=False
            self.image = self.preGrowImage
        elif self.attackFrame < 57:
            self.box = [16-3, 32-12, 16+3, 32-4]
            self.attackBox = [16-2, 32-15, 16+2, 32-4,10,40,10]
            self.image = self.idleImage
        elif self.attackFrame < 58:
            self.box = [16-3, 32-15, 16+3, 32-4]
        else:
            self.state = State.idle
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame == 1:
            if not self.y==280:
                self.state = State.idle
            else:
                Player.growSound.play()
        elif self.attackFrame < 10:
            self.image = self.preGrowImage
            self.box = [16-3, 32-12, 16+3, 32-4]
        elif self.attackFrame < 17:
            self.image = self.growImage
            self.invincible=True
            self.box = [16-3, 32-8, 16+3, 32-4]
        elif self.attackFrame < 32:
            self.invisible=True
            self.box = [16-3, 32-4, 16+3, 32-4]
        elif self.attackFrame < 44:
            self.invisible = False
            self.attackBox = [16-2, 32-8, 16+2, 32-4,20,60,20]
        elif self.attackFrame < 56:
            self.invincible=False
            self.image = self.preGrowImage
            self.attackBox = [16-2, 32-12, 16+2, 32-4,15,50,15]
            self.box = [16-3, 32-8, 16+3, 32-4]
        elif self.attackFrame < 68:
            self.attackBox = [16-2, 32-15, 16+2, 32-4,10,40,10]
            self.box = [16-3, 32-12, 16+3, 32-4]
            self.image = self.idleImage
        elif self.attackFrame < 70:
            self.box = [16-3, 32-15, 16+3, 32-4]
        else:
            self.state = State.idle
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame == 1:
            Player.growSound.play()
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

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

        elif self.attackFrame < 10:
            self.invisible = True
            self.attackBox = [16-2, 32-8, 16+2, 32-4,20,60,20]
            self.box = [16-3, 32-4, 16+3, 32-4]
            self.y=700
        elif self.attackFrame < 20:
            self.invisible = False
            self.invincible=True
            self.image = self.growImage
            self.attackBox = [16-2, 32-12, 16+2, 32-4,15,50,15]
            self.box = [16-3, 32-8, 16+3, 32-4]
        elif self.attackFrame < 50:
            self.invincible=False
            self.image = self.preGrowImage
            self.attackBox = [16-2, 32-15, 16+2, 32-4,10,40,10]
            self.box = [16-3, 32-12, 16+3, 32-4]
        else:
            self.box = [16-3, 32-15, 16+3, 32-4]
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
    text = "A subspecies of acer platanoides evolved as an r-strategist"
class Sad(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Sad, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-6]
        self.image = Sad.idleImage
        self.flyingHeight=2*Player.SCALE
        self.xspeed = 2.5
        self.init2()

        self.first = [
        [5, self.stunnedImage],
        [8, self.idleImage],
        [13, self.preSkullImage, [19, 15, 20, 22, 15]],
        [22, self.preSkullImage],
        ]

        self.second = [
        [10, self.stunnedImage],
        [13, self.idleImage],
        [16, self.preSkullImage],
        [20, self.skullImage, [19, 15, 24, 22, 35]],
        [31, self.skullImage],
        [40, self.preSkullImage],
        ]

        self.jump = [
        [6, self.preJumpImage],
        [12, self.jumpImage, [10, 24, 15, 29, 16, 40]],
        [21, self.jumpImage],
        [29, self.preJumpImage],
        ]

    def attack3(self, pressed):
        if self.attackFrame > 0:
            self.ultCharge+=0.1
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
            if not self.pressed["3"]:
                self.attackFrame = -2
        else:
            self.state=State.idle
            self.image=self.idleImage
            self.attackBox=None
    
    def attack4(self, pressed):
        self.executeAttack(self.jump, not self.pressed["4"])
        if self.attackFrame==12:
            self.yv=-11
            r=(self.facingRight-0.5)*2
            self.xv=max(self.xv*r,4)*r
    
    def attack5(self, pressed):
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

    idleImage = Player.load("sad", "idle.png")
    stunnedImage = Player.load("sad", "stunned.png")
    magic1Image = Player.load("sad", "magic1.png")
    magic2Image = Player.load("sad", "magic2.png")
    preSkullImage = Player.load("sad", "preskull.png")
    skullImage = Player.load("sad", "skull.png")
    preJumpImage = Player.load("sad", "prejump.png")
    jumpImage = Player.load("sad", "jump.png")
    projbImage = Player.load("sad", "somehorn.png")
    text = "Solemnity is the key to telekinesis"
class Animals(Player):

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Animals, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 19, 16+5, 32-4]
        self.image = self.idleImage
        self.init2()

        self.first = [
        [5, self.prePunchImage],
        [10, self.punchImage, [24,21,26,23, 10]],
        [15, self.punchImage],
        [20, self.prePunchImage],
        ]

        self.second = [
        [10, self.prePunchImage],
        [15, self.punchImage, [24,21,26,23, 1,0,5]],
        [20, self.punchImage],
        [25, self.punchImage, [24,21,26,23, 3,-60,10]],
        [34, self.postPunchImage, [22,14,24,16, 9,-35,20]],
        [39, self.prePunchImage],
        ]

        self.third = [
        [15, self.preKickImage],
        [20, self.kickImage, [15,28,19,32, 30]],
        [30, self.kickImage],
        [40, self.preKickImage],
        ]

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])
        if self.attackFrame==1:
            Player.lickSound.play()
    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==5:
            Player.lickSound.play()
    def attack3(self, pressed):
        if self.onGround and self.attackFrame>14 and self.attackFrame<20:
            self.yv=-13
        self.executeAttack(self.third, not self.pressed["3"])
    def confirmedHit(self, damage):
        if self.state==3:
            self.yv=-13
    def attack4(self, pressed):
        if self.attackFrame<10:
            self.image=self.preFlyImage
        elif self.attackFrame<100:
            if self.attackFrame%10<5:
                self.image = self.flyImage
                self.attackBox=None
            else:
                self.image = self.fly2Image
                self.attackBox=[10,12,23,15,5,-7]

            if(self.pressed["d"]):
                self.xv=min(self.xspeed*2, self.xv+0.1)
                self.facingRight = True
            if(self.pressed["a"]):
                self.xv=max(-self.xspeed*2, self.xv-0.1)
                self.facingRight = False

            self.yv-=1
            self.yv=self.yv*0.95
            if not (self.pressed["4"]):
                self.attackFrame=99
        elif self.attackFrame<110:
            self.image = self.preFlyImage
            self.yv=self.yv*0.95
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        if self.attackFrame<10:
            self.image = self.preUltImage
        elif self.attackFrame < 90:
            self.image = self.ultImage
            if self.attackFrame%3==1:
                Player.lickSound.stop()
                Player.lickSound.play()
                Projectile.projectiles.append(Projectile(self, op=True))
        elif self.attackFrame<100:
            self.image = self.preUltImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    idleImage = Player.load("animals", "idle.png")
    stunnedImage = Player.load("animals", "stunned.png")
    prePunchImage = Player.load("animals", "prelick.png")
    punchImage = Player.load("animals", "lick.png")
    postPunchImage = Player.load("animals", "postlick.png")
    preKickImage = Player.load("animals", "prekick.png")
    kickImage = Player.load("animals", "kick.png")
    preFlyImage = Player.load("animals", "prefly.png")
    flyImage = Player.load("animals", "fly.png")
    fly2Image = Player.load("animals", "fly2.png")
    ultImage = Player.load("animals", "ult.png")
    preUltImage = Player.load("animals", "preult.png")
    projbImage = Player.load("animals", "projb.png")
    text = "The animal is bloody. The snake is fighting. The relationship is questionable."# (symbiosis or ?)
class Pufferfish(Player):

    def confirmedHit(self, damage):
        if self.state==3:
            self.ultCharge=51
        if self.state<3:
            self.hp=min(self.hp+damage//2, self.maxhp)

    def passive(self):
        if self.pressed["5"] and self.ultCharge>self.CHARGE:
            Pillar(self.x,-300,True,{"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_s})
            self.ultCharge = 0
        if self.image == self.longImage:
            self.yv-=0.79
            self.yv*=0.95
        elif self.image == self.preImage:
            self.yv-=0.51
            self.yv*=0.97
        elif self.image == self.longPunchImage:
            self.yv-=0.79
            self.yv*=0.95
        elif self.image == self.punchImage or self.image == self.prePunchImage:
            self.yv-=0.51
            self.yv*=0.97

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Pufferfish, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-4, 18, 16+4, 32-6] #+-3 is actual box but it grows so...
        self.image = self.idleImage
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

    def attack3(self, pressed):
        self.executeAttack(self.tail, not self.pressed["3"])
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

    def attack4(self, pressed):
        self.executeAttack(self.ball, not self.pressed["4"])
        if(self.pressed["d"]):
            self.xv=min(self.xspeed*2, self.xv+0.1)
            self.facingRight = True
        if(self.pressed["a"]):
            self.xv=max(-self.xspeed*2, self.xv-0.1)
            self.facingRight = False

    def attack5(self, pressed):
        Pillar(self.x,-300,True,{"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_x, "2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_s})
        self.image = self.idleImage
        self.state = State.idle
        self.attackBox = None

    idleImage = Player.load("pufferfish", "idle.png")
    prePunchImage = Player.load("pufferfish", "prepunch.png")
    punchImage = Player.load("pufferfish", "punch.png")
    longPunchImage = Player.load("pufferfish", "longpunch.png")
    preImage = Player.load("pufferfish", "pre.png")
    longImage = Player.load("pufferfish", "long.png")
    magicImage = Player.load("pufferfish", "magic.png")
    stunnedImage = Player.load("pufferfish", "stunned.png")
    text = "yo"

class Bird(Player):

    def confirmedHit(self, damage):
        if self.state==3:
            self.ultCharge+=1
        
    def passive(self):
        if(self.pressed["5"] and self.ultCharge>self.CHARGE): #ult
            self.ultCharge = 0
            self.yv=-22
            self.xv=(self.facingRight-0.5)*10
            self.state = State.idle
            self.stun = 0
            self.attackBox =None
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        self.yv-=0.1

        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage

        if self.pressed["w"] and (self.yv>=0 or (self.yv<-18 and not self.stun)): #float
            self.yv=2
            self.image = self.idleImage

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Bird, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-18, 16+3, 32-10]
        self.flyingHeight=4*Player.SCALE
        self.image = Bird.idleImage
        self.CHARGE = 25
        self.maxhp = 200
        self.xspeed = 2.5
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

        elif self.attackFrame < 182:
            self.image = self.elaImage
            self.attackBox = [0, 15, 9, 15+9, 7,6]
            if self.attackFrame%6>2:
                self.attackBox = [23, 15, 23+9, 21, 7,6]
                self.image = self.elbImage
        
        elif self.attackFrame < 205:
            self.image = self.preelImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 5:
            self.invincible=False
            self.image = self.idlebImage
            self.attackBox = None
        elif self.attackFrame < 30:
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

    text = "The electric avian predator"
class Robot(Player):

    def grounded(self):
        Player.shake+=int(self.yv*0.6)
    
    def passive(self):
        if self.attackFrame%20<10: #idle animation
            self.image = self.idlebImage
        else:
            self.image = self.idleImage
        self.yv+=0.15
        if self.state == State.stunned:
            self.stun-=0.3
            self.yv-=0.1

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Robot, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-4, 32-18, 16+4, 32-7]
        self.image = Robot.idleImage
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

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])
        if self.attackFrame==15:
            Player.bzzzSound.play()
        if self.attackFrame==101:
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
            playHitSound(State.volume*0.2)
        elif self.attackFrame < 42:
            self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        if self.attackFrame < 10:
            self.image = self.idleImage
            self.attackBox = None        
        elif self.attackFrame < 15: 
            self.image = self.jetpackImage
            self.attackBox = [13, 32-7, 18, 32-3, 20]
        elif self.attackFrame == 15:
            self.image = self.jetpackImage
            self.attackBox = None
            self.yv=-14
        elif self.attackFrame < 32:
            self.image = self.stunnedImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
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
    idleImage = Player.load("robot", "idle.png")
    idlebImage = Player.load("robot", "idleb.png")
    stunnedImage = Player.load("robot", "stunned.png")
    fireImage = Player.load("robot", "fire.png")
    projbImage = Player.load("robot", "proj.png")
    punchImage = Player.load("robot", "punch.png")
    prePunchImage = Player.load("robot", "prepunch.png")
    jetpackImage = Player.load("robot", "jetpack.png")
class Lizard(Player):

    def confirmedHit(self, damage):
        if self.state==4:
            self.ultCharge=100

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Lizard, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = Lizard.idleImage
        self.xspeed = 3.5
        self.CHARGE = 25
        self.init2()
        self.canDoubleJump = True

        self.first = [
        [4, self.prePunchImage],
        [8, self.midPunchImage],
        [10, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 22,11,22]],
        [17, self.punchImage],
        [25, self.midPunchImage],
        ]

        self.second = [
        [10, self.prePunchImage],
        [14, self.midPunchImage],
        [18, self.punchImage, [32-9-6, 32-8-5, 32-9, 32-8, 30,11,34]],
        [29, self.punchImage],
        [34, self.midPunchImage],
        [47, self.prePunchImage],
        ]
        self.tail = [
        [11, self.preTailImage],
        [15, self.tailImage, [7, 32-4, 10, 32-2, 27, -23]],
        [25, self.tailImage],
        ]
        self.lick = [
        [8, self.preLickImage],
        [12, self.lickImage, [15, 32-13, 28, 32-12, 0,-29]],
        [15, self.lickImage],
        [29, self.preLickImage],
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
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            self.ultCharge = 0
            self.stun = 0
            self.state = State.idle
            self.image = self.magicImage
            self.attackBox = None

    preLickImage=Player.load("lizard", "prelick.png")
    lickImage=Player.load("lizard", "lick.png")
    idleImage = Player.load("lizard", "idle.png")
    magicImage = Player.load("lizard", "magic.png")
    stunnedImage = Player.load("lizard", "stunned.png")
    prePunchImage = Player.load("lizard", "prepunch.png")
    midPunchImage = Player.load("lizard", "midpunch.png")
    punchImage = Player.load("lizard", "punch.png")
    preTailImage = Player.load("lizard", "prekick.png")
    tailImage = Player.load("lizard", "kick.png")
    text = "To master the reptile you must first understand endlag"
class Golem(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Golem, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [11, 15, 21, 28]
        self.image = self.idleImage
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [10, self.punchImage, [21, 18, 25, 22, 15]],
        [17, self.punchImage],
        [23, self.prePunchImage],
        ]

        self.second = [
        [11, self.prePunchImage],
        [15, self.kickImage, [17, 23, 23, 27, 10, -45, 17]],
        [22, self.kickImage],
        [28, self.prePunchImage],
        [35, self.punchImage, [21, 18, 25, 22, 10, -60, 22]],
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

    def confirmedHit(self, damage):
        if self.state==4:
            self.xv*=0.5
            self.yv*=0.2

    def attack3(self, pressed):
        if self.attackFrame==20:
            Player.bzzzSound.play()
            Player.growSound.play()
        self.executeAttack(self.grass, not self.pressed["3"])

    def attack4(self, pressed):
        if self.attackFrame==1:
            Player.lickSound.play()
        self.executeAttack(self.lick, not self.pressed["4"])

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        self.executeAttack(self.ultimate, not self.pressed["5"])

    idleImage = Player.load("golem", "idle.png")
    stunnedImage = Player.load("golem", "stunned.png")
    fireImage = Player.load("golem", "fire.png")
    prePunchImage = Player.load("golem", "prepunch.png")
    punchImage = Player.load("golem", "punch.png")
    kickImage = Player.load("golem", "kick.png")
    preGrassImage = Player.load("golem", "pregrass.png")
    grassImage = Player.load("golem", "grass.png")
    preLickImage = Player.load("golem", "prelick.png")
    lickImage = Player.load("golem", "lick.png")
    text = "Animated igneous rock infused with elemental powers"
class Alien(Player):

    def passive(self):
        self.yv-=0.1

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Alien, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [13, 14, 19, 28]
        self.image = self.idleImage
        self.init2()
        self.xspeed=3.5
        self.canDoubleJump = True

        self.first = [
        [9, self.prePunchImage],
        [14, self.punchImage, [17, 19, 23, 23, 5,-11]],
        [17, self.punchImage],
        [21, self.prePunchImage],
        [31, self.punchImage, [17, 19, 23, 23, 13]],
        [36, self.prePunchImage],
        ]

        self.second = [
        [20, self.prePunchImage],
        [23, self.punchImage, [17, 19, 23, 23, 25,-7, 33]],
        [27, self.punchImage],
        [40, self.prePunchImage],
        ]

        self.ultimate = [
        [5, self.footImage,[19, 23, 23, 28, 5,-25,10]],
        [15, self.armImage, [19, 17, 24, 20, 1, -22,5]],
        [19, self.rise1Image, [19, 17, 24, 20, 1, 22,4]],
        [23, self.rise2Image, [19, 15, 24, 18, 2, -15,4]],
        [27, self.rise3Image, [19, 13, 24, 16, 5, -15,4]],
        [31, self.rise4Image, [19, 11, 24, 14, 10, 15,4]],
        [35, self.rise3Image, [19, 13, 24, 16, 5, -15,4]],
        [39, self.rise2Image, [19, 15, 24, 18, 2, 0,4]],
        [44, self.rise1Image, [19, 17, 24, 20, 10, 60]],
        [56, self.idleImage]
        ]

    def attack3(self, pressed):
        if self.attackFrame < 13:
            self.image = self.stunnedImage
        elif self.attackFrame < 22: 
            self.image = self.fireImage
        elif self.attackFrame == 22:
            self.image = self.fireImage
            Projectile.projectiles.append(Projectile(self))
        elif self.attackFrame < 27:
            self.image = self.fireImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack4(self, pressed):
        #self.executeAttack(self.hair, not self.pressed["3"])
        if self.attackFrame < 5:
            self.image = self.preHairImage
            self.attackBox = None
            self.xv=self.xv-(self.facingRight*2-1)*2
        elif self.attackFrame < 8: 
            self.image = self.hairImage
            self.attackBox = [5, 16, 9, 24, 15]
        elif self.attackFrame < 17:
            self.image = self.hairImage
            self.attackBox = None
        elif self.attackFrame < 22:
            self.image = self.preHairImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
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
    text = "Trained in higher gravity"
class Glitch(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Glitch, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [13, 15, 19, 28]
        self.canDoubleJump = True
        self.image = self.idleImage
        self.init2()

        self.first = [
        [10, self.prePunchImage],
        [16, self.punchImage, [15, 19, 22, 22, 18,36,18]],
        [22, self.punchImage],
        [32, self.prePunchImage]
        ]
        self.second = [
        [15, self.idleImage],
        [20, self.chimneyImage, [15, 8, 20, 13, 30,100,25]],
        [22, self.chimneyImage],
        [25, self.idleImage],
        ]
        self.glitch = [
        #[10, self.idleImage],
        [27, self.preGlitchImage],
        [40, self.glitchImage, [9, 15, 23, 27, 5,-4,2]],
        [45, self.glitchImage, [9, 15, 23, 27, 15,50,14]],
        [60, self.idleImage],
        ]

    def confirmedHit(self, damage):
        if self.state==2:
            self.xv*=0.5
            self.yv*=0.2
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
    def attack1(self, pressed):
        if(self.image==self.shimmerImage):
            self.attackFrame=11
        if self.attackFrame==11:
            self.xv+=(self.facingRight-0.5)*10
        self.executeAttack(self.first, not self.pressed["1"])
    def attack2(self, pressed):
        if(self.image==self.shimmerImage):
            self.attackFrame=25
        self.executeAttack(self.glitch, not self.pressed["2"])
    def attack3(self, pressed):
        if(self.image==self.shimmerImage):
            self.attackFrame=46
        if self.attackFrame < 12:
            self.image = self.prePunchImage
        elif self.attackFrame < 16: 
            self.image = self.punchImage
            if self.attackFrame==13:
                self.xv+=(self.facingRight-0.5)*10
            self.attackBox = [15, 19, 22, 22, 18,36,18]
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

    def attack4(self, pressed):
        if(self.image==self.shimmerImage):
            self.attackFrame=13
        if self.attackFrame==13:
            self.yv+=10
        self.executeAttack(self.second, not self.pressed["4"])
    def attack5(self, pressed):
        self.attackBox = [14,11,18,16,10,160,0]
        if self.attackFrame==2:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            self.image = self.shimmerImage
            self.state = State.idle
            self.attackBox = None

    idleImage = Player.load("glitch", "idle.png")
    stunnedImage = Player.load("glitch", "stunned.png")
    fireImage = Player.load("glitch", "fire.png")
    prePunchImage = Player.load("glitch", "prepunch.png")
    punchImage = Player.load("glitch", "punch.png")
    shimmerImage = Player.load("glitch", "shimmer.png")
    chimneyImage = Player.load("glitch", "chimney.png")
    projbImage = Player.load("glitch", "proj.png")
    
    preGlitchImage = Player.load("glitch", "preGlitch.png")
    glitchImage = Player.load("glitch", "glitch.png")
    preFire1Image = Player.load("glitch", "preFire1.png")
    preFire2Image = Player.load("glitch", "preFire2.png")
    preFire3Image = Player.load("glitch", "preFire3.png")
    preFire4Image = Player.load("glitch", "preFire4.png")
    text = "A glitch in the simulation"
class Rat(Player):

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Rat, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [14, 17, 18, 28]
        self.hp = 200
        self.xspeed=2

        self.image = self.idleImage
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
        [4, self.idleImage],
        [9, self.preJump1Image],
        [14, self.preJump2Image],
        [20, self.preTail1Image],
        [25, self.preTail2Image],
        [29, self.tailImage, [22, 8, 32, 19, 20,30,25]],
        [41, self.preTail2Image],
        [49, self.preTail1Image],
        [59, self.preJump1Image],
        ]

    def passive(self):
        self.xspeed=max(1.8,self.xspeed*0.997)
    def confirmedHit(self,damage):
        self.xspeed+=damage/8
    def attack3(self, pressed):
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
            self.image = self.jumpImage
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

    def attack4(self, pressed):
        self.executeAttack(self.tail, not self.pressed["4"])

    def attack5(self, pressed):
        Player.ultSound.play()
        pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        self.xspeed+=6
        self.state = State.idle
        self.image = self.idleImage
        self.attackBox = None


    idleImage = Player.load("rat", "idle.png")
    stunnedImage = Player.load("rat", "stunned.png")
    prePunchImage = Player.load("rat", "prepunch.png")
    punchImage = Player.load("rat", "punch.png")

    jumpImage = Player.load("rat", "jump.png")
    nibbleImage = Player.load("rat", "nibble.png")
    preJump1Image = Player.load("rat", "preJump1.png")
    preJump2Image = Player.load("rat", "preJump2.png")
    
    preTail1Image = Player.load("rat", "preTail1.png")
    preTail2Image = Player.load("rat", "preTail2.png")
    tailImage = Player.load("rat", "tail.png")

    text = "Technically a mouse"
class Skugg(Player):

    def passive(self):
        if self.state == State.idle:
            if not self.onGround:
                self.image = self.idleImage
            elif self.pressed["d"] or self.pressed["a"]:
                self.image = self.walkImages[(self.attackFrame//4)%8]
            else:
                self.image = self.idleImage
    def grounded(self):
        Player.shake+=int(self.yv)

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Skugg, self).__init__(x, y, facingRight, controls, joystick)
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

    def attack3(self, pressed):
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

    def attack4(self, pressed):
        self.executeAttack(self.jump, not self.pressed["4"])
        if self.attackFrame==19:
            self.yv=-11.1

    def attack5(self, pressed):
        if self.attackFrame == 1:
            Player.ultSound.play()
            Player.growSound.play()
        pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
        if self.attackFrame == 5*8:
            self.invincible=1
        if self.attackFrame < 5*17:
            self.image = self.ultImages[self.attackFrame//5]
        else:
            if self in Player.players:
                Player.players.remove(self)
            candidates = [Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Bird, Robot, Lizard, Golem, Alien, Glitch, Monster, Penguin]
            new = random.choice(candidates)(self.x, self.y, self.facingRight, self.controls, self.joystick)
            new.hp = min(new.maxhp, self.hp)
            new.random = self.random

    idleImage = Player.load("skugg", "idle.png")
    walkImages = [Player.load("skugg", "SkuggVarg_0"+str(i)+".png") for i in range(2,10)]
    elImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png") for i in range(11,15)]
    jumpImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png") for i in range(19,25)]
    kickImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png") for i in range(26,37)]
    skullImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png") for i in range(38,43)]
    ultImages = [Player.load("skugg", "SkuggVarg_"+str(i)+".png") for i in range(44,61)]
    stunnedImage = Player.load("skugg", "SkuggVarg_16.png")

    text = "Simultaneous wolf or elk silhouette?"

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

    def attack4(self, pressed):
        self.attack3(pressed)
        #self.state = State.idle (wut

    def attack5(self, pressed):
        Player.ultSound.play()
        pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
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
        [12, self.lickImage, [26, 18, 28, 21, 15, -21]],
        [18, self.lickImage],
        [38, self.preLickImage],
        ]

        self.second = [
        [9, self.preLickImage],
        [12, self.lickImage, [26, 18, 28, 21, 15, -21]],
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
            self.image = self.jumpImage
            self.xv += (self.facingRight-0.5)*8
            self.yv -= 16
        elif self.attackFrame < 500:
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 505:
            self.image = self.jumpImage
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 32]
        elif self.attackFrame < 515:
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
            self.image = self.jumpImage
            self.xv += (self.facingRight-0.5)*12
            self.yv -=24
        elif self.attackFrame < 500:
            self.image = self.idleImage
            if self.onGround:
                self.attackFrame = 500
        elif self.attackFrame < 510:
            self.image = self.jumpImage
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 40]
        elif self.attackFrame < 530:
            self.image = self.jumpImage
            self.attackBox = None
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def attack5(self, pressed):
        if self.attackFrame==1:
            Player.ultSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
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
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)
            self.attackBox = [16-6, 32-8, 16+5, 32-3, 50, 100]
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

    def passive(self):
        if(self.pressed["5"] and self.ultCharge>1 and not self.stun and self.state==State.idle): #needed both?
            self.ultCharge = min(self.ultCharge, self.CHARGE)
            self.state = 5
            Player.ultSound.play()
            Player.growSound.play()
            pygame.draw.rect(gameDisplay, (0, 100, 100), (0,0,1000,504), 0)

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Monster, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-5, 16, 16+5, 32-4]
        self.image = Monster.idleImage
        self.init2()

        self.first = [
        [7, self.prePunchImage],
        [11, self.punch2Image, [21, 22, 25, 25, 27, 50, 5]],
        [14, self.punch2Image],
        [17, self.prePunchImage],
        [22, self.idleImage],
        ]

        self.second = [
        [15, self.prePunchImage],
        [18, self.punch2Image],
        [21, self.punchImage, [22, 20, 26, 23, 48, 90, 10]],
        [27, self.punchImage],
        [33, self.punch2Image],
        [38, self.prePunchImage],
        [43, self.idleImage],
        ]

        self.tail = [
        [7, self.preKickImage],
        [13, self.kickImage, [8, 28, 11, 29, 20]],
        [18, self.kickImage],
        [22, self.idleImage],
        ]

    def attack3(self, pressed):
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

    def attack4(self, pressed):
        self.executeAttack(self.tail, not self.pressed["4"])

    def attack5(self, pressed):
        if self.ultCharge >=0:
            self.ultCharge-=0.2
            self.yv-=0.4
            self.image = self.prePunchImage
            self.hp=min(self.hp+0.5, self.maxhp)
            self.facingRight = not self.facingRight
        else:
            self.ultCharge = 0
            self.state = State.idle
            self.image = self.idleImage

    idleImage = Player.load("monster", "idle.png")
    stunnedImage = Player.load("monster", "stunned.png")
    prePunchImage = Player.load("monster", "prepunch.png")
    punchImage = Player.load("monster", "punch.png")
    punch2Image = Player.load("monster", "punch2.png")
    preKickImage = Player.load("monster", "prekick.png")
    kickImage = Player.load("monster", "kick.png")
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
            self.xspeed = 2
            self.canDoubleJump = True
        else:
            self.idleImage = self.ninjaImage
            self.stunnedImage = self.stunnedNinjaImage
            self.first = self.ninjaFirst
            self.second = self.ninjaSecond
            self.attack3 = self.shuriken
            self.xspeed = 3.5
            self.canDoubleJump = False
    def confirmedHit(self, damage):
        if (self.state>0 and self.state<3) and self.wizard:
            self.xv*=0.5
            self.yv*=0.2
            self.yv-=5

    def __init__(self, x, y, facingRight, controls,joystick=None):
        super(Penguin, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-3, 32-17, 16+3, 32-4]
        self.image = self.ninjaImage
        self.xspeed = 2.5
        self.wizard = False
        self.init2()

        self.ninjaFirst = [
        [6, self.prePunchImage],
        [11, self.punchImage, [18, 19, 24, 23, 16]],
        [20, self.punchImage],
        [25, self.prePunchImage],
        ]

        self.ninjaSecond = [
        [12, self.prePunchImage],
        [21, self.punchImage, [18, 19, 24, 23, 38]],
        [30, self.punchImage],
        [36, self.ninjaImage],
        [44, self.prePunchImage],
        ]

        self.wizardFirst = [
        [10, self.preMagicImage],
        [14, self.midMagicImage],
        [70, self.magicImage, [23,17,24+6,17+6, 10,20,10], True],
        [78, self.magicImage],
        [85, self.midMagicImage],
        [95,self.preMagicImage],
        ]
        self.wizardSecond = self.wizardFirst

    def attack1(self, pressed):
        self.executeAttack(self.first, not self.pressed["1"])
        if self.attackFrame==17 and self.wizard:
            Player.bzzzSound.play()
            Player.growSound.play()
    def attack2(self, pressed):
        self.executeAttack(self.second, not self.pressed["2"])
        if self.attackFrame==17 and self.wizard:
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
            self.attackFrame = 82
        elif self.attackFrame < 100:
            self.image = self.punchImage
        else:
            self.state = State.idle
            self.image = self.idleImage
            self.attackBox = None

    def throw(self,pressed):
        if self.attackFrame < 10:
            self.image = self.preHatImage
            self.attackBox = None
        elif self.attackFrame < 22: 
            self.image = self.midHatImage
        elif self.attackFrame == 22:
            self.wizard = False
            self.image = self.midHatImage
            Projectile.projectiles.append(Projectile(self))
            self.attackFrame=80 #to 100
        #attack3 becomes shuriken.
        #i could have made a becomeWizard func. this works tho. dont question

    def attack4(self, pressed):
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

class Pillar(Player):

    def confirmedHit(self, damage):
        pass
        self.yv=-10 #-10 if we dont want the infinite

    def passive(self):
        if random.randint(1,30)==1:
            p=0
            for player in Player.players:
                if not isinstance(player,Pillar):
                    p+=1
            if p<2:
                if self in Player.players:
                    Player.players.remove(self)

    def __init__(self, x, y, facingRight, controls, joystick=None):
        super(Pillar, self).__init__(x, y, facingRight, controls, joystick)
        self.box = [16-2, 1, 16+2, 30]
        self.attackBox = [16-3,31,16+3,32,20,10]
        self.image=Pillar.idleImage
        self.maxhp=0
        self.CHARGE=10000
        self.init2()

    def action(self):
        self.passive()

    def hurt(self, player, damage, knockback=0, stun=0):
        if self in Player.players:
            Player.players.remove(self)
        #player.confirmedHit(damage)
        playHitSound(State.volume*damage*0.01)
        Player.shake+=int(damage)
        
    idleImage = Player.load("pufferfish", "pillar.png")

allClasses = [
Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Bird, Robot, Lizard, Golem, Alien, Glitch, Skugg, Monster, Penguin,
Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Bird, Robot, Lizard, Golem, Alien, Glitch, Skugg, Rat, Can, Frog, Monster, Penguin,
Puncher, Big, Green, Tree, Sad, Animals, Pufferfish, Bird, Robot, Lizard, Golem, Alien, Glitch, Skugg, Monster, Penguin,
]

def restart():
    Player.players = []
    choices = []
    num = 0
    myfont = pygame.font.SysFont('Times New', 100)
    myfont2 = pygame.font.SysFont('Times New Roman', 20)
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
        if pressed[pygame.K_1]:
            Player.AIoption+=1
            if Player.AIoption==3:
                Player.AIoption=0
                State.playerCount+=1
            if Player.AIoption==2:
                State.playerCount-=1
            lag+=0.2
        if pressed[pygame.K_2]:
            Player.AI2option+=1
            if Player.AI2option==3:
                Player.AI2option=0
                State.playerCount+=1
            if Player.AI2option==2:
                State.playerCount-=1
            lag+=0.2
        if pressed[pygame.K_r]:
            choices.append(random.choice(allClasses))
            #num=0
            if len(choices)>=State.playerCount:
                return choices
            lag+=0.5
        if pressed[pygame.K_BACKSPACE] and len(choices)>0:
            choices.pop()
            #num=0
            lag+=0.5
        if pressed[pygame.K_SPACE] or pressed[pygame.K_RETURN]:
            choices.append(allClasses[num%len(allClasses)])
            #num=0
            if len(choices)>=State.playerCount:
                return choices
            lag+=0.5

        #draw
        gameDisplay.fill((100,100,100))
        pygame.draw.rect(gameDisplay,(200,200,200),(400+64,0,16*8,200+28*8),0)
        for i in range(len(choices)):
            gameDisplay.blit(choices[i].idleImage[1], (100*i, 0))
        for i in [-4,-3,-2,-1,0,1,2,3,4]:
            gameDisplay.blit(allClasses[(num-i)%len(allClasses)].idleImage[1], (400-104*i, 200))
        
        name = allClasses[num%len(allClasses)].__name__
        text = allClasses[num%len(allClasses)].text
        textsurface = myfont.render(name, True, (0, 0, 0))
        textsurface2 = myfont2.render(text, True, (0, 0, 0))
        textsurfaceAI = myfont2.render("player 1: "+["WASD, UIOP","AI","Off"][Player.AIoption]+"                        (press 1)", True, (0,0,0))
        textsurfaceAI2 = myfont2.render("player 2: "+["Arrowkeys, XCVB","AI","Off"][Player.AI2option]+"                (press 2)", True, (0,0,0))
        gameDisplay.blit(textsurface,(545-len(name)*24,450))
        gameDisplay.blit(textsurface2,(10,570))
        gameDisplay.blit(textsurfaceAI,(600,10))
        gameDisplay.blit(textsurfaceAI2,(600,50))

        pygame.display.update()
        clock.tick(100)
        time.sleep(lag)
    
    pygame.quit()
    quit()

gameDisplay = pygame.display.set_mode((1000, 600),)# pygame.FULLSCREEN)
backgrounds = []
for name in ["LDbackground.png","LDbackground2.png","background4.png"]:
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
    print(i)

State.playerCount = 2+len(sticks)
State.frameRate = 60
State.jump_out = False
Player.AIoption = 0 #0:XCVB 1:ai 2:off
Player.AI2option = 0 #0:UIOP 1:ai 2:off
while State.jump_out == False:

    #pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            State.jump_out = True
    if Player.hitLag:
        time.sleep(Player.hitLag)
        Player.hitLag=0
    if len(Player.players)<2 or pressed[pygame.K_ESCAPE]:
        choices = restart()
        
        if Player.AIoption != 2:
            choices[0](200, 300, True, {"a":pygame.K_a, "d":pygame.K_d, "w":pygame.K_w, "1":pygame.K_u, "2":pygame.K_i,"3":pygame.K_o,"4":pygame.K_p,"5":pygame.K_s})
            if Player.AIoption == 1:
                Player.players[-1].random=1
        humansBefore=len(Player.players)
        if Player.AI2option != 2:
            choices[humansBefore](600, 300, False, {"a":pygame.K_LEFT, "d":pygame.K_RIGHT, "w":pygame.K_UP, "1":pygame.K_x,"2":pygame.K_c,"3":pygame.K_v,"4":pygame.K_b,"5":pygame.K_DOWN})
            if Player.AI2option == 1:
                Player.players[-1].random=1
        humansBefore=len(Player.players)
        for i in range(len(sticks)):
            choices[humansBefore+i](400, 300, False, {"w":0,"3":4,"4":5,"5":1}, sticks[i])
        AiFocus = 0

        currentBackground = random.choice(backgrounds)
        Platform.restart()
        Player.shake=0
        Projectile.projectiles=[]
        pygame.display.update()
    
    #shake
    if Player.shake>0 and not Player.hitLag:
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
quit()
