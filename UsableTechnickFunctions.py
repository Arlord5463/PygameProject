import os
import sys
from PIL import Image
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def cut_sheet(sheet, columns, rows, frames, crop=(0, 0)):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    sprites = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            im = pygame.transform.rotate(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), 90)
            if any(crop):
                im = img_center(im, crop[0], crop[1])
            sprites.append(im)
    frames.append(sprites)


def img_center(py_img, crop_width: int, crop_height: int):
    img_width, img_height = py_img.get_size()
    return py_img.subsurface((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2 - (img_width - crop_width) // 2,
                             (img_height + crop_height) // 2 - (img_height - crop_height) // 2)
