import pygame, sys, random, time
from pygame.locals import*

pygame.init()
screen = pygame.display.set_mode([500, 500])
running = True
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60
GRAV = 0.5

sp=[]
pl=0
pic=[0,0]
print(pygame.QUIT)
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shit")

logo=pygame.image.load("./lmao.gif")
pic[0]=pygame.image.load("./spike.png")

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE)
fart=pygame.mixer.Sound(file="./fart.mp3")
explode=pygame.mixer.Sound(file="./expl.mp3")
sus=pygame.mixer.Sound(file="./amogus.mp3")
pygame.mixer.Sound(file="./bgmusic.mp3").play(loops=-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 40))

        self.pos = vec(50,0)
        self.pos.y=HEIGHT-20
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jump=False
        self.gameover=False

    def move(self):
        pl=self.rect
        self.acc = vec(0,0)
        self.acc.y=GRAV
        
        pkeys = pygame.key.get_pressed()
            
        if pkeys[K_LEFT] or pkeys[K_a]:
            self.acc.x = -ACC
        if pkeys[K_RIGHT] or pkeys[K_d]:
            self.acc.x = ACC
        if pkeys[K_SPACE] or pkeys[K_UP] or pkeys[K_w]:
            if not self.jump:
                if self.pos.y >= HEIGHT-20:
                    self.vel.y =-10
                    self.jump=True
                    fart.play(loops=0)
            else:
                self.jump=False
        else:
            self.jump=False
        if self.gameover:
            if pkeys[K_RETURN]:
                pygame.quit()
            else:
                return 0
        elif pkeys[K_RETURN]:
            raise Exception("Stupid")
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.y > HEIGHT-20:
            self.pos.y=HEIGHT-20
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
            sus.play(loops=0)
            O.spksw()
        if self.pos.x < 0:
            self.pos.x = 0
     
        self.rect.midbottom = self.pos

        for ps in sp:
            if abs(ps[0]-self.pos.x) <= 25:
                if abs(ps[1]-self.pos.y) <= 25:
                    self.gameover=True
                    explode.play(loops=0)
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

class obj(pygame.sprite.Sprite):
    def __init__(self,ide,spk=True):
        super().__init__()
        self.surf=pic[0]
        self.rect = self.surf.get_rect()
        sp.append(0)

        self.spk = 250
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.update(ide,spk)
        
    def update(self,ide,spk=True):
        self.pos.xy = self.spk,HEIGHT-20
        self.rect.midbottom = self.pos
        if spk:
            sp[ide] = [self.pos.x,self.pos.y]
        else:
            del sp[len(sp)]
        
    def spksw(self):
        self.spk=random.randint(40,WIDTH-40)
        self.update(0)

global PT1
global P1
global O
PT1 = platform()
P1 = Player()
O=obj(ide=0)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(O)
if True:
    while running:
        if "<Event(32787-WindowClose {'window': None})>" in str(pygame.event.get()):
            running = False
        
        pygame.display.update()
        FramePerSec.tick(FPS)        
        screen.fill((0xff, 0xff, 0xff))
        rect = logo.get_rect()
        rect.center = 30, 30
        screen.blit(logo, rect)
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
        pygame.display.flip()
        
        P1.move()
else:
    pygame.quit()
    sys.exit()

pygame.quit()
sys.exit()
