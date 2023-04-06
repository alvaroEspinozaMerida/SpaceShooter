import random

import pygame

import constants

pygame.init()

vec = pygame.math.Vector2

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Space Shooter")

font = pygame.font.SysFont("monospace", 30)

game_clock = pygame.time.Clock()


# The CharacterPrototype class serves as a base class for creating prototypical characters in the game,
# with the PlayerPrototype, EnemyPrototype, and LaserPrototype classes defining specific prototypes
# for different types of characters.

# The main purpose of this prototype class is create a set of prototypical objects that
# serve as templates for creating new objects.

# These prototypical objects define a basic structure or behavior that can
# be customized by modifying the attributes or behavior of the new objects.

# In this class I have defined the default attributes/Methods that all CharacterSprites will have
# such as an image that is scaled by default to 64,64 and a clone function that is used in the creation
# of a new CharacterProtype clone

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


# PlayerProtype Class is a subclass of the CharacterProtype class
# this class defines the defualt image of the player along with the lives and movement speed

# By using the Prototype Design Pattern, you can create generic objects
# that have common attributes and behavior, and then customize those
# objects by creating copies and modifying the copies as needed.
# This can be useful when you have objects that are expensive to create,
# or when you need to create many similar objects with small variations.
class PlayerPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/spaceship.png")


class EnemyPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/rocket.png", movement_speed=.75)


class LaserPrototype(CharacterPrototype):
    def __init__(self):
        super().__init__("assets/laser.png", movement_speed=.75)
        self.image = pygame.transform.scale(self.image, (32, 32))


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

    def move(self, *args):
        pass

    def hitbox(self):
        pass


# If you are adding attributes to the player that are specific to the sprite object,
# such as the player's current score or the number of lives they have remaining,
# then you should add these attributes to the PlayerSprite class constructor.
#
# On the other hand, if the attributes are more general and apply to all
# instances of the player object, such as the player's default movement speed or attack power,
# then you should add these attributes to the PlayerPrototype class constructor.

class PlayerSprite(CharacterSprite):
    def __init__(self, pos):
        super().__init__(PlayerPrototype(), pos)
        self.next_shot = 0

    def move(self, all_sprites, current_time):
        keys = pygame.key.get_pressed()

        if True in keys:

            if current_time > self.next_shot and keys[pygame.K_SPACE]:
                self.next_shot += constants.SHOT_DELAY
                current_pos = vec(self.pos.x, self.pos.y)
                all_sprites.add(LaserSprite(current_pos))

            if keys[pygame.K_LEFT]:
                self.x_change = -5

            if keys[pygame.K_RIGHT]:
                self.x_change = 5






        else:
            self.x_change = 0

    def update(self):
        self.pos.x += self.x_change
        self.rect.midbottom = self.pos


class EnemySprite(CharacterSprite):
    def __init__(self, pos):
        super().__init__(EnemyPrototype(), pos)
        self.direction = 1

    def move(self):

        if self.pos.x > constants.WIDTH * .95:
            self.y_change = 64
            self.direction *= -1

        elif self.pos.x < constants.WIDTH * .05:
            self.y_change = 64
            self.direction *= -1

        else:
            self.y_change = 0

        if self.direction == 1:
            self.x_change = -1

        else:
            self.x_change = 1

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
    # BACKGROUND SET UP
    background = pygame.image.load("assets/space.jpg")
    background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))

    # GROUPING SET UP
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    # ENEMY TIME SET UP
    enemy_time_interval = random.randint(1000, 3000)
    next_enemy_time = 0

    # Player Creation
    player = PlayerSprite(vec(constants.WIDTH / 2, constants.HEIGHT * .95))
    all_sprites.add(player)

    while True:
        game_clock.tick(constants.FPS)
        screen.blit(background, (0, 0))

        current_time = pygame.time.get_ticks()
        print(f"Current Time:{current_time}")
        print(f"Next Shot Time:{player.next_shot}")

        player.move(all_sprites, current_time)

        # enemy spawner
        if current_time > next_enemy_time:
            next_enemy_time += enemy_time_interval
            random_x = random.randrange(round(constants.WIDTH * .05), round(constants.WIDTH * .95))

            enemy = EnemySprite(vec(random_x, constants.HEIGHT / 10))
            all_sprites.add(enemy)
            enemies.add(enemy)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for e in enemies:
            e.move()

        for sprite in all_sprites:
            sprite.update()
            screen.blit(sprite.surf, sprite.rect)

        pygame.display.update()


main()
