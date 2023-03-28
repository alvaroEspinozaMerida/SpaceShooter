import random

import pygame

pygame.init()

vec = pygame.math.Vector2

HEIGHT = 573
WIDTH = 918

FPS = 60

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

font = pygame.font.SysFont("monospace", 30)

game_clock = pygame.time.Clock()


class CharacterPrototype:
    def __init__(self, image_path, **kwargs):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.attributes = kwargs

    def clone(self):
        return CharacterPrototype(self.image, **self.attributes)

    def hitbox(self):
        pass

    def boundary(self):
        pass

    def move(self):
        pass

    def update(self):
        pass


class PlayerPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/spaceship.png", lives=3, movement_speed=.65)


class EnemyPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/rocket.png", movement_speed=.75)


class LaserPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/laser.png", movement_speed=.75)
        self.image = pygame.transform.scale(self.image, (16, 16))


class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self, prototype, pos):
        super().__init__()
        self.prototype = prototype
        self.image = self.prototype.image

        # It is an instance of the pygame.Surface class, which represents a
        # two-dimensional array of pixels that can be used for drawing graphics.
        # As an object, a surface has its own set of attributes and methods that
        # can be accessed and manipulated through the surface instance.
        self.pos = pos
        self.surf = self.image

        self.x_change = 0
        self.y_change = 0

        # a rect is an object that represents a rectangular
        # area of the screen or a surface. It is an instance
        # of the pygame.Rect class, which provides various
        # attributes and methods to manipulate and work with rectangular areas
        self.rect = self.surf.get_rect()
        self.rect.midbottom = self.pos

    def move(self):
        pass


class PlayerSprite(CharacterSprite):
    def __init__(self, pos):
        super().__init__(PlayerPrototype(), pos)

    def move(self, event, all_sprites):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x_change = -5
            elif event.key == pygame.K_RIGHT:
                self.x_change = 5

            elif event.key == pygame.K_SPACE:
                current_pos = vec(self.pos.x, self.pos.y)
                all_sprites.add(LaserSprite(current_pos))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.x_change = 0


    # def shoot(self, event, all_sprites):
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE:
    #             current_pos = vec(self.pos.x, self.pos.y)
    #             all_sprites.add(LaserSprite(current_pos))

    def update(self):
        self.pos.x += self.x_change
        self.rect.midbottom = self.pos


class EnemySprite(CharacterSprite):
    def __init__(self, pos):
        super().__init__(EnemyPrototype(), pos)
        self.direction = 1

    def move(self):

        if self.pos.x > WIDTH * .95:
            self.y_change = 10
            self.direction *= -1

        elif self.pos.x < WIDTH * .05:
            self.y_change = 10
            self.direction *= -1
        else:
            self.y_change = 0

        if self.direction == 1:
            self.x_change = -1
        else:
            self.x_change = 1

        self.pos.x += self.x_change

    def update(self):
        self.pos.x += self.x_change
        self.pos.y += self.y_change
        self.rect.midbottom = self.pos

class LaserSprite(CharacterSprite):
    def __init__(self, pos):
        super().__init__(LaserPrototype(), pos)
        self.y_change = -10


    def update(self):
        self.pos.y += self.y_change
        self.rect.midbottom = self.pos


def restart_game():
    pass


def main():
    background = pygame.image.load("assets/space.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    enemy_time_interval = random.randint(1000, 3000)
    next_enemy_time = 0

    player = PlayerSprite(vec(WIDTH / 2, HEIGHT * .95))

    all_sprites.add(player)

    while True:
        screen.blit(background, (0, 0))

        current_time = pygame.time.get_ticks()

        if current_time > next_enemy_time:
            next_enemy_time += enemy_time_interval
            random_x = random.randrange(round(WIDTH * .05), round(WIDTH * .95))

            enemy = EnemySprite(vec(random_x, HEIGHT / 10))
            all_sprites.add(enemy)
            enemies.add(enemy)

        for event in pygame.event.get():

            player.move(event,all_sprites)
            # player.shoot(event,all_sprites)

            if event.type == pygame.QUIT:
                pygame.quit()

        for e in enemies:
            e.move()

        for sprite in all_sprites:
            sprite.update()
            screen.blit(sprite.surf, sprite.rect)

        pygame.display.update()
        game_clock.tick(FPS)


main()
