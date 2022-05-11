import pygame
import os

# Ordner deklarieren
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
map_folder = os.path.join(game_folder, "map")
snd_folder = os.path.join(game_folder, "sound")


# Klasse: Spieler
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.tilesize = tilesize
        self.groups = game.all_sprites, game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "player.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    # Methode zum Bewegen
    def move(self, dx=0, dy=0):
        if not self.collide_wall(dx, dy) == "wall":
            self.x += dx
            self.y += dy
        if self.collide_item() == "lava":
            return 21
        if self.collide_item() == "water":
            return 22
        if self.collide_item() == "goal":
            return 1
        if self.collide_item() == "keyY":
            return 31
        if self.collide_item() == "keyB":
            return 32
        return 0

    # Kollisionen, die am Bewegen hindern
    def collide_wall(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return "wall"
        for lock in self.game.locks:
            if lock.x == self.x + dx and lock.y == self.y + dy:
                return "wall"
        return "none"

    # Kollisionen, die nach dem Bewegen einen Effekt haben
    def collide_item(self):
        for goal in self.game.goals:
            if goal.x == self.x and goal.y == self.y:
                return "goal"
        for lava in self.game.lavas:
            if lava.x == self.x and lava.y == self.y:
                return "lava"
        for water in self.game.waters:
            if water.x == self.x and water.y == self.y:
                return "water"
        for key in self.game.keysY:
            if key.x == self.x and key.y == self.y:
                return "keyY"
        for key in self.game.keysB:
            if key.x == self.x and key.y == self.y:
                return "keyB"
        return "none"

    # Bewegung umsetzen
    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize


# Klasse: Wand
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "wall.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


# Klasse: Ziel
class Goal(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.groups = game.all_sprites, game.goals
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "flag.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


# Klasse: Wasser
class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.tilesize = tilesize
        self.groups = game.all_sprites, game.waters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "water.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


# Klasse: Lava
class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.tilesize = tilesize
        self.groups = game.all_sprites, game.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "lava.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

    # Lava breitet sich in alle Richtungen aus. Es sei denn, etwas ist im Weg
    def spread(self):
        for lava in self.game.lavas:
            right = False
            left = False
            up = False
            down = False
            for wall in self.game.walls:
                if wall.x == lava.x + 1 and wall.y == lava.y:
                    right = True
            for lock in self.game.locks:
                if lock.x == lava.x + 1 and lock.y == lava.y:
                    right = True
            for water in self.game.waters:
                if water.x == lava.x + 1 and water.y == lava.y:
                    right = True
            for nextlava in self.game.lavas:
                if nextlava.x == lava.x + 1 and nextlava.y == lava.y:
                    right = True
            if not right and self.game.width / self.game.tilesize > lava.x > 0 and 0 < lava.y < self.game.height / self.game.tilesize:
                Lava(self.game, lava.x + 1, lava.y, self.game.tilesize)
            for wall in self.game.walls:
                if wall.x == lava.x - 1 and wall.y == lava.y:
                    left = True
            for lock in self.game.locks:
                if lock.x == lava.x - 1 and lock.y == lava.y:
                    left = True
            for water in self.game.waters:
                if water.x == lava.x - 1 and water.y == lava.y:
                    left = True
            for nextlava in self.game.lavas:
                if nextlava.x == lava.x - 1 and nextlava.y == lava.y:
                    left = True
            if not left and self.game.width / self.tilesize > lava.x > 0 and 0 < lava.y < self.game.height / self.game.tilesize:
                Lava(self.game, lava.x - 1, lava.y, self.tilesize)
            for wall in self.game.walls:
                if wall.x == lava.x and wall.y == lava.y + 1:
                    down = True
            for lock in self.game.locks:
                if lock.x == lava.x and lock.y == lava.y + 1:
                    down = True
            for water in self.game.waters:
                if water.x == lava.x and water.y == lava.y + 1:
                    down = True
            for nextlava in self.game.lavas:
                if nextlava.x == lava.x and nextlava.y == lava.y + 1:
                    down = True
            if not down and self.game.width / self.tilesize > lava.x > 0 and 0 < lava.y < self.game.height / self.tilesize:
                Lava(self.game, lava.x, lava.y + 1, self.tilesize)
            for wall in self.game.walls:
                if wall.x == lava.x and wall.y == lava.y - 1:
                    up = True
            for lock in self.game.locks:
                if lock.x == lava.x and lock.y == lava.y - 1:
                    up = True
            for water in self.game.waters:
                if water.x == lava.x and water.y == lava.y - 1:
                    up = True
            for nextlava in self.game.lavas:
                if nextlava.x == lava.x and nextlava.y == lava.y - 1:
                    up = True
            if not up and self.game.width / self.tilesize > lava.x > 0 and 0 < lava.y < self.game.height / self.tilesize:
                Lava(self.game, lava.x, lava.y - 1, self.game.tilesize)


# Klasse: Schlüssel
class Key(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize, color):
        self.tilesize = tilesize
        self.color = color
        self.game = game
        # Farbe des Schlüssels
        if color == 1:
            self.groups = game.all_sprites, game.keys, game.keysY
        if color == 2:
            self.groups = game.all_sprites, game.keys, game.keysB
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(os.path.join(img_folder, "key%d.png" % color)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

    # Entfernt den Schlüssel
    def destroy(self):
        self.x += 100000
        self.y += 100000

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize


# Klasse: Schloss
class Lock(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize, color):
        self.tilesize = tilesize
        self.color = color
        self.game = game
        # Farbe des Schlosses
        if color == 1:
            self.groups = game.all_sprites, game.locks, game.locksY
        if color == 2:
            self.groups = game.all_sprites, game.locks, game.locksB
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(os.path.join(img_folder, "lock%d.png" % color)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

    # Entfernt das Schloss
    def destroy(self):
        self.x += 100000
        self.y += 100000

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize


# Klasse: Boden
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tilesize):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_folder, "ground.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize