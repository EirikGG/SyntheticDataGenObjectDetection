import numpy as np

from PIL import Image

def get_depth(scene, renderer):
    '''Takes a rendered image from the scene'''
    _, depth = renderer.render(scene)                               # Get image

    depth_img = Image.fromarray(np.uint8(depth*255), 'L')           # Convert from 2d array to pil image

    return depth_img