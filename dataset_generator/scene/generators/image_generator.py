import pyrender, random

from PIL import Image

def get_img(scene, renderer):
    '''Takes a rendered image from the scene'''
    color, _ = renderer.render(scene)                               # Get image

    img = Image.fromarray(color.astype('uint8'), 'RGB')             # Convert from point cloud to pil image

    return img