from PIL import Image


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


im = Image.open('data/Fighter/Idle.png')
im_new = crop_center(im, 100, 100)
im_new.save('data/Fighter/Idle_1.png', quality=95)
