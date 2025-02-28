import random
import sys

import pygame

from UsableTechnickFunctions import load_image
from sprites import *

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
FPS = 50


def start_screen(i):
    clock = pygame.time.Clock()
    if i == 'start':
        intro_text = ["ВАААУ!",
                      "Проект кажись подъехал.",
                      "Удачной игры))"]
    else:
        intro_text = ['Вы проиграли((',
                      'Попробуйте снова?']
    fon = pygame.transform.scale(load_image('fon.jpg'), (1000, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return start_game()  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def move_player(keys):
    speed = 2
    for obj in player_group:
        if any([keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]):
            if keys[pygame.K_DOWN]:
                obj.rect.y += speed
            if keys[pygame.K_UP]:
                obj.rect.y -= speed
            if keys[pygame.K_LEFT]:
                obj.rect.x -= speed
            if keys[pygame.K_RIGHT]:
                obj.rect.x += speed
            for player in player_group:
                player.actions['movement'] = True

            if obj.rect.x < 0:
                obj.rect.x = 0
            if obj.rect.y < 0:
                obj.rect.y = 0
            if obj.rect.x > width - obj.rect.width:
                obj.rect.x = width - obj.rect.width
            if obj.rect.y > height - obj.rect.height:
                obj.rect.y = height - obj.rect.height
        else:
            for player in player_group:
                player.actions['movement'] = False


def asteroid_movement():
    for obj in asteroid_group:
        if obj.actions['movement']:
            obj.rect.x += obj.speed_x
            obj.rect.y += obj.speed_y


def enemy_movement():
    for obj in enemy_group:
        if obj.actions['movement']:
            obj.rect.x += obj.speed_x
            obj.rect.y += obj.speed_y
        if random.randint(-50, 1) == 1:
            obj.actions['attack'] = True
            attack_2(obj)


def border_collision_check():
    for obj in asteroid_group:
        killed = pygame.sprite.spritecollide(obj, border, False)
        if killed:
            obj.kill()
    for obj in bullet_group:
        killed = pygame.sprite.spritecollide(obj, border, False)
        if killed:
            obj.kill()
    for obj in enemy_group:
        killed = pygame.sprite.spritecollide(obj, border, False)
        if killed:
            obj.kill()


def player_update():
    for obj in player_group:
        health_update(obj)
        attack_1(obj)


def health_update(obj):
    if (pygame.sprite.spritecollide(obj, asteroid_group, False, pygame.sprite.collide_rect_ratio(0.7)) and not
    obj.actions[
        'damage']
            and not obj.actions['destroyed']):
        obj.health -= 1
        if not obj.health:
            obj.actions['destroyed'] = True
        else:
            obj.actions['damage'] = True

    if (pygame.sprite.spritecollide(obj, bullet_group, False, pygame.sprite.collide_rect_ratio(0.6)) and not
    obj.actions[
        'damage']
            and not obj.actions['destroyed']):
        obj.health -= 1
        if not obj.health:
            obj.actions['destroyed'] = True
        else:
            obj.actions['damage'] = True

    if obj.actions['end']:
        obj.actions['end'] = False
        obj.health = 3
        start_screen('end')
        print(obj.actions)



def attack_anim_1(obj):
    obj.actions['attack_anim'] = True


def attack_1(obj):
    if obj.actions['attack'] == True:
        create_bullet(obj.rect.x + 22, obj.rect.y, 'Fighter/Charge_1.png', 5)
        create_bullet(obj.rect.x + 17, obj.rect.y, 'Fighter/Charge_1.png', 5)
        obj.actions['attack'] = False


def attack_2(obj):
    if obj.actions['attack']:
        create_bullet(obj.rect.x + 40, obj.rect.y + 80, 'Fighter/Charge_2.png', speed=-5)
        obj.actions['attack'] = False


def create_bullet(x, y, image, speed):
    Bullet_1(all_sprites, bullet_group, x_pos=x, y_pos=y, image=image, speed=speed)


def bullet_movement():
    for obj in bullet_group:
        obj.rect.y -= obj.speed_y


def asteroid_and_enemy_destroyer_update():
    for obj in asteroid_group:
        if pygame.sprite.spritecollide(obj, bullet_group, True, pygame.sprite.collide_rect_ratio(0.7)):
            obj.actions['movement'] = False
            obj.actions['explosion'] = True

    for obj in enemy_group:
        if pygame.sprite.spritecollide(obj, bullet_group, True, pygame.sprite.collide_rect_ratio(0.7)):
            obj.actions['movement'] = False
            obj.actions['explosion'] = True


# создадим группу, содержащую все спрайты
def start_game():
    clock = pygame.time.Clock()
    # ожидание закрытия окна:
    pygame.display.set_mode(size)
    running = True
    while running:
        fon = load_image('background.png')
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for player in player_group:
                        attack_anim_1(player)

        # Настраиваем управление на зажатие клавижи
        keys = pygame.key.get_pressed()
        if keys:
            move_player(keys)

        player_update()
        asteroid_movement()
        enemy_movement()
        bullet_movement()
        border_collision_check()

        if random.randint(-50, 1) == 1:
            Asteroid(all_sprites, asteroid_group)

        if random.randint(-200, 1) == 1:
            Enemy(all_sprites, enemy_group)

        if bullet_group:
            asteroid_and_enemy_destroyer_update()

        all_sprites.draw(screen)
        all_sprites.update()
        # смена (отрисовка) кадра:
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 600))
    start_screen('start')
    # завершение работы:
