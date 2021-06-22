import os, random

import numpy as np

from PIL import Image

def get_rand_img(folder):
    '''Returns random image from folder path'''
    bg_path = os.path.join(os.getcwd(), folder)                             # Get full folder path
    images_filtered = list(filter(lambda x: x.endswith((                    # Filter images
        '.jpg',
        '.png',
        '.jpeg'
    )), os.listdir(bg_path)))

    bg_img_name = random.choice(images_filtered)                            # List images in directory
    return Image.open(os.path.join(bg_path, bg_img_name))                   # Open random image

def get_color_noise(image_size):
    # https://stackoverflow.com/questions/59056216/how-do-you-generate-an-image-where-each-pixel-is-a-random-color-in-python
    rand_arr = np.random.randint(low = 0, high = 255, size=image_size)
    return Image.fromarray(rand_arr.astype('uint8')).convert('RGB') # Create image of rnadom color

def get_color_img(image_size, color=None):
    if None == color:     # No color specified, use random color
        color = np.random.randint(low = 0, high = 255, size=3)

    img_arr = np.ones((*image_size, 3))*color

    return Image.fromarray(img_arr.astype('uint8')).convert('RGB')



if __name__ == '__main__': get_color_img((1000, 1000))