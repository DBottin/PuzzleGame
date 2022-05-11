import sys
from os import path

import pygame
from sprites import snd_folder, map_folder
from sprites import Player, Ground, Lava, Lock, Water, Key, Goal, Wall

# pylint: disable=E1101

# Klasse: Spiel
def quitting():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self, stage, width, height, tilesize):
        pygame.init()
        pygame.mixer.init()
        # Gruppen für alle Sprite-Arten
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.locks = pygame.sprite.Group()
        self.keysY = pygame.sprite.Group()
        self.locksY = pygame.sprite.Group()
        self.keysB = pygame.sprite.Group()
        self.locksB = pygame.sprite.Group()
        # Soundeffekte
        self.lava_sound = pygame.mixer.Sound(path.join(snd_folder, 'lava.wav'))
        self.water_sound = pygame.mixer.Sound(path.join(snd_folder, 'splash.wav'))
        self.key_sound = pygame.mixer.Sound(path.join(snd_folder, 'key.wav'))
        self.win_sound = pygame.mixer.Sound(path.join(snd_folder, 'win.wav'))
        # Andere Attribute des Spiels
        self.map_data = []
        self.playerplace = []
        self.playing = 0
        self.game = self
        self.grid = False
        self.tilesize = tilesize
        self.width = width * tilesize
        self.height = height * tilesize
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simples Puzzle")
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        # Musik am Anfang starten
        if stage == 1:
            pygame.mixer.music.load(path.join(snd_folder, 'background.wav'))
            pygame.mixer.music.play(loops=-1)
        self.load_data(stage)

    # Level wird geladen
    def load_data(self, level):
        with open(path.join(map_folder, 'map%d.txt' % level), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    # Level wird gebaut, Map Dateien werden eingelesen
    def new(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    Ground(self, col, row, self.tilesize)
                if tile == 'W':
                    Ground(self, col, row, self.tilesize)
                    Wall(self, col, row, self.tilesize)
                if tile == 'G':
                    Ground(self, col, row, self.tilesize)
                    Goal(self, col, row, self.tilesize)
                if tile == 'D':
                    Lava(self, col, row, self.tilesize)
                if tile == 'S':
                    Water(self, col, row, self.tilesize)
                if tile == 'K':
                    Ground(self, col, row, self.tilesize)
                    Key(self, col, row, self.tilesize, 1)
                if tile == 'L':
                    Ground(self, col, row, self.tilesize)
                    Lock(self, col, row, self.tilesize, 1)
                if tile == 'I':
                    Ground(self, col, row, self.tilesize)
                    Key(self, col, row, self.tilesize, 2)
                if tile == 'O':
                    Ground(self, col, row, self.tilesize)
                    Lock(self, col, row, self.tilesize, 2)
                if tile == 'P':
                    Ground(self, col, row, self.tilesize)
                    self.playerplace.append([col, row])
        # Spieler werden alle zum Schluss erstellt, damit sie über dem Boden sind und nicht darunter
        for col, row in self.playerplace:
            self.player = Player(self, col, row, self.tilesize)

    # Loop des Spiels
    def run(self):
        # Playing ist der Spielstatus. 0 = läuft, 1 = Sieg, 2 = Niederlage
        while self.playing == 0:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()

    # Bei jeder Aktion updated alles
    def update(self):
        self.all_sprites.update()

    # Grid zeichnen, falls vom Spieler gewollt
    def draw_grid(self):
        for x in range(0, self.width, self.tilesize):
            pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.height))
        for y in range(0, self.height, self.tilesize):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.width, y))

    # Level wird auf Bildschirm angezeigt
    def draw(self):
        self.screen.fill((40, 40, 40))
        self.all_sprites.draw(self.screen)
        if self.grid:
            self.draw_grid()
        pygame.display.flip()

    # Events bei Knopfdruck
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting()
            if event.type == pygame.KEYDOWN:
                if event.key not in (pygame.K_g, pygame.K_n, pygame.K_r):
                    Lava.spread(self)
                if event.key == pygame.K_ESCAPE:
                    quitting()
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    # Alle Players bewegen sich wenn möglich
                    for player in self.players:
                        result = player.move(dx=-1)
                        # Ziel
                        if result == 1:
                            self.win_sound.play()
                            self.playing = 1
                            break
                        # Verloren
                        if result == 21:
                            self.lava_sound.play()
                            self.playing = 2
                            break
                        if result == 22:
                            self.water_sound.play()
                            self.playing = 2
                            break
                        # Schlüssel gesammelt
                        if result == 31:
                            self.key_sound.play()
                            for lock in self.locksY:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                        if result == 32:
                            self.key_sound.play()
                            for lock in self.locksB:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                # Wiederholen der Befehle für andere Bewegungsrichtungen
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    for player in self.players:
                        result = player.move(dx=1)
                        if result == 1:
                            self.win_sound.play()
                            self.playing = 1
                            break
                        if result == 21:
                            self.lava_sound.play()
                            self.playing = 2
                            break
                        if result == 22:
                            self.water_sound.play()
                            self.playing = 2
                            break
                        if result == 31:
                            self.key_sound.play()
                            for lock in self.locksY:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                        if result == 32:
                            self.key_sound.play()
                            for lock in self.locksB:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                if event.key in (pygame.K_UP, pygame.K_w):
                    for player in self.players:
                        result = player.move(dy=-1)
                        if result == 1:
                            self.win_sound.play()
                            self.playing = 1
                            break
                        if result == 21:
                            self.lava_sound.play()
                            self.playing = 2
                            break
                        if result == 22:
                            self.water_sound.play()
                            self.playing = 2
                            break
                        if result == 31:
                            self.key_sound.play()
                            for lock in self.locksY:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                        if result == 32:
                            self.key_sound.play()
                            for lock in self.locksB:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    for player in self.players:
                        result = player.move(dy=1)
                        if result == 1:
                            self.win_sound.play()
                            self.playing = 1
                            break
                        if result == 21:
                            self.lava_sound.play()
                            self.playing = 2
                            break
                        if result == 22:
                            self.water_sound.play()
                            self.playing = 2
                            break
                        if result == 31:
                            self.key_sound.play()
                            for lock in self.locksY:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                        if result == 32:
                            self.key_sound.play()
                            for lock in self.locksB:
                                lock.destroy()
                            for key in self.keys:
                                if key.x == player.x and key.y == player.y:
                                    key.destroy()
                # Level überspringen
                if event.key == pygame.K_n:
                    self.playing = 1
                # Level neu starten
                if event.key == pygame.K_r:
                    self.playing = 2
                # Grid an- und ausmachen
                if event.key == pygame.K_g:
                    if not self.grid:
                        self.grid = True
                    else:
                        self.grid = False


# Level werden nacheinander gestartet, bis alle geschafft sind
COMPLETE = False
LEVEL = 1
while not COMPLETE:
    SUCCESS = False
    while not SUCCESS:
        g = Game(LEVEL, 21, 12, 64)
        while g.playing == 0:
            g.new()
            g.run()
        if g.playing == 1:
            SUCCESS = True
            if LEVEL == 11:
                COMPLETE = True
            else:
                LEVEL += 1
