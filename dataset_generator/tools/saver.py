import os

from PIL import Image

def save_pil_img(pil_img, folder, name):
    '''Save PIL image to path'''
    file_path = os.path.join(folder, name)
    pil_img.save(file_path)
    return os.stat(file_path).st_size

def save_txt(dic, folder, name):
    '''Save json to file'''
    file_path = os.path.join(folder, name)
    with open(file_path, 'w') as f:
        f.write(dic)
    return os.stat(file_path).st_size