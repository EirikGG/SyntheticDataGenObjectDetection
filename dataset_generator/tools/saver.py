import os

from PIL import Image

def _save_pil_img(pil_img, folder, name):
    '''Save PIL image to path'''
    file_path = '\\'.join((folder, name))
    pil_img.save(file_path)
    return os.stat(file_path).st_size