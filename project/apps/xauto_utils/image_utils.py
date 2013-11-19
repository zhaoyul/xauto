import os
from PIL import Image, ImageOps
from time import time


def get_thumbnail_url(image_url, size=150):
    image_url_parts = image_url.rsplit('/', 1)
    return image_url_parts[0] + '/' + get_folder_name(size) + '/' + image_url_parts[1]

def get_folder_name(size):
    return 'thumbs_' + str(size)

def get_thumbnail_path(image_path, size=150):
    dirname, filename = os.path.split(image_path)
    dirname = os.path.join(dirname, get_folder_name(size))
    if not os.path.exists(dirname):
        os.mkdir(dirname, 0755)
    return os.path.join(dirname, filename)

def create_thumbnail(image_path, size=150, sizeH = 150, pad=False):
    thumb_path = get_thumbnail_path(image_path, size)
    delete_thumbnail(image_path, size)
    try:
        img = Image.open(image_path)
    except IOError as e:
        return False
    img.thumbnail((size, sizeH), Image.ANTIALIAS)
    if pad:
        thumb = ImageOps.fit(img, (size, sizeH), Image.ANTIALIAS, (0.5, 0.5))
        thumb.save(thumb_path)
    else:
        img.save(thumb_path)

def delete_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
