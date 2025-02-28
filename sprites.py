import random

import pygame
from UsableTechnickFunctions import load_image, cut_sheet
from GameplayScreen import width, height
import os

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, *group, x_pos, y_pos):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.sprites = []

        cut_sheet(load_image('Fighter/Idle.png'), 1, 1, self.sprites, (65, 120))
        cut_sheet(load_image('Fighter/Move.png'), 6, 1, self.sprites, (65, 120))
        cut_sheet(load_image('Fighter/Damage.png'), 9, 1, self.sprites, (65, 120))
        cut_sheet(load_image('Fighter/Destroyed.png'), 15, 1, self.sprites, (65, 120))
        cut_sheet(load_image('Fighter/Attack_1.png'), 4, 1, self.sprites, (65, 120))

        self.actions = {'movement': False, 'damage': False, 'destroyed': False, 'attack': False, 'attack_anim': False,
                        'end': False}
        self.current_sprite = 0
        self.image = self.sprites[0][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.health = 3

    def update(self):
        if self.actions['destroyed']:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites[3]):
                self.current_sprite = 0
                self.actions['destroyed'] = False
                self.actions['end'] = True

            self.image = self.sprites[3][int(self.current_sprite)]

        elif self.actions['damage']:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites[2]):
                self.current_sprite = 0
                self.actions['damage'] = False

            self.image = self.sprites[2][int(self.current_sprite)]

        elif self.actions['attack_anim']:
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites[4]):
                self.current_sprite = 0
                self.actions['attack_anim'] = False
                self.actions['attack'] = True

            self.image = self.sprites[4][int(self.current_sprite)]


        elif self.actions['movement']:
            self.current_sprite += 1

            if self.current_sprite >= len(self.sprites[1]):
                self.current_sprite = 0
            self.image = self.sprites[1][self.current_sprite]

        if not any(self.actions.values()):
            self.current_sprite = 0
            self.image = self.sprites[0][self.current_sprite]


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.sprites = []

        dyrectory = '/Users/arkadij/PycharmProjects/PygameProject/data/Meteors'
        files = os.listdir(dyrectory)
        images = []
        for image in files:
            images.append(load_image(f"Meteors/{image}"))
        self.sprites.append(images)

        cut_sheet(load_image('Meteors/Explosion.png'), 8, 7, self.sprites)

        self.actions = {'movement': True, 'explosion': False}
        self.current_sprite = 0
        self.image = self.sprites[0][random.randint(0, len(self.sprites[0]) - 1)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-100, width + 100)
        self.rect.y = random.randint(-140, -100)
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(1, 5)

    def update(self):
        if self.actions['explosion']:
            self.current_sprite += 1

            if self.current_sprite >= len(self.sprites[1]):
                self.current_sprite = 0
                self.kill()

            self.image = pygame.transform.rotozoom(
                pygame.transform.scale(self.sprites[1][self.current_sprite], self.rect.size), 0, 1.5)


class Bullet_1(pygame.sprite.Sprite):
    def __init__(self, *group, x_pos, y_pos, image, speed):
        super().__init__(*group)
        self.sprites = []
        cut_sheet(load_image(image), 1, 1, self.sprites)

        self.image = self.sprites[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed_y = speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.sprites = []

        cut_sheet(load_image('Fighter/Enemy.png'), 1, 1, self.sprites)
        cut_sheet(load_image('Meteors/Explosion.png'), 8, 7, self.sprites)

        self.actions = {'movement': True, 'explosion': False, 'attack': False}
        self.current_sprite = 0
        self.image = self.sprites[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-100, width + 100)
        self.rect.y = random.randint(-140, -100)
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(1, 5)

    def update(self):
        if self.actions['explosion']:
            self.current_sprite += 1

            if self.current_sprite >= len(self.sprites[1]):
                self.current_sprite = 0
                self.kill()

            self.image = pygame.transform.rotozoom(
                pygame.transform.scale(self.sprites[1][self.current_sprite], self.rect.size), 0, 1.5)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.add(border)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
border = pygame.sprite.Group()

Border(-150, -150, width + 150, -150)
Border(-150, height + 150, width + 150, height + 150)
Border(-150, -150, -150, height + 150)
Border(width + 150, -150, width + 150, height + 150)

Player(all_sprites, player_group, x_pos=(width - 65) / 2, y_pos=(height - 120))

for sprite in all_sprites:
    pygame.sprite.collide_rect_ratio(0.7)
